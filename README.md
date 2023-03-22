# Chicago houses

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