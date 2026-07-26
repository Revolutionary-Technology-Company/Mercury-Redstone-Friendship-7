class RightPanelSwitchboard:
    def __init__(self):
        self.pins = {
            "R_ASCS_MONITOR": 0.0625,# Hex 1
            "R_MANUAL_OVER": 0.125,  # Hex 2
            "R_AUX_THRUSTER": 0.1875,# Hex 3
            "R_PITCH_MONITOR": 0.25,  # Hex 4
            "R_ROLL_MONITOR": 0.3125, # Hex 5
            "R_ANIMAL_PRESS": 0.375,  # Hex 6
            "R_CHAMBER_FAN_1": 0.4375,# Hex 7
            "R_CHAMBER_FAN_2": 0.50,  # Hex 8
            "R_SECONDARY_O2": 0.5625, # Hex 9
            "R_ANIMAL_O2_EMER": 0.625,# Hex A
            "R_DATA_RECORDER": 0.6875,# Hex B
            "R_UHF_SQUELCH": 0.75,    # Hex C
            "R_AUDIO_MONITOR": 0.8125,# Hex D
            "R_ORBIT_RECOVERY": 0.875,# Hex E
            "R_CABIN_ARM": 0.9375     # Hex F
        }

    def read_right_matrix(self, line_voltage):
        for switch_name, target_voltage in self.pins.items():
            if abs(line_voltage - target_voltage) < 0.03:
                return switch_name
        return "UNKNOWN_RIGHT_STATE"
