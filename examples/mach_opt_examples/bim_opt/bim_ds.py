import numpy as np


class BIMDesignSpace:
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
            em_results = final_state.conditions.em

            # motor_mass = em_results['motor_mass']            
            # power = em_results['torque_avg'] * final_state.design.settings.speed * 2 * np.pi / 60
            # f1 = -1 * 0.001 * power / motor_mass    # power density kW/kg

            f1 = -1 * 0.001 * em_results['TRV'] # torque per rotor volume [kN/m^3]
            f2 = -1 * em_results['efficiency'] # final_state.conditions.windage -> final efficiency after adding thermal and windage steps

            weighted_ripple_sum = em_results['torque_ripple'] / 0.05 + em_results['Em'] / 0.05 + em_results['Ea'] / 1
            f3 = weighted_ripple_sum
        return f1, f2, f3

    def check_constraints(self, full_results):
        valid_constraints = True
        final_results = full_results[-1]
        final_state = final_results[-1]
        em_results = final_state.conditions.em
        if abs(em_results['torque_ripple']) >= 0.3 or em_results['Em'] >= 0.3 or abs(em_results['Ea']) > 10 or \
                em_results['FRW'] < 0.75:
            print('Constraints are violated:')
            print('\t torque_ripple: ', em_results['torque_ripple'], ', Em: ', em_results['Em'],
                  ', Ea: ', em_results['Ea'], ', FRW: ', em_results['FRW'])
            valid_constraints = False
        return valid_constraints
