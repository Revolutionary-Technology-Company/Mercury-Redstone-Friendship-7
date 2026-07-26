import time

class RetroDescentSequenceController:
    def __init__(self):
        # Tracking states for the primary descent stages
        self.retro_seq_1_ready = False
        self.retro_seq_2_ready = False
        self.retro_pwr_active = False
        self.capsule_separated = False

    def process_retro_pwr(self, switch_state):
        """Processes the main RETRO PWR safety toggle on the bottom row."""
        if switch_state == "UP":
            self.retro_pwr_active = True
            print("[RETRO BUS] RETRO PWR -> ON. Emergency separation circuits energized.")
        elif switch_state == "DOWN":
            self.retro_pwr_active = False
            print("[RETRO BUS] RETRO PWR -> OFF. Descent sequence systems isolated.")

    def process_retro_seq_toggles(self, switch_id, switch_state):
        """
        Processes inputs for RETRO SEQ 1 and RETRO SEQ 2 manually.
        Allows manual staging logic if the automated orbit decay clocks falter.
        """
        if not self.retro_pwr_active:
            print(f"[STAGE BLOCKED] Cannot cycle RETRO SEQ {switch_id}. Main RETRO PWR is SAFE.")
            return False

        if switch_id == 1 and switch_state == "UP":
            self.retro_seq_1_ready = True
            print("[RETRO STAGE 1] Manual interlock cleared. Pitch/Yaw stabilization locked for entry.")
        elif switch_id == 2 and switch_state == "UP":
            if self.retro_seq_1_ready:
                self.retro_seq_2_ready = True
                print("[RETRO STAGE 2] Manual interlock cleared. Entry timeline calculation initialized.")
            else:
                print("[STAGE ERR] Invalid sequence order. Step 1 must be active prior to Step 2.")
                return False
        return True

    def trigger_manual_separation(self, jett_switch_state):
        """Processes manual separation of the retrograde package frame from the capsule base."""
        if not self.retro_pwr_active or not self.retro_seq_2_ready:
            print("[JETT BLOCKED] Mechanical safety locks active. Retros must finish burning.")
            return False

        if jett_switch_state == "UP":
            self.capsule_separated = True
            print("\n[RETRO STAGING] ---> RETROGRADE PACKAGE JETTISONED <---")
            print("[INDICATOR STATUS] ---> **RETRO COUPLING LIGHTS: OFF**")
            print("[MECHANICAL] Retaining straps severed. Heat shield clear for entry interface.")
            return True
        return False

if __name__ == "__main__":
    controller = RetroDescentSequenceController()
    print("--- Simulating Manual Emergency Entry Configuration ---")
    # 1. Flip main power line on
    controller.process_retro_pwr("UP")
    # 2. Cycle sequence steps manually
    controller.process_retro_seq_toggles(switch_id=1, switch_state="UP")
    controller.process_retro_seq_toggles(switch_id=2, switch_state="UP")
    # 3. Discard the spent engine block assembly
    controller.trigger_manual_separation(jett_switch_state="UP")
