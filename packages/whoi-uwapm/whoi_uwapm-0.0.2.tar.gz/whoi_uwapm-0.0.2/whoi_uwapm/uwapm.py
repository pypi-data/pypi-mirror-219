##############################################################################
#
# Copyright (c) 2018, Mandar Chitre
#
# This file is part of arlpy which is released under Simplified BSD License.
# See file LICENSE or go to http://www.opensource.org/licenses/BSD-3-Clause
# for full license details.
#
##############################################################################

"""Underwater acoustic propagation modeling toolbox.

This toolbox currently uses the Bellhop acoustic propagation model. For this model
to work, the `acoustic toolbox <https://oalib-acoustics.org/>`_
must be installed on your computer and `bellhop.exe` should be in your PATH.

.. sidebar:: Sample Jupyter notebook

    For usage examples of this toolbox, see `Bellhop notebook <_static/bellhop.html>`_.
"""

import os as _os
import re as _re
import subprocess as _proc
import numpy as _np
from scipy import interpolate as _interp
import pandas as _pd
from tempfile import mkstemp as _mkstemp
from struct import unpack as _unpack

# constants
linear = 'linear'
spline = 'spline'
curvilinear = 'curvilinear'
arrivals = 'arrivals'
eigenrays = 'eigenrays'
rays = 'rays'
coherent = 'coherent'
incoherent = 'incoherent'
semicoherent = 'semicoherent'

# models (in order of preference)
_models = []

def create_env2d(**kv):
    """Create a new 2D underwater environment.

    A basic environment is created with default values. To see all the parameters
    available and their default values:

    >>> import arlpy.uwapm as pm
    >>> env = pm.create_env2d()
    >>> pm.print_env(env)

    The environment parameters may be changed by passing keyword arguments
    or modified later using a dictionary notation:

    >>> import arlpy.uwapm as pm
    >>> env = pm.create_env2d(depth=40, soundspeed=1540)
    >>> pm.print_env(env)
    >>> env['depth'] = 25
    >>> env['bottom_soundspeed'] = 1800
    >>> pm.print_env(env)

    The default environment has a constant sound speed. A depth dependent sound speed
    profile be provided as a Nx2 array of (depth, sound speed):

    >>> import arlpy.uwapm as pm
    >>> env = pm.create_env2d(depth=20, soundspeed=[[0,1540], [5,1535], [10,1535], [20,1530]])

    A range-and-depth dependent sound speed profile can be provided as a Pandas frame:

    >>> import arlpy.uwapm as pm
    >>> import pandas as pd
    >>> ssp2 = pd.DataFrame({
              0: [1540, 1530, 1532, 1533],     # profile at 0 m range
            100: [1540, 1535, 1530, 1533],     # profile at 100 m range
            200: [1530, 1520, 1522, 1525] },   # profile at 200 m range
            index=[0, 10, 20, 30])             # depths of the profile entries in m
    >>> env = pm.create_env2d(depth=20, soundspeed=ssp2)

    The default environment has a constant water depth. A range dependent bathymetry
    can be provided as a Nx2 array of (range, water depth):

    >>> import arlpy.uwapm as pm
    >>> env = pm.create_env2d(depth=[[0,20], [300,10], [500,18], [1000,15]])
    """
    env = {
        'name': 'arlpy',
        'type': '2D',                   # 2D/3D
        'frequency': 25000,             # Hz
        'soundspeed': 1500,             # m/s
        'soundspeed_interp': spline,    # spline/linear
        'bottom_soundspeed': 1600,      # m/s
        'bottom_density': 1600,         # kg/m^3
        'bottom_absorption': 0.1,       # dB/wavelength
        'bottom_roughness': 0,          # m (rms)
        'surface': None,                # surface profile
        'surface_interp': linear,       # curvilinear/linear
        'tx_depth': 5,                  # m
        'tx_directionality': None,      # [(deg, dB)...]
        'rx_depth': 10,                 # m
        'rx_range': 1000,               # m
        'depth': 25,                    # m
        'depth_interp': linear,         # curvilinear/linear
        'min_angle': -80,               # deg
        'max_angle': 80,                # deg
        'nbeams': 0                     # number of beams (0 = auto)
    }
    for k, v in kv.items():
        if k not in env.keys():
            raise KeyError('Unknown key: '+k)
        env[k] = _np.asarray(v, dtype=_np.float64) if not isinstance(v, _pd.DataFrame) and _np.size(v) > 1 else v
    env = check_env2d(env)
    return env

