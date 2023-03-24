"""Get list of houses in Chicago community areas."""

import os
import time
import requests
import geopandas as gpd
import matplotlib.pyplot as plt
from numpy.random import randint
import filetype


class Houses:
    """Get data for Chicago houses.

    This class includes methods to get property characteristics (e.g.
    number of bedrooms, wall materials, etc.), images, and footprint
    shapes of houses in Chicago. The results are filtered by community
    area and build year.

    Attributes:
        community_areas: User-provided list of community areas
        year_range: User-provided tuple of min and max build years
        house_list: Geopandas GeoDataFrame with house data
        community_boundaries: Shapely Multipolygon of community area shapes
    """
    def __init__(self, community_areas: list, year_range: tuple = False):
        """Instance of Houses class.

        Args:
            community_areas: A list of neighborhoods, e.g. ['Logan Square', 'Edgewater'].
                See [Chicago community areas]
                (https://en.wikipedia.org/wiki/Community_areas_in_Chicago).
            year_range: A two-element tuple with min and max build years, e.g. (1890, 1910)
        """
        self.community_areas = community_areas
        self.year_range = year_range
        self.house_list = None
        self.community_boundaries = None

    def get_houses(self, results_limit: int = 100000, all_data: bool = False):
        """Get a list of houses (with residential characteristics).

        The data come from the Cook County Assessor. By default, this method
        returns a subset of fields from the dataset: tax pin, address, and coordniates.
        Setting `full_results` to `true` will return all fields, which include
        property characteristics (e.g. number of bedrooms, wall materials, etc.).

        Args:   
            all_data: Return all fields, including property characteristics 
                (e.g. number of bedrooms, wall materials, etc.). May reutrn multiple
                rows per address.
            results_limit: Max number of results to obtain from the Assessor API
                (the actual number of houses may be smaller after filtering
                by community area shape).

        Returns:  
            GeoPandas GeoDataFrame of house data
        """
        boundaries, outer_boundary = get_community_boundaries(
            self.community_areas)
        self.community_boundaries = boundaries
        house_list = get_house_list(outer_boundary, self.year_range,
                                      results_limit, all_data)
        house_list = process_house_list(
            house_list, outer_boundary)
        self.house_list = house_list
        return house_list

    def get_images(self, output_path: str = 'img/'):
        """Get house images.

        The Cook County Assessor has photos of most residential properties available 
        on its website (e.g. https://www.cookcountyassessor.com/pin/13253100070000).
        The photos are retrieved via structured urls; this function retreives and 
        saves those images if available, recording the paths to a new column in the
        house list.

        Note: please use this sparingly. This is basically scraping and your access 
        may be rate limited or blocked if you aren't considerate.

        Args:
            output_path (optional): Set path where images are saved

        Returns:  
            img_paths: GeoPandas GeoDataFrame of house data with image paths
        """
        # Create destination directory.
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Prep data.
        pins = self.house_list['pin'].to_list()
        img_paths = []

        # Get images.
        for i, pin in enumerate(pins):
            print(f'Fetching image {i} of {len(pins)}...', end='\r')
            img_data = get_image(pin)
            save_path = save_image(pin, img_data, output_path)
            img_paths.append(save_path)
            time.sleep(randint(5, 10))
        print('Image retrieval complete.' + ' ' * 50)
        self.house_list['img_paths'] = img_paths
        return self.house_list


def get_community_boundaries(community_areas):
    """Get geo outlines for a list of community areas.
    """
    community_areas = [x.upper() for x in community_areas]
    url = ('https://data.cityofchicago.org/api/geospatial/'
           'cauq-8yn6?method=export&format=GeoJSON')
    gdf = gpd.read_file(url)
    gdf = gdf[gdf['community'].isin(community_areas)]
    # Merge geometries for every community area into one.
    shape = gdf.unary_union
    return gdf, shape


def get_house_list(community_boundaries, year_range,
                   results_limit, all_data):
    """Get raw property data.
    """
    # Note: the datasource is from 2022.
    url = 'https://datacatalog.cookcountyil.gov/resource/bcnq-qi2z.json'
    # Coords for box enclosing community area
    # The `x` values are negative here.
    minx, miny, maxx, maxy = community_boundaries.bounds
    if all_data:
        query = f"""
        SELECT 
            *
        WHERE 
            centroid_y > "{miny}" 
            AND centroid_y < "{maxy}" 
            AND centroid_x > "{maxx}" 
            AND centroid_x < "{minx}" """
        if year_range:
            query += (f'AND age BETWEEN {2022 - year_range[1]}'
                      f' AND {2022 - year_range[0]} ')
    else:
        query = f"""
        SELECT 
            MIN(pin) AS pin, 
            addr, 
            MIN(centroid_x) AS centroid_x,
            MIN(centroid_y) AS centroid_y, 
            MIN(2022 - age) AS year_built
        GROUP BY addr 
        HAVING 
            centroid_y > "{miny}" 
            AND centroid_y < "{maxy}" 
            AND centroid_x > "{maxx}" 
            AND centroid_x < "{minx}" """
        if year_range:
            query += (f'AND year_built BETWEEN {year_range[0]}'
                      f' AND {year_range[1]} ')
    if results_limit:
        query += f'LIMIT {results_limit}'
    r = requests.get(url, params={'$query': query})
    if len(r.json()) == 0:
        raise RuntimeError('API response had no results.')
    return r.json()


def process_house_list(house_list, shape):
    """Filter house list by community boundaries.
    """
    gdf = gpd.GeoDataFrame(house_list)
    gdf = gdf.set_geometry(gpd.points_from_xy(gdf['centroid_x'],
                                              gdf['centroid_y']))
    gdf = gdf.set_crs('EPSG:4326')
    gdf = gdf[gdf['geometry'].within(shape)]
    if len(gdf.index) == 0:
        raise RuntimeError('No results in community boundaries.')
    gdf = gdf.drop(columns=['centroid_x', 'centroid_y'])
    return gdf


def get_image(pin, debug=False):
    """Build URL and request image.
    """
    url_stub = 'https://prodassets.cookcountyassessor.com/s3fs-public/pin_detail/'
    url_encoding = f'{pin[0:3]}-{pin[3:5]}/{pin[5:8]}/{pin}_AA.JPG'
    img_data = requests.get(url_stub + url_encoding, timeout=120).content
    if debug:
        print(f'Attempted to retrieve image at {url_stub + url_encoding}')
    return img_data


def save_image(pin, img_data, output_path, debug=False):
    """If input is valid image, create image file.
    """
    file_path = f"{output_path}{pin}.jpg"
    if filetype.is_image(img_data):
        with open(file_path, 'wb') as img:
            img.write(img_data)
        if debug:
            print(f'{pin}: created image at {file_path}')
        return file_path
    else:
        if debug:
            print(f'{pin}: pin did not return valid image')
        return None
