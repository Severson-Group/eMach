import copy


class LengthScaleStep:
    def step(state_in):
        state_out = copy.deepcopy(state_in)
        machine = state_out.design.machine
        expected_torque = machine.mech_power / machine.mech_omega

        avg_torque = state_out.conditions.em["torque_avg"]
        scale_ratio = expected_torque / avg_torque
        new_stack_length = machine.l_st * scale_ratio

        state_out.design.machine.clone(
            machine_parameter_dict={"l_st": new_stack_length}
        )

        state_out.conditions.em["Fx"] = state_out.conditions.em["Fx"] * scale_ratio
        state_out.conditions.em["Fy"] = state_out.conditions.em["Fy"] * scale_ratio
        state_out.conditions.em["force_avg"] = (
            state_out.conditions.em["force_avg"] * scale_ratio
        )

        state_out.conditions.em["rotor_iron_loss"] = (
            state_out.conditions.em["rotor_iron_loss"] * scale_ratio
        )
        state_out.conditions.em["stator_iron_loss"] = (
            state_out.conditions.em["stator_iron_loss"] * scale_ratio
        )
        state_out.conditions.em["magnet_loss"] = (
            state_out.conditions.em["magnet_loss"] * scale_ratio
        )
        state_out.conditions.em["phase_voltage_rms"] = (
            state_out.conditions.em["phase_voltage_rms"] * scale_ratio
        )
        print("Magnet loss is ", state_out.conditions.em["magnet_loss"])
        print("New stack length is ", new_stack_length)

        results = None
        return results, state_out
