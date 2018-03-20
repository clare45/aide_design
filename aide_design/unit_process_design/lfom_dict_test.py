
"""This file contains all the functions needed to design the linear flow
orifice meter (LFOM) for an AguaClara plant.

"""

#Here we import packages that we will need for this notebook. You can find out about these packages in the Help menu.
from aide_design.play import*

#primary outputs from this file are
#Nominal diameter nom_diam_lfom_pipe(FLOW,HL_LFOM,con.RATIO_LFOM_SAFETY)
#number of rows n_lfom_rows(FLOW,HL_LFOM)
#orifice diameter orifice_diameter(FLOW,HL_LFOM,drill_series_uom)
#number of orifices in each row n_lfom_orifices(FLOW,HL_LFOM,drill_series_uom)
#height of the center of each row height_lfom_orifices(FLOW,HL_LFOM,drill_series_uom)

# will eventually define this by rendering a template, but we'll get to that later:
lfom_dict = {'sdr': 26, 'RATIO_VC_ORIFICE': 0.63, 'ratio_safety':  1.5,
             'S_orifice': 1*u.cm, 'hl': 20*u.cm}

# output is width per flow rate.
@u.wraps(u.s/(u.m**2), [u.m,u.m], False)
def width_stout(hl, Z, lfom_inputs=lfom_dict):
    """?

    Parameters
    ----------
    hl : float
        headloss through the LFOM

    Z : float
        depth of water

    lfom_inputs : dict
        a dictionary of all of the constant inputs needed for LFOM calculations
        can be found in lfom.yaml

    Returns
    -------
    float
        ?

    Examples
    --------
    >>> from aide_design.play import*
    >>> lfom_dict = {'sdr': 26, 'RATIO_VC_ORIFICE': 0.63, 'ratio_safety':  1.5,
    ...              'S_orifice': 1*u.cm, 'hl': 20*u.cm}
    >>> width_stout(40*u.cm, 40*u.cm)
    0.9019329453483474 second/meter²
    >>> width_stout(20*u.cm, 1*u.cm, lfom_dict)
    11.408649616179787 second/meter²

    """
    return (2/((2 * pc.gravity.magnitude*Z)**(1/2)
            * lfom_inputs['RATIO_VC_ORIFICE']*np.pi*hl))

@u.wraps(None, [u.m**3/u.s,u.m], False)
def n_lfom_rows(Q, hl, lfom_inputs=lfom_dict):
    """This equation states that the open area corresponding to one row can be
    set equal to two orifices of diameter=row height. If there are more than
    two orifices per row at the top of the LFOM then there are more orifices
    than are convenient to drill and more than necessary for good accuracy.
    Thus this relationship can be used to increase the spacing between the
    rows and thus increase the diameter of the orifices. This spacing function
    also sets the lower depth on the high flow rate LFOM with no accurate
    flows below a depth equal to the first row height.

    But it might be better to always set then number of rows to 10.
    The challenge is to figure out a reasonable system of constraints that
    reliably returns a valid solution.

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl: float
        headloss through the LFOM

    lfom_inputs : dict
        a dictionary of all of the constant inputs needed for LFOM calculations
        can be found in lfom.yaml

    Returns
    -------
    float
        ?

    Examples
    --------
    >>> from aide_design.play import*
    >>> lfom_dict = {'sdr': 26, 'RATIO_VC_ORIFICE': 0.63, 'ratio_safety':  1.5,
    ...              'S_orifice': 1*u.cm, 'hl': 20*u.cm}
    """
    N_est = (hl*np.pi/(2*width_stout(hl, hl, lfom_inputs)*Q))
    variablerow = min(10, max(4, math.trunc(N_est)))
    # Forcing the LFOM to either have 4 or 8 rows, for design purposes
    # If the hydraulic calculation finds that there should be 4 rows, then there
    # will be 4 rows. If anything other besides 4 rows is found, then assign 8
    # rows.
    # This can be improved in the future.
    if variablerow != 4:
        variablerow = 8
    return variablerow

