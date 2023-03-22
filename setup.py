from setuptools import setup

setup(
    name='chi_houses',
    description='Find historic Chicago houses.',
    version='0.0.1',
    author='Travis Birch',
    packages=['chi_houses'],
    install_requires=['requests', 'matplotlib',
                      'geopandas', 'filetype',
                      'numpy']
)
