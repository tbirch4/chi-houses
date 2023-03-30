"""Get a filterable list of houses in Chicago.
"""

import polars as pl
import geopandas as gpd
import data


def get_houses(community_areas: list[str] = False, year_range: list[int] = False, 
               full_data: bool = False, output_type: str = 'geopandas'):
    """Get a filterable list of houses in Chicago.

    This uses a combination of house data from the Cook County Assessor
    and community area data from the Chicago Data Portal. The house data
    is from 2022 and doesn't include any changes after that year.

    Args:
        community_areas: One or more Chicago [community areas]
            (https://en.wikipedia.org/wiki/Community_areas_in_Chicago)
        year_range: Minimum and maximum build years. Tear-down renovations
            should reset the build year (e.g. a house built in 1900 but
            torn down and rebuilt in 2000 should have a build year of 2000).
        full_data: Optionally include property characteristics (e.g. square
            footage, number of rooms, etc.) in the output data. If false,
            results will include a minimal subset of columns.
        output_type: Data type returned; can be "geopandas" (default), 
            "pandas", or "polars"

    Returns:
        A GeoPandas GeoDataFrame of house data (or another data type 
        specified in `output_type`)
    """
    # Import data.
    data_file = 'data/houses.parquet.gzip'
    try:
        p_df = pl.scan_parquet(data_file)
    except FileNotFoundError:
        raise RuntimeError('Unable to scan data file. Ensure file exists '
                                f'at "{data_file}".')

    # Clean and validate inputs.
    community_areas, year_range = __validate_args(community_areas, output_type, year_range, p_df)

    # Filter data.
    if not full_data:
        p_df = p_df.select(['pin', 'addr', 'build_year', 'community', 'house_point'])
    else:
        print('See dataset documentation here: https://datacatalog.cookcountyil.gov/'
              'Property-Taxation/Assessor-Archived-05-11-2022-Residential-Property-/'
              'bcnq-qi2z')
    if community_areas:
        p_df = p_df.filter(pl.col('community').is_in([x.upper() for x in community_areas]))
    if year_range:
        p_df = p_df.filter(pl.col('build_year').is_between(year_range[0], year_range[1]))
    
    # Return filtered data according to output_type selection.
    if output_type == 'geopandas':
        gdf = gpd.GeoDataFrame(p_df.collect().to_pandas())
        gdf = gdf.set_geometry(gpd.GeoSeries.from_wkt(gdf['house_point']))
        gdf = gdf.set_crs('EPSG:4326')
        return gdf
    if output_type == 'pandas':
        return p_df.collect().to_pandas()
    if output_type == 'polars':
        return p_df
    

def __validate_args(community_areas, output_type, year_range, p_df):
        """Validate arguments for get_houses.
        """
        # Attempt to convert abnormal inputs into useable format.
        if community_areas:
            if isinstance(community_areas, str): community_areas = [community_areas]
            community_areas = [x.upper() for x in community_areas]

        if year_range:
            if isinstance(year_range, (int, float)): year_range = [year_range]
            if len(year_range) == 1: year_range.extend(year_range)
            if len(year_range) != 2:
                raise RuntimeError('Invalid date range. Requires a 2-integer list of values.')

        # Check for valid output_type selection.
        if output_type not in ['geopandas', 'pandas', 'polars']:
            raise RuntimeError('Invalid selection for "output_type". Choose one of the '
                            'following: "polars", "geopandas", or "pandas".')
        
        # Check for validity of community_areas.
        if community_areas:
            full_ca_list = (p_df.select('community')
                                .unique()
                                .collect()
                                .to_series()
                                .to_list())
            invalid_areas = [area for area in community_areas 
                            if area not in full_ca_list]
            if invalid_areas:
                raise RuntimeError('The following are not valid community area(s): '
                                f'{", ".join(invalid_areas)}.')
        
        return community_areas, year_range