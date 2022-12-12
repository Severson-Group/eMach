class BIM_Time_Harmonic_Analyzer_Config:
    def __init__(self, **kwargs) -> None:
        self.run_folder = kwargs["run_folder"]
        self.fraction = kwargs["fraction"]
        self.freq_start = kwargs["freq_start"]
        self.freq_end = kwargs["freq_end"]
        self.no_of_freqs = kwargs["no_of_freqs"]
        self.max_freq_error = kwargs["max_freq_error"]

