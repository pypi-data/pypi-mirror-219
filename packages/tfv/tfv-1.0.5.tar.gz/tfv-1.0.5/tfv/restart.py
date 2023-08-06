"""A module for reading and writing TUFLOW FV restart files"""

import os
import numpy as np
from netCDF4 import Dataset

def write_restart_file(nc2, nc3, time_stamp, cell_Zb, fv_data, out_file):
    """
    Creates a new restart file from data.

    Parameters
    ----------
    nc2 : int
        Number of 2d cells.
    nc3 : int
        Number of 3d cells.
    time_stamp : float
        Time as TUFLOW FV time stamp (hours from 1/1/1990).
    cell_Zb : ndarray
        Cell elevation as (nc2,) array.
    fv_data : ndarray
        Conserved 3D variables as (nc3, n) array (depth, V_x, V_y, SAL, TEMP, SED_1, .... , SED_N)
    out_file : str
        Output path of restart file.
    """

    # get some basic parameters
    t = np.array(time_stamp * 3600)  # time in seconds since 01/01/1990 00:00:00
    nv = fv_data.shape[1]  # number of conserved variables
    dims = np.array([nc2, nc3, nv])  # array of dimensions

    # scale data by depth and transpose
    fv_data[:, 1:] = fv_data[:, 1:]*fv_data[:, 0:1]
    fv_data = fv_data.transpose()

    # write the data in binary format as shown
    with open(out_file, 'wb') as f:
        t.astype(np.float64).tofile(f)
        dims.astype(np.int32).tofile(f)
        cell_Zb.astype(np.float32).tofile(f)
        fv_data.transpose().astype(np.float32).tofile(f)

def read_restart_file(restart_file):
    """Reads data from a TUFLOW FV restart file"""
    with open(restart_file, 'rb') as f:
        time_stamp = np.fromfile(f, np.float64, 1)[0]/3600
        nc2 = np.fromfile(f, np.int32, 1)[0]
        nc3 = np.fromfile(f, np.int32, 1)[0]
        nv = np.fromfile(f, np.int32, 1)[0]

        cell_Zb = np.fromfile(f, np.float32, nc2)

        fv_data = np.zeros((nv, nc3,), np.float32)
        for aa in range(nv):
            fv_data[aa, :] = np.fromfile(f, np.float32, nc3)
        fv_data = fv_data.transpose()

        good, bad = fv_data[:, 0] != 0, fv_data[:, 0] == 0
        fv_data[good, 1:] = fv_data[good, 1:] / fv_data[good, 0:1]
        fv_data[bad, :] = np.nan

    return nc2, nc3, time_stamp, cell_Zb, fv_data

def restart_from_result(old_result_file, new_result_file, out_file, n_sigma, time_stamp, variables):
    """
    Creates a restart file from an existing TUFLOW FV result file, using a separate result file for geometry input.

    Parameters
    ----------
    old_result_file : str
        Path of result file from which restart is being generated.
    new_result_file : str
        Path of result file from which to use geometry data (mesh and cell elevations).
    out_file : str
        Output path of restart file.
    n_sigma : int
        Number of sigma layers being used in new model.
    time_stamp : float
        Time as TUFLOW FV time stamp (hours from 1/1/1990).
    variables : list
        List of conserved variables to include in the restart file (V_x, V_y, SAL, TEMP, SED_1, ...).
    """

    # get old result file netCDF handle
    old = Dataset(old_result_file)

    # get new result file netCDF handle
    new = Dataset(new_result_file)

    # get time index from target result file
    tt = np.argmin(np.abs(old['ResTime'][:] - time_stamp))

    # find the nearest 3D index for each cell
    index3D = np.array([], dtype=np.int32)  # maps new 3D to old 3D
    for aa in range(new.dimensions['NumCells2D'].size):

        # get the distance to each 2D cell
        dx = old['cell_X'] - new['cell_X'][aa]
        dy = old['cell_Y'] - new['cell_Y'][aa]
        distance = np.hypot(dx, dy)

        # get the index of the nearest old 2D cell
        nearest2D = np.argmin(distance)

        # get the new water level and bed level
        wl, bl = old['H'][tt, nearest2D].data, new['cell_Zb'][aa].data

        # check if old and new cell is\isn't dry
        dryDepth = new.getncattr('Dry depth')
        newDry = (wl - bl) < dryDepth
        oldDry = (old['stat'][tt, nearest2D] == 0)

        # if new cell is wet but old cell is dry, remap, otherwise bad data
        if (not newDry) and oldDry:
            distance[old['stat'][tt, :] == 0] = np.inf
            nearest2D = np.argmin(distance)
            wl = old['H'][tt, nearest2D].data

        # get the NEW layer face Z for current cell
        idx3 = new['idx3'][aa] - 1
        nlfz = new['NL'][aa] + 1
        idx4 = idx3 + aa

        lfzNew = new['layerface_Z'][tt, idx4:idx4 + nlfz].data

        # update the sigma layers using new water level
        dzTop = (wl - lfzNew[n_sigma]) / n_sigma
        lfzNew[0:n_sigma] = wl - dzTop * np.arange(n_sigma)

        # get the OLD layer face Z for current cell
        idx3 = old['idx3'][nearest2D] - 1
        nlfz = old['NL'][nearest2D] + 1
        idx4 = idx3 + nearest2D

        lfzOld = old['layerface_Z'][tt, idx4:idx4 + nlfz].data

        # get the centres to do a minimum distance search
        zcNew = 0.5 * (lfzNew[:-1] + lfzNew[1:])
        zcOld = 0.5 * (lfzOld[:-1] + lfzOld[1:])

        zcOld = np.tile(zcOld, (zcNew.size, 1)).transpose()

        nearest3D = np.argmin(np.abs(zcOld - zcNew), axis=0)

        index3D = np.hstack((index3D, idx3 + nearest3D))

    # get the 2D depth at each 3D cell (used to scale variables for some reason)
    depth = old['H'][tt, (old['idx2'][index3D] - 1)] - new['cell_Zb'][new['idx2'][:] - 1]

    # create empty array for data
    fvData = np.zeros((len(index3D), len(variables) + 1))

    # always set first column to depth
    fvData[:, 0] = depth

    # fill with other conserved variables
    for aa in range(len(variables)):
        if variables[aa] in old.variables:
            fvData[:, aa + 1] = old[variables[aa]][tt, index3D]

    write_restart_file(new.dimensions['NumCells2D'].size, new.dimensions['NumCells3D'].size,
                       time_stamp, new['cell_Zb'][:].data, fvData, out_file)

