# Created: 4/13/2023
# Author: Dante Newman

class WindingLayout(object):
    def __init__(self, Q, p):

        # separate winding
        if Q == 24 \
        and p == 2:
            self.l41=[ 'W', 'W', 'U', 'U', 'V', 'V', 'W', 'W', 'U', 'U', 'V', 'V', 'W', 'W', 'U', 'U', 'V', 'V', 'W', 'W', 'U', 'U', 'V', 'V', ]
            self.l42=[ '+', '+', '-', '-', '+', '+', '-', '-', '+', '+', '-', '-', '+', '+', '-', '-', '+', '+', '-', '-', '+', '+', '-', '-', ]
            # separate style for one phase: ---- ++++
            self.l21=[ 'U', 'U', 'V', 'V', 'V', 'V', 'W', 'W', 'W', 'W', 'U', 'U', 'U', 'U', 'V', 'V', 'V', 'V', 'W', 'W', 'W', 'W', 'U', 'U', ]
            self.l22=[ '-', '-', '+', '+', '+', '+', '-', '-', '-', '-', '+', '+', '+', '+', '-', '-', '-', '-', '+', '+', '+', '+', '-', '-', ]
            self.coil_pitch = 6 # = Qs / poles for single layer
            self.CommutatingSequenceD = 0
            self.CommutatingSequenceB = 0
            self.number_parallel_branch = 1.
            self.bool_3PhaseCurrentSource = True
            self.no_winding_layer = 1 # for torque winding

        # PMSM ONLY

        # combined winding
        # concentrated winding
        if Q == 6 \
        and p == 2:
            # DPNV winding implemented as DPNV winding (GroupAC means it experiences flip phasor excitation from suspension inverter, while GroupBD does not.)
            self.rightlayer_phase = ['U', 'V', 'W', 'U', 'V', 'W'] # torque winding right layer
            self.rightlayer_polarity = ['+', '+', '+', '+', '+', '+']
            self.leftlayer_phase  = ['W', 'U', 'V', 'W', 'U', 'V']
            self.leftlayer_polarity  = ['-', '-', '-', '-', '-', '-']
            # self.grouping_AC   = [  0,   0,   0,   1,   1,   1] 
            
            self.grouping_a   = ['b', 'a', 'b', 'a', 'b', 'a']# Jingwei's layout

            self.y    = 1 # left layer can be inferred from coil pitch and right layer diagram

            self.bool_3PhaseCurrentSource = False # 3PhaseCurrentSource is a macro in circuit setup of JMAG
            self.no_winding_layer = 2 # for torque winding and this means there could be a short pitch

            self.initial_excitation_bias_compensation_deg = 0 # for torque winding

        # combined winding
        # distrubuted winding
        if Q == 12 \
        and p == 2:
            # DPNV winding implemented as DPNV winding (GroupAC means it experiences flip phasor excitation from suspension inverter, while GroupBD does not.)
            self.rightlayer_phase = ['U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V'] # torque winding right layer
            self.rightlayer_polarity = ['+', '-', '+', '-', '+', '-', '+', '-', '+', '-', '+', '-']
            self.leftlayer_phase  = ['U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V']
            self.leftlayer_polarity  = ['+', '-', '+', '-', '+', '-', '+', '-', '+', '-', '+', '-']

            # self.grouping_AC   = [  0,   1,   0,   0,   0,   0,   1,   0,   1,   1,   1,   1] 
            # self.CommutatingSequenceB = 1 # 0 # [CHECKED] # B stands for Bearing winding (i.e., suspension winding), commutating sequence decides the direction of the rotating field
            self.grouping_AC   = [  0,   1,   1,   0,   0,   1,   1,   0,   0,   1,   1,   0] # Jingwei's layout
            self.CommutatingSequenceB = 0 # 0 # [CHECKED] # B stands for Bearing winding (i.e., suspension winding), commutating sequence decides the direction of the rotating field
            
            self.CommutatingSequenceD = 1 # D stands for Drive winding (i.e., torque winding)
            self.coil_pitch    = 3 # left layer can be inferred from coil pitch and right layer diagram
            self.number_parallel_branch = 2.
            self.bool_3PhaseCurrentSource = False # 3PhaseCurrentSource is a macro in circuit setup of JMAG
            self.no_winding_layer = 2 # for torque winding and this means there could be a short pitch

            self.initial_excitation_bias_compensation_deg = 0 # for u phase torque winding

            # backward compatibility
            self.l41 = self.rightlayer_phase
            self.l42 = self.rightlayer_polarity
            self.l21 = self.leftlayer_phase
            self.l22 = self.leftlayer_polarity