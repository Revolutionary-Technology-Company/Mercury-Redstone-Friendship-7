import time

class BoostInsertionController:
    def __init__(self):
        self.boost_insert_1_latch = False
        self.boost_insert_2_latch = False
        self.power_rail_energized = False
        self.orbital_insertion_verified = False

    def set_boost_pwr_rail(self, switch_state):
        """Controls primary voltage distribution lines for orbital cutoff telemetry."""
        if switch_state == "UP":
            self.power_rail_energized = True
            print("[BOOST BUS] BOOST INSERT PWR -> ON. Cutoff sensor matrix live.")
        else:
            self.power_rail_energized = False
            print("[BOOST BUS] BOOST INSERT PWR -> SAFE. Isolation circuit active.")

    def evaluate_insertion_toggles(self, switch_id, switch_state):
        """
        Processes manual verification lines for stage cut-off events.
        Confirms velocity vectors before matching tracking nodes can close.
        """
        if not self.power_rail_energized:
            print(f"[BOOST ERR] Cannot toggle BOOST INSERT {switch_id}. Power rail is offline.")
            return False

        if switch_id == 1 and switch_state == "UP":
            self.boost_insert_1_latch = True
            print("[BOOST TRACK] Node 1 latched. Velocity curves within safe structural window.")
        elif switch_id == 2 and switch_state == "UP":
            self.boost_insert_2_latch = True
            print("[BOOST TRACK] Node 2 latched. Radial positioning vectors locked.")

        if self.boost_insert_1_latch and self.boost_insert_2_latch:
            self.orbital_insertion_verified = True
            print("\n[BOOST TRACK] ---> OPTIMAL ORBITAL INSERTION CONFIRMED <---")
            print("[INDICATOR STATUS] ---> **BOOST INSERT STATUS LIGHT: GREEN**")
        
        return True

if __name__ == "__main__":
    booster = BoostInsertionController()
    print("--- Simulating Ascent and Cutoff Stages ---")
    booster.set_boost_pwr_rail("UP")
    booster.evaluate_insertion_toggles(switch_id=1, switch_state="UP")
    booster.evaluate_insertion_toggles(switch_id=2, switch_state="UP")
