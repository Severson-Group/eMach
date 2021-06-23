import copy

class LengthScaleStep():
    
    def step(state_in):
        
        state_out = copy.deepcopy(state_in)
        machine = state_out.design.machine
        expected_torque = machine.mech_power / machine.mech_omega
        
        avg_torque = state_out.conditions['torque_avg']
        scale_ratio = expected_torque/avg_torque
        new_stack_length = machine.l_st * scale_ratio
        
        # state_out.design.machine.update_attr(l_st = new_stack_length) 
        
        state_out.conditions['Fx'] = state_out.conditions['Fx'] * scale_ratio
        state_out.conditions['Fy'] = state_out.conditions['Fy'] * scale_ratio
        state_out.conditions['force_avg'] = state_out.conditions['force_avg'] \
                                            * scale_ratio
        
        state_out.conditions['rotor_loss'] = state_out.conditions['rotor_loss'] \
                                            * scale_ratio
        state_out.conditions['stator_loss'] = state_out.conditions['stator_loss'] \
                                            * scale_ratio
        state_out.conditions['magnet_loss'] = state_out.conditions['magnet_loss'] \
                                            * scale_ratio
        state_out.conditions['phase_voltage_rms'] = state_out.conditions['phase_voltage_rms'] \
                                            * scale_ratio
        
        results = None
        return results, state_out