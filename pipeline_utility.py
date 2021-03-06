"""
This utility is used to provide useful functions for all things related to pipeline
design.
"""

from aide_design.units import unit_registry as u
from aide_design import physchem as pc
import aide_design.expert_inputs as exp
import aide_design.materials_database as mats
import numpy as numpy

@u.wraps(u.m**3/u.s, [u.m, u.m, None, u.m], False)
def flow_pipeline(diameters: numpy.ndarray, lengths: numpy.ndarray, k_minors: numpy.ndarray, target_headloss: float,
                  nu=exp.NU_WATER, pipe_rough=mats.PIPE_ROUGH_PVC):
    """
    This function takes a single pipeline with multiple sections, each potentially with different diameters,
    lengths and minor loss coefficients and determines the flow rate for a given headloss.

    Args:
        diameters: list of diameters, where the i_th diameter corresponds to the i_th pipe section
        lengths: list of diameters, where the i_th diameter corresponds to the i_th pipe section
        k_minors: list of diameters, where the i_th diameter corresponds to the i_th pipe section
        target_headloss: a single headloss describing the total headloss through the system
        nu: The fluid dynamic viscosity of the fluid. Defaults to water at room temperature (1 * 10**-6 * m**2/s)
        pipe_rough:  The pipe roughness. Defaults to PVC roughness.
    Returns:
        flow: the total flow through the system
    """

    # Ensure all the arguments except total headloss are the same length
    #TODO

    # Total number of pipe lengths
    n = diameters.size

    # Start with a flow rate guess based on the flow through a single pipe section
    flow = pc.flow_pipe(diameters[0], target_headloss, lengths[0], nu, pipe_rough, k_minors[0])
    err = 1.0

    # Add all the pipe length headlosses together to test the error
    while abs(err) > 0.01 :
        headloss = sum([pc.headloss(flow, diameters[i], lengths[i], nu, pipe_rough,
                                    k_minors[i]).to(u.m).magnitude for i in range(n)])
        # Test the error. This is always less than one.
        err = (target_headloss - headloss) / (target_headloss + headloss)
        # Adjust the total flow in the direction of the error. If there is more headloss than target headloss,
        # The flow should be reduced, and vice-versa.
        flow = flow + err * flow

    return flow