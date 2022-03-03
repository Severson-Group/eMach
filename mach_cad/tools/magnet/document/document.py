__all__ = ['make_simple_coil', 'set_parameter', 'make_motion_component', 'get_parameter']


def make_simple_coil(doc, problem_id, array_values):
    """ function to make a simple coil with 'ArrayOfValues' and 'ProblemID',
    returns path to the coil
    """
    coil = doc.makeSimpleCoil(problem_id, array_values)
    return coil


def set_parameter(doc, o_path, param, value, mn_consts):
    """ sets parameter, 'param' of object with path 'opath' as 'value'
    """
    if isinstance(value, str):
        doc.setParameter(o_path, param, value, mn_consts.infoStringParameter)
    elif isinstance(value, int):
        doc.setParameter(o_path, param, str(value), mn_consts.infoNumberParameter)
    elif isinstance(value, list):
        doc.setParameter(o_path, param, str(value), mn_consts.infoArrayParameter)


def make_motion_component(doc, array_values):
    """makes a Motion component of 'ArrayOfValues', returns path of the Motion component
    """
    motion = doc.makeMotionComponent(array_values)
    return motion


def get_parameter(mn, o_path, parameter):
    mn.processCommand("REDIM strArray(0)")
    mn.processCommand("DIM pType")
    mn.processCommand("pType = getDocument.getParameter(\"{}\", \"{}\", strArray)"
                      .format(o_path, parameter))
    mn.processCommand('Call setVariant(0, strArray, "PYTHON")')
    param = mn.getVariant(0, "PYTHON")
    mn.processCommand('Call setVariant(0, pType,"PYTHON")')
    param_type = mn.getVariant(0, "PYTHON")
    return param, param_type
