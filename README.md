# Chicago houses 🏠

Get data for Chicago houses with filtering by build year and neighborhood.

The module uses property data from the Cook County Assessor and community area boundaries from the Chicago data portal. It can also retrieve property images from the Assessor's website--these images are typically better than other sources (e.g. Google Maps Street View) at (a) directly framing each building, and (b) clearly showing each building's features.

Example usage:
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
