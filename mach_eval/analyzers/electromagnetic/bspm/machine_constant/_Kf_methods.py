from functools import cached_property, lru_cache

def testing(self):
    return self.Iq_step

# @cached_property
# def Kf(self):
#         # Run simulations to obtain necessary data
#     force_df_list, torque_df_list = self.run_Kf_Kt_simulations()

#     # calculate the number of initial data point to ignore
#     idx_ignore = int(360/angle_step*rev_ignore)
#     print(idx_ignore)

#     # extract average force value from each run
#     force = []
#     for force_df in force_df_list:
#         force_prob = ProcessForceDataProblem(
#             Fx=force_df["ForCon:1st"].iloc[idx_ignore:].to_numpy(),
#             Fy=force_df["ForCon:2nd"].iloc[idx_ignore:].to_numpy())
#         force_ana = ProcessForceDataAnalyzer()
#         _,_,f_abs_avg,_,_ = force_ana.analyze(force_prob)
#         force.append(f_abs_avg)

#     Is = [np.sqrt(2)*I_rms*(1-Iq_pu_val) for Iq_pu_val in Iq_pu]
#     Kf,_ = np.polyfit(Is,force,deg=1)

#     return Kf 

# @cached_property
# def Kt(self):
#     # extract average torque value from each run
#     torque = np.zeros(len(self.torque_df_list))
#     for idx, torque_df in enumerate(self.torque_df_list):
#         torque_prob = ProcessTorqueDataProblem(torque_df["TorCon"].iloc[idx_ignore:].to_numpy())
#         torque_analyzer = ProcessTorqueDataAnalyzer()
#         torque_avg,_ = torque_analyzer.analyze(torque_prob)
#         torque[idx] = torque_avg

#     Iq = [np.sqrt(2)*I_rms*Iq_pu_val for Iq_pu_val in Iq_pu]
#     Kt,_ = np.polyfit(Iq,torque,deg=1)

#     return Kt

# @lru_cache
# def run_Kf_Kt_simulations(self):

#     # use operating point rated current and result for speed 
#     force_df_list = []
#     torque_df_list = []

#     Iq_pu_list = np.linspace(0,np.sqrt(2)*self.machine.Rated_current)
#     tqdm_Iq = tqdm(self.Iq_list, desc='') 
#     for idx, Iq_val in enumerate(tqdm_Iq):
#         tqdm_Iq.set_description("Run "+ str(idx+1)+"/"+str(len(Iq_val))
#                                 +" , Iq_pu = "+str(round(Iq_val,2)))

#         # duplicate initial study
#         self.init_model.DuplicateStudyName(self.init_study_name,
#                             self.init_study_name+'_Kf_Kt'
#                             +'_Iq_'+str(round(Iq_val,2)).replace(".", "_")
#                             +'_Is_'+str(round(1-Iq_val, 2)).replace(".", "_"),True)
        
#         # set duplicated study as present study
#         present_study = self.toolJd.GetCurrentStudy()
        
#         # rotor should rotate one full revolution over 1 second
#         # 1 rev/s = 60 rev/min
#         speed = 60
#         self._set_study_speed(present_study,speed)
#         excitation_freq = self._get_elec_freq(present_study,speed)

#         # set study step control
#         self._set_study_steps(present_study,angle_step,rev)

#         # obtain handle to circuit for present study
#         circuit = present_study.GetCircuit()

#         # set torque and suspension currents for all coils
#         ampT = 2*Iq_pu_val*I_rms*np.sqrt(2)
#         ampS = (1-Iq_pu_val)*I_rms*np.sqrt(2)

#         func = self.toolJd.FunctionFactory().Composite()
#         f1 = self.toolJd.FunctionFactory().Sin(ampT, excitation_freq, 0)
#         # "freq" variable cannot be used here. So pay extra attension when you create new case of a different freq.
#         func.AddFunction(f1)
#         circuit.GetComponent("CS_t-1").SetFunction(func)

#         func = self.toolJd.FunctionFactory().Composite()
#         f1 = self.toolJd.FunctionFactory().Sin(ampT, excitation_freq, -120)
#         func.AddFunction(f1)
#         circuit.GetComponent("CS_t-2").SetFunction(func)

#         func = self.toolJd.FunctionFactory().Composite()
#         f1 = self.toolJd.FunctionFactory().Sin(ampT, excitation_freq, -240)
#         func.AddFunction(f1)
#         circuit.GetComponent("CS_t-3").SetFunction(func)

#         func = self.toolJd.FunctionFactory().Composite()
#         f1 = self.toolJd.FunctionFactory().Sin(ampS, excitation_freq, 0)
#         f2 = self.toolJd.FunctionFactory().Sin(-ampT / 2, excitation_freq, 0)
#         func.AddFunction(f1)
#         func.AddFunction(f2)
#         circuit.GetComponent("CS_s-1").SetFunction(func)

#         func = self.toolJd.FunctionFactory().Composite()
#         f1 = self.toolJd.FunctionFactory().Sin(ampS, excitation_freq, 120)
#         f2 = self.toolJd.FunctionFactory().Sin(-ampT / 2, excitation_freq, -120)
#         func.AddFunction(f1)
#         func.AddFunction(f2)
#         circuit.GetComponent("CS_s-2").SetFunction(func)

#         func = self.toolJd.FunctionFactory().Composite()
#         f1 = self.toolJd.FunctionFactory().Sin(ampS, excitation_freq, 240)
#         f2 = self.toolJd.FunctionFactory().Sin(-ampT / 2, excitation_freq, -240)
#         func.AddFunction(f1)
#         func.AddFunction(f2)
#         circuit.GetComponent("CS_s-3").SetFunction(func)

#         # run the study
#         present_study.RunAllCases()

#         # extract FEA results from CSV
#         force_df = self._extract_csv_results(present_study.GetName(), "Force")
#         torque_df = self._extract_csv_results(present_study.GetName(),"Torque")

#         force_df_list.append(force_df)
#         torque_df_list.append(torque_df)
    
#     self.force_df_list = force_df_list
#     return force_df_list, torque_df_list
