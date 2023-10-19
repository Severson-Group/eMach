import copy
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import pandas as pd

from mach_eval.analyzers.electromagnetic.inductance_analyzer import (
    Inductance_Problem,
    Inductance_Analyzer,
)

class SynR_Inductance_PostAnalyzer:
    
    def get_next_state(results, in_state):
        state_out = copy.deepcopy(in_state)

        ############################ Extract required info ###########################
        path = results["csv_folder"]
        study_name = results["study_name"]
        I_hat = results["current_peak"]
        time_step = results["time_step"]

        U_linkages = pd.read_csv(path + study_name + "_0_flux_of_fem_coil.csv", skiprows=7)
        V_linkages = pd.read_csv(path + study_name + "_1_flux_of_fem_coil.csv", skiprows=7)
        W_linkages = pd.read_csv(path + study_name + "_2_flux_of_fem_coil.csv", skiprows=7)

        ############################ post processing ###########################
        U_linkages = U_linkages.to_numpy() # change csv format to readable array
        V_linkages = V_linkages.to_numpy() # change csv format to readable array
        W_linkages = W_linkages.to_numpy() # change csv format to readable array
        
        t = U_linkages[:,0] # define x axis data as time
        rotor_angle = t/time_step
        Uu = U_linkages[:,1] # define y axis data as self inductance
        Uv = U_linkages[:,2] # define y axis data as mutual inductance
        Uw = U_linkages[:,3]
        Vu = V_linkages[:,1]
        Vv = V_linkages[:,2]
        Vw = V_linkages[:,3]
        Wu = W_linkages[:,1]
        Wv = W_linkages[:,2]
        Ww = W_linkages[:,3]

        inductance_prob = Inductance_Problem(t, rotor_angle, I_hat, Uu, Uv)
        inductance_analyzer = Inductance_Analyzer()
        Ld, Lq, saliency_ratio = inductance_analyzer.analyze(inductance_prob)

        ############################ Output #################################
        post_processing_fluxes = {}
        post_processing_fluxes["t"] = t
        post_processing_fluxes["rotor_angle"] = rotor_angle
        post_processing_fluxes["Uu"] = Uu
        post_processing_fluxes["Uv"] = Uv
        post_processing_fluxes["Uw"] = Uw
        post_processing_fluxes["Vu"] = Vu
        post_processing_fluxes["Vv"] = Vv
        post_processing_fluxes["Vw"] = Vw
        post_processing_fluxes["Wu"] = Wu
        post_processing_fluxes["Wv"] = Wv
        post_processing_fluxes["Ww"] = Ww

        state_out.conditions.flux_linkages = post_processing_fluxes

        post_processing_inductances = {}
        post_processing_inductances["Ld"] = Ld
        post_processing_inductances["Lq"] = Lq
        post_processing_inductances["saliency_ratio"] = saliency_ratio

        state_out.conditions.inductances = post_processing_inductances
        
        ############################ Results #################################
        print("\n************************ INDUCTANCE RESULTS ************************")
        print("Ld = ", Ld, " H")
        print("Lq = ", Lq, " H")
        print("Saliency Ratio = ", saliency_ratio)
        print("*************************************************************************\n")

        return state_out