@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def dist_center_lfom_rows(Q, hl, lfom_inputs=lfom_dict):
    """
    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl: float
        headloss through the LFOM

    lfom_inputs : dict
        a dictionary of all of the constant inputs needed for LFOM calculations
        can be found in lfom.yaml

    Returns
    -------
    float
        ?

    Examples
    --------
    >>> from aide_design.play import*
    >>> lfom_dict = {'sdr': 26, 'RATIO_VC_ORIFICE': 0.63, 'ratio_safety':  1.5,
    ...              'S_orifice': 1*u.cm, 'hl': 20*u.cm}
    >>> dist_center_lfom_rows(20*u.m**3/u.s, 20*u.m)
    ?
    """
    return hl/n_lfom_rows(Q, hl, lfom_inputs)



@u.wraps(u.m/u.s, [u.m], False)
def vel_lfom_pipe_critical(hl, lfom_inputs=lfom_dict):
    """
    The average vertical velocity of the water inside the LFOM pipe
    at the very bottom of the bottom row of orifices
    The speed of falling water is 0.841 m/s for all linear flow orifice meters
    of height 20 cm, independent of total plant flow rate.

    Parameters
    ----------
    hl: float
        headloss through the LFOM

    lfom_inputs : dict
        a dictionary of all of the constant inputs needed for LFOM calculations
        can be found in lfom.yaml

    Returns
    -------
    float
        ?

    Examples
    --------
    >>> from aide_design.play import*
    >>> lfom_dict = {'sdr': 26, 'RATIO_VC_ORIFICE': 0.63, 'ratio_safety':  1.5,
    ...              'S_orifice': 1*u.cm, 'hl': 20*u.cm}
    >>> vel_lfom_pipe_critical(20*u.cm)
    0.8405802802312778 meter/second
    >>> vel_lfom_pipe_critical(60*u.cm)
    1.4559277532010582 meter/second
    """
    return 4/(3*math.pi)*(2*pc.gravity.magnitude*hl)**(1/2)


@u.wraps(u.m**2, [u.m**3/u.s, u.m], False)
def area_lfom_pipe_min(Q, hl, lfom_inputs=lfom_dict):
    """
    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl: float
        headloss through the LFOM

    lfom_inputs : dict
        a dictionary of all of the constant inputs needed for LFOM calculations
        can be found in lfom.yaml

    Returns
    -------
    float
        ?

    Examples
    --------
    >>> from aide_design.play import*
    >>> lfom_dict = {'sdr': 26, 'RATIO_VC_ORIFICE': 0.63, 'ratio_safety':  1.5,
    ...              'S_orifice': 1*u.cm, 'hl': 20*u.cm}
    >>> dist_center_lfom_rows(20*u.m**3/u.s, 20*u.m)
    """
    return (lfom_inputs.ratio_safety*Q/vel_lfom_pipe_critical(hl, lfom_inputs).magnitude)

@u.wraps(u.inch, [u.m**3/u.s, u.m], False)
def nom_diam_lfom_pipe(Q, hl, lfom_inputs=lfom_dict):
    ID = pc.diam_circle(area_lfom_pipe_min(Q, hl, lfom_inputs))
    return pipe.ND_SDR_available(ID, lfom_inputs['sdr']).magnitude

@u.wraps(u.m**2, [u.m**3/u.s, u.m], False)
def area_lfom_orifices_top(Q, hl, lfom_inputs=lfom_dict):
    """Estimate the orifice area corresponding to the top row of orifices.
    Another solution method is to use integration to solve this problem.
    Here we use the width of the stout weir in the center of the top row
    to estimate the area of the top orifice
    """
    return ((Q * width_stout(hl*u.m, hl*u.m-0.5 *
            dist_center_lfom_rows(Q, hl, lfom_inputs), lfom_inputs).magnitude *
            dist_center_lfom_rows(Q, hl, lfom_inputs).magnitude))

