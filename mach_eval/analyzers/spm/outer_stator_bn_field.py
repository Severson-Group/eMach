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
        MMF: Current linkage or Magneto-Motive Force [A-turns]
        n: Harmonic under consideration (v*p)
        delta_e: Effective airgap [m]
        r_si: Inner radius of the stator [m]
        r_rfe: Outer radius of rotor iron [m]
        alpha_so: stator slot opening [radians]
    """

    def __init__(self, m, zq, Nc, k_w, I_hat, n, delta_e, r_si, r_rfe, alpha_so):
        self.MMF = self.mmf(m, zq, Nc, n, k_w, I_hat)
        self.n = n
        self.delta_e = delta_e
        self.r_si = r_si
        self.r_rfe = r_rfe
        self.alpha_so = alpha_so

    def mmf(self, m, zq, N, n, k_w, I_hat):
        """Determines electric loading of winding

        Args:
            m : number of phases
            zq : number of turns
            r_si : inner stator radius
            N : number of coils per phase
            k_w : winding factor
            I_hat : peak current

        Returns:
            mmf: Current linkage or Magneto-Motive Force
        """
        mmf = m / np.pi * zq * N * k_w * I_hat / n
        return mmf


class OuterStatorBnFieldAnalyzer:
    """Analyzer class to evaluate stator radial B field"""

    def analyze(self, problem=None):
        """Determines normal B-field at radius r due to stator windings

        Args:
            problem: Object of type OuterStatorBfieldProblem
        Returns:
            b_field: Radial magnetic field at radius r from stator windings [T]
        """

        b_field = OuterStatorBField(
            mmf=problem.MMF,
            n=problem.n,
            delta_e=problem.delta_e,
            r_si=problem.r_si,
            r_rfe=problem.r_rfe,
            alpha_so=problem.alpha_so,
        )
        return b_field


class OuterStatorBField:
    """Class representing radial B field across motor airgap and tangential B field at stator inner bore

    Attributes:
        MMF: Current linkage or Magneto-Motive Force [A-turns]
        n: Harmonic under consideration (v*p)
        delta_e: Effective airgap [m]
        r_si: Inner radius of the stator [m]
        r_rfe: Outer radius of rotor iron [m]
        alpha_so: stator slot opening [radians]
    """

    def __init__(self, mmf: np.array, n: np.array, delta_e, r_si, r_rfe, alpha_so):
        self.MMF = mmf
        self.n = n
        self.delta_e = delta_e
        self.r_si = r_si
        self.r_rfe = r_rfe
        self.alpha_so = alpha_so

    def radial(self, alpha: np.array, r):
        """Determines radial B field at angle(s) alpha and radius r

        Args:
            alpha: A numpy array holding angles at which B field is calculated.
            r: Radius at which B field is calculated. Should be of type int or float.
        Returns:
            b_radial: A numpy array of normal B fields in airgap at radius r and angle(s) alpha
        """

        b_radial_h = self.radial_harmonics(r)

        # get phase and magnitude of B field harmonics
        b_radial_mag = abs(b_radial_h)
        b_phase = np.angle(b_radial_h)

        n = self.n.reshape(len(self.n), 1)  # reshape n for matrix multilication
        alpha_t = alpha.reshape(1, len(alpha))  # reshape alpha for matrix multilication
        # get effective theta at each harmonic based on n, alpha, and phase shift
        theta = n * alpha_t + b_phase.reshape(len(b_phase), 1)
        # get cosine asuuming MMF phase is provided relative to cos function
        cos_array = np.cos(theta)

        # get effective normal B field at each alpha as a sum of all harmonics
        b_radial = np.sum(b_radial_mag.reshape(len(b_phase), 1) * cos_array, axis=0)
        return b_radial

    def tan(self, alpha: np.array):
        """Determines tanglential B field at angle(s) alpha and inner bore of stator r_si

        Args:
            alpha: A numpy array holding angles at which B field is calculated.
        Returns:
            b_tan: A numpy array of tangential B fields
        """

        b_tan_h = self.tangetial_harmonics()

        # get phase and magnitude of B field harmonics
        b_tan_mag = abs(b_tan_h)
        b_tan_phase = np.angle(b_tan_h)

        n = self.n.reshape(len(self.n), 1)  # reshape n for matrix multilication
        alpha_t = alpha.reshape(1, len(alpha))  # reshape alpha for matrix multilication
        # get effective theta at each harmonic based on n, alpha, and phase shift
        theta = n * alpha_t + b_tan_phase.reshape(len(b_tan_phase), 1)
        # get cosine asuuming MMF phase is provided relative to cos function
        cos_array = np.cos(theta)

        # get effective tangential B field at each alpha as a sum of all harmonics
        b_tan = np.sum(b_tan_mag.reshape(len(b_tan_phase), 1) * cos_array, axis=0)
        return b_tan

    def radial_harmonics(self, r):
        """Determines radial B field harmonics at radius r

        Args:
            r: Radius at which B field harmonics are calculated. Should be of type int or float.
        Returns:
            b_radial_h: A numpy array of normal B field harmonics at r
        """

        mu0 = 4 * np.pi * 10**-7
        conv_b_field = self.MMF * mu0 / self.delta_e
        k_sov = self.slot_opening_factor()
        k_cu = self.curvature_coefficient(r)
        # scale field by slot opening factor and curvature coefficient
        b_radial_h = conv_b_field * k_sov * k_cu
        return b_radial_h

    def tangetial_harmonics(self):
        """Determines radial B field harmonics at inner bore of stator

        Args:
            r: Radius at which B field harmonics are calculated. Should be of type int or float.
        Returns:
            b_radial_h: A numpy array of normal B field harmonics at r
        """

        mu0 = 4 * np.pi * 10**-7
        # rotate mmf angle by -ve pi/2
        A_hat = self.MMF * self.n / self.r_si * np.exp(-np.pi / 2 * 1j)
        b_tan_h = -mu0 * A_hat
        return b_tan_h

    def slot_opening_factor(self):
        """Determines reduction in normal B-field due to slot opening in stator

        Args:
            n: harmonic under consideration (v*p)
            Sq: Slot opening in radians
        Returns:
            k_sov: slot opening factor
        """

        k_sov = np.sin(self.n * self.alpha_so / 2) / (self.n * self.alpha_so / 2)
        return k_sov

    def curvature_coefficient(self, r):
        """Determines curavture coefficient that causes field magnitude to vary across the airgap

        Curvature coefficient is especially important to determine in machine with large effective radial
        airgaps such as ultra-high speed SPMs
        Args:
            delta_e: Effective airgap of SPM. Sum of magnet. sleeve thickness and airgap
            r_si: Inner radius of the stator
            r_rfe: Outer radius of rotor iron
            r: Radius at which radial B-field is to be calculated
            n: harmonic under consideration (v*p)
        Returns:
            k_cu: curvature coefficient
        """

        k_cu = (
            self.delta_e
            * self.n
            / r
            * (r / self.r_si) ** self.n
            * (1 + (self.r_rfe / r) ** (2 * self.n))
            / (1 - (self.r_rfe / self.r_si) ** (2 * self.n))
        )
        return k_cu
