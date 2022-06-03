import numpy as np
import scipy.optimize as op
from typing import List,Any

#%% Thermal Resistance Network Analyzer
class ThermalNetworkProblem:
    """Problem class from Thermal Resistance Network Analyzer.
    
    Attributes:
        res: List of Resistance objects
        
        Q_dot: List of Thermal sources at nodal locations
        
        T_ref: List of [ref_node,ref_temp]
        
        N_nodes: Number of Nodes in system
    """
    def __init__(self,res: List['Resistance'],
                 Q_dot: List[float],
                 T_ref: List[List[int,float]],
                 N_nodes: int):
        self.res=res
        self.Q_dot=Q_dot
        self.T_ref=T_ref
        self.N_nodes=N_nodes

class ThermalNetworkAnalyzer:
    """Thermal Resistance Network Analyzer.
    """
    def analyze(self,problem: ThermalNetworkProblem):
        """Analyze imported resistance network problem

        Args:
            problem: ThermalNetworkProblem object to be analyzed
                
        Returns:
            T: Temperature distribution at each node in system
        """
        R_inv=np.zeros([problem.N_nodes,problem.N_nodes])
        for i,r in enumerate(problem.res):
            N1=r.Node1
            N2=r.Node2
            res=r.resistance_value
            R_inv[N1,N2]=(1/res)
            R_inv[N2,N1]=(1/res)
        one=np.ones([len(R_inv[:,1]),1])
        Sum_R=np.dot(R_inv,one)
        G=-R_inv
        for i,r in enumerate(R_inv[:,1]):
            E=np.zeros([len(R_inv[:,1]),len(R_inv[:,1])])
            E[i,i]=1
            e=np.zeros([1,len(R_inv[:,1])])
            e[0,i]=1
            G=G+np.dot(np.dot(E,Sum_R),e)
            
        G_aug=G
        for node,temp in problem.T_ref:
            G_aug[node,:]=np.zeros_like(G_aug[0,:])
            G_aug[node,node]=1
            Q_dot_aug=problem.Q_dot
            Q_dot_aug[node]=temp
        T=np.dot(np.linalg.inv(G_aug),Q_dot_aug) 
        print(T)
        return T

class Material:
    """ Class holding material parameters.
    
    Attributes:
        
        k: Thermal conductivity [W/m-K]
        cp: cp value of fluid []
        mu: Viscosity of fluid []
        
    """
    def __init__(self, k:float,
                 cp: float = 0.0,
                 mu: float = 0.0):
        self.k = k
        self.cp=cp
        self.mu=mu



class Resistance:
    """Base class for thermal resisance
    
    Attributes: 
        Material: Material object holding material properties
        
        Node1: First node connected to resistance
        
        Node2: Second node connected to resistance
        
        resistance_value: Thermal resistance [K/W]
        
    """
    def __init__(self, Material: Material,
                 Node1: int,
                 Node2: int):
        self.Material = Material
        self.Node1 = Node1
        self.Node2 = Node2

    @property
    def resistance_value(self):
        return None


class plane_wall(Resistance):
    """Plane wall thermal resistance.
    
    Attributes: 
        Material: Material object holding material properties
        
        Node1: First node connected to resistance
        
        Node2: Second node connected to resistance
        
        resistance_value: Thermal resistance [K/W]
        
        L1: Position of node-1 [m]
        
        L2: Position of node-2 [m]
        
        A: Cross sectional area [m^2]
        
    """
    def __init__(self, Material: Material,
                 Node1: int,
                 Node2: int,
                 L1: float,
                 L2: float,
                 A: float):
        super().__init__(Material, Node1, Node2)
        self.L1 = L1
        self.L2 = L2
        self.A = A

    @property
    def resistance_value(self):
        return (self.L2 - self.L1) / (self.Material.k * self.A)


class cylind_wall(Resistance):
    """Cylindrical wall thermal resistance.
    
    Attributes: 
        Material: Material object holding material properties
        
        Node1: First node connected to resistance
        
        Node2: Second node connected to resistance
        
        resistance_value: Thermal resistance [K/W]
        
        R1: Radial position of node-1 [m]
        
        R2: Radial position of node-2 [m]
        
        H: Height of wall [m]
        
    """
    def __init__(self, Material: Material,
                 Node1: int,
                 Node2: int,
                 R1: float,
                 R2: float,
                 H: float):
        super().__init__(Material, Node1, Node2)
        self.R1 = R1
        self.R2 = R2
        self.H = H

    @property
    def resistance_value(self):
        return np.log(self.R2 / self.R1) / (2 * np.pi * self.H * self.Material.k)


