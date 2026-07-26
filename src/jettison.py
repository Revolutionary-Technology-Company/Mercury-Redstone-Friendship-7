import time

class NoseTowerJettisonController:
    def __init__(self):
        # Hardware Interlock States
        self.jettison_executed = False
        self.explosive_bolts_fired = False

    def process_jett_switch_toggle(self, switch_state, escape_burn_completed=False, safety_override=False):
        """
        Processes inputs from the physical JETT switch on the center panel.
        Ensures the tower is not discarded prematurely unless an escape burn has finished
        or a ground-command manual safety override is active.
        """
        if self.jettison_executed:
            print("[JETT CONTROL] Nose tower frame has already separated. Circuit open.")
            return {"JETT_LIGHT": "OFF", "TOWER_ATTACHED": False}

        if switch_state == "UP":
            print("\n[COCKPIT INPUT] JETT switch toggled UP. Evaluating hardware interlocks...")
            
            # Verify flight dynamics environment before executing mechanical detachment
            if escape_burn_completed or safety_override:
                self.execute_tower_separation()
                return {"JETT_LIGHT": "ON", "TOWER_ATTACHED": False}
            else:
                print("[INTERLOCK BLOCKED] Structural danger: Acceleration/Atmospheric loads unstable.")
                print("[INTERLOCK BLOCKED] Cannot jettison nose tower during active launch/escape tracking.")
                return {"JETT_LIGHT": "OFF", "TOWER_ATTACHED": True}
                
        elif switch_state == "DOWN":
            print("[JETT CONTROL] JETT switch set to neutral/down. Monitoring structural stress lines.")
            return {"JETT_LIGHT": "OFF", "TOWER_ATTACHED": not self.jettison_executed}

    def execute_tower_separation(self):
        """Executes the high-voltage explosive charge sequence to push the tower away."""
        print("\n[SEPARATION PROTOCOL] ---> ENERGIZING CAPACITOR BANKS <---")
        self.explosive_bolts_fired = True
        self.jettison_executed = True
        
        # Flash the dashboard status lights to reflect mechanical configuration change
        print("[INDICATOR STATUS] ---> **JETT LIGHT: FLASHING AMBER** (Severance Initiated)")
        print("[MECHANICAL] Firing pneumatic thrusters and explosive severance bolts...")
        print("[MECHANICAL] Nose tower frame successfully pushed away from capsule envelope.")
        print("[INDICATOR STATUS] ---> **JETT LIGHT: SOLID GREEN** (Tower Clear / Drogue Path Open)")

# Simulation pipeline showing both blocked and verified manual jettison paths
if __name__ == "__main__":
    controller = NoseTowerJettisonController()
    
    print("--- Scenario A: Attempting Premature Tower Jettison ---")
    # Pilot tries to hit the switch before the defensive system finishes its duties
    status = controller.process_jett_switch_toggle(switch_state="UP", escape_burn_completed=False)
    
    print("\n--- Scenario B: Safe Post-Escape Burn Jettison Sequence ---")
    # The evasive maneuver finishes, clearing the lethal zone
    escape_burn_status = True 
    
    # Pilot hits the JETT switch to discard the dead structural weight
    status = controller.process_jett_switch_toggle(switch_state="UP", escape_burn_completed=escape_burn_status)
