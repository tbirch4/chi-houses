from distutils.core import setup

setup(name='chicagohouses',
      version='0.0.1',
      description='Get a filterable list of houses in Chicago.',
      author='Travis Birch',
      author_email='aml-toolbox-feedback@googlegroups.com',
      packages=['chicagohouses', 'data'],
      install_requires=['polars', 'geopandas']
     )
