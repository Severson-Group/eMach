import numpy as np
from .machine import MachineComponent, Winding, Winding_IM


class Shaft(MachineComponent):
    @staticmethod
    def required_dimensions():
        return ("r_sh",)

    @staticmethod
    def required_materials():
        return ("shaft_mat",)

    @property
    def r_sh(self):
        return self._dimensions_dict["r_sh"]

    @property
    def shaft_mat(self):
        return self._materials_dict["shaft_mat"]

    @property
    def V_sh(self):
        return np.pi * (self.r_sh**2) * self.l_st


class Shaft_IM(MachineComponent):
    def required_parameters():
        return ("Radius_Shaft",)

    def required_materials():
        return ("shaft_mat",)

    @property
    def r_sh(self):
        return self._machine_parameter_dict["r_sh"]

    @property
    def Radius_Shaft(self):
        return self._machine_parameter_dict["Radius_Shaft"]


class Rotor_Iron(MachineComponent):
    @staticmethod
    def required_dimensions():
        return ("d_ri",)

    @staticmethod
    def required_materials():
        return ("rotor_iron_mat",)

    @property
    def d_ri(self):
        return self._dimensions_dict["d_ri"]

    @property
    def rotor_iron_mat(self):
        return self._materials_dict["rotor_iron_mat"]


class IM_Rotor_Iron(MachineComponent):
    def required_parameters():
        return (
            "Angle_RotorSlotSpan",
            "Length_HeadNeckRotorSlot",
            "Radius_OuterRotor",
            "Radius_of_RotorSlot",
            "Radius_of_RotorSlot2",
            "Width_RotorSlotOpen",
        )

    def required_materials():
        return ("rotor_iron_mat",)

    @property
    def Angle_RotorSlotSpan(self):
        return self._machine_parameter_dict["Angle_RotorSlotSpan"]

    @property
    def Radius_OuterRotor(self):
        return self._machine_parameter_dict["Radius_OuterRotor"]

    @property
    def Radius_of_RotorSlot2(self):
        return self._machine_parameter_dict["Radius_of_RotorSlot2"]

    @property
    def Radius_of_RotorSlot(self):
        return self._machine_parameter_dict["Radius_of_RotorSlot"]

    @property
    def Width_RotorSlotOpen(self):
        return self._machine_parameter_dict["Width_RotorSlotOpen"]

    @property
    def rotor_iron_mat(self):
        return self._materials_dict["rotor_iron_mat"]


class IM_Rotor_Bar(MachineComponent):
    # It uses some dimesnions from IM_Rotor_Iron

    def required_materials():
        return (
            "Location_RotorBarCenter2",
            "use_drop_shape_rotor_bar",
        )

    def required_materials():
        return ("rotor_bar_mat",)

    @property
    def use_drop_shape_rotor_bar(self):
        return self._machine_parameter_dict["use_drop_shape_rotor_bar"]

    @property
    def Location_RotorBarCenter2(self):
        return self._machine_parameter_dict["Location_RotorBarCenter2"]

    @property
    def rotor_bar_mat(self):
        return self._materials_dict["rotor_bar_mat"]


class PM(MachineComponent):
    @staticmethod
    def required_dimensions():
        return "d_m", "alpha_ms", "alpha_m"

    @staticmethod
    def required_parameters():
        return ("n_m",)

    @staticmethod
    def required_materials():
        return ("magnet_mat",)

    @property
    def d_m(self):
        return self._dimensions_dict["d_m"]

    @property
    def alpha_m(self):
        return self._dimensions_dict["alpha_m"]

    @property
    def alpha_ms(self):
        return self._dimensions_dict["alpha_ms"]

    @property
    def n_m(self):
        return self._parameters_dict["n_m"]

    @property
    def magnet_mat(self):
        return self._materials_dict["magnet_mat"]


class RotorSleeve(MachineComponent):
    @staticmethod
    def required_dimensions():
        return ("d_sl",)

    @staticmethod
    def required_materials():
        return ("rotor_sleeve_mat",)

    @property
    def d_sl(self):
        return self._dimensions_dict["d_sl"]

    @property
    def rotor_sleeve_mat(self):
        return self._materials_dict["rotor_sleeve_mat"]


# class Rotor_bar(MachineComponent):
#     def required_parameters():
#         return ()
#     def required_materials():


