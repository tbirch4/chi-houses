# Chicago houses 🏠

Get data for Chicago houses with filtering by neighborhood and build year.

This uses property data from the [Cook County Assessor](https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Archived-05-11-2022-Residential-Property-/bcnq-qi2z) and [community area](https://en.wikipedia.org/wiki/Community_areas_in_Chicago) boundaries from the [Chicago Data Portal](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-current-/cauq-8yn6).

## Example usage

Install with pip.
```shell
pip install git+https://github.com/tbirch4/chi-houses.git@full
```

Get houses data and images.

```python
from chicagohouses import get_houses

community_areas = ['edgewater', 'logan square']
year_range = [1900, 1901]

# Get a simple list of houses.
houses = get_houses(community_areas, year_range)

# Get a list of houses with property characteristics.
houses = get_houses(community_areas, year_range, full_data=True)
```

## Full residential characteristics data
By default, `get_houses` returns a minimal list of addresses meeting the search parameters. It gets a small subset of columns from the data source: address, tax pin, year built, and coordinates. However, the data source has many additional columns that could be helpful for machine learning and other applications. To access the full data, set the `full_data` parameter of `get_houses` to `True`. You can find a full list of columns [here](https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Archived-05-11-2022-Residential-Property-/bcnq-qi2z).
