import copy
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

class Inductance_Problem:
    """Problem class for torque data processing
    Attributes:
        torque: numpy array of torque against time or position
    """

    def __init__(self, time, rotor_angle, I_hat, Uu, Uv):
        self.time = time
        self.rotor_angle = rotor_angle
        self.I_hat = I_hat
        self.Uu = Uu 
        self.Uv = Uv


class Inductance_Analyzer:
    def analyze(self, problem: Inductance_Problem):
        """Calcuates average torque and torque ripple

        Args:
            problem: object of type ProcessTorqueDataProblem holding torque data
        Returns:
            torque_avg: Average torque calculated from provided data
            torque_ripple: Torque ripple calculated from provided data
        """
        time = problem.time
        rotor_angle = problem.rotor_angle
        I_hat = problem.I_hat
        Uu = problem.Uu
        Uv = problem.Uv

        [Uu_fit, sUu] = self.fit_sin(time, Uu) # carry out calculations on self inductance
        [Uv_fit, sUv] = self.fit_sin(time, Uv) # carry out calculations on mutual inductance

        fig1, ax1 = plt.subplots()
        ax1.plot(rotor_angle, Uu, "-k", label="y", linewidth=2)
        ax1.plot(rotor_angle, Uu_fit["fitfunc"](time), "r-", label="y fit curve", linewidth=2)
        ax1.legend(loc="best")
        plt.savefig("temp1.svg")

        fig2, ax2 = plt.subplots()
        ax2.plot(rotor_angle, Uv, "-k", label="y", linewidth=2)
        ax2.plot(rotor_angle, Uv_fit["fitfunc"](time), "r-", label="y fit curve", linewidth=2)
        ax2.legend(loc="best")
        plt.savefig("temp2.svg")

        Lzero = -2*sUv.x[3]/I_hat; # calculate L0 based on equations in publication
        Lg = sUv.x[0]/I_hat # calculate Lg based on equations in publication
        Lls = (sUu.x[3] + 2*sUv.x[3])/I_hat # calculate Lls based on equations in publication
        Ld = Lls + 3/2*(Lzero - Lg) # calculate Ld based on equations in publication
        Lq = Lls + 3/2*(Lzero + Lg) # calculate Lq based on equations in publication
        saliency_ratio = Ld/Lq # calculate saliency ratio

        return Ld, Lq, saliency_ratio
    
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