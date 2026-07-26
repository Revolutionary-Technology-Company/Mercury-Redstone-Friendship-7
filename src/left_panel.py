class LeftPanelSwitchboard:
    def __init__(self):
        # 16-State Hexadecimal Native Voltage steps (0.0625V per interval)
        self.pins = {
            "L_ASCS_AUTO": 0.0625,  # Hex 1
            "L_MANUAL_PROPR": 0.125, # Hex 2
            "L_YAW_THRUSTER": 0.1875,# Hex 3
            "L_PITCH_COMMAND": 0.25, # Hex 4
            "L_ROLL_COMMAND": 0.3125,# Hex 5
            "L_CABIN_PRESS": 0.375,  # Hex 6
            "L_SUIT_FAN_1": 0.4375,  # Hex 7
            "L_SUIT_FAN_2": 0.50,    # Hex 8
            "L_O2_PRIMARY": 0.5625,  # Hex 9
            "L_O2_EMERGENCY": 0.625, # Hex A
            "L_TELEMETRY_TX": 0.6875,# Hex B
            "L_BEACON_MODE": 0.75,   # Hex C
            "L_AUDIO_INTER": 0.8125, # Hex D
            "L_EARTH_PATH_CAL": 0.875,# Hex E
            "L_MASTER_ARM": 0.9375   # Hex F
        }

    def read_left_matrix(self, line_voltage):
        for switch_name, target_voltage in self.pins.items():
            if abs(line_voltage - target_voltage) < 0.03:
                return switch_name
        return "UNKNOWN_LEFT_STATE"
