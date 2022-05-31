import numpy as np
import scipy.optimize as op

#%% Thermal Resistance Network Analyzer
class ThermalProblem:
    def __init__(self,res,Q_dot,T_ref,N_nodes):
        self.res=res
        self.Q_dot=Q_dot
        self.T_ref=T_ref
        self.N_nodes=N_nodes

class ThermalAnalyzer:
    def analyze(self,problem):
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
    def __init__(self, k):
        self.k = k

    def set_cp(self, cp):
        self.cp = cp

    def set_mu(self, mu):
        self.mu = mu


class Resistance:
    def __init__(self, Material, Node1, Node2):
        self.Material = Material
        self.Node1 = Node1
        self.Node2 = Node2

    @property
    def resistance_value(self):
        return None


class plane_wall(Resistance):
    """Material,Node1,Node2,L1,L2,A"""

    def __init__(self, Material, Node1, Node2, L1, L2, A):
        super().__init__(Material, Node1, Node2)
        self.L1 = L1
        self.L2 = L2
        self.A = A

    @property
    def resistance_value(self):
        return (self.L2 - self.L1) / (self.Material.k * self.A)


class cylind_wall(Resistance):
    def __init__(self, Material, Node1, Node2, R1, R2, H):
        super().__init__(Material, Node1, Node2)
        self.R1 = R1
        self.R2 = R2
        self.H = H

    @property
    def resistance_value(self):
        return np.log(self.R2 / self.R1) / (2 * np.pi * self.H * self.Material.k)


class air_gap_conv(Resistance):
    def __init__(self, Material, Node1, Node2, omega, R_r, R_s, u_z, A):
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

    def conv_coeff(self):
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
    def __init__(self, Material, Node1, Node2, omega, A):
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
    def __init__(self, Material, Node1, Node2, omega, R, A, u_z):
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
    def __init__(self, Material, Node1, Node2, h, A):
        super().__init__(Material, Node1, Node2)
        self._h = h
        self.A = A

    @property
    def h(self):
        return self._h

    @property
    def resistance_value(self):
        return 1 / (self.h * self.A)



