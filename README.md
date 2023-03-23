# Chicago houses 🏠

Get data for Chicago houses with filtering by neighborhood and build year.

The module uses property data from the [Cook County Assessor](https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Archived-05-11-2022-Residential-Property-/bcnq-qi2z) and [community area](https://en.wikipedia.org/wiki/Community_areas_in_Chicago) boundaries from the [Chicago Data Portal](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-current-/cauq-8yn6). It can also retrieve property images from the Assessor's website--these images are typically better than other sources (e.g. Google Maps Street View) at (a) directly framing each building, and (b) clearly showing each building's features.

## Example usage
Install with pip
```shell
pip install git+https://github.com/tbirch4/chi-houses.git
```

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

## Branches
`main`: This branch returns only five fields: `pin`, `addr`, `centroid_x` (longitude), `centroid_y` (latitude), and `year_built`. It also includes only one `pin` per address (some addresses have multiple pins, such as apartment buildings).

`full`: This branch returns every data point available from the Assessor table. The results are presented as-is, with no manipulation or filtering apart from limiting to the year range and community areas specified by the user.
