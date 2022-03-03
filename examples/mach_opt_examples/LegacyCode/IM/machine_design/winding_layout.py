
class WindingLayout(object):
    def __init__(self, DPNV_or_SEPA, Qs, p, ps=None):

        # separate winding
        if DPNV_or_SEPA == False \
        and Qs == 24 \
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

        # combined winding
        if DPNV_or_SEPA == True \
        and Qs == 24 \
        and p == 2:
            # DPNV winding implemented as DPNV winding (GroupAC means it experiences flip phasor excitation from suspension inverter, while GroupBD does not.)
            #                     U-GrBD                        U-GrBD    W-GrBD                        W-GrBD    V-GrBD                        V-GrBD
            #                               W-GrAC    V-GrAC                        V-GrAC    U-GrAC                        U-GrAC    W-GrAC             : flip phases 19-14??? slot of phase U??? (这个例子的这句话看不懂)
            self.rightlayer_phase = ['U', 'U', 'W', 'W', 'V', 'V', 'U', 'U', 'W', 'W', 'V', 'V', 'U', 'U', 'W', 'W', 'V', 'V', 'U', 'U', 'W', 'W', 'V', 'V'] # ExampleQ24p2m3ps1: torque winding outer layer
            self.rightlayer_polarity = ['+', '+', '-', '-', '+', '+', '-', '-', '+', '+', '-', '-', '+', '+', '-', '-', '+', '+', '-', '-', '+', '+', '-', '-']
            self.leftlayer_phase  = self.rightlayer_phase[::] # ExampleQ24p2m3ps1: torque winding inner layer
            self.leftlayer_polarity  = self.rightlayer_polarity[::]
            self.grouping_a   = [  'b',   'b',   'a',   'a',   'a',   'a',   'b',
                                   'b',   'b',   'b',   'a',   'a',   'a',   'a',
                                   'b',   'b',   'b',   'b',   'a',   'a',   'a',   'a',   'b',   'b'] # 只取决于outerlayer/rightlayer的反相情况
            self.coil_pitch    = 6 # left layer can be inferred from coil pitch and right layer diagram
            self.CommutatingSequenceD = 1 # D stands for Drive winding (i.e., torque winding)
            self.CommutatingSequenceB = 0 # B stands for Bearing winding (i.e., suspension winding), commutating sequence decides the direction of the rotating field
            self.number_parallel_branch = 2.
            self.bool_3PhaseCurrentSource = False # 3PhaseCurrentSource is a macro in circuit setup of JMAG
            self.no_winding_layer = 2 # for torque winding and this means there could be a short pitch

            self.y    = 6 # coil_pitch, left layer can be inferred from coil pitch and right layer diagram
            self.Kw    = 0.966
            self.initial_excitation_bias_compensation_deg = -30

            # backward compatibility
            self.l41 = self.rightlayer_phase
            self.l42 = self.rightlayer_polarity
            self.l21 = self.leftlayer_phase
            self.l22 = self.leftlayer_polarity

        # combined winding
        if DPNV_or_SEPA == True \
        and Qs == 24 \
        and p == 1:
            # DPNV winding implemented as DPNV winding (GroupAC means it experiences flip phasor excitation from suspension inverter, while GroupBD does not.)
            #                     U-GroupBD                               V-GroupBD                               W-GroupBD
            #                                         W-GroupAC                               U-GroupAC                               V-GroupAC           : flip phases 13-16 slot of phase U
            self.rightlayer_phase = ['U', 'U', 'U', 'U', 'W', 'W', 'W', 'W', 'V', 'V', 'V', 'V', 'U', 'U', 'U', 'U', 'W', 'W', 'W', 'W', 'V', 'V', 'V', 'V'] # ExampleQ24p1m3ps2: torque winding outer layer
            self.rightlayer_polarity = ['+', '+', '+', '+', '-', '-', '-', '-', '+', '+', '+', '+', '-', '-', '-', '-', '+', '+', '+', '+', '-', '-', '-', '-'] 
            self.leftlayer_phase  = ['U', 'W', 'W', 'W', 'W', 'V', 'V', 'V', 'V', 'U', 'U', 'U', 'U', 'W', 'W', 'W', 'W', 'V', 'V', 'V', 'V', 'U', 'U', 'U'] # ExampleQ24p1m3ps2: torque winding inner layer
            self.leftlayer_polarity  = ['+', '-', '-', '-', '-', '+', '+', '+', '+', '-', '-', '-', '-', '+', '+', '+', '+', '-', '-', '-', '-', '+', '+', '+']
            self.grouping_AC   = [  0,   0,   0,   0,   1,   1,   1,   1,   0,   0,   0,   0,   1,   1,   1,   1,   0,   0,   0,   0,   1,   1,   1,   1] # 只取决于rightlayer的反相情况
            self.coil_pitch    = 9 # left layer can be inferred from coil pitch and right layer diagram
            self.CommutatingSequenceD = 1
            self.CommutatingSequenceB = 0
            self.number_parallel_branch = 2.
            self.bool_3PhaseCurrentSource = False # 3PhaseCurrentSource is a macro in circuit setup of JMAG
            self.no_winding_layer = 2 # for torque winding and this means there could be a short pitch
            self.initial_excitation_bias_compensation_deg = 360/24*0.5 # for torque winding # Note that the initial excitation direction is biased (not aligned with x-axis) due to the fact that the u-phase winding is not aligned with x-axis

            # backward compatibility
            self.l41 = self.rightlayer_phase
            self.l42 = self.rightlayer_polarity
            self.l21 = self.leftlayer_phase
            self.l22 = self.leftlayer_polarity


        # PMSM ONLY

        # combined winding
        # concentrated winding
        if DPNV_or_SEPA == True \
        and Qs == 6 \
        and p == 2:
            # DPNV winding implemented as DPNV winding (GroupAC means it experiences flip phasor excitation from suspension inverter, while GroupBD does not.)
            self.rightlayer_phase = ['U', 'V', 'W', 'U', 'V', 'W'] # torque winding right layer
            self.rightlayer_polarity = ['+', '+', '+', '+', '+', '+']
            self.leftlayer_phase  = ['W', 'U', 'V', 'W', 'U', 'V']
            self.leftlayer_polarity  = ['-', '-', '-', '-', '-', '-']
            # self.grouping_AC   = [  0,   0,   0,   1,   1,   1] # 只取决于outerlayer/rightlayer的反相情况，AC是在悬浮逆变器激励下会反相的
            self.CommutatingSequenceB = 1 # [???]

            self.grouping_AC   = [  0,   1,   0,   1,   0,   1] # Jingwei's layout
            self.CommutatingSequenceB = 0 # [CHECKED]

            self.coil_pitch    = -1 # left layer can be inferred from coil pitch and right layer diagram
                                    # We use negative coil_pitch to indicate concentrated winding
            self.CommutatingSequenceD = 1
            self.number_parallel_branch = 2.
            self.bool_3PhaseCurrentSource = False # 3PhaseCurrentSource is a macro in circuit setup of JMAG
            self.no_winding_layer = 2 # for torque winding and this means there could be a short pitch

            self.initial_excitation_bias_compensation_deg = 0 # for torque winding

            # backward compatibility
            self.l41 = self.rightlayer_phase
            self.l42 = self.rightlayer_polarity
            self.l21 = self.leftlayer_phase
            self.l22 = self.leftlayer_polarity

        # combined winding
        # distrubuted winding
        if DPNV_or_SEPA == True \
        and Qs == 6 \
        and p == 1:
            # DPNV winding implemented as DPNV winding (GroupAC means it experiences flip phasor excitation from suspension inverter, while GroupBD does not.)
            self.rightlayer_phase = ['U', 'W', 'V', 'U', 'W', 'V'] # torque winding right layer
            self.rightlayer_polarity = ['+', '-', '+', '-', '+', '-']
            self.leftlayer_phase  = ['W', 'V', 'U', 'W', 'V', 'U']
            self.leftlayer_polarity  = ['-', '+', '-', '+', '-', '+']
            self.grouping_a   = [  'b', 'a', 'b', 'a', 'b', 'a'] # 只取决于outerlayer/rightlayer的反相情况，AC是在悬浮逆变器激励下会反相的
                                                                # Same with Jingwei's layout
            self.y    = 2 # coil_pitch, left layer can be inferred from coil pitch and right layer diagram
            self.Kw    = 0.866
            self.CommutatingSequenceD = 1
            self.CommutatingSequenceB = 0 # [CHECKED]
            self.number_parallel_branch = 2.
            self.bool_3PhaseCurrentSource = False # 3PhaseCurrentSource is a macro in circuit setup of JMAG
            self.no_winding_layer = 2 # for torque winding and this means there could be a short pitch

            self.initial_excitation_bias_compensation_deg = 0 # for torque winding

            # backward compatibility
            self.l41 = self.rightlayer_phase
            self.l42 = self.rightlayer_polarity
            self.l21 = self.leftlayer_phase
            self.l22 = self.leftlayer_polarity



        # combined winding
        # distrubuted winding
        if DPNV_or_SEPA == True \
        and Qs == 12 \
        and p == 2:
            # DPNV winding implemented as DPNV winding (GroupAC means it experiences flip phasor excitation from suspension inverter, while GroupBD does not.)
            self.rightlayer_phase = ['U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V'] # torque winding right layer
            self.rightlayer_polarity = ['+', '-', '+', '-', '+', '-', '+', '-', '+', '-', '+', '-']
            self.leftlayer_phase  = ['U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V']
            self.leftlayer_polarity  = ['+', '-', '+', '-', '+', '-', '+', '-', '+', '-', '+', '-']

            # self.grouping_AC   = [  0,   1,   0,   0,   0,   0,   1,   0,   1,   1,   1,   1] # 只取决于outerlayer/rightlayer的反相情况，AC是在悬浮逆变器激励下会反相的
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

        # combined winding
        # concentrated winding
        ps = 5 # ps should be specified in future revision
        if DPNV_or_SEPA == True \
        and Qs == 12 \
        and p == 4 \
        and ps == 5:
            # DPNV winding implemented as DPNV winding (GroupAC means it experiences flip phasor excitation from suspension inverter, while GroupBD does not.)
            # self.rightlayer_phase = ['U', 'V', 'W', 'U', 'V', 'W', 'U', 'V', 'W', 'U', 'V', 'W'] # torque winding right layer
            # self.rightlayer_polarity = ['+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+'] # This configuration gives negative torque
            # self.leftlayer_phase  = ['W', 'U', 'V', 'W', 'U', 'V', 'W', 'U', 'V', 'W', 'U', 'V']
            # self.leftlayer_polarity  = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
            # self.rightlayer_phase = ['U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V'] # Want to change the commutating sequence so the torque is positive? No, it is not that intuitive.
            # self.rightlayer_polarity = ['+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+']
            # self.leftlayer_phase  = ['V', 'U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V', 'U', 'W']
            # self.leftlayer_polarity  = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
            self.rightlayer_phase = ['U', 'V', 'W', 'U', 'V', 'W', 'U', 'V', 'W', 'U', 'V', 'W'] # Want to change torque sign? Yes, this works
            self.rightlayer_polarity = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
            self.leftlayer_phase  = ['W', 'U', 'V', 'W', 'U', 'V', 'W', 'U', 'V', 'W', 'U', 'V']
            self.leftlayer_polarity  = ['+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+']
            # self.grouping_AC   = [  0,   0,   0,   1,   1,   1,   1,   1,   1,   0,   0,   0] # 只取决于outerlayer/rightlayer的反相情况，AC是在悬浮逆变器激励下会反相的
            self.grouping_a   = [  'b',   'b',   'a',   'a',   'b',   'b',   'a',   'a',   'b',   'b',   'a',   'a'] # Jingwei's layout
            self.coil_pitch    = -1 # left layer can be inferred from coil pitch and right layer diagram
                                    # We use negative coil_pitch to indicate concentrated winding
            self.CommutatingSequenceD = 1 # D stands for Drive winding (i.e., torque winding)
            self.CommutatingSequenceB = 0 # [CHECKED] # B stands for Bearing winding (i.e., suspension winding), commutating sequence decides the direction of the rotating field
            self.number_parallel_branch = 2.
            self.bool_3PhaseCurrentSource = False # 3PhaseCurrentSource is a macro in circuit setup of JMAG
            self.no_winding_layer = 2 # for torque winding and this means there could be a short pitch

            self.y = 1
            self.Kw = 0.866
            self.initial_excitation_bias_compensation_deg = -15 # for torque winding

            # backward compatibility
            self.l41 = self.rightlayer_phase
            self.l42 = self.rightlayer_polarity
            self.l21 = self.leftlayer_phase
            self.l22 = self.leftlayer_polarity



        # combined winding
        # distrubuted winding
        if DPNV_or_SEPA == True \
        and Qs == 12 \
        and p == 1:

            # DPNV winding implemented as DPNV winding (GroupAC means it experiences flip phasor excitation from suspension inverter, while GroupBD does not.)
            self.rightlayer_phase = ['U', 'U', 'W', 'W', 'V', 'V', 'U', 'U', 'W', 'W', 'V', 'V'] # torque winding right layer
            self.rightlayer_polarity = ['+', '+', '-', '-', '+', '+', '-', '-', '+', '+', '-', '-']
            self.leftlayer_phase  = ['U', 'W', 'W', 'V', 'V', 'U', 'U', 'W', 'W', 'V', 'V', 'U']
            self.leftlayer_polarity  = ['+', '-', '-', '+', '+', '-', '-', '+', '+', '-', '-', '+']
            self.grouping_a   = ['b','b','a','a','b','b','a','a','b','b','a','a'] # 只取决于outerlayer/rightlayer的反相情况，AC是在悬浮逆变器激励下会反相的
                                                                # Same with Jingwei's layout
            self.y    = 5 # coil_pitch, left layer can be inferred from coil pitch and right layer diagram
            self.Kw    = 0.933
            self.CommutatingSequenceD = 1
            self.CommutatingSequenceB = 0 # [CHECKED]
            self.number_parallel_branch = 2.
            self.bool_3PhaseCurrentSource = False # 3PhaseCurrentSource is a macro in circuit setup of JMAG
            self.no_winding_layer = 2 # for torque winding and this means there could be a short pitch

            self.initial_excitation_bias_compensation_deg = 0 # for torque winding

            # backward compatibility
            self.l41 = self.rightlayer_phase
            self.l42 = self.rightlayer_polarity
            self.l21 = self.leftlayer_phase
            self.l22 = self.leftlayer_polarity

        try: 
            self.y
            self.distributed_or_concentrated = False if abs(self.y) == 1 else True
        except:
            raise Exception('Error: Not implemented for this winding.')


        # # combined winding
        # if DPNV_or_SEPA == True \
        # and Qs == 24 \
        # and p == 2:
        #     # DPNV winding implemented as separate winding
        #     # if self.fea_config_dict['DPNV_separate_winding_implementation'] == True or self.fea_config_dict['DPNV'] == False: 
        #         # You may see this msg because there are more than one designs in the initial_design.txt file.
        #         # msg = 'Not implemented error. In fact, this equivalent implementation works for 4 pole motor only.'
        #         # logging.getLogger(__name__).warn(msg)

        #     # this is legacy codes for easy implementation in FEMM
        #     self.l41=[ 'W', 'W', 'U', 'U', 'V', 'V', 'W', 'W', 'U', 'U', 'V', 'V', 'W', 'W', 'U', 'U', 'V', 'V', 'W', 'W', 'U', 'U', 'V', 'V']
        #     self.l42=[ '+', '+', '-', '-', '+', '+', '-', '-', '+', '+', '-', '-', '+', '+', '-', '-', '+', '+', '-', '-', '+', '+', '-', '-']
        #     # DPNV style for one phase: -- oo ++ oo
        #     self.l21=[  'U', 'U', 'W', 'W', 'V', 'V', 
        #                 'U', 'U', 'W', 'W', 'V', 'V', 
        #                 'U', 'U', 'W', 'W', 'V', 'V', 
        #                 'U', 'U', 'W', 'W', 'V', 'V']
        #     self.l22=[  '-', '-', 'o', 'o', '+', '+', # 横着读和竖着读都是负零正零。 
        #                 'o', 'o', '-', '-', 'o', 'o', 
        #                 '+', '+', 'o', 'o', '-', '-', 
        #                 'o', 'o', '+', '+', 'o', 'o']
        #     self.coil_pitch = 6
        #     self.CommutatingSequenceD = 0
        #     self.CommutatingSequenceB = 0
        #     self.number_parallel_branch = 1.
        #     self.bool_3PhaseCurrentSource = True
        #     self.no_winding_layer = 1 # for torque winding
