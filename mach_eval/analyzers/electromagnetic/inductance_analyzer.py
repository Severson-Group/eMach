import copy
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import pandas as pd

class Inductance_Problem:
    """Problem class for torque data processing
    Attributes:
        torque: numpy array of torque against time or position
    """

    def __init__(self, I_hat, jmag_csv_folder, study_name, time_step):
        self.I_hat = I_hat
        self.jmag_csv_folder = jmag_csv_folder 
        self.study_name = study_name
        self.time_step = time_step


class Inductance_Analyzer:

    def analyze(self, problem: Inductance_Problem):
        """Calcuates average torque and torque ripple

        Args:
            problem: object of type ProcessTorqueDataProblem holding torque data
        Returns:
            torque_avg: Average torque calculated from provided data
            torque_ripple: Torque ripple calculated from provided data
        """
        path = problem.jmag_csv_folder
        study_name = problem.study_name
        I_hat = problem.I_hat
        time_step = problem.time_step

        U_linkages = pd.read_csv(path + study_name + "_0_flux_of_fem_coil.csv", skiprows=7)
        V_linkages = pd.read_csv(path + study_name + "_1_flux_of_fem_coil.csv", skiprows=7)
        W_linkages = pd.read_csv(path + study_name + "_2_flux_of_fem_coil.csv", skiprows=7)

        U_linkages = U_linkages.to_numpy() # change csv format to readable array
        V_linkages = V_linkages.to_numpy() # change csv format to readable array
        W_linkages = W_linkages.to_numpy() # change csv format to readable array
        
        time = U_linkages[:,0] # define x axis data as time
        rotor_angle = time/time_step
        Uu = U_linkages[:,1] # define y axis data as self inductance
        Uv = U_linkages[:,2] # define y axis data as mutual inductance
        Uw = U_linkages[:,3]
        Vu = V_linkages[:,1]
        Vv = V_linkages[:,2]
        Vw = V_linkages[:,3]
        Wu = W_linkages[:,1]
        Wv = W_linkages[:,2]
        Ww = W_linkages[:,3]
        
        [Uu_fit, sUu] = self.fit_sin(time, Uu) # carry out calculations on self inductance
        [Uv_fit, sUv] = self.fit_sin(time, Uv) # carry out calculations on mutual inductance

        #fig1, ax1 = plt.subplots()
        #ax1.plot(rotor_angle, Uu, "-k", label="y", linewidth=2)
        #ax1.plot(rotor_angle, Uu_fit["fitfunc"](time), "r-", label="y fit curve", linewidth=2)
        #ax1.legend(loc="best")
        #plt.savefig("temp1.svg")

        #fig2, ax2 = plt.subplots()
        #ax2.plot(rotor_angle, Uv, "-k", label="y", linewidth=2)
        #ax2.plot(rotor_angle, Uv_fit["fitfunc"](time), "r-", label="y fit curve", linewidth=2)
        #ax2.legend(loc="best")
        #plt.savefig("temp2.svg")

        data = self.extract_results(I_hat, sUu, sUv, path, study_name) 

        return data
    
    def fit_sin(self, t, y):
            fft_func = np.fft.fftfreq(len(t), (t[1]-t[0])) # define fft function with assumed uniform spacing
            fft_y = abs(np.fft.fft(y)) # carry out fft function for inductance values
            guess_freq = abs(fft_func[np.argmax(fft_y[1:])+1]) # excluding the zero frequency "peak", which can cause problematic fits
            guess_amp = np.std(y) # guess amplitude based on one standard deviation
            guess_offset = np.mean(y) # guess y offset based on average of magnitude
            guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0, guess_offset]) # arrage in array
            
            # define sin function 
            def sinfunc(t, A, w, p, c):  
                return A * np.sin(w*t + p) + c
            
            popt, pcov = scipy.optimize.curve_fit(sinfunc, t, y, p0=guess) # calculate sin function fit
            A, w, p, c = popt # assign appropriate variables
            fitfunc = lambda t: A * np.sin(w*t + p) + c # define fit function for curve fit
            
            # define function used to calculate least square
            def sumfunc(x):
                return sum((sinfunc(t, x[0], x[1], x[2], x[3]) - y)**2)
            
            sUx = scipy.optimize.minimize(fun=sumfunc, x0=np.array([guess_amp, 2.*np.pi*guess_freq, 0, guess_offset])) # calculate matching curve fit values with minimum error
            return [{"amp": A, "omega": w, "phase": p, "offset": c, "fitfunc": fitfunc}, sUx]
    
    def extract_results(self, I_hat, sUu, sUv, path, study_name):

        Lzero = -2*sUv.x[3]/I_hat; # calculate L0 based on equations in publication
        Lg = sUv.x[0]/I_hat # calculate Lg based on equations in publication
        Lls = (sUu.x[3] + 2*sUv.x[3])/I_hat # calculate Lls based on equations in publication
        Ld = Lls + 3/2*(Lzero - Lg) # calculate Ld based on equations in publication
        Lq = Lls + 3/2*(Lzero + Lg) # calculate Lq based on equations in publication

        data = {
                "Ld": Ld,
                "Lq": Lq,
                "csv_folder": path,
                "study_name": study_name,
            }

        return data