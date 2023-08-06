from pickle import TRUE
import pkg_resources

__version__ = "1.0.5"
__author__ = "support@tulow.com"
__aus_date__ = "%d/%m/%Y %H:%M:%S"

# List of dependencies copied from requirements.txt
dependencies = \
    [
        'numpy>=1.19.0',
        'matplotlib>=3.2.2',
        'netCDF4>=1.5.3',
        'xarray>=0.16.2',
        'dask>=2021.3.0',
        'scipy>=1.6.0',
        'tqdm>=4.50.0',
    ]

# Throw exception if correct dependencies are not met
pkg_resources.require(dependencies)