def check_env2d(env):
    """Check the validity of a 2D underwater environment definition.

    :param env: environment definition

    Exceptions are thrown with appropriate error messages if the environment is invalid.

    >>> import arlpy.uwapm as pm
    >>> env = pm.create_env2d()
    >>> check_env2d(env)
    """
    try:
        assert env['type'] == '2D', 'Not a 2D environment'
        max_range = _np.max(env['rx_range'])
        if env['surface'] is not None:
            assert _np.size(env['surface']) > 1, 'surface must be an Nx2 array'
            assert env['surface'].ndim == 2, 'surface must be a scalar or an Nx2 array'
            assert env['surface'].shape[1] == 2, 'surface must be a scalar or an Nx2 array'
            assert env['surface'][0,0] <= 0, 'First range in surface array must be 0 m'
            assert env['surface'][-1,0] >= max_range, 'Last range in surface array must be beyond maximum range: '+str(max_range)+' m'
            assert _np.all(_np.diff(env['surface'][:,0]) > 0), 'surface array must be strictly monotonic in range'
            assert env['surface_interp'] == curvilinear or env['surface_interp'] == linear, 'Invalid interpolation type: '+str(env['surface_interp'])
        if _np.size(env['depth']) > 1:
            assert env['depth'].ndim == 2, 'depth must be a scalar or an Nx2 array'
            assert env['depth'].shape[1] == 2, 'depth must be a scalar or an Nx2 array'
            assert env['depth'][0,0] <= 0, 'First range in depth array must be 0 m'
            assert env['depth'][-1,0] >= max_range, 'Last range in depth array must be beyond maximum range: '+str(max_range)+' m'
            assert _np.all(_np.diff(env['depth'][:,0]) > 0), 'Depth array must be strictly monotonic in range'
            assert env['depth_interp'] == curvilinear or env['depth_interp'] == linear, 'Invalid interpolation type: '+str(env['depth_interp'])
            max_depth = _np.max(env['depth'][:,1])
        else:
            max_depth = env['depth']
        if isinstance(env['soundspeed'], _pd.DataFrame):
            assert env['soundspeed'].shape[0] > 3, 'soundspeed profile must have at least 4 points'
            assert env['soundspeed'].index[0] <= 0, 'First depth in soundspeed array must be 0 m'
            assert env['soundspeed'].index[-1] >= max_depth, 'Last depth in soundspeed array must be beyond water depth: '+str(max_depth)+' m'
            assert _np.all(_np.diff(env['soundspeed'].index) > 0), 'Soundspeed array must be strictly monotonic in depth'
        elif _np.size(env['soundspeed']) > 1:
            assert env['soundspeed'].ndim == 2, 'soundspeed must be a scalar or an Nx2 array'
            assert env['soundspeed'].shape[1] == 2, 'soundspeed must be a scalar or an Nx2 array'
            assert env['soundspeed'].shape[0] > 3, 'soundspeed profile must have at least 4 points'
            assert env['soundspeed'][0,0] <= 0, 'First depth in soundspeed array must be 0 m'
            assert env['soundspeed'][-1,0] >= max_depth, 'Last depth in soundspeed array must be beyond water depth: '+str(max_depth)+' m'
            assert _np.all(_np.diff(env['soundspeed'][:,0]) > 0), 'Soundspeed array must be strictly monotonic in depth'
            assert env['soundspeed_interp'] == spline or env['soundspeed_interp'] == linear, 'Invalid interpolation type: '+str(env['soundspeed_interp'])
            if not(max_depth in env['soundspeed'][:,0]):
                indlarger = _np.argwhere(env['soundspeed'][:,0]>max_depth)[0][0]
                if env['soundspeed_interp'] == spline:
                    tck = _interp.splrep(env['soundspeed'][:,0], env['soundspeed'][:,1], s=0)
                    insert_ss_val = _interp.splev(max_depth, tck, der=0)
                else:
                    insert_ss_val = _np.interp(max_depth, env['soundspeed'][:,0], env['soundspeed'][:,1])
                env['soundspeed'] = _np.insert(env['soundspeed'],indlarger,[max_depth,insert_ss_val],axis = 0)
                env['soundspeed'] = env['soundspeed'][:indlarger+1,:]
        assert _np.max(env['tx_depth']) <= max_depth, 'tx_depth cannot exceed water depth: '+str(max_depth)+' m'
        assert _np.max(env['rx_depth']) <= max_depth, 'rx_depth cannot exceed water depth: '+str(max_depth)+' m'
        assert env['min_angle'] > -90 and env['min_angle'] < 90, 'min_angle must be in range (-90, 90)'
        assert env['max_angle'] > -90 and env['max_angle'] < 90, 'max_angle must be in range (-90, 90)'
        if env['tx_directionality'] is not None:
            assert _np.size(env['tx_directionality']) > 1, 'tx_directionality must be an Nx2 array'
            assert env['tx_directionality'].ndim == 2, 'tx_directionality must be an Nx2 array'
            assert env['tx_directionality'].shape[1] == 2, 'tx_directionality must be an Nx2 array'
            assert _np.all(env['tx_directionality'][:,0] >= -180) and _np.all(env['tx_directionality'][:,0] <= 180), 'tx_directionality angles must be in [-90, 90]'
        return env
    except AssertionError as e:
        raise ValueError(e.args)

