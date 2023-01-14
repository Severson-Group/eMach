class BIM_Time_Harmonic_Analyzer_Config:
    def __init__(self, **kwargs) -> None:
        self.run_folder = kwargs["run_folder"]
        self.fraction = kwargs["fraction"]
        self.freq_start = kwargs["freq_start"]
        self.freq_end = kwargs["freq_end"]
        self.no_of_freqs = kwargs["no_of_freqs"]
        self.max_freq_error = kwargs["max_freq_error"]
        self.get_results_in_t2tss_analyzer = kwargs["get_results_in_t2tss_analyzer"] # True: if we want to run BIM_Transient_2TSS_Analyzer in parallel
        self.id_rotor_iron = kwargs["id_rotor_iron"]
        self.id_rotor_bars = kwargs["id_rotor_bars"]
        self.id_stator_slots = kwargs["id_stator_slots"]
        self.id_stator_iron = kwargs["id_stator_iron"]
        self.automesh = kwargs["automesh"]
        # can be set to zero if using automesh
        self.mesh_size_aluminum = kwargs["mesh_size_aluminum"]
        self.mesh_size_steel = kwargs["mesh_size_steel"]
        self.mesh_size_airgap = kwargs["mesh_size_airgap"]
        self.mesh_size_copper = kwargs["mesh_size_copper"]
        self.mesh_size_other_regions = kwargs["mesh_size_other_regions"]
        self.double_cage = kwargs["double_cage"]
