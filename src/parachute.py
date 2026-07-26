import time

class ParachuteRecoveryController:
    def __init__(self):
        self.para_cntl_mode = "AUTO"
        self.attitude_indicator_mode = "WITH_F_DI" # Default with Flight Director
        self.drogue_deployed = False
        self.main_deployed = False

    def set_parachute_control(self, switch_state):
        """
        Processes the PARA CNTL toggle.
        Allows manual structural deployment overrides if automatic barometric altimeters lock up.
        """
        if switch_state == "UP":
            self.para_cntl_mode = "MANUAL_OVERRIDE"
            print("[RECOVERY] PARA CNTL -> UP. Automatic barometric triggers bypassed.")
            self.execute_emergency_chute_deploy()
        elif switch_state == "DOWN":
            self.para_cntl_mode = "AUTO"
            print("[RECOVERY] PARA CNTL -> DOWN. Standard barometric tracking loops active.")

    def set_attitude_indicator_source(self, switch_state):
        """
        Processes the ATT IND (Attitude Indicator) selector.
        Determines if entry tracking displays use the Flight Director (F DI) cross-pointers.
        """
        if switch_state == "UP":
            self.attitude_indicator_mode = "WITH_F_DI"
            print("[DISPLAY] ATT IND -> UP. Horizon display synchronized WITH Flight Director.")
        elif switch_state == "DOWN":
            self.attitude_indicator_mode = "W_O_F_DI"
            print("[DISPLAY] ATT IND -> DOWN. Horizon display running WITHOUT Flight Director.")

    def execute_emergency_chute_deploy(self):
        """Simulates rapid manual mechanical line deployments during terminal descent phase."""
        if not self.drogue_deployed:
            self.drogue_deployed = True
            print("[MECHANICAL] Mortar fired: Drogue stabilization chute deployed at terminal velocity.")
            print("[INDICATOR STATUS] ---> **PARA CNTL LIGHT: AMBER**")
        elif self.drogue_deployed and not self.main_deployed:
            self.main_deployed = True
            print("[MECHANICAL] Snatch cords blown: Main landing canopy fully deployed.")
            print("[INDICATOR STATUS] ---> **PARA CNTL LIGHT: GREEN**")

if __name__ == "__main__":
    recovery = ParachuteRecoveryController()
    print("--- Simulating Terminal Low-Altitude Descent ---")
    recovery.set_parachute_control("UP")  # Trigger step 1: Drogue
    recovery.set_parachute_control("UP")  # Trigger step 2: Main canopy
