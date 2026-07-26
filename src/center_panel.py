class CenterPanelDashboard:
    def __init__(self):
        self.pins = {
            "CTR_BOOSTER_IGN": 0.0625, # Hex 1
            "CTR_SUSTAINER_ENG": 0.125,# Hex 2
            "CTR_ESCAPE_TOWER": 0.1875,# Hex 3
            "CTR_RETRO_SEQ": 0.25,     # Hex 4
            "CTR_RETRO_FIRE": 0.3125,  # Hex 5
            "CTR_RETRO_JETTISON": 0.375,# Hex 6
            "CTR_PERISCOPE_EXT": 0.4375,# Hex 7
            "CTR_DROGUE_CHUTE": 0.50,  # Hex 8
            "CTR_MAIN_CHUTE": 0.5625,  # Hex 9
            "CTR_RECOVERY_LIGHT": 0.625,# Hex A
            "CTR_DUMP_VALVE": 0.6875,  # Hex B
            "CTR_PNEUMATIC_GAS": 0.75, # Hex C
            "CTR_CRYSTAL_FIELD": 0.8125,# Hex D
            "CTR_UNIVAC_RESET": 0.875, # Hex E
            "CTR_ABORT_HANDLE": 0.9375 # Hex F
        }

    def read_center_matrix(self, line_voltage):
        for switch_name, target_voltage in self.pins.items():
            if abs(line_voltage - target_voltage) < 0.03:
                return switch_name
        return "UNKNOWN_CENTER_STATE"
