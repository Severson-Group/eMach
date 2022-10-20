from machine_design import BSPMArchitectType1
from specifications.bspm_specification import BSPMMachineSpec

from specifications.machine_specs.bp1_machine_specs import DesignSpec
from specifications.materials.electric_steels import Arnon5
from specifications.materials.jmag_library_magnets import N40H
from specifications.materials.miscellaneous_materials import (
    CarbonFiber,
    Steel,
    Copper,
    Hub,
    Air,
)
from settings.bspm_settings_handler import BSPM_Settings_Handler
from mach_eval import MachineDesigner

# create specification object for the BSPM machine
machine_spec = BSPMMachineSpec(
    design_spec=DesignSpec,
    rotor_core=Arnon5,
    stator_core=Arnon5,
    magnet=N40H,
    conductor=Copper,
    shaft=Steel,
    air=Air,
    sleeve=CarbonFiber,
    hub=Hub,
)

# initialize BSPMArchitect with machine specification
arch = BSPMArchitectType1(machine_spec)
set_handler = BSPM_Settings_Handler()

designer = MachineDesigner(arch, set_handler)
