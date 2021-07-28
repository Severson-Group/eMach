# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 10:39:47 2021

@author: Martin Johnson
"""

import numpy as np
from spec_USmotor_Q6p1 import fea_config_dict
import scipy.optimize as op

class StructuralProblem:
    """Problem class for StructuralAnalyzer.

    Attributes:
        sh (RotorComponent): Shaft RotorComponent object.
        rc (RotorComponent): Rotor core RotorComponent object.
        pm (RotorComponent): Magnets RotorComponent object.
        sl (RotorComponent): Sleeve RotorComponent object.
        deltaT (float): Temperature rise in deg C.
        omega (float): rotational speed in rad/s.

    """
    def __init__(self, sh, rc, pm, sl, deltaT, omega):
        """StructuralProblem __init__ method.

        Args:
            sh (RotorComponent): Shaft RotorComponent object.
            rc (RotorComponent): Rotor core RotorComponent object.
            pm (RotorComponent): Magnets RotorComponent object.
            sl (RotorComponent): Sleeve RotorComponent object.
            deltaT (float): Temperature rise in deg C.
            omega (float): rotational speed in rad/s.

        """
        self.sh=sh
        self.rc=rc
        self.pm=pm
        self.sl=sl
        self.deltaT=deltaT
        self.omega=omega
        
class StructuralProblemDef:
    """ProblemDefinition class for StructuralAnalyzer.

    Attributes:
        mat_dict (dict): material parameters dictionary.

    """
    def __init__(self,mat_dict: dict)->'StructuralProblemDef':
        """StructuralProblemDef __init__ method.

        Args:
            mat_dict (dict): material parameters dictionary.

        """
        self.mat_dict=mat_dict
    
    def get_problem(self,r_sh: float,d_m: float,r_ro: float,d_sl : float,
                   delta_sl: float, deltaT: float,N: float)->'StructuralProblem':
        """Creates StructuralProblem object from input

        Args:
            r_sh (float): Shaft outer radius.
            d_m (float): Shaft outer radius.
            r_ro (float): Shaft outer radius.
            d_sl (float): Shaft outer radius.
            delta_sl (float): Shaft outer radius.
            deltaT (float): Shaft outer radius.
            N (float): Shaft outer radius.

        Returns:
            problem (StructuralProblem): StructuralProblem

        """
        R1=r_sh
        R2=r_ro-d_m
        R3=r_ro
        R4=r_ro+d_sl
        # print('R1:',R1,'R2:',R2,'R3:',R3)
        ##############################
        #    Load Operating Point
        ##############################
        omega=N*2*np.pi/60
        ##############################
        #   Load Material Properties
        ##############################
        rho_sh=self.mat_dict['shaft_material_density']
        E_sh=self.mat_dict['shaft_youngs_modulus']
        nu_sh=self.mat_dict['shaft_poission_ratio']
        alpha_sh=self.mat_dict['alpha_sh']#1.2E-5
        
        rho_rc=self.mat_dict['core_material_density']
        E_rc=self.mat_dict['core_youngs_modulus']
        nu_rc=self.mat_dict['core_poission_ratio']
        alpha_rc=self.mat_dict['alpha_rc']#1.2E-5
        
        rho_pm=self.mat_dict['magnet_material_density']
        E_pm=self.mat_dict['magnet_youngs_modulus']
        nu_pm=self.mat_dict['magnet_poission_ratio']
        alpha_pm=self.mat_dict['alpha_pm']#5E-6
        
        rho_sl=self.mat_dict['sleeve_material_density']
        E_t_sl=self.mat_dict['sleeve_youngs_th_direction']
        E_p_sl=self.mat_dict['sleeve_youngs_p_direction']
        nu_p_sl=self.mat_dict['sleeve_poission_ratio_p']
        nu_tp_sl=self.mat_dict['sleeve_poission_ratio_tp']
        alpha_t=self.mat_dict['alpha_sl_t']#-4.7E-7
        alpha_r=self.mat_dict['alpha_sl_r']#.3E-6
        MaxRadialSleeveStress=self.mat_dict['sleeve_max_rad_stress']
        MaxTanSleeveStress=self.mat_dict['sleeve_max_tan_stress']
        ##############################
        #   Make Rotor Materials
        ##############################
        ShaftMaterial=Material_Isotropic(rho_sh,E_sh,nu_sh,alpha_sh)
        RotorCoreMaterial=Material_Isotropic(rho_rc,E_rc,nu_rc,alpha_rc)
        MagnetMaterial=Material_Isotropic(rho_pm,E_pm,nu_pm,alpha_pm)
        SleeveMaterial=Material_Transverse_Isotropic(rho_sl,E_t_sl,E_p_sl,nu_tp_sl,
                                                     nu_p_sl,alpha_r,alpha_t)
        
        #######################################################################
        #                      Create Rotor Section Objects
        #######################################################################
        
        ##############################
        #    Create Shaft Object
        ##############################
        
        sh=RotorComponent(ShaftMaterial,0,R1)
        
        ##############################
        #  Create Rotor Core Object
        ##############################
        
        rc=RotorComponent(RotorCoreMaterial,R1,R2)
        
        
        ##############################
        #    Create Magnets Object
        ##############################
         
        pm=RotorComponent(MagnetMaterial,R2,R3)
        pm.set_MaxRadialStress(0)
        
        
        ##############################
        #   Create Sleeve Object
        ##############################
        
        sl=RotorComponent(SleeveMaterial,R3,R4)
        sl.set_MaxRadialStress(MaxRadialSleeveStress)
        sl.set_MaxTanStress(MaxTanSleeveStress)
        
        
        sl.set_th(d_sl)
        sl.set_delta_sl(delta_sl)
        
        problem=StructuralProblem(sh,rc,pm,sl,deltaT,omega)
        return problem
    
class StructuralAnalyzer:
    
    def analyze(self,problem: 'StructuralProblem')->['Sigma','Sigma','Sigma','Sigma']:
        """Analyze structural problem

        Args:
            problem (StructuralProblem): problem for analyzer.

        Returns:
            results (['Sigma','Sigma','Sigma','Sigma']): Sigma objects

        """
        sh=problem.sh
        rc=problem.rc
        pm=problem.pm
        sl=problem.sl
        deltaT=problem.deltaT
        omega=problem.omega
        
        A=self.DetermineCoeff(sh,rc,pm,sl,deltaT,omega)
        sigma_sh=Sigma(sh,[A[0],0],omega,deltaT)
        sigma_rc=Sigma(rc,[A[1],A[2]],omega,deltaT)
        sigma_pm=Sigma(pm,[A[3],A[4]],omega,deltaT)
        sigma_sl=Sigma(sl,[A[5],A[6]],omega,deltaT)
        
        return [sigma_sh,sigma_rc,sigma_pm,sigma_sl]
        
        
        
        
    def DetermineCoeff(self,sh: 'RotorComponent',rc,pm,sl,deltaT,omega):
        """Deterimine coeffiecents for calculating stresses

        Args:
            sh (RotorComponent): Shaft RotorComponent object.
            rc (RotorComponent): Rotor core RotorComponent object.
            pm (RotorComponent): Magnets RotorComponent object.
            sl (RotorComponent): Sleeve RotorComponent object.
            deltaT (float): Temperature rise in deg C.
            omega (float): rotational speed in rad/s.

        Returns:
            A (np.Array): numpy array of stress coeffiecents.

        """
        r1=sh.R_o
        r2=rc.R_o
        r3=pm.R_o
        r4=sl.R_o
        delta_1=0
        delta_2=0
        delta_3=sl.Dr
        K=np.zeros([7,7])
        X=np.zeros([7,1])
        
        #Stress at interface between shaft and rotor core
        K[0,0]=(sh.C1*sh.h + sh.C2)*(r1**(sh.h-1))
        K[0,1]=-(rc.C1*rc.h + rc.C2)*(r1**(rc.h-1))
        K[0,2]=-(rc.C2 -rc.C1*rc.h)*(r1**(-rc.h-1))
        X[0]= (3*rc.C1 +rc.C2)*rc.Beta*(omega**2)*(r1**2)\
            +rc.zeta_r*deltaT\
            -((3*sh.C1+sh.C2)*sh.Beta*(omega**2)*(r1**2))\
            -sh.zeta_r*deltaT
        
        #Stress at interface between rotor core and magnet array
        K[1,1]=(rc.C1*rc.h + rc.C2)*(r2**(rc.h-1))
        K[1,2]=(rc.C2 -rc.C1*rc.h)*(r2**(-rc.h-1))
        K[1,3]=-(pm.C1*pm.h + pm.C2)*(r2**(pm.h-1))
        K[1,4]=-(pm.C2 -pm.C1*pm.h)*(r2**(-pm.h-1))
        X[1] = (3*pm.C1 +pm.C2)*pm.Beta*(omega**2)*(r2**2)\
            +pm.zeta_r*deltaT\
            -((3*rc.C1+rc.C2)*rc.Beta*(omega**2)*(r2**2))\
            -rc.zeta_r*deltaT
        
        #Stress at interface between magnet array and rotor sleeve
        K[2,3]=(pm.C1*pm.h + pm.C2)*(r3**(pm.h-1))
        K[2,4]=(pm.C2 -pm.C1*pm.h)*(r3**(-pm.h-1))
        K[2,5]=-(sl.C1*sl.h + sl.C2)*(r3**(sl.h-1))
        K[2,6]=-(sl.C2 -sl.C1*sl.h)*(r3**(-sl.h-1))
        X[2] = (3*sl.C1 +sl.C2)*sl.Beta*(omega**2)*(r3**2)\
            +sl.zeta_r*deltaT\
            -((3*pm.C1+pm.C2)*pm.Beta*(omega**2)*(r3**2))\
            -pm.zeta_r*deltaT
        
        #Stress at Outside of rotor sleeve
        K[3,5]=(sl.C1*sl.h + sl.C2)*(r4**(sl.h-1))
        K[3,6]=(sl.C2 -sl.C1*sl.h)*(r4**(-sl.h-1))
        X[3] = -((3*sl.C1 +sl.C2)*sl.Beta*(omega**2)*(r4**2))\
            -sl.zeta_r*deltaT
    
    
        #Displacement at interface between shaft and rotor core
        K[4,0] = r1**sh.h
        K[4,1] = -r1**rc.h
        K[4,2] = -r1**-rc.h
        X[4] = delta_1 + rc.Beta*(omega**2)*(r1**3) - (sh.Beta*(omega**2)*(r1**3))
        
        #Displacement at interface between rotor core and Magnets
        K[5,1] = r2**rc.h
        K[5,2] = r2**-rc.h
        K[5,3]= -r2**pm.h
        K[5,4] = -r2**-pm.h
        X[5] = delta_2 + pm.Beta*(r2**3) - (rc.Beta*(r2**3))
        
        #Displacement at interface between Magnets and Sleeve
        K[6,3] = r3**pm.h;
        K[6,4] = r3**-pm.h;
        K[6,5] = -r3**sl.h;
        K[6,6] = -r3**-sl.h;
        X[6] = delta_3 + sl.Beta*(r3**3)+sl.zeta_u*deltaT*r3- (pm.Beta*(omega**2)*(r3**3));
    
        A=np.dot(np.linalg.inv(K),X)
        return A
    
class Material_Isotropic:
    
    def __init__(self,Density,ElasticMod,PoissonRatio,alpha):
        """__init__ definition for Material_Isotropic class.

        Args:
            Density (float): Mass Density.
            ElasticMod (float): Elastic modulus.
            PoissonRatio (float): Poisson ratio.
            alpha (float): Coeffiecent of thermal expansion.

        """
        self.rho = Density #Density of material
        self.E = ElasticMod #Elastic modulus of material
        self.Nu = PoissonRatio #Poisson Ratio of material
        self.alpha=alpha

    @property
    def Del(self):
        return self.E/((1+self.Nu)*(1-2*self.Nu))
        #Del = self.E/((1+self.Nu)*(1-2*self.Nu))
    @property
    def C1(self):
        return self.Del*(1-self.Nu)
        #self.C1 = Del*(1-self.Nu)
    @property
    def C2(self):
        return self.Del*self.Nu
        #self.C2 = Del*self.Nu
    @property
    def C3(self):
        return self.C1
    @property
    def h(self):
        return 1
        #self.C3 = self.C1
        #self.lamb = (self.C2 -self.C1)*self.alpha +(self.C2 -self.C3)*self.alpha
    @property
    def zeta_r(self):
        return-(self.C1+self.C2)*self.alpha
    @property
    def zeta_t(self):
        return-(self.C2+self.C3)*self.alpha
    @property
    def zeta_u(self):
        return 0
class Material_Transverse_Isotropic:
        
    def __init__(self,Density,ElasticMod_Thread,ElasticMod_Plane,PoissonRatio_tp,
                 PoissonRatio_p,alpha_r,alpha_t):
        """__init__ definition for Material_Transverse_Isotropic class.

        Args:
            Density (float): Mass Density.
            ElasticMod_Thread (float): Elastic modulus.
            ElasticMod_Plane (float): Elastic modulus.
            PoissonRatio_tp (float): Poisson ratio thread to plane.
            PoissonRatio_p (float): Poisson ratio plane.
            alpha_r (float): Coeffiecent of thermal expansion radial.
            alpha_t (float): Coeffiecent of thermal expansion tangential.

        """
        self.rho = Density #Density of material
        self.E_t = ElasticMod_Thread #Elastic modulus of material in the thread direction
        self.E_p = ElasticMod_Plane #Elastic modulus of material in the plane direction
        self.Nu_tp  = PoissonRatio_tp  #Poission Ratio stress in plane causing elongation in thread
        self.Nu_p  = PoissonRatio_p #Poisson Ratio of material in plane direction
        self.alpha_r = alpha_r
        self.alpha_t = alpha_t
        
    @property
    def Nu_pt(self):
        return self.Nu_tp*(self.E_p/self.E_t)
    @property
    def Del(self):
        return ((1+self.Nu_p)*(1-self.Nu_p - 2*self.Nu_pt*self.Nu_tp))/((self.E_p**2)*self.E_t)
    @property
    def C1(self):
        return (1-self.Nu_tp*self.Nu_pt)/(self.E_t*self.E_p*self.Del)
    @property
    def C2(self):
        return (self.Nu_tp + self.Nu_tp*self.Nu_p)/(self.E_t*self.E_p*self.Del)
    @property
    def C3(self):
        return (1-(self.Nu_p**2))/((self.E_p**2)*self.Del)
    @property
    def h(self):
        return np.sqrt(self.C3/self.C1)
    @property
    def zeta_r(self):
        return-((((self.C1-self.C2)/(self.C1-self.C3))-self.C1)*self.alpha_r\
                +(((self.C2-self.C3)/(self.C1-self.C3))-self.C2)*self.alpha_r)
    @property
    def zeta_t(self):
        return-((((self.C1-self.C2)/(self.C1-self.C3))-self.C2)*self.alpha_r\
                +(((self.C2-self.C3)/(self.C1-self.C3))-self.C3)*self.alpha_r)

    @property
    def zeta_u(self):
        return-( (((self.C1-self.C2)/(self.C1-self.C3)))*self.alpha_r\
                +(((self.C2-self.C3)/(self.C1-self.C3)))*self.alpha_r)

    

class RotorComponent:
   
    def __init__(self,MaterialObject,InnerRadius,OuterRadius):
        """__init__ definition for RotorComponent class.

        Args:
            MaterialObject (Material_Isotropic or Material_Transverse_Isotropic): Material object.
            InnerRadius (float): Inner radius.
            OuterRadius (float): Outer radius.

        """
        self.R_i=InnerRadius
        self.R_o=OuterRadius
        if isinstance(MaterialObject,Material_Transverse_Isotropic):
            self.E_t=MaterialObject.E_t
            self.E_p=MaterialObject.E_p
            self.Nu_tp=MaterialObject.Nu_tp
            self.Nu_pt=MaterialObject.Nu_pt
            self.Nu_p=MaterialObject.Nu_p
            self.rho=MaterialObject.rho
            self.alpha_r=MaterialObject.alpha_r
            self.alpha_t=MaterialObject.alpha_t
            
        else:
            self.E=MaterialObject.E
            self.Nu=MaterialObject.Nu
            self.rho=MaterialObject.rho
            self.alpha=MaterialObject.alpha
        self.C1=MaterialObject.C1
        self.C2=MaterialObject.C2
        self.C3=MaterialObject.C3
        self.h=MaterialObject.h
        self.zeta_r=MaterialObject.zeta_r
        self.zeta_t=MaterialObject.zeta_t
        self.zeta_u=MaterialObject.zeta_u
        self.material=MaterialObject
        
        
    @property
    def Beta(self):
        return -self.rho/(9*self.C1 -self.C3)
        #self.OMEGA=  -self.rho*(omega**2)/(9*obj.C1 -obj.C3);
    def set_delta_sl(self,Dr):
        self.Dr=Dr
    def set_th(self,th):
        if th is None:
            th=0
        self.th=th
        self.R_o=self.R_i+self.th
    def set_MaxRadialStress(self,sigmaMax):
        self.sigmaMaxR=sigmaMax
    def set_MaxTanStress(self,sigmaMax):
        self.sigmaMaxT=sigmaMax
    
        
class Sigma:
    
    def __init__(self,rotorComponent,A,omega,deltaT):
        """__init__ definition for Sigma class.

        Args:
            rotorComponent (Material_Isotropic or Material_Transverse_Isotropic): Material object.
            A (np.array): Stress Coeffiecents.
            omega (float): Rotational speed rad/s.
            deltaT (float): Temperature rise.

        """
        self.rotComp=rotorComponent
        self.A=A
        self.omega=omega
        self.deltaT=deltaT
        
    def radial(self,R):
        """Radial Stress at radius R.
        
        Args:
            R (float): location to evaluate stress.
        """
        #Radial Stress
        sigma_r=self.A[0]*(self.rotComp.C1*self.rotComp.h + self.rotComp.C2)*(np.power(R,(self.rotComp.h-1)))+self.A[1]*(self.rotComp.C2 - self.rotComp.C1*self.rotComp.h)*(np.power(R,(-self.rotComp.h-1)))+(3*self.rotComp.C1 + self.rotComp.C2)*self.rotComp.Beta*(self.omega**2)*(np.power(R,2))+self.rotComp.zeta_r*self.deltaT
        #Tangential Stress    
        return sigma_r
    
    def tangential(self,R):
        """Tangential Stress at radius R
        
        Args:
            R (float): location to evaluate stress.
        """
        #Tangential Stress
        sigma_t= self.A[0]*(self.rotComp.C2*self.rotComp.h + self.rotComp.C3)*(np.power(R,(self.rotComp.h-1)))+self.A[1]*(self.rotComp.C3 - self.rotComp.C2*self.rotComp.h)*(np.power(R,(-self.rotComp.h-1)))+(3*self.rotComp.C2 + self.rotComp.C3)*self.rotComp.Beta*(self.omega**2)*(np.power(R,2))+self.rotComp.zeta_t*self.deltaT
        return sigma_t

class SleeveProblem:
    
    def __init__(self,r_sh: float,d_m: float,r_ro: float,
                   deltaT: float,mat_dict: dict,N: float):
        """__init__ definition for SleeveProblem class
        
        Args:
            r_sh (float): shaft radius.
            d_m (float): Magnet thickness.
            r_ro (float): Outer rotor radius.
            deltaT (float): Temperature rise.
            mat_dict (dict): Material Dictionary.
            N (float): Rotational speed RPM.
        """
        
        self.r_sh=r_sh
        self.d_m=d_m
        self.r_ro=r_ro
        self.deltaT=deltaT
        self.mat_dict=mat_dict
        self.N = N
        
    def tan_sleeve(self,x):
        """Calculate sigma_t_sl_max for given sleeve design"""
        d_sl=x[0]
        delta_sl=x[1]
        R_ro=self.r_ro
        N=self.N
        r_sh=self.r_sh
        d_m=self.d_m
        deltaT=self.deltaT
        struc_prob_def=StructuralProblemDef(self.mat_dict)
        problem=struc_prob_def.get_problem(r_sh,d_m,R_ro,d_sl,delta_sl,deltaT,N)
        analyzer=StructuralAnalyzer()
        sigmas=analyzer.analyze(problem)
        x_sl=np.linspace(R_ro,R_ro+d_sl,50)
        sigma_t_sl=sigmas[3].tangential(x_sl)
        stress=sigma_t_sl[0]
        return stress
    
    def rad_sleeve(self,x):
        """Calculate P_sl for given sleeve design"""
        d_sl=x[0]
        delta_sl=x[1]
        R_ro=self.r_ro
        N=self.N
        r_sh=self.r_sh
        d_m=self.d_m
        deltaT=self.deltaT
        struc_prob_def=StructuralProblemDef(self.mat_dict)
        problem=struc_prob_def.get_problem(r_sh,d_m,R_ro,d_sl,delta_sl,deltaT,N)
        analyzer=StructuralAnalyzer()
        sigmas=analyzer.analyze(problem)
        x_sl=np.linspace(R_ro,R_ro+d_sl,50)
        sigma_r_sl=sigmas[3].radial(x_sl)
        stress=sigma_r_sl[0]
        return stress
    def rad_magnet(self,x):
        """Calculate P_pm for given sleeve design"""
        d_sl=x[0]
        delta_sl=x[1]
        R_ro=self.r_ro
        N=self.N
        r_sh=self.r_sh
        d_m=self.d_m
        deltaT=self.deltaT
        struc_prob_def=StructuralProblemDef(self.mat_dict)
        problem=struc_prob_def.get_problem(r_sh,d_m,R_ro,d_sl,delta_sl,deltaT,N)
        analyzer=StructuralAnalyzer()
        sigmas=analyzer.analyze(problem)
        x_pm=np.linspace(R_ro-d_m,R_ro,50)
        sigma_r_pm=sigmas[2].radial(x_pm)
        stress=sigma_r_pm[0]
        return stress
    def tan_magnet(self,x):
        """Calculate sigma_t_pm_max for given sleeve design"""
        d_sl=x[0]
        delta_sl=x[1]
        R_ro=self.r_ro
        N=self.N
        r_sh=self.r_sh
        d_m=self.d_m
        deltaT=self.deltaT
        struc_prob_def=StructuralProblemDef(self.mat_dict)
        problem=struc_prob_def.get_problem(r_sh,d_m,R_ro,d_sl,delta_sl,deltaT,N)
        analyzer=StructuralAnalyzer()
        sigmas=analyzer.analyze(problem)
        x_pm=np.linspace(R_ro-d_m,R_ro,50)
        sigma_t_pm=sigmas[2].tangential(x_pm)
        stress=sigma_t_pm[0]
        return stress
    def cost(self,x):
        return x[0]
    
class SleeveProblemDef:
    
    def __init__(self,mat_dict: dict):
        self.mat_dict  =mat_dict
        
    def get_problem(self,r_sh: float,d_m: float,r_ro: float,
                   deltaT: float,N: float)->'StructuralProblem':
        problem=SleeveProblem(r_sh,d_m,r_ro,deltaT,self.mat_dict,N)
        return problem
    
class SleeveAnalyzer:
    def __init__(self,stress_limits):
        self.stress_limits=stress_limits
    
    def analyze(self,problem: 'SleeveProblem'):
        nlc1 = op.NonlinearConstraint(problem.rad_sleeve,
                                      self.stress_limits['rad_sleeve'],
                                      0)
        nlc2 = op.NonlinearConstraint(problem.tan_sleeve,-np.inf,
                                      self.stress_limits['tan_sleeve'])
        nlc3 = op.NonlinearConstraint(problem.rad_magnet, -np.inf,
                                      self.stress_limits['rad_magnets'])
        nlc4 = op.NonlinearConstraint(problem.tan_magnet,-np.inf,
                                      self.stress_limits['tan_magnets'])
        const=[nlc1,nlc2,nlc3,nlc4]
        sol=op.minimize(problem.cost,[1E-3,-1E-3],tol=1E-4,constraints=const,bounds=[[0,1],[-.01,0]])
        print(sol.success)
        print(sol)
        if sol.success == True:
            return sol.x
        else:
            return False
    

if __name__ == "__main__":
    mat_dict=fea_config_dict
    stress_limits={'rad_sleeve':-100E6,
                   'tan_sleeve':1300E6,
                   'rad_magnets':0,
                   'tan_magnets':80E6}
    mat_dict['alpha_sh']=1.2E-5
    mat_dict['alpha_rc']=1.2E-5
    mat_dict['alpha_pm']=5E-6
    mat_dict['alpha_sl_t']=-4.7E-7
    mat_dict['alpha_sl_r']=0.3E-6
    r_sh=5E-3
    d_m=3E-3
    r_ro=12.5E-2
    deltaT=10
    N=10E3
    spd=SleeveProblemDef(mat_dict)   
    problem=spd.get_problem(r_sh, d_m, r_ro, deltaT, N)
    ana=SleeveAnalyzer(stress_limits)
    sleeve_dim=ana.analyze(problem)
    print(sleeve_dim)