@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def d_lfom_orifices_max(Q, hl, lfom_inputs=lfom_dict):
    return (pc.diam_circle(
            area_lfom_orifices_top(Q, hl, lfom_inputs).magnitude).magnitude)

@u.wraps(u.m, [u.m**3/u.s, u.m, u.inch], False)
def orifice_diameter(Q, hl, drill_bits, lfom_inputs=lfom_dict):
    maxdrill = (min((dist_center_lfom_rows(Q, hl, lfom_inputs).magnitude),
                (d_lfom_orifices_max(Q, hl, lfom_inputs).magnitude)))
    return ut.floor_nearest(maxdrill, drill_bits)

@u.wraps(u.m**2, [u.m**3/u.s, u.m, u.inch], False)
def drillbit_area(Q, hl, drill_bits, lfom_inputs=lfom_dict):
    return pc.area_circle(
            orifice_diameter(Q, hl, drill_bits, lfom_inputs).magnitude)

@u.wraps(None, [u.m**3/u.s, u.m, u.inch], False)
def n_lfom_orifices_per_row_max(Q, hl, drill_bits, lfom_inputs=lfom_dict):
    """A bound on the number of orifices allowed in each row.
    The distance between consecutive orifices must be enough to retain
    structural integrity of the pipe.
    """
    return math.floor(math.pi*(pipe.ID_SDR(
        nom_diam_lfom_pipe(Q, hl, lfom_inputs)).magnitude)
        / (orifice_diameter(Q, hl, drill_bits, lfom_inputs).magnitude +
            lfom_inputs['S_orifice'].magnitude))

@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.m], False)
def flow_ramp(Q, hl, lfom_inputs=lfom_dict):
    n_rows = n_lfom_rows(Q, hl, lfom_inputs)
    return np.linspace(Q/n_rows, Q, n_rows)

@u.wraps(u.m, [u.m**3/u.s, u.m, u.inch], False)
def height_lfom_orifices(Q, hl, drill_bits, lfom_inputs=lfom_dict):
    """Calculates the height of the center of each row of orifices.
    The bottom of the bottom row orifices is at the zero elevation
    point of the LFOM so that the flow goes to zero when the water height
    is at zero.
    """
    return (np.arange((orifice_diameter(Q, hl, drill_bits, lfom_inputs)*0.5),
                      hl, (dist_center_lfom_rows(Q, hl, lfom_inputs))))

@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.m, u.inch, None, None], False)
def flow_lfom_actual(Q, hl, drill_bits, Row_Index_Submerged, N_lfom_Orifices, lfom_inputs=lfom_dict):
    """Calculates the flow for a given number of submerged rows of orifices
    harray is the distance from the water level to the center of the orifices
    when the water is at the max level
    """
    D_lfom_Orifices = orifice_diameter(Q, hl, drill_bits, lfom_inputs).magnitude
    row_height = dist_center_lfom_rows(Q, hl, lfom_inputs).magnitude
    harray = (np.linspace(row_height, hl, n_lfom_rows(Q, hl, lfom_inputs))) - 0.5 * D_lfom_Orifices
    Q_new = 0
    for i in range(Row_Index_Submerged+1):
        Q_new = Q_new + (N_lfom_Orifices[i]*(
            pc.flow_orifice_vert(D_lfom_Orifices,
                                 harray[Row_Index_Submerged-i],
                                 lfom_inputs['RATIO_VC_ORIFICE']).magnitude))
    return Q_new