def print_env(env):
    """Display the environment in a human readable form.

    :param env: environment definition

    >>> import arlpy.uwapm as pm
    >>> env = pm.create_env2d(depth=40, soundspeed=1540)
    >>> pm.print_env(env)
    """
    env = check_env2d(env)
    keys = ['name'] + sorted(list(env.keys()-['name']))
    for k in keys:
        v = str(env[k])
        if '\n' in v:
            v = v.split('\n')
            print('%20s : '%(k) + v[0])
            for v1 in v[1:]:
                print('%20s   '%('') + v1)
        else:
            print('%20s : '%(k) + v)

def compute_arrivals(env, model=None, debug=False):
    """Compute arrivals between each transmitter and receiver.

    :param env: environment definition
    :param model: propagation model to use (None to auto-select)
    :param debug: generate debug information for propagation model
    :returns: arrival times and coefficients for all transmitter-receiver combinations

    >>> import arlpy.uwapm as pm
    >>> env = pm.create_env2d()
    >>> arrivals = pm.compute_arrivals(env)
    >>> pm.plot_arrivals(arrivals)
    """
    env = check_env2d(env)
    (model_name, model) = _select_model(env, arrivals, model)
    if debug:
        print('[DEBUG] Model: '+model_name)
    return model.run(env, arrivals, debug)

def compute_transmission_loss(env, tx_depth_ndx=0, mode=coherent, model=None, debug=False):
    """Compute transmission loss from a given transmitter to all receviers.

    :param env: environment definition
    :param tx_depth_ndx: transmitter depth index
    :param mode: coherent, incoherent or semicoherent
    :param model: propagation model to use (None to auto-select)
    :param debug: generate debug information for propagation model
    :returns: complex transmission loss at each receiver depth and range

    >>> import arlpy.uwapm as pm
    >>> env = pm.create_env2d()
    >>> tloss = pm.compute_transmission_loss(env, mode=pm.incoherent)
    >>> pm.plot_transmission_loss(tloss, width=1000)
    """
    env = check_env2d(env)
    if mode not in [coherent, incoherent, semicoherent]:
        raise ValueError('Unknown transmission loss mode: '+mode)
    if _np.size(env['tx_depth']) > 1:
        env = env.copy()
        env['tx_depth'] = env['tx_depth'][tx_depth_ndx]
    (model_name, model) = _select_model(env, mode, model)
    if debug:
        print('[DEBUG] Model: '+model_name)
    return model.run(env, mode, debug)


def models(env=None, task=None):
    """List available models.

    :param env: environment to model
    :param task: arrivals/eigenrays/rays/coherent/incoherent/semicoherent
    :returns: list of models that can be used

    >>> import arlpy.uwapm as pm
    >>> pm.models()
    ['bellhop']
    >>> env = pm.create_env2d()
    >>> pm.models(env, task=coherent)
    ['bellhop']
    """
    if env is not None:
        env = check_env2d(env)
    if (env is None and task is not None) or (env is not None and task is None):
        raise ValueError('env and task should be both specified together')
    rv = []
    for m in _models:
        if m[1]().supports(env, task):
            rv.append(m[0])
    return rv