def _restart_from_result_beta(old_result_file, new_fvc_file, out_file, time_stamp, variables):
    """
    An untested version in the making which directly reads from a .fvc file the new geometry.

    Limited because it does not read for elevation limits set based on material type or shape file.

    This could one day be improved.
    """

    # set default geometry parameters
    cellFile = None
    numSigma = None
    layerFile = None
    minThick = None

    # read parameters from .fvc file
    with open(new_fvc_file, 'r') as f:
        # get start line
        line = f.readline()
        while line != '':
            if 'cell elevation file' in line:
                cellFile = line.split('==')[-1].strip()
            if 'sigma layers' in line:
                numSigma = int(line.split('==')[-1].strip())
            if 'layer faces' in line:
                layerFile = line.split('==')[-1].strip()
            if 'min bottom layer thickness' in line:
                minThick = float(line.split('==')[-1].strip())

            # read the next line
            line = f.readline()

    # get path to .fvc file folder
    fvcFolder = os.path.split(new_fvc_file)[0]

    # set paths to absolute, assume they are relative in the .fvc file
    cellFile = os.path.abspath(os.path.join(fvcFolder, cellFile))
    layerFile = os.path.abspath(os.path.join(fvcFolder, layerFile))

    # read the cell centred elevations
    data = np.loadtxt(cellFile, skiprows=1, delimiter=',', dtype=np.float64)
    cellX, cellY, cellZb = data[:, 0], data[:, 1], data[:, 2]

    # read the fixed elevation layers
    zLayers = np.loadtxt(layerFile, skiprows=1, delimiter=',', dtype=np.float64)

    # get result file netCDF handle
    old = Dataset(old_result_file)

    # get time index from target result file
    tt = np.argmin(np.abs(old['ResTime'] - time_stamp))

    # find the nearest 3D index for each cell
    index3D = np.array([], dtype=np.int32)  # maps new 3D to old 3D
    idx2 = np.array([], dtype=np.int32)  # maps new 2D to 3D
    for aa in range(cellZb.size):

        # get the distance to each 2D cell
        dx = old['cell_X'] - cellX[aa]
        dy = old['cell_Y'] - cellY[aa]
        distance = np.hypot(dx, dy)

        # get the index of the nearest old 2D cell
        nearest2D = np.argmin(distance)

        # check if old and new cell is\isn't dry
        dryDepth = old.getncattr('Dry depth')
        newDry = (old['H'][tt, nearest2D] - cellZb[aa]) < dryDepth
        oldDry = (old['stat'][tt, nearest2D] == 0)

        # if new cell is wet but old cell is dry, remap
        if (not newDry) and oldDry:
            distance[old['stat'][tt, :] == 0] = np.inf
            nearest2D = np.argmin(distance)

        # get the new water level and bed level
        wl, bl = old['H'][tt, nearest2D].data, cellZb[aa]

        # start from the top with the sigma layers
        dzTop = (wl - zLayers[0]) / numSigma
        lfzNew = wl - dzTop * np.arange(numSigma)

        # add in the elevation layers above the bed
        aboveBed = zLayers > bl
        botThick = zLayers - bl
        goodThick = botThick > minThick

        lgi = aboveBed & goodThick

        lfzNew = np.hstack((lfzNew, zLayers[lgi], bl))

        idx2 = np.hstack((idx2, np.repeat(aa, len(lfzNew) - 1)))

        # use layer faces to map new to old 3D points
        idx3 = old['idx3'][nearest2D] - 1
        nlfz = old['NL'][nearest2D] + 1
        idx4 = idx3 + nearest2D

        lfzOld = old['layerface_Z'][tt, idx4:idx4 + nlfz].data

        zcNew = 0.5 * (lfzNew[:-1] + lfzNew[1:])
        zcOld = 0.5 * (lfzOld[:-1] + lfzOld[1:])

        zcOld = np.tile(zcOld, (zcNew.size, 1)).transpose()

        nearest3D = np.argmin(np.abs(zcOld - zcNew), axis=0)

        index3D = np.hstack((index3D, idx3 + nearest3D))

    # get the 2D depth at each 3D cell (used to scale variables for some reason)
    depth = old['H'][tt, (old['idx2'][index3D] - 1)] - cellZb[idx2]

    # create empty array for data
    fvData = np.zeros((len(index3D), len(variables) + 1))

    # always set first column to depth
    fvData[:, 0] = depth

    # fill with other conserved variables
    for aa in range(len(variables)):
        if variables[aa] in old.variables:
            fvData[:, aa + 1] = old[variables[aa]][tt, index3D]

    write_restart_file(cellZb.size, idx2.size, time_stamp, cellZb, fvData, out_file)

