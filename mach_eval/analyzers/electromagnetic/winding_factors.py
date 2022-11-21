import numpy as np

class WindingFactorsProblem:
    """Problem class for winding factor analyzer
    Attributes:
        harmonics_list: list of harmonics to be included in calculations []
        winding_layout: array of winding layers beginning with top layer
                        and ending with bottom layer, length will be number 
                        of teeth and height will be number of layers, "+1" 
                        for conductor into page, 0 for no present conductors, 
                        and "-1" for conductor out of page [turns]
        alpha_1: angle of first slot counterclockwise from +x axis [rad]
    """
    
    def __init__(self, harmonics_list, winding_layout, alpha_1):
        
        self.harmonics_list = harmonics_list
        self.winding_layout = winding_layout
        self.alpha_1 = alpha_1
        
        
            
class WindingFactorsAnalyzer:
    """Analyzer class to evaluate winding factors"""
    
    
    
    def analyze(self, problem="WindingFactorsProblem"):
        """Determines winding factors using calculations function
        
        Args:
            harmonics: harmonics array definied in problem
            winding_layout: winding layout defined in problem
            alpha_1: angle of slot 1 defined in problem
            
        Returns:
            kw_final: complex winding factor array
        """
        
        harmonics = problem.harmonics
        winding_layout = problem.winding_layout
        alpha_1 = problem.alpha_1
        kw_final = self.calculations(harmonics,winding_layout,alpha_1)
        
        return kw_final
    
    
    
    def calculations(self,harmonics,winding_layout,alpha_1):
        """Determines winding factors given harmonics requested, winding
            layout, and alpha_1
            
        Variables:
            n: 1D array from 1-harmonics used in iterations
            layer: layout of layer for single layer winding
            top_layer: layout of top layer for double layer winding
            bottom_layer: layout of bottom layer for double layer winding
            alpha_c: angle between stator teeth
            filled_slots: number of slots filled in total layout
            slot: slot at which each term is calculated
            
        Returns:
            k_w: winding factor array for each winding layout
        """        
        
        n = np.arange(1,harmonics+1)
        
        if len(winding_layout[:,0]) == 1:
            layer = winding_layout[0][:,None]
            alpha_c = 2*np.pi/len(layer)
            filled_slots = np.count_nonzero(layer)
            slot = np.arange(1,len(layer)+1)[:,None]
            k_w = layer*np.exp(1j*n*((slot-1)*alpha_c+alpha_1))
        elif len(winding_layout[:,0]) == 2:
            top_layer = winding_layout[0][:,None]
            bottom_layer = winding_layout[1][:,None]
            alpha_u = 2*np.pi/len(top_layer)
            filled_slots = np.count_nonzero(top_layer) + np.count_nonzero(bottom_layer)
            slot = np.arange(1,len(layer)+1)[:,None]
            k_w = top_layer*np.exp(1j*n*(slot-1)*alpha_u)+bottom_layer*np.exp(1j*n*(slot-1)*alpha_u)
        else:
            raise Exception("Error: Winding layer must be 1 or 2!")
            
        k_w = sum(k_w)/filled_slots
        
        return k_w