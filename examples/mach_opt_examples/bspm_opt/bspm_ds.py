import numpy as np


class BSPMDesignSpace:
    def __init__(self, n_obj, bounds):
        self.__n_obj = n_obj
        self.__bounds = bounds

    @property
    def n_obj(self):
        return self.__n_obj

    @property
    def bounds(self):
        min_b, max_b = np.asarray(self.__bounds).T
        min_b, max_b = min_b.astype(float), max_b.astype(float)
        return min_b.tolist(), max_b.tolist()

    def get_objectives(self, full_results):
        valid_constraints = self.check_constraints(full_results)
        if not valid_constraints:
            f1, f2, f3 = 9999, 9999, 9999  # bad fitness values
        else:
            final_results = full_results[-1]
            final_state = final_results[-1]
            machine = final_state.design.machine
            stator_iron = machine.stator_iron_mat
            shaft = machine.shaft_mat
            rotor_iron = machine.rotor_iron_mat
            magnet = machine.magnet_mat
            coil = machine.coil_mat

            weight = machine.V_rfe * rotor_iron['core_material_density'] + \
                     machine.V_sh * shaft['shaft_material_density'] + \
                     machine.V_rPM * magnet['magnet_material_density'] + \
                     machine.V_sfe * stator_iron['core_material_density'] + \
                     machine.V_scu * coil['copper_material_density']
            
            em_results = final_state.conditions.em
            power = em_results['torque_avg'] * final_state.design.settings.speed * np.pi/30

            f1 = -1 * 0.001*power/weight    # power density kW/kg
            f2 = -1 * final_state.conditions.windage['efficiency']

            em_results = final_state.conditions.em
            weighted_ripple_sum = em_results['torque_ripple'] / 0.05 + em_results['Em'] / 0.05 + em_results['Ea'] / 1
            f3 = weighted_ripple_sum
        return f1, f2, f3

    def check_constraints(self, full_results):
        valid_constraints = True
        final_results = full_results[-1]
        final_state = final_results[-1]
        em_results = final_state.conditions.em
        if abs(em_results['torque_ripple']) >= 0.5 or em_results['Em'] >= 0.35 or abs(em_results['Ea']) > 20 or \
                em_results['FRW'] < 0.5:
            print('Constraints are violated:')
            print('\t torque_ripple: ', em_results['torque_ripple'], ', Em: ', em_results['Em'],
                  ', Ea: ', em_results['Ea'], ', FRW: ', em_results['FRW'])
            valid_constraints = False
        return valid_constraints
