

import abc
from typing import Union

import numpy as np
from numpy.typing import NDArray

class BFieldAnalyzerBase(abc.ABC):
    """Defines interface for all analyzer field classes"""

    @abc.abstractmethod
    def radial(
        self, alpha: NDArray, r: Union[int, float], harmonics: NDArray
        ) -> NDArray:
        ...

    @abc.abstractmethod
    def tangential(
        self, alpha: NDArray, r: Union[int, float], harmonics: NDArray
        ) -> NDArray:
        ...


class BFieldOuterStatorProblem1:
    """Problem class for stator radial B field analyzer
    Attributes:
        MMF: Current linkage or Magneto-Motive Force [A-turns]
        n: Harmonic corresponding to MMF
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
        mmf = m / np.pi * zq * N * k_w * I_hat / n * np.exp(-np.pi / 2 * 1j)
        return mmf


class BFieldOuterStatorProblem2:
    """Problem class for stator radial B field analyzer
    Attributes:
        MMF: Current linkage or Magneto-Motive Force [A-turns]
        n: Harmonic corresponding to MMF
        delta_e: Effective airgap [m]
        r_si: Inner radius of the stator [m]
        r_rfe: Outer radius of rotor iron [m]
        alpha_so: stator slot opening [radians]
    """

    def __init__(self, MMF, n, delta_e, r_si, r_rfe, alpha_so):
        self.MMF = MMF
        self.n = n
        self.delta_e = delta_e
        self.r_si = r_si
        self.r_rfe = r_rfe
        self.alpha_so = alpha_so


class BFieldOuterStatorAnalyzer:
    """Analyzer class to evaluate stator radial B field"""

    def analyze(self, problem=None):
        """Determines normal B-field at radius r due to stator windings

        Args:
            problem: Object of type OuterStatorBfieldProblem
        Returns:
            b_field: Radial magnetic field at radius r from stator windings [T]
        """

        b_field = BFieldOuterStator(
            mmf=problem.MMF,
            n=problem.n,
            delta_e=problem.delta_e,
            r_si=problem.r_si,
            r_rfe=problem.r_rfe,
            alpha_so=problem.alpha_so,
        )
        return b_field


class BFieldOuterStator(BFieldAnalyzerBase):
    """Class representing radial B field across motor airgap and tangential B field at stator inner bore
    
    ########################### source of equations ###############################
    # [1] G. Bergmann and A. Binder, “Design guidelines of bearingless PMSM with
    # two separate poly-phase windings,” in 2016 XXII International Conference on
    # Electrical Machines (ICEM), Lausanne, Switzerland, Sep. 2016, pp. 2588–2594.
    # doi: 10.1109/ICELMACH.2016.7732886.

    # [2] Z. Q. Zhu and D. Howe, “Instantaneous magnetic field distribution in
    # brushless permanent magnet DC motors. II. Armature-reaction field,” IEEE
    # Trans. Magn., vol. 29, no. 1, pp. 136–142, Jan. 1993, doi: 10.1109/20.195558.
    ###############################################################################

    Attributes:
        MMF: Current linkage or Magneto-Motive Force [A-turns]
        n: Harmonic corresponding to MMF
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

    def radial(self, alpha, r=None, harmonics=None):
        """Determines radial B field at angle(s) alpha and radius r

        Args:
            alpha: A numpy array holding angles at which B field is calculated.
            r: Radius at which B field is calculated. Should be of type int or float.
            harmonics: Optional argument to get fields from select harmonics alone. Type numpy array
        Returns:
            b_radial: A numpy array of normal B fields in airgap at radius r and angle(s) alpha
        """

        # check if harmonics passed as argument
        if harmonics is None:
            b_radial_h = self.radial_harmonics(r)
            n = self.n
        else:
            mask = np.in1d(self.n, harmonics)  # find array ids at which harmonics exist
            # n and b_radial_h only take harmonic values
            n = self.n[mask]
            b_radial_h = self.radial_harmonics(r)[mask]

        b_radial = self.__field_from_harmonics(b_radial_h, n, alpha)
        return b_radial

    def tangential(self, alpha, r=None, harmonics=None):
        """Determines tanglential B field at angle(s) alpha and inner bore of stator r_si

        Args:
            alpha: A numpy array holding angles at which B field is calculated.
            harmonics: Optional argument to get fields from select harmonics alone. Type numpy array
        Returns:
            b_tan: A numpy array of tangential B fields
        """
        if r is not None:
            print(
                "WARNING: stator tangential fields are always calculated at stator inner bore"
            )
        # check if harmonics passed as argument
        if harmonics is None:
            b_tan_h = self.tangential_harmonics()
            n = self.n
        else:
            mask = np.in1d(self.n, harmonics)  # find array ids at which harmonics exist
            # n and b_radial_h only take harmonic values
            n = self.n[mask]
            b_tan_h = self.tangential_harmonics()[mask]

        b_tan = self.__field_from_harmonics(b_tan_h, n, alpha)
        return b_tan

    def radial_harmonics(self, r=None):
        """Determines radial B field harmonics at radius r

        Args:
            r: Radius at which B field harmonics are calculated. Should be of type int or float. Defaults to
              inner bore of stator if not defined.
        Returns:
            b_radial_h: A numpy array of normal B field harmonics at r
        """
        if r is None:
            r = self.r_si
        elif r < self.r_rfe or r > self.r_si:
            print(r)
            raise ValueError("Radius provided not within machine airgap")

        mu0 = 4 * np.pi * 10**-7
        conv_b_field = self.MMF * mu0 / self.delta_e
        k_sov = self.__slot_opening_factor()
        k_cu = self.__curvature_coefficient(r)
        # scale field by slot opening factor and curvature coefficient
        # EQUATION 9 from [2]
        b_radial_h = conv_b_field * k_sov * k_cu
        return b_radial_h

    def tangential_harmonics(self):
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

    def __slot_opening_factor(self):
        """Determines reduction in normal B-field due to slot opening in stator

        Args:
            n: harmonic under consideration (v*p)
            Sq: Slot opening in radians
        Returns:
            k_sov: slot opening factor
        """
        # EQUATION 10 from [2]
        k_sov = np.sin(self.n * self.alpha_so / 2) / (self.n * self.alpha_so / 2)
        return k_sov

    def __curvature_coefficient(self, r):
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
        # EQUATION 11 from [2]
        k_cu = (
            self.delta_e
            * self.n
            / r
            * (r / self.r_si) ** self.n
            * (1 + (self.r_rfe / r) ** (2 * self.n))
            / (1 - (self.r_rfe / self.r_si) ** (2 * self.n))
        )
        return k_cu

    def __field_from_harmonics(self, fields, n, alpha):
        # get phase and magnitude of B field harmonics
        b_mag = abs(fields)
        b_phase = np.angle(fields)

        n = n.reshape(len(n), 1)  # reshape n for matrix multilication
        alpha_t = alpha.reshape(1, len(alpha))  # reshape alpha for matrix multilication
        # get effective theta at each harmonic based on n, alpha, and phase shift
        theta = n * alpha_t + b_phase.reshape(len(b_phase), 1)
        # get cosine asuuming MMF phase is provided relative to cos function
        cos_array = np.cos(theta)

        # get effective tangential B field at each alpha as a sum of all harmonics
        b_tan = np.sum(b_mag.reshape(len(b_mag), 1) * cos_array, axis=0)
        return b_tan