#Calculate number of orifices at each level given a diameter
@u.wraps(None, [u.m**3/u.s, u.m, u.inch], False)
def n_lfom_orifices(Q, hl, drill_bits, lfom_inputs=lfom_dict):
    Q_ramp_local = flow_ramp(Q, hl, lfom_inputs).magnitude
    N_orifices_max = n_lfom_orifices_per_row_max(Q, hl, drill_bits, lfom_inputs)
    N_rows = (n_lfom_rows(Q, hl, lfom_inputs))
    D_lfom_Orifices = orifice_diameter(Q, hl, drill_bits, lfom_inputs).magnitude
    # H is distance from the elevation between two rows of orifices down to the center of the orifices
    H = dist_center_lfom_rows(Q, hl, lfom_inputs).magnitude - D_lfom_Orifices*0.5
    n = []
    for i in range(N_rows):
        #place zero in the row that we are going to calculate the required number of orifices
        n = np.append(n, 0)
        #calculate the ideal number of orifices at the current row without constraining to an integer
        N_orifices_real = ((Q_ramp_local[i] - flow_lfom_actual(Q, hl, drill_bits, i, n, lfom_inputs).magnitude) /
                           pc.flow_orifice_vert(D_lfom_Orifices, H, lfom_inputs['RATIO_VC_ORIFICE']).magnitude
        #constrain number of orifices to be less than the max per row and greater or equal to 0
        n[i] = min((max(0, round(N_orifices_real))), N_orifices_max)
    return n

#This function takes the output of n_lfom_orifices and converts it to a list with 8
#entries that corresponds to the 8 possible rows. This is necessary to make the lfom
# easier to construct in Fusion using patterns
@u.wraps(None, [u.m**3/u.s, u.m, u.inch, None], False)
def n_lfom_orifices_fusion(Q, hl, drill_bits, num_rows, lfom_inputs=lfom_dict):
    N_orifices_per_row = n_lfom_orifices(Q, hl, drill_bits, lfom_inputs)
    N_orifices_final = np.zeros(8)
    centerline = np.zeros(8)
    center = True
    for i in range(8):
        if i % 2 == 1 and N_rows == 4:
            centerline[i] = int(center)
        elif N_rows == 4:
            N_orifices_final[i] = N_orifices_per_row[i/2]
            centerline[i] = int(center)
            center = not center
        else:
            N_orifices_final[i] = N_orifices_per_row[i]
            centerline[i] = int(center)
            center = not center

    return N_orifices_final, centerline

#This function calculates the error of the design based on the differences between the predicted flow rate
#and the actual flow rate through the LFOM.
@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.m, u.inch], False)
def flow_lfom_error(Q, hl, drill_bits, lfom_inputs=lfom_dict):
    N_lfom_orifices = n_lfom_orifices(Q, hl, drill_bits, lfom_inputs)
    Q_lfom_error = []
    for j in range(len(N_lfom_orifices)-1):
        Q_lfom_error.append((flow_lfom_actual(
            Q, hl, drill_bits, j, N_lfom_orifices, lfom_inputs).magnitude -
            flow_ramp(Q, hl, lfom_inputs)[j].magnitude)/Q)
    return Q_lfom_error

@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.m, u.m], False)
def flow_lfom_ideal(Q, hl, H):
    Q_lfom_ideal = (Q*H)/hl
    return Q_lfom_ideal

@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.m, u.inch, u.m], False)
def flow_lfom(Q, hl, drill_bits, H, lfom_inputs=lfom_dict):
    D_lfom_orifices = orifice_diameter(Q, hl, drill_bits, lfom_inputs).magnitude
    H_submerged = np.arange(H-0.5*D_lfom_orifices, hl,
                            H-dist_center_lfom_rows(Q, hl, lfom_inputs).magnitude, dtype=object)
    N_lfom_orifices = n_lfom_orifices(Q, hl, drill_bits, lfom_inputs)
    Q = []
    for i in range(len(H_submerged)):
        Q.append(pc.flow_orifice_vert(D_lfom_orifices, H_submerged[i],
                                      lfom_inputs['RATIO_VC_ORIFICE']) *
                 N_lfom_orifices[i])
    return sum(Q)