class air_gap_conv(Resistance):
    """Air gap convection thermal resistance
    
    Attributes: 
        Material: Material object holding material properties
        
        Node1: First node connected to resistance
        
        Node2: Second node connected to resistance
        
        resistance_value: Thermal resistance [K/W]
        
        omega: rotational speed [rad/s]
        
        R_r: Rotor outer radius [m]
         
        R_s: Stator inner radius [m]
        
        u_z: Axial airflow speed [m/s]
        
        A: Cross sectional area [m^2]
        
        h: Convection Coeff [W/m^2-K]
        
    """
    def __init__(self, Material: Material,
                 Node1: int,
                 Node2: int,
                 omega: float,
                 R_r: float,
                 R_s: float,
                 u_z: float,
                 A: float):
        super().__init__(Material, Node1, Node2)
        self.omega = omega
        self.R_r = R_r
        self.R_s = R_s
        self.u_z = u_z
        self.A = A

    @property
    def h(self):
        g = self.R_s = self.R_r
        r_m = (self.R_r + self.R_s) / 2
        a = self.R_r
        b = self.R_s
        D_h = 2 * g
        u_theta = self.omega * self.R_r
        Re_g = (self.omega * g * self.R_r) / self.Material.mu
        Re_theta = (self.omega * (self.R_r ** 2)) / self.Material.mu
        Re_z = (
            np.sqrt((self.omega * self.R_r) ** 2 + self.u_z ** 2)
            * D_h
            / self.Material.mu
        )
        g_dim = g / self.R_r
        Ta_m = Re_g * ((g / self.R_r) ** (0.5))
        Pr = 1000 * self.Material.cp * self.Material.mu / self.Material.k
        if Ta_m <= 41:
            self.Nu = 2
        elif Ta_m > 41 and Ta_m < 100:
            self.Nu = 0.202 * (Ta_m ** (0.63)) * (Pr ** (0.27))
        elif Ta_m >= 100:
            if self.u_z == 0:
                self.Nu = 0.03 * Re_z ** 0.8
            else:
                self.Nu = (
                    (
                        0.022
                        * (1 + D_h * u_theta / (np.pi * a * self.u_z) ** 2) ** 0.8714
                    )
                    * (Re_z ** 0.8)
                    * (Pr ** 0.5)
                )
        else:
            self.Nu = None
        return self.Nu * self.Material.k / D_h

    @property
    def resistance_value(self):
        return 1 / (self.h * self.A)


class hub_conv(Resistance):
    """Hub convection thermal resistance
    
    Attributes: 
        Material: Material object holding material properties
        
        Node1: First node connected to resistance
        
        Node2: Second node connected to resistance
        
        resistance_value: Thermal resistance [K/W]
        
        omega: rotational speed [rad/s]
        
        A: Cross sectional area [m^2]
        
        h: Convection Coeff [W/m^2-K]
        
    """
    def __init__(self, Material: Material,
                 Node1: int,
                 Node2: int,
                 omega: float,
                 A: float):
        super().__init__(Material, Node1, Node2)
        self.omega = omega
        # self.R=R
        self.A = A

    @property
    def h(self):
        return 0.35 * self.Material.k * (self.omega / self.Material.mu) ** 0.5

    @property
    def resistance_value(self):
        return 1 / (self.h * self.A)


class shaft_conv(Resistance):
    """Shaft convection thermal resistance
    
    Attributes: 
        Material: Material object holding material properties
        
        Node1: First node connected to resistance
        
        Node2: Second node connected to resistance
        
        resistance_value: Thermal resistance [K/W]
        
        omega: rotational speed [rad/s]
        
        R: Shaft outer radius [m]
        
        u_z: Axial airflow speed [m/s]
        
        A: Cross sectional area [m^2]
        
        h: Convection Coeff [W/m^2-K]
        
        Re: Reynolds number []
        
        Pr: Prandlt number []
        
        Nu: Nusselt number []
        
    """
    def __init__(self, Material: Material,
                 Node1: int,
                 Node2: int,
                 omega: float,
                 R: float,
                 A: float,
                 u_z: float):
        super().__init__(Material, Node1, Node2)
        self.omega = omega
        self.R = R
        self.A = A
        self.u_z = u_z

    @property
    def Re(self):
        return ((self.R * self.omega)) * self.R / self.Material.mu
        # return np.sqrt((self.R*self.omega)**2+self.u_z**2)*self.R/self.Material.mu

    @property
    def Pr(self):
        return 1000 * self.Material.cp * self.Material.mu / self.Material.k

    @property
    def Nu(self):
        return 0.036 * self.Re ** 0.8 * self.Pr ** 0.33

    @property
    def h(self):
        return self.Nu * self.Material.k / (2 * self.R)

    @property
    def resistance_value(self):
        return 1 / (self.h * self.A)


class conv(Resistance):
    """Air gap convection thermal resistance
    
    Attributes: 
        Material: Material object holding material properties
        
        Node1: First node connected to resistance
        
        Node2: Second node connected to resistance
        
        resistance_value: Thermal resistance [K/W]
        
        A: Cross sectional area [m^2]
        
        h: Convection Coeff [W/m^2-K]
        
    """
    def __init__(self, Material: Material,
                 Node1: int,
                 Node2: int,
                 h: float,
                 A: float):
        super().__init__(Material, Node1, Node2)
        self._h = h
        self.A = A

    @property
    def h(self):
        return self._h

    @property
    def resistance_value(self):
        return 1 / (self.h * self.A)



