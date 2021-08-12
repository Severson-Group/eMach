class BspmObjectives:
    def get_objectives(valid_constraints, full_results):
        if not valid_constraints:
            f1, f2, f3 = 9999, 9999, 9999  # bad fitness values
        else:
            final_results = full_results[-1]
            final_state = final_results[-1]
            machine = final_state.design.machine
            stator_iron = machine.stator_iron_mat
            rotor_iron = machine.rotor_iron_mat
            magnet = machine.magnet_mat
            coil = machine.coil_mat

            cost_of_machine = stator_iron['core_material_cost'] * machine.V_sfe + rotor_iron['core_material_cost'] * \
                              machine.V_rfe + magnet['magnet_material_cost'] * machine.V_rPM + \
                              coil['copper_material_cost'] * machine.V_scu
            f1 = cost_of_machine
            f2 = -1*final_state.conditions.efficiency

            em_results = final_state.conditions.em
            weighted_ripple_sum = em_results['torque_ripple'] / 0.05 + em_results['Em'] / 0.05 + em_results['Ea'] / 1
            f3 = weighted_ripple_sum
        return f1, f2, f3