class BFieldSPM_InnerRotorProblem:
    """Problem class for stator radial B field analyzer
    Attributes:
        alpha_p: angular length of magnet in pu
        theta: orientation of rotor d-axis
        p: Number of pole pairs
        muR: Relative permeability
        r_fe: Outer radius of rotor iron
        dm: Thickness of magnet
        delta: Rotor sleeve and airgap dimension
        mag_dir: Direction of magnetization, 'parallel' or 'radial'
    """

    def __init__(self, alpha_p, theta, p, muR, Br, r_fe, dm, delta, mag_dir):
        self.alpha_p = alpha_p
        self.theta = theta
        self.p = p
        self.muR = muR
        self.Br=Br
        self.r_fe = r_fe
        self.dm = dm
        self.delta = delta
        self.mag_dir = mag_dir


class BFieldSPM_InnerRotorAnalyzer:
    """Analyzer class to evaluate SPM arc magnet radial B field"""

    def analyze(self, problem=None):
        """Determines normal B-field at radius r due to arc magnets

        Args:
            problem: Object of type SPM_InnerRotorPMFieldProblem
        Returns:
            b_field: Radial magnetic field at radius r from stator windings [T]
        """

        b_field = BFieldSPM_InnerRotor(
            alpha_p=problem.alpha_p,
            theta=problem.theta,
            p=problem.p,
            muR=problem.muR,
            Br=problem.Br,
            r_fe=problem.r_fe,
            dm=problem.dm,
            delta=problem.delta,
            mag_dir=problem.mag_dir,
        )
        return b_field


