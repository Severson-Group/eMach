########################### source of equations ###############################
# Z. Q. Zhu, D. Howe, and C. C. Chan, “Improved analytical model for predicting 
# the magnetic field distribution in brushless permanent-magnet machines,” 
# IEEE Trans. Magn., doi: 10.1109/20.990112.
###############################################################################

import numpy as np
import os
import sys

sys.path.append(os.path.dirname(__file__))
from bfield_protocol import BField

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


class BFieldSPM_InnerRotor(BField):
    """Class representing radial B field across motor airgap of SPM from arc magnets

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

    def tan(self, alpha, r=None, harmonics=None):
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
        # calculate radial b field magnitudes
        Bov = (Mv*vp/(muR*(vp)**2-1))*\
                (c3v-1+2*(r_fe/Rmo)**(vp+1)-(c3v+1)*(r_fe/Rmo)**(2*vp))*muR/\
                ((muR+1)*(1-(r_fe/Rsi)**(2*vp))-(muR-1)*((Rmo/Rsi)**(2*vp)-(r_fe/Rmo)**(2*vp)))*\
                ((r/Rsi)**(vp-1)*(Rmo/Rsi)**(vp+1)+(Rmo/r)**(vp+1))

        # discard even harmoincs and revise formula for vp=1
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
        # calculate tangential b field magnitudes
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
            c1v = np.sin((vp+1)*alpha_p*np.pi/(2*p))/((vp+1)*alpha_p*np.pi/(2*p))
            c2v = np.sin((vp-1)*alpha_p*np.pi/(2*p))/((vp-1)*alpha_p*np.pi/(2*p))
            for i in range(len(vp)):
                if vp[i]==1:
                    c2v[i] = 1
                    break
            Mrv = Br*alpha_p*(c1v+c2v)
            Mtv = Br*alpha_p*(c1v-c2v)
            Mv = Mrv+vp*Mtv
            c3v = (vp-1/(vp))*Mrv/Mv + 1/(vp)
            c3v[i] = 2*Mrv[i]/Mv[i]

        elif self.mag_dir=="radial":
            Mrv = 2*Br*alpha_p*np.sin(v*np.pi*alpha_p/2)/(v*np.pi*alpha_p/2)
            Mtv = 0
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