class IM_Rotor(Shaft_IM, IM_Rotor_Iron, IM_Rotor_Bar, MachineComponent):

    # Add bar component a bit later
    def required_parameters():
        req_param = (
            "r_rs",
            "d_rbc",
            "w_rso",
        )
        for cl in IM_Rotor.__bases__:
            if cl.required_parameters() is not None:
                req_param = req_param + cl.required_parameters()
        return req_param

    def required_materials():
        req_mat = tuple()
        for cl in IM_Rotor.__bases__:
            if cl.required_materials() is not None:
                req_mat = req_mat + cl.required_materials()
        return req_mat

    @property
    def Qr(self):
        return self._machine_parameter_dict["Qr"]


class PM_Rotor(Shaft, Rotor_Iron, PM, MachineComponent):
    @staticmethod
    def required_dimensions():
        req_dims = ("d_mp", "d_ms")
        for cl in PM_Rotor.__bases__:
            if cl.required_dimensions() is not None:
                req_dims = req_dims + cl.required_dimensions()
        return req_dims

    @staticmethod
    def required_parameters():
        req_params = ("p",)
        for cl in PM_Rotor.__bases__:
            if cl.required_parameters() is not None:
                req_params = req_params + cl.required_parameters()
        return req_params

    @staticmethod
    def required_materials():
        req_mat = ("air_mat", "rotor_hub")
        for cl in PM_Rotor.__bases__:
            if cl.required_materials() is not None:
                req_mat = req_mat + cl.required_materials()
        return req_mat

    @property
    def d_mp(self):
        return self._dimensions_dict["d_mp"]

    @property
    def d_ms(self):
        return self._dimensions_dict["d_ms"]

    @property
    def p(self):
        return self._parameters_dict["p"]

    @property
    def air_mat(self):
        return self._materials_dict["air_mat"]

    @property
    def rotor_hub(self):
        return self._materials_dict["rotor_hub"]

    @property
    def r_ro(self):
        r_ro = self.r_sh + self.d_ri + self.d_m
        return r_ro

    @property
    def V_r(self):
        r_ro = self.r_ro
        l_st = self.l_st
        V_r = np.pi * r_ro**2 * l_st
        return V_r

    @property
    def V_rfe(self):
        r_ro = self.r_ro
        alpha_m = self.alpha_m * np.pi / 180
        d_m = self.d_m
        d_mp = self.d_mp
        p = self.p
        l_st = self.l_st
        V_rfe = (
            np.pi * ((r_ro - d_m) ** 2 - self.r_sh**2) * l_st
            + (np.pi - p * alpha_m) * ((r_ro - d_mp) ** 2 - (r_ro - d_m) ** 2) * l_st
        )
        return V_rfe

    @property
    def V_rPM(self):
        r_ro = self.r_ro
        alpha_m = self.alpha_m * np.pi / 180
        d_m = self.d_m
        p = self.p
        l_st = self.l_st
        V_rPM = p * alpha_m * (r_ro**2 - (r_ro - d_m) ** 2) * l_st
        return V_rPM


class PM_Rotor_Sleeved(PM_Rotor, RotorSleeve, MachineComponent):
    @staticmethod
    def required_dimensions():
        req_dims = ("delta_sl",)
        for cl in PM_Rotor_Sleeved.__bases__:
            if cl.required_dimensions() is not None:
                req_dims = req_dims + cl.required_dimensions()
        return req_dims

    @staticmethod
    def required_materials():
        req_mat = tuple()
        for cl in PM_Rotor_Sleeved.__bases__:
            if cl.required_materials() is not None:
                req_mat = req_mat + cl.required_materials()
        return req_mat

    @property
    def delta_sl(self):
        return self._dimensions_dict["delta_sl"]


