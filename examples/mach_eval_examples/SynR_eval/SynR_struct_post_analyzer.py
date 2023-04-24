import copy

class SynR_Struct_PostAnalyzer:
    def get_next_state(results, in_state):
        state_out = copy.deepcopy(in_state)

        ############################ Extract required info ###########################
        struct = results["max_stress"]
        s = struct['Maximum Value']
        max_stress = s[0]
        yield_stress = 300 * 1000000

        ############################ Output #################################
        print("\n************************ STRUCTURAL RESULT ************************")
        print("Maximum Stress = ", max_stress/1000000, " MPa",)
        if max_stress > yield_stress:
            print("This exceeds the yield stress of the rotor!")
        print("************************************************************\n")

        return state_out