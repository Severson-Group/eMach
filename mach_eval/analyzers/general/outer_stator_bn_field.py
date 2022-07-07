########################### source of equations ###############################
# [1] G. Bergmann and A. Binder, “Design guidelines of bearingless PMSM with 
# two separate poly-phase windings,” in 2016 XXII International Conference on 
# Electrical Machines (ICEM), Lausanne, Switzerland, Sep. 2016, pp. 2588–2594. 
# doi: 10.1109/ICELMACH.2016.7732886.

# [2] Z. Q. Zhu and D. Howe, “Instantaneous magnetic field distribution in 
# brushless permanent magnet DC motors. II. Armature-reaction field,” IEEE 
# Trans. Magn., vol. 29, no. 1, pp. 136–142, Jan. 1993, doi: 10.1109/20.195558.
###############################################################################

import numpy as np

class OuterStatorBnfieldProblem:
    """Problem class for stator radial B field analyzer
    Attributes:
        A_hat: Electric loading [A/m]
        n: Harmonic under consideration (v*p)
        delta_e: Effective airgap [m]
        r_si: Inner radius of the stator [m]
        r_rfe: Outer radius of rotor iron [m]
        r: Radius at which radial B-field is to be calculated [m]
        alpha_so: stator slot opening [radians]   
    """

    def __init__(self, m, zq, Nc, k_w, I_hat, n, delta_e, r_si, r_rfe, r, alpha_so):
        self.A_hat = self.electric_loading(m, zq, r_si, Nc, k_w, I_hat)
        self.n = n
        self.delta_e = delta_e
        self.r_si = r_si
        self.r_rfe = r_rfe
        self.r = r
        self.alpha_so = alpha_so

    def electric_loading(self, m, zq, r_si, N, k_w, I_hat):
        """Determines electric loading of winding
        
        Args:
            m : number of phases
            zq : number of turns
            r_si : inner stator radius
            N : number of coils per phase
            k_w : winding factor
            I_hat : peak current

        Returns:
            A: electric loading of winding
        """
        A = m/np.pi * zq * N * k_w * I_hat/r_si
        return A    


class OuterStatorBnfieldAnalyzer:
    """Analyzer class to evaluate stator radial B field"""

    def analyze(self, problem=None):
        """ Determines normal B-field at radius r due to stator windings

            Args:
                problem: Object of type OuterStatorBfieldProblem 
            Returns:
                b_field: Radial magnetic field at radius r from stator windings [T]
        """

        # determine reduction in B field due to slot opening
        k_sov = np.sin(problem.n*problem.alpha_so/2)/(problem.n*problem.alpha_so/2)

        # determine curavture coefficient that causes field magnitude to vary across the airgap
        k_cu = problem.delta_e*problem.n/problem.r*(problem.r/problem.r_si)**problem.n * \
             (1+(problem.r_rfe/problem.r)**(2*problem.n))/(1-(problem.r_rfe/problem.r_si)**(2*problem.n))
        
        mu0 = 4 * np.pi * 10**-7
        conv_b_field = (problem.A_hat * mu0 * problem.r_si) / (problem.n * problem.delta_e)

        b_field = conv_b_field * k_sov * k_cu
        return b_field
    
    