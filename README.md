# Chicago houses 🏠

Get data for Chicago houses with filtering by neighborhood and build year.

The module uses property data from the [Cook County Assessor](https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Archived-05-11-2022-Residential-Property-/bcnq-qi2z) and [community area](https://en.wikipedia.org/wiki/Community_areas_in_Chicago) boundaries from the [Chicago Data Portal](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-current-/cauq-8yn6). It can also retrieve property images from the Assessor's website--these images are typically better than other sources (e.g. Google Maps Street View) at (a) directly framing each building, and (b) clearly showing each building's features.

## Example usage

Install with pip.
```shell
pip install git+https://github.com/tbirch4/chi-houses.git
```

Get houses data and images.

```python
from chi_houses import Houses

community_areas = ['edgewater', 'logan square']
year_range = (1900, 1901)

houses = Houses(community_areas, year_range)

# Get list of matching properties.
houses.get_houses()

# Get an image of each property.
houses.get_images()

houses.house_list
```

## Full residential characteristics data
By default, `get_houses` functions as a list of addresses meeting the search parameters. It takes only a few columns from the data source: address, tax pin, year built, and coordinates. However, the data source has many additional columns that could be helpful for machine learning and other uses. To access the full data, set the `all_data` parameter of `get_houses` to `True`. You can find a full list of columns [here](https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Archived-05-11-2022-Residential-Property-/bcnq-qi2z).