def _select_model(env, task, model):
    if model is not None:
        for m in _models:
            if m[0] == model:
                return (m[0], m[1]())
        raise ValueError('Unknown model: '+model)
    for m in _models:
        mm = m[1]()
        if mm.supports(env, task):
            return (m[0], mm)
    raise ValueError('No suitable propagation model available')

### Bellhop propagation model ###

class _Bellhop:

    def __init__(self):
        pass

    def supports(self, env=None, task=None):
        if env is not None and env['type'] != '2D':
            return False
        fh, fname = _mkstemp(suffix='.env')
        _os.close(fh)
        fname_base = fname[:-4]
        self._unlink(fname_base+'.env')
        rv = self._bellhop(fname_base)
        self._unlink(fname_base+'.prt')
        self._unlink(fname_base+'.log')
        return rv

    def run(self, env, task, debug=False):
        taskmap = {
            arrivals:     ['A', self._load_arrivals],
            eigenrays:    ['E', self._load_rays],
            rays:         ['R', self._load_rays],
            coherent:     ['C', self._load_shd],
            incoherent:   ['I', self._load_shd],
            semicoherent: ['S', self._load_shd]
        }
        fname_base = self._create_env_file(env, taskmap[task][0])
        results = None
        if self._bellhop(fname_base):
            err = self._check_error(fname_base)
            if err is not None:
                print(err)
            else:
                try:
                    results = taskmap[task][1](fname_base)
                except FileNotFoundError:
                    print('[WARN] Bellhop did not generate expected output file')
        if debug:
            print('[DEBUG] Bellhop working files: '+fname_base+'.*')
        else:
            self._unlink(fname_base+'.env')
            self._unlink(fname_base+'.bty')
            self._unlink(fname_base+'.ssp')
            self._unlink(fname_base+'.ati')
            self._unlink(fname_base+'.sbp')
            self._unlink(fname_base+'.prt')
            self._unlink(fname_base+'.log')
            self._unlink(fname_base+'.arr')
            self._unlink(fname_base+'.ray')
            self._unlink(fname_base+'.shd')
        return results

    def _bellhop(self, *args):
        try: 
            bellhop_file_path = _os.path.join(_os.path.dirname(__file__), 'bellhopcxx')
            _proc.run(f'{bellhop_file_path} {" ".join(list(args))}', 
                      stderr=_proc.STDOUT, stdout=_proc.PIPE,
                      shell=True)
        except OSError:
            return False
        return True

    def _unlink(self, f):
        try:
            _os.unlink(f)
        except:
            pass

    def _print(self, fh, s, newline=True):
        _os.write(fh, (s+'\n' if newline else s).encode())

    def _print_array(self, fh, a):
        if _np.size(a) == 1:
            self._print(fh, "1")
            self._print(fh, "%0.6f /" % (a))
        else:
            self._print(fh, str(_np.size(a)))
            for j in a:
                self._print(fh, "%0.6f " % (j), newline=False)
            self._print(fh, "/")

    def _create_env_file(self, env, taskcode):
        fh, fname = _mkstemp(suffix='.env')
        fname_base = fname[:-4]
        self._print(fh, "'"+env['name']+"'")
        self._print(fh, "%0.6f" % (env['frequency']))
        self._print(fh, "1")
        svp = env['soundspeed']
        svp_depth = 0.0
        svp_interp = 'S' if env['soundspeed_interp'] == spline else 'C'
        if isinstance(svp, _pd.DataFrame):
            svp_depth = svp.index[-1]
            if len(svp.columns) > 1:
                svp_interp = 'Q'
            else:
                svp = _np.hstack((_np.array([svp.index]).T, _np.asarray(svp)))
        if env['surface'] is None:
            self._print(fh, "'%cVWT'" % svp_interp)
        else:
            self._print(fh, "'%cVWT*'" % svp_interp)
            self._create_bty_ati_file(fname_base+'.ati', env['surface'], env['surface_interp'])
        #max depth should be the depth of the acoustic domain, which can be deeper than the max depth bathymetry
        max_depth = env['depth'] if _np.size(env['depth']) == 1 else max(_np.max(env['depth'][:,1]), svp_depth)
        self._print(fh, "1 0.0 %0.6f" % (max_depth))
        if _np.size(svp) == 1:
            self._print(fh, "0.0 %0.6f /" % (svp))
            self._print(fh, "%0.6f %0.6f /" % (max_depth, svp))
        elif svp_interp == 'Q':
            for j in range(svp.shape[0]):
                self._print(fh, "%0.6f %0.6f /" % (svp.index[j], svp.iloc[j,0]))
            self._create_ssp_file(fname_base+'.ssp', svp)
        else:
            for j in range(svp.shape[0]):
                self._print(fh, "%0.6f %0.6f /" % (svp[j,0], svp[j,1]))
        depth = env['depth']
        if _np.size(depth) == 1:
            self._print(fh, "'A' %0.6f" % (env['bottom_roughness']))
        else:
            self._print(fh, "'A*' %0.6f" % (env['bottom_roughness']))
            self._create_bty_ati_file(fname_base+'.bty', depth, env['depth_interp'])
        self._print(fh, "%0.6f %0.6f 0.0 %0.6f %0.6f /" % (max_depth, env['bottom_soundspeed'], env['bottom_density']/1000, env['bottom_absorption']))
        self._print_array(fh, env['tx_depth'])
        self._print_array(fh, env['rx_depth'])
        self._print_array(fh, env['rx_range']/1000)
        if env['tx_directionality'] is None:
            self._print(fh, "'"+taskcode+"'")
        else:
            self._print(fh, "'"+taskcode+" *'")
            self._create_sbp_file(fname_base+'.sbp', env['tx_directionality'])
        self._print(fh, "%d" % (env['nbeams']))
        self._print(fh, "%0.6f %0.6f /" % (env['min_angle'], env['max_angle']))
        self._print(fh, "0.0 %0.6f %0.6f" % (1.01*max_depth, 1.01*_np.max(env['rx_range'])/1000))
        _os.close(fh)
        return fname_base

    def _create_bty_ati_file(self, filename, depth, interp):
        with open(filename, 'wt') as f:
            f.write("'%c'\n" % ('C' if interp == curvilinear else 'L'))
            f.write(str(depth.shape[0])+"\n")
            for j in range(depth.shape[0]):
                f.write("%0.6f %0.6f\n" % (depth[j,0]/1000, depth[j,1]))

    def _create_sbp_file(self, filename, dir):
        with open(filename, 'wt') as f:
            f.write(str(dir.shape[0])+"\n")
            for j in range(dir.shape[0]):
                f.write("%0.6f %0.6f\n" % (dir[j,0], dir[j,1]))

    def _create_ssp_file(self, filename, svp):
        with open(filename, 'wt') as f:
            f.write(str(svp.shape[1])+"\n")
            for j in range(svp.shape[1]):
                f.write("%0.6f%c" % (svp.columns[j]/1000, '\n' if j == svp.shape[1]-1 else ' '))
            for k in range(svp.shape[0]):
                for j in range(svp.shape[1]):
                    f.write("%0.6f%c" % (svp.iloc[k,j], '\n' if j == svp.shape[1]-1 else ' '))

    def _readf(self, f, types, dtype=str):
        if type(f) is str:
            p = _re.split(r' +', f.strip())
        else:
            p = _re.split(r' +', f.readline().strip())
        for j in range(len(p)):
            if len(types) > j:
                p[j] = types[j](p[j])
            else:
                p[j] = dtype(p[j])
        return tuple(p)

    def _check_error(self, fname_base):
        err = None
        try:
            with open(fname_base+'.prt', 'rt') as f:
                for lno, s in enumerate(f):
                    if err is not None:
                        err += '[BELLHOP] ' + s
                    elif '*** FATAL ERROR ***' in s:
                        err = '\n[BELLHOP] ' + s
        except:
            pass
        return err

    def _load_arrivals(self, fname_base):
        with open(fname_base+'.arr', 'rt') as f:
            hdr = f.readline()
            if hdr.find('2D') >= 0:
                freq = self._readf(f, (float,))
                tx_depth_info = self._readf(f, (int,), float)
                tx_depth_count = tx_depth_info[0]
                tx_depth = tx_depth_info[1:]
                assert tx_depth_count == len(tx_depth)
                rx_depth_info = self._readf(f, (int,), float)
                rx_depth_count = rx_depth_info[0]
                rx_depth = rx_depth_info[1:]
                assert rx_depth_count == len(rx_depth)
                rx_range_info = self._readf(f, (int,), float)
                rx_range_count = rx_range_info[0]
                rx_range = rx_range_info[1:]
                assert rx_range_count == len(rx_range)
            else:
                freq, tx_depth_count, rx_depth_count, rx_range_count = self._readf(hdr, (float, int, int, int))
                tx_depth = self._readf(f, (float,)*tx_depth_count)
                rx_depth = self._readf(f, (float,)*rx_depth_count)
                rx_range = self._readf(f, (float,)*rx_range_count)
            arrivals = []
            for j in range(tx_depth_count):
                f.readline()
                for k in range(rx_depth_count):
                    for m in range(rx_range_count):
                        count = int(f.readline())
                        for n in range(count):
                            data = self._readf(f, (float, float, float, float, float, float, int, int))
                            arrivals.append(_pd.DataFrame({
                                'tx_depth_ndx': [j],
                                'rx_depth_ndx': [k],
                                'rx_range_ndx': [m],
                                'tx_depth': [tx_depth[j]],
                                'rx_depth': [rx_depth[k]],
                                'rx_range': [rx_range[m]],
                                'arrival_number': [n],
                                'arrival_amplitude': [data[0]*_np.exp(1j*data[1])],
                                'time_of_arrival': [data[2]],
                                'angle_of_departure': [data[4]],
                                'angle_of_arrival': [data[5]],
                                'surface_bounces': [data[6]],
                                'bottom_bounces': [data[7]]
                            }, index=[len(arrivals)+1]))
        return _pd.concat(arrivals)

    def _load_rays(self, fname_base):
        with open(fname_base+'.ray', 'rt') as f:
            f.readline()
            f.readline()
            f.readline()
            f.readline()
            f.readline()
            f.readline()
            f.readline()
            rays = []
            while True:
                s = f.readline()
                if s is None or len(s.strip()) == 0:
                    break
                a = float(s)
                pts, sb, bb = self._readf(f, (int, int, int))
                ray = _np.empty((pts, 2))
                for k in range(pts):
                    ray[k,:] = self._readf(f, (float, float))
                rays.append(_pd.DataFrame({
                    'angle_of_departure': [a],
                    'surface_bounces': [sb],
                    'bottom_bounces': [bb],
                    'ray': [ray]
                }))
        return _pd.concat(rays)

    def _load_shd(self, fname_base):
        with open(fname_base+'.shd', 'rb') as f:
            recl, = _unpack('i', f.read(4))
            title = str(f.read(80))
            f.seek(4*recl, 0)
            ptype = f.read(10).decode('utf8').strip()
            assert ptype == 'rectilin', 'Invalid file format (expecting ptype == "rectilin")'
            f.seek(8*recl, 0)
            nfreq, ntheta, nsx, nsy, nsd, nrd, nrr, atten = _unpack('iiiiiiif', f.read(32))
            assert nfreq == 1, 'Invalid file format (expecting nfreq == 1)'
            assert ntheta == 1, 'Invalid file format (expecting ntheta == 1)'
            assert nsd == 1, 'Invalid file format (expecting nsd == 1)'
            f.seek(32*recl, 0)
            pos_r_depth = _unpack('f'*nrd, f.read(4*nrd))
            f.seek(36*recl, 0)
            pos_r_range = _unpack('f'*nrr, f.read(4*nrr))
            pressure = _np.zeros((nrd, nrr), dtype=_np.complex128)
            for ird in range(nrd):
                recnum = 10 + ird
                f.seek(recnum*4*recl, 0)
                temp = _np.array(_unpack('f'*2*nrr, f.read(2*nrr*4)))
                pressure[ird,:] = temp[::2] + 1j*temp[1::2]
        return _pd.DataFrame(pressure, index=pos_r_depth, columns=pos_r_range)

_models.append(('bellhop', _Bellhop))