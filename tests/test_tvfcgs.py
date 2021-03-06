# -*- coding: utf-8 -*-
"""


"""
import nose
from nose import tools
import scipy as sp
from scipy import io
import numpy as np
from numpy import testing

# dynfunconn
from dyfunconn import tvfcg, tvfcg_ts, tvfcg_cfc
from dyfunconn.fc import PAC, PLV, plv


tvfcg_plv_ts = None
tvfcg_plv_fcgs = None
tvfcg_pac_plv_fcgs = None


def sample_ufunc(data):
    return np.abs(np.real(data))


def setup_module(module):
    global tvfcg_plv_ts
    global tvfcg_plv_fcgs
    global tvfcg_pac_plv_fcgs

    original_data = np.load("../examples/data/eeg_32chans_10secs.npy")

    # TVFCGS with PLV
    data = original_data[0:2, 0:1024]
    fb = [1.0, 4.0]
    fs = 128
    estimator = PLV(fb, fs)
    tvfcg_plv_fcgs = tvfcg(data, estimator, fb, fs)
    # tvfcg_plv_fcgs = np.real(tvfcg_plv_fcgs)
    np.save("data/test_tvfcgs_plv.npy", tvfcg_plv_fcgs)

    # TVFCGS with PAC and PLV
    data = original_data[..., 0:1024]
    fb = [1.0, 4.0]
    fs = 128
    f_lo = fb
    f_hi = [20.0, 30.0]
    estimator = PLV(fb, fs)
    pac = PAC(f_lo, f_hi, fs, estimator)
    tvfcg_pac_plv_fcgs = tvfcg_cfc(data, pac, f_lo, f_hi, fs)
    np.save("data/test_tvfcgs_pac_plv.npy", tvfcg_pac_plv_fcgs)

    # TVFCGS with PLV (ts)
    # fb = [1.0, 4.0]
    # fs = 128.0
    # ts, avg = plv(data, fb, fs)
    # tvfcg_plv_ts = tvfcg_ts(ts, [1.0, 4.0], 128, avg_func=PLV.mean)


def test_tvfcgs_plv():
    result_fcgs = np.load("data/test_tvfcgs_plv.npy")
    np.testing.assert_array_equal(tvfcg_plv_fcgs, result_fcgs)


def test_tvfcgs_pac_plv():
    result_ts = np.load("data/test_tvfcgs_pac_plv.npy")
    np.testing.assert_array_equal(tvfcg_pac_plv_fcgs, result_ts)


def test_tvfcgs_from_plv_ts():
    assert True
    # result_fcgs = np.load("data/test_tvfcgs_from_plv_ts.npy")
    # np.testing.assert_array_equal(tvfcg_plv_ts, result_fcgs)