class Stator(MachineComponent):
    @staticmethod
    def required_dimensions():
        return (
            "alpha_st",  # Stator Tooth Angle
            "d_so",  # Stator
            "w_st",  # Stator Tooth Width
            "d_st",  # Stator Tooth Length
            "d_sy",  # Stator Yoke width
            "alpha_so",  #
            "d_sp",  # Stator Shoe pole thickness
            "r_si",  # Stator Tooth Radius
        )

    @staticmethod
    def required_parameters():
        return ("Q",)

    @staticmethod
    def required_materials():
        return ("stator_iron_mat",)

    @property
    def alpha_st(self):
        return self._dimensions_dict["alpha_st"]

    @property
    def d_so(self):
        return self._dimensions_dict["d_so"]

    @property
    def w_st(self):
        return self._dimensions_dict["w_st"]

    @property
    def d_st(self):
        return self._dimensions_dict["d_st"]

    @property
    def d_sy(self):
        return self._dimensions_dict["d_sy"]

    @property
    def alpha_so(self):
        return self._dimensions_dict["alpha_so"]

    @property
    def d_sp(self):
        return self._dimensions_dict["d_sp"]

    @property
    def r_si(self):
        return self._dimensions_dict["r_si"]

    @property
    def Q(self):
        return self._parameters_dict["Q"]

    @property
    def stator_iron_mat(self):
        return self._materials_dict["stator_iron_mat"]

    @property
    def r_so(self):
        r_so = self.r_si + self.d_sp + self.d_st + self.d_sy
        return r_so

    @property
    def s_slot(self):
        r_si = self.r_si
        d_sp = self.d_sp
        w_st = self.w_st
        d_st = self.d_st
        return (np.pi / self.Q) * (
            (r_si + d_sp + d_st) ** 2 - (r_si + d_sp) ** 2
        ) - w_st * d_st

    @property
    def V_sfe(self):
        V_sfe = (
            np.pi * (self.r_so**2 - self.r_si**2) * self.l_st
            - self.Q * self.s_slot * self.l_st
        )
        return V_sfe

    @property
    def l_coil(self):
        tau_u = (2 * np.pi / self.Q) * (self.r_si + self.d_sp + self.d_st / 2)
        l_ew = np.pi * 0.5 * (tau_u + self.w_st) / 2 + tau_u * self.Kov * (
            self.pitch - 1
        )
        l_coil = 2 * (self.l_st + l_ew)  # length of one coil
        return l_coil

    @property
    def V_scu(self):
        V_scu = self.Q * self.l_coil * self.Kcu * self.s_slot / self.no_of_layers
        return V_scu


class Stator_IM(MachineComponent):
    def required_parameters():
        # return None
        # Add this later
        return (
            "Angle_StatorSlotOpen",  # Stator Tooth Angle
            "Angle_StatorSlotSpan",  # Stator
            "Width_StatorTeethBody",  # Stator Tooth Width
            "Width_StatorTeethHeadThickness",  # Stator Tooth Length
            "Width_StatorTeethNeck",  # Stator Yoke width
            "Radius_InnerStatorYoke",  #
            "Radius_OuterStatorYoke",  # Stator Shoe pole thickness
            "Qs"
            # 'l_st'        , #ADD to MOTOR
        )

    def required_materials():
        return ("stator_iron_mat",)

    @property
    def Angle_StatorSlotOpen(self):
        return self._machine_parameter_dict["Angle_StatorSlotOpen"]

    @property
    def Angle_StatorSlotSpan(self):
        return self._machine_parameter_dict["Angle_StatorSlotSpan"]

    @property
    def Width_StatorTeethBody(self):
        return self._machine_parameter_dict["Width_StatorTeethBody"]

    @property
    def Width_StatorTeethHeadThickness(self):
        return self._machine_parameter_dict["Width_StatorTeethHeadThickness"]

    @property
    def Width_StatorTeethNeck(self):
        return self._machine_parameter_dict["Width_StatorTeethNeck"]

    @property
    def Radius_InnerStatorYoke(self):
        return self._machine_parameter_dict["Radius_InnerStatorYoke"]

    @property
    def Radius_OuterStatorYoke(self):
        return self._machine_parameter_dict["Radius_OuterStatorYoke"]

    @property
    def Qs(self):
        return self._machine_parameter_dict["Qs"]

    @property
    def stator_iron_mat(self):
        return self._materials_dict["stator_iron_mat"]


class DPNVWinding(Winding):
    @staticmethod
    def required_winding():
        req_wind = ("coil_groups",)
        for cl in DPNVWinding.__bases__:
            if cl.required_winding() is not None:
                req_wind = req_wind + cl.required_winding()
        return req_wind

    @staticmethod
    def required_materials():
        return ()

    @property
    def coil_groups(self):
        return self._winding_dict["coil_groups"]


class DPNVWinding_IM(Winding_IM, MachineComponent):
    def required_parameters():
        req_param = (
            "coil_groups",
            "DPNV_or_SEPA",
            "PoleSpecificNeutral",
            "pitch",
            "number_parallel_branch",
            "CommutatingSequenceD",
        )
        for cl in DPNVWinding_IM.__bases__:
            if cl.required_parameters() is not None:
                req_param = req_param + cl.required_parameters()
        return req_param

    def required_materials():
        return ()

    @property
    def coil_groups(self):
        return self._machine_parameter_dict["coil_groups"]

    @property
    def DPNV_or_SEPA(self):
        return self._machine_parameter_dict["DPNV_or_SEPA"]

    @property
    def PoleSpecificNeutral(self):
        return self._machine_parameter_dict["PoleSpecificNeutral"]

    @property
    def pitch(self):
        return self._machine_parameter_dict["pitch"]

    @property
    def number_parallel_branch(self):
        return self._machine_parameter_dict["number_parallel_branch"]

    @property
    def CommutatingSequenceD(self):
        return self._machine_parameter_dict["CommutatingSequenceD"]


