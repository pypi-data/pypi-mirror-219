import unittest
import xarray as xr
import tfv.xarray
import matplotlib.pyplot as plt
from pathlib import Path

path = Path(__file__).parent / 'data'
fv = xr.open_dataset(path / 'HYD_002_mini.nc').tfv

class TestTfvDomain(unittest.TestCase):
    def test_get_sheet_H_numcells2d(self):
        ''' Test that get sheet runs with very simple defaults and a 2D var '''
        dims = fv.get_sheet('H')['H'].shape
        self.assertEqual(dims[1], fv.dims['NumCells2D'])

    def test_get_sheet_V_numcells2d(self):
        ''' Test that get sheet runs with the magic 'V' variable '''
        dims = fv.get_sheet('V')['V'].shape 
        self.assertEqual(dims[1], fv.dims['NumCells2D'])
        
    def test_get_sheet_TEMP_time_integer_slice(self):
        ''' Test that get sheet runs with integer slicing '''
        tslc = slice(1, 3)
        ts = fv._obj.isel(Time=tslc).dims['Time'] # Correct behaviour 
        
        # Check func behaviour
        dims = fv.get_sheet('TEMP', time=tslc)['TEMP'].shape
        self.assertEqual(dims[0], ts)
        
    def test_get_sheet_TEMP_time_single_time_integer(self):
        ''' Test that get sheet runs with single integer time '''        
        # Check func behaviour
        dims = fv.get_sheet('TEMP', time=1)['TEMP'].shape
        self.assertEqual(dims[0], 1)
        
    # def test_get_sheet_TEMP_time_single_time_datestr(self):
        # ''' Test that get sheet runs with a hard datestr '''        
        ## Check func behaviour
        # dims = fv.get_sheet('TEMP', time='2011-02-01T02:00:00.263494800')['TEMP'].shape
        # self.assertEqual(dims[0], 1)
        
    def test_get_statistics_single_stat(self):
        ''' Test a single statistic '''
        # Check func behaviour
        dims = fv.get_statistics('mean', 'V')['V_mean'].shape
        self.assertEqual(dims[0], 1)
        
    def test_get_statistics_several_stats(self):
        ''' Test several statistics '''        
        # Check func behaviour
        stats = ['mean', 'p95', 'p20', 'sum']
        var = 'SAL'
        
        fv2d = fv.get_statistics(stats, var)
        
        svar = f'{var}_{stats[2]}'
        timecheck = fv2d.dims['Time'] == 1
        varcheck = len(fv2d.variables) == len(stats)
        dimcheck = fv2d[svar].shape[1] == fv.dims['NumCells2D']
        
        self.assertTrue(timecheck & varcheck & dimcheck)
        
    def test_get_timeseries(self):
        ''' Test get timeseries with defaults, multi locations. '''        
        # Check func behaviour
        locs = dict(
            pt1=(159.09380193, -31.39236190),
            pt2=(159.11004448, -31.39781102)
        )
        vars = ('H', 'V', 'V_x', 'SAL')
        
        ts = fv.get_timeseries(vars, locs)
        
        timecheck = ts.dims['Time'] == fv.dims['Time']
        varcheck = len(ts.data_vars) == len(vars)
        dimcheck = ts.dims['Location'] == len(locs)
        
        self.assertTrue(timecheck & varcheck & dimcheck)

    def test_get_timeseries_with_dave_opts(self):
        ''' Test get timeseries with depthaveraging options'''        
        # Check func behaviour
        locs = dict(
            pt1=(159.09380193, -31.39236190),
        )
        vars = ('H', 'SAL')
        datum = 'height'
        limits=(0,2.42)
        agg='max'
        
        ts = fv.get_timeseries(vars, locs, datum=datum, limits=limits, agg=agg)
        
        timecheck = ts.dims['Time'] == fv.dims['Time']
        varcheck = len(ts.data_vars) == len(vars)
        dimcheck = 'Location' not in ts.dims  # Only one location, should not be present!
        
        self.assertTrue(timecheck & varcheck & dimcheck)

    def test_get_profile_variables(self):
        ''' Test get profile a set of variables '''
        locs = dict(
            pt1=(159.09380193, -31.39236190),
        )
        vars = ('H', 'V', 'V_x', 'SAL')

        prof = fv.get_profile(locs, variables=vars)

        # Check all variables made it through
        vars_all = len(prof.data_vars) == len(vars)+5
        vars_in = all([x in prof.data_vars for x in vars])
        
        self.assertTrue(all([vars_all, vars_in]))
        
    def test_get_profile_dims(self):
        ''' Test get profile a set of variables '''
        locs = dict(
            pt1=(159.09380193, -31.39236190),
        )
        vars = ('H', 'V', 'V_x', 'SAL')
        nt = 2
        prof = fv.get_profile(locs, time=slice(nt), variables=vars)
        
        dims = all([
            'N1' in prof.dims, # to match TUFLOW FV output
            'NumLayers' in prof.dims,  # 3D model should have this!
            'NumLayerFaces' in prof.dims, # Lfz as standard
        ])

        shp = all([
            prof.dims['Time'] == nt,
        ])
        self.assertTrue(all([dims, shp]))
    
    def test_plot_defaults_H(self):
        ''' Test whether the default plot picks the correct time, and runs without issue. '''
        var = 'H'
        time = '2011-02-01 02:00'

        fv.plot(var, time)
        ax = plt.gca()

        self.assertEqual(time, ax.get_title())
        
    def test_plot_defaults_V(self):
        ''' Test whether the default plot works with the magic V var, and auto-labels'''
        var = 'V'
        vlbl = 'current speed (m s^-1)' # Auto label should assign this.
        time = '2011-02-01 02:30'

        fv.plot(var, time)
        fig = plt.gcf()
        
        # Loop through children to get colorbar
        for c in fig.get_children():
            if hasattr(c.axes, 'get_label'):
                if c.axes.get_label() == '<colorbar>':
                    lbl = c.axes.get_ylabel()

        self.assertEqual(vlbl, lbl)

if __name__ == '__main__':
    unittest.main()
