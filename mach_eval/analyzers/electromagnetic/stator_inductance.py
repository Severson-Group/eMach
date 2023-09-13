import pandas as pd
import scipy.optimize
import numpy as np
import matplotlib.pyplot as plt

class ProcessInductanceProblem:
    """Problem class for inductance and saliency ratio calculations
    Attributes:
        Uu_flux: numpy array of torque against time or position
    """

    def __init__(self, file_path, graph, save_path=None):
        self.file_path = file_path
        self.graph = graph
        self.save_path = save_path


class ProcessInductanceAnalyzer:
    def analyze(self, problem: ProcessInductanceProblem):
        """Calcuates average torque and torque ripple

        Args:
            problem: object of type ProcessTorqueDataProblem holding torque data
        Returns:
            torque_avg: Average torque calculated from provided data
            torque_ripple: Torque ripple calculated from provided data
        """

        self.problem = problem

        df = pd.read_csv(self.file_path + "_inductance_of_fem_coil.csv", skiprows = 7) # read in csv file <-- NEED TO CHANGE NAME
        data = df.to_numpy() # change csv format to readable array
        t = data[:,0] # define x axis data as time
        Uu = data[:,1] # define y axis data as self inductance
        Uv = data[:,2] # define y axis data as mutual inductance

        [Uu_fit, sUu] = self.fit_sin(t, Uu) # carry out calculations on self inductance
        [Uv_fit, sUv] = self.fit_sin(t, Uv) # carry out calculations on mutual inductance

        if self.graph == 1:
            fig1, ax1 = plt.subplots()
            ax1.plot(t, Uu, "-k", label="y", linewidth=2)
            ax1.plot(t, Uu_fit["fitfunc"](t), "r-", label="y fit curve", linewidth=2)
            ax1.legend(loc="best")
            plt.savefig(self.save_path + '/Uu_inductance_fit.svg')   

            fig2, ax2 = plt.subplots()
            ax2.plot(t, Uv, "-k", label="y", linewidth=2)
            ax2.plot(t, Uv_fit["fitfunc"](t), "r-", label="y fit curve", linewidth=2)
            ax2.legend(loc="best")
            plt.savefig(self.save_path + '/Uv_inductance_fit.svg') 
        else:
            return

        Lzero = 2/3 * abs(sUv.x[3]); # calculate L0 based on equations in publication
        Lg = abs(sUv.x[0]) # calculate Lg based on equations in publication
        Lls = abs(sUu.x[3]) # calculate Lls based on equations in publication
        Ld = Lls + 3/2*(Lzero + Lg) # calculate Ld based on equations in publication
        Lq = Lls + 3/2*(Lzero - Lg) # calculate Lq based on equations in publication
        saliency_ratio = Ld/Lq # calculate saliency ratio

        return Ld, Lq, saliency_ratio


    # curve fit inductance values and calculate curve
    def fit_sin(t, y):
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