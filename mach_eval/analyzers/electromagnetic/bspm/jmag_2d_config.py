class JMAG_2D_Config:
    def __init__(self, **kwargs) -> None:
        # attributes for rev and steps per rev
        self.no_of_rev_1TS = kwargs["no_of_rev_1TS"]
        self.no_of_rev_2TS = kwargs["no_of_rev_2TS"]
        self.no_of_steps_per_rev_1TS = kwargs["no_of_steps_per_rev_1TS"]
        self.no_of_steps_per_rev_2TS = kwargs["no_of_steps_per_rev_2TS"]
        # mesh attributes in m
        self.mesh_size = kwargs["mesh_size"]
        self.magnet_mesh_size = kwargs["magnet_mesh_size"]
        self.airgap_mesh_radial_div = kwargs["airgap_mesh_radial_div"]
        self.airgap_mesh_circum_div = kwargs["airgap_mesh_circum_div"]
        self.mesh_air_region_scale = kwargs["mesh_air_region_scale"]
        # results and paths
        self.only_table_results = kwargs["only_table_results"]
        self.csv_results = kwargs["csv_results"]
        self.del_results_after_calc = kwargs["del_results_after_calc"]
        self.run_folder = kwargs["run_folder"]
        self.jmag_csv_folder = kwargs["jmag_csv_folder"]
        # other settings
        self.max_nonlinear_iterations = kwargs["max_nonlinear_iterations"]
        self.multiple_cpus = kwargs["multiple_cpus"]
        self.jmag_scheduler = kwargs["jmag_scheduler"]
        self.jmag_visible = kwargs["jmag_visible"]
