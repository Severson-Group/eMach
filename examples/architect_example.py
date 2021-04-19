# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 16:50:14 2021

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



machine_spec = BSPMMachineSpec(design_spec = DesignSpec, rotor_core = Arnon5, \
                         stator_core = Arnon5, magnet = N40H, conductor = Copper, \
                         shaft = Steel, air = Air, sleeve = CarbonFiber, hub = Hub)

arch = BSPMArchitectType1(machine_spec)
free_var = [0.00390399,0.00964596,35.9925,0.00358376,0.00722451,0.0128492,\
            0.0143288,177.875,0.00514122,0.00308507,0.00363824]

machine_des = arch.create_new_design(free_var)
print(machine_des.coil_groups)