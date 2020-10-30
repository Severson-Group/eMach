# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 02:27:35 2020

@author: Bharat
"""
__all__ = ['draw_circle', 'select_section', 'make_component_in_a_line']

def draw_circle(view, centre_x, centre_y, circle_r):
    """draw circle with centre_x, centre_y as the coordinates of the centre,
    circle_r as the radius
    """
    view.newCircle(centre_x, centre_y, circle_r)
    view.viewAll()

def select_section(view, mn_consts, section_x, section_y):
    """select section containing coordinate (x,y)
    """
    view.selectAt(section_x, section_y, mn_consts.infoSetSelection)


def make_component_in_a_line(view, mn_consts, sweep_dist, array_values, material):
    '''command to extrude a selected section by 'sweepDis't and assign to the
    component the 'sectionName' and 'material'  as specified, returns 0 if
    extrusion is succesful, 1 if extrusion failed
    '''
    ret = view.makeComponentInALine(sweep_dist, array_values, "Name="+material,
                                    mn_consts.infoMakeComponentUnionSurfaces
                                    or mn_consts.infoMakeComponentRemoveVertices)
    return ret