class Rotor_Iron_Round_Slots(MachineComponent):
    @staticmethod
    def required_dimensions():
        return (
            "r_ri",  # Rotor inner radius
            "d_ri",  # Rotor back iron length
            "r_rb",  # Rotor bar radius
            "d_rso",  # Rotor tooth height
            "w_so",  # Rotor slot opening
        )

    @staticmethod
    def required_parameters():
        return ("Qr",)

    @staticmethod
    def required_materials():
        return ("rotor_iron_mat",)

    @property
    def r_ri(self):
        return self._dimensions_dict["r_ri"]

    @property
    def d_ri(self):
        return self._dimensions_dict["d_ri"]

    @property
    def r_rb(self):
        return self._dimensions_dict["r_rb"]

    @property
    def d_rso(self):
        return self._dimensions_dict["d_rso"]

    @property
    def w_so(self):
        return self._dimensions_dict["w_so"]

    @property
    def Qr(self):
        return self._parameters_dict["Qr"]

    @property
    def rotor_iron_mat(self):
        return self._materials_dict["rotor_iron_mat"]

    @property
    def r_ro(self):
        alpha_u = 2 * np.pi / self.Qr
        r1 = self.r_ri + self.d_ri + self.r_rb + np.sqrt(self.r_rb ** 2 - (self.w_so / 2) ** 2) + self.d_so
        r2 = self.w_so / 2
        r_ro = np.sqrt(r1 ** 2 + r2 ** 2)
        return r_ro

    @property
    def V_rfe(self):
        V_rfe = self.l_st * (
            np.pi * (self.r_ro ** 2 - self.r_ri ** 2) - 
            self.Qr * (np.pi * self.r_rb ** 2 + self.w_so * self.d_rso)
        )
        return V_rfe


class Rotor_Iron_Round_Slots_Bar(MachineComponent):
    @staticmethod
    def required_dimensions():
        return (
            "r_rb", # Rotor bar radius
        )

    @staticmethod
    def required_materials():
        return ("rotor_bar_mat",)

    @property
    def r_rb(self):
        return self._machine_parameter_dict["r_rb"]

    @property
    def rotor_bar_mat(self):
        return self._materials_dict["rotor_bar_mat"]


class IM_Rotor_Round_Slots(Rotor_Iron_Round_Slots, Rotor_Iron_Round_Slots_Bar, Shaft, MachineComponent):
    @staticmethod
    def required_dimensions():
        req_dims = ()
        for cl in IM_Rotor_Round_Slots.__bases__:
            if cl.required_dimensions() is not None:
                req_dims = req_dims + cl.required_dimensions()
        return req_dims

    @staticmethod
    def required_materials():
        req_mat = tuple()
        for cl in IM_Rotor_Round_Slots.__bases__:
            if cl.required_materials() is not None:
                req_mat = req_mat + cl.required_materials()
        return req_mat

    @staticmethod
    def required_winding():
        return (
            "no_of_phases_rotor",
            "no_of_layers_rotor",
            "layer_phases_rotor",
            "layer_polarity_rotor",
            "Z_q_rotor",
            "Kov_rotor"
        )

    @property
    def name_phases_rotor(self):
        return self._winding_dict["name_phases_rotor"]

    @property
    def no_of_phases_rotor(self):
        return self._winding_dict["no_of_phases_rotor"]

    @property
    def no_of_layers_rotor(self):
        return self._winding_dict["no_of_layers_rotor"]

    @property
    def layer_phases_rotor(self):
        return self._winding_dict["layer_phases_rotor"]

    @property
    def layer_polarity_rotor(self):
        return self._winding_dict["layer_polarity_rotor"]

    @property
    def Z_q_rotor(self):
        return self._winding_dict["Z_q_rotor"]

    @property
    def Kov_rotor(self):
        return self._winding_dict["Kov_rotor"]




class MPWinding(Winding):
    @staticmethod
    def required_winding():
        req_wind = ("no_of_phases",)
        for cl in MPWinding.__bases__:
            if cl.required_winding() is not None:
                req_wind = req_wind + cl.required_winding()
        return req_wind

    @staticmethod
    def required_materials():
        return ()

    @property
    def no_of_phases(self):
        return self._winding_dict["no_of_phases"]

    @property
    def name_phases(self):
        return self._winding_dict["name_phases"]