class BFieldSPM_InnerRotor(BFieldAnalyzerBase):
    """Class representing radial B field across motor airgap of SPM from arc magnets
    
    ########################### source of equations ###############################
    # Z. Q. Zhu, D. Howe, and C. C. Chan, “Improved analytical model for predicting 
    # the magnetic field distribution in brushless permanent-magnet machines,” 
    # IEEE Trans. Magn., doi: 10.1109/20.990112.
    ###############################################################################

    Attributes:
        alpha_p: angular length of magnet in pu
        p: Number of pole pairs
        muR: Relative permeability
        r_fe: Outer radius of rotor iron
        dm: Thickness of magnet
        delta: Rotor sleeve and airgap dimension
        mag_dir: Direction of magnetization, 'parallel' or 'radial'
    """

    def __init__(self, alpha_p, theta, p, muR, Br, r_fe, dm, delta, mag_dir):
        self.alpha_p = alpha_p
        self.theta = theta
        self.p = p
        self.muR = muR
        self.Br=Br
        self.r_fe = r_fe
        self.dm = dm
        self.delta = delta
        self.mag_dir = mag_dir
        self.Rmo = r_fe+dm
        self.Rsi = r_fe+dm+delta

    def radial(self, alpha, r=None, harmonics=None):
        """Determines radial B field at angle(s) alpha and radius r

        Args:
            alpha: A numpy array holding angles at which B field is calculated.
            r: Radius at which B field is calculated.
            theta: Angular orientation of PM rotor d-axis.
            harmonics: A numpy array holding holding harmonics of interest.
        Returns:
            b_radial: A numpy array of normal B fields in airgap at radius r and angle(s) alpha
        """
        if harmonics is None:
            harmonics = self.p * np.arange(1,15,2)  # first 13 harmonics
        b_radial_h = self.radial_harmonics(r, harmonics)
        n = harmonics
        b_radial = self.__field_from_harmonics(b_radial_h, n, alpha)
        return b_radial

    def tangential(self, alpha, r=None, harmonics=None):
        """Determines tangential B field at angle(s) alpha and radius r

        Args:
            alpha: A numpy array holding angles at which B field is calculated.
            r: Radius at which B field is calculated. Should be of type int or float
            theta: angular orientation of PM rotor d-axis
            harmonics: A numpy array holding holding harmonics of interest
        Returns:
            b_tan: A numpy array of tangential B fields in airgap at radius r and angle(s) alpha
        """
        if harmonics is None:
            harmonics = self.p * np.arange(1,15,2)  # first 13 harmonics
        b_tan_h = self.tan_harmonics(r, harmonics)
        n = harmonics
        b_tan = self.__field_from_harmonics(b_tan_h, n, alpha)
        return b_tan

    def radial_harmonics(self, r=None, harmonics=None):
        """Determines radial B field harmonics at radius r

        Args:
            r: Radius at which B field is calculated. Should be of type int or float. Defaults to 
              inner bore of stator if not defined.
            theta: angular orientation of PM rotor d-axis
            harmonics: A numpy array holding holding harmonics of interest. Considers 1st thirteen
              harmonics of p if not defined 
        Returns:
            b_rad_h: A numpy array of radial B field harmonics corresponding harmonics array
        """
        if r==None:
            r = self.Rsi    # stator inner bore
        if harmonics is None:
            harmonics = self.p * np.arange(1,15,2)  # first 13 harmonics
        r_fe = self.r_fe
        p = self.p
        muR = self.muR
        Rmo = self.Rmo # rotor outer radius
        Rsi = self.Rsi # stator inner radius
        vp = harmonics
        # get magnetization vector
        Mv, c3v = self.__get_Mv_c3v(harmonics)

        # calculate radial b field magnitudes using EQUATION 15a
        Bov = (Mv*vp/(muR*(vp)**2-1))*\
                (c3v-1+2*(r_fe/Rmo)**(vp+1)-(c3v+1)*(r_fe/Rmo)**(2*vp))*muR/\
                ((muR+1)*(1-(r_fe/Rsi)**(2*vp))-(muR-1)*((Rmo/Rsi)**(2*vp)-(r_fe/Rmo)**(2*vp)))*\
                ((r/Rsi)**(vp-1)*(Rmo/Rsi)**(vp+1)+(Rmo/r)**(vp+1))

        # discard even and fractional harmonics and revise formula for vp=1
        for i in range(len(vp)):
            # even harmonics non-existent
            if harmonics[i]/p % 2 == 0 or harmonics[i]/p % 1 != 0:
                Bov[i] = 0
                continue
            # vp=1 has different field formula
            elif vp[i] == 1:
                Bov[i] = ((Mv[i]/(muR*2))*(c3v[i]*(Rmo/Rsi)**2 -(c3v[i])*(r_fe/Rsi)**2 +\
                            (r_fe/Rsi)**2*np.log((Rmo/r_fe)**2))*muR/((muR+1)*(1-(r_fe/Rsi)**2)-\
                            (muR-1)*((Rmo/Rsi)**2-(r_fe/Rmo)**2))*(1+(Rsi/r)**2))
        # rotate based on rotor orientation
        b_rad_h = np.array(Bov) * np.exp(-self.theta*vp* 1j)
        return b_rad_h 
    
    def tan_harmonics(self, r=None, harmonics=None):
        """Determines tangential B field harmonics at radius r

        Args:
            r: Radius at which B field is calculated. Should be of type int or float. Defaults to 
              inner bore of stator if not defined.
            theta: angular orientation of PM rotor d-axis
            harmonics: A numpy array holding holding harmonics of interest. Considers 1st thirteen
              harmonics of p if not defined 
        Returns:
            b_rad_h: A numpy array of tangential B field harmonics corresponding harmonics array
        """
        if r==None:
            r = self.Rsi    # stator inner bore
        if harmonics is None:
            harmonics = self.p * np.arange(1,15,2)  # first 13 harmonics
        r_fe = self.r_fe
        p = self.p
        muR = self.muR
        Rmo = self.Rmo # rotor outer radius
        Rsi = self.Rsi # stator inner radius
        vp = harmonics
        # get magnetization vector
        Mv, c3v = self.__get_Mv_c3v(harmonics)

        # calculate radial b field magnitudes using EQUATION 15b
        Bov = (Mv*vp/(muR*(vp)**2-1))*\
            (c3v-1+2*(r_fe/Rmo)**(vp+1)-(c3v+1)*(r_fe/Rmo)**(2*vp))*muR/\
            ((muR+1)*(1-(r_fe/Rsi)**(2*vp))-(muR-1)*((Rmo/Rsi)**(2*vp)-(r_fe/Rmo)**(2*vp)))*\
            (-1*(r/Rsi)**(vp-1)*(Rmo/Rsi)**(vp+1)+(Rmo/r)**(vp+1))

        # discard even harmoincs and revise formula for vp=1
        for i in range(len(vp)):
            # even harmonics non-existent
            if harmonics[i]/p % 2 == 0 or harmonics[i]/p % 1 != 0:
                Bov[i] = 0
                continue
            # vp=1 has different field formula
            elif vp[i] == 1:
                Bov[i] = (Mv[i]/(muR*2))*(c3v[i]*(Rmo/Rsi)**2 -(c3v[i])*(r_fe/Rsi)**2 +\
                            (r_fe/Rsi)**2*np.log((Rmo/r_fe)**2))*muR/((muR+1)*(1-(r_fe/Rsi)**2)-\
                            (muR-1)*((Rmo/Rsi)**2-(r_fe/Rmo)**2))*(-1+(Rsi/r)**2)
        # rotate based on rotor orientation
        b_tan_h = np.array(Bov) * np.exp(-self.theta*vp* 1j)
        # rotate again considering tan is a sine function 
        b_tan_h = b_tan_h * np.exp(-np.pi/2* 1j)
        return b_tan_h 

    def __get_Mv_c3v(self, harmonics):
        alpha_p = self.alpha_p
        Br = self.Br
        p = self.p
        vp = harmonics
        v = vp/p
        if self.mag_dir=="parallel":
            # EQUATION 7c and 7d
            c1v = np.sin((vp+1)*alpha_p*np.pi/(2*p))/((vp+1)*alpha_p*np.pi/(2*p))
            c2v = np.sin((vp-1)*alpha_p*np.pi/(2*p))/((vp-1)*alpha_p*np.pi/(2*p))
            for i in range(len(vp)):
                if vp[i]==1:
                    c2v[i] = 1
                    break
            Mrv = Br*alpha_p*(c1v+c2v)
            Mtv = Br*alpha_p*(c1v-c2v)
            # EQUATION 10b
            Mv = Mrv+vp*Mtv
            c3v = (vp-1/(vp))*Mrv/Mv + 1/(vp)
            c3v[i] = 2*Mrv[i]/Mv[i]

        elif self.mag_dir=="radial":
            # EQUATION 7a and 7b
            Mrv = 2*Br*alpha_p*np.sin(v*np.pi*alpha_p/2)/(v*np.pi*alpha_p/2)
            Mtv = 0
            # EQUATION 10b
            Mv = Mrv+vp*Mtv
            c3v = vp
        else:
            raise NotImplemented("Invalid magnetization direction")
        return Mv, c3v

    def __field_from_harmonics(self, fields, n, alpha):
        # get phase and magnitude of B field harmonics
        b_mag = abs(fields)
        b_phase = np.angle(fields)

        n = n.reshape(len(n), 1)  # reshape n for matrix multilication
        alpha_t = alpha.reshape(1, len(alpha))  # reshape alpha for matrix multilication
        # get effective theta at each harmonic based on n, alpha, and phase shift
        theta = n * alpha_t + b_phase.reshape(len(b_phase), 1)
        # get cosine asuuming MMF phase is provided relative to cos function
        cos_array = np.cos(theta)

        # get effective tangential B field at each alpha as a sum of all harmonics
        b_field = np.sum(b_mag.reshape(len(b_mag), 1) * cos_array, axis=0)
        return b_field
