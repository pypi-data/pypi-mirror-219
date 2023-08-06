# Xarray Module

## Introduction
**Xarray** is a python package to simplify working with labelled multi-dimension arrays in Python. 

**tfv** uses Xarray to handle data extraction and management under-the-hood, and this xarray accessor module extends the functionality of native **Xarray** so that it can be used to directly handle TUFLOW FV data.

We now recommend that these functions are used to handle data access, analysis and plotting of TUFLOW FV results in Python, over the use of the original 'low-level' functions (e.g., provided in `FvExtractor`). These methods directly call on the functions in the other modules, however simplify their use for typical analyses.

## Usage
To enable the accessor methods, load up a TUFLOW FV domain (i.e., 2D or 3D spatial output netcdf) or profile timeseries netcdf in xarray. 

General examples:

1.  **TfvDomain File (i.e., a spatial 2D or 3D TUFLOW FV netcdf)** \
    `ds = xr.open_dataset('tuflowfv_domain_result.nc')` \
    Note: can swap with `xr.open_mfdataset` for multiple TUFLOW FV files with matching geometry, or for parallelised access using `dask`). 
    <br><br>
    Finally, calling `ds.tfv` will return a `TfvDomain` object, that appears as a normal Xarray file, but has access to additional tuflow fv specific methods. For example, `fv = ds.tfv` and then resulting methods can be used like `fv.get_statistics(...)`

	<br>

2. **TfvTimeseries File (i.e., a profile timeseries TUFLOW FV netcdf)** \
    `ds = xr.open_dataset('tuflowfv_profile_timeseries_result.nc')` \
    Note: can swap with `xr.open_mfdataset` for parallelised access using `dask`, *however accessing multiple profile timeseries files using `open_mfdataset` is NOT currently supported*. 
    <br><br>
    Calling `ds.tfv` will return a `TfvTimeseries` object that has several methods to enable conveniently accessing the profile timeseries groups.

## Accessor methods
 ```{eval-rst}
.. toctree::
    :maxdepth: 3
    
    tfvdomain
    tfvtimeseries
```

<!-- ```{eval-rst}
.. toctree::
    :maxdepth: 4

    tfvdomain
    tfvtimeseries
``` -->