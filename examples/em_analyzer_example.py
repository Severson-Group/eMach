# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 16:50:14 2021

@author: Bharat
"""
import sys

sys.path.append("..")

from architect import BSPMArchitectType1
from specifications.bspm_specification import BSPMMachineSpec

from specifications.machine_specs.bp1_machine_specs import DesignSpec
from specifications.materials.electric_steels import Arnon5
from specifications.materials.jmag_library_magnets import N40H
from specifications.materials.miscellaneous_materials import CarbonFiber, \
Steel, Copper, Hub, Air
from operating_points.bspm_op_point import BSPM_EMAnalyzer_Op_Point
from analyzers.em_analyzer import  BSPM_EM_Analysis
from specifications.analyzer_config.em_fea_config import JMAG_FEA_Configuration


# create specification object for the BSPM machine
machine_spec = BSPMMachineSpec(design_spec = DesignSpec, rotor_core = Arnon5, \
                         stator_core = Arnon5, magnet = N40H, conductor = Copper, \
                         shaft = Steel, air = Air, sleeve = CarbonFiber, hub = Hub)

# intialize BSPMArchitect with machine specification
arch = BSPMArchitectType1(machine_spec)

# create machine variant using architect
free_var = [0.00390399,0.00964596,35.9925,0.00358376,0.00722451,0.0128492,\
            0.0143288,177.875,0.00514122,0.00308507,0.00363824]
machine_variant = arch.create_new_design(free_var)

# set operating point for BSPM machine 
em_op = BSPM_EMAnalyzer_Op_Point(Id = 0, Iq = 0.95, Ix = 0, Iy = 0.05, speed =2000,\
                                 magnet_temp = 80)


design = BSPM_EM_Analysis(JMAG_FEA_Configuration)

y = design.analyze(machine_variant, em_op,counter = 3)



