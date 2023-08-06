"""
   Tests for the pysid module 
"""

import pysid as sid
from numpy import dot, randn
from scipy.signal import lfilter
from scipy.stats import chi2

# Define an elispe
def get_value_elipse(t, t0, P):
    """ Returns the value (t - t0).T P (t - t0) """


def test_arx_siso(N):
    # Generate Data
    u = randn(N, 1)
    e = 0.01*randn(N, 1)
    A = np.array([1, -1.2, 0.36])
    B = np.array([0, 0.8, 0.2])
    theto = np.array(A[1:].to_list()+B[1:].to_list())
    
    thetao = np.array([-1.2, 0.36])

