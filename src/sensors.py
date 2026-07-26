import sys
import time
import math
from decimal import Decimal, getcontext

# Standardize context execution rules to exactly 36 positions
getcontext().prec = 36


class ModernVectorEngine:
    def __init__(self):
        # Simulated orbital sensor buffer matching current altitude profiles
        self.scanned_vectors = [
            {"id": 0, "type": "HUMAN_DOCKING", "shape": "RECTANGLE", "dimensions": (4.0, 4.0), "range": 1200, "velocity": 240},
            {"id": 1, "type": "CYLINDER_PROFILE", "shape": "TUBE", "dimensions": (12.5, 1.8), "range": 3400, "velocity": 850},
            {"id": 2, "type": "HUMAN_STRUCT", "shape": "SQUARE", "dimensions": (2.5, 2.5), "range": 800, "velocity": 110},
            {"id": 3, "type": "CYLINDER_PROFILE", "shape": "TUBE", "dimensions": (18.2, 2.1), "range": 5100, "velocity": 1200}
        ]
        self.active_index = 0
        self.filtered_targets = []
        self.apply_geometric_filters()

    def apply_geometric_filters(self):
        """Filters out friendly square/rectangular docking structures using aspect ratios."""
        self.filtered_targets = []
        for target in self.scanned_vectors:
            length, width = target["dimensions"]
            aspect_ratio = length / width
            
            # If the shape is close to a 1:1 ratio, it's flagged as a friendly docking hub
            if math.isclose(aspect_ratio, 1.0, rel_tol=0.1):
                print(f"[FILTER] Vector {target['id']}: Friendly human docking square detected. Suppressing track.")
                continue
            
            # Tube shapes generate high Maxwell force whine profiles as altitude scales
            if target["shape"] == "TUBE" and aspect_ratio > 3.0:
                print(f"[TRACKING] Vector {target['id']}: Cylindrical tube signature locked. Phase whine active.")
                self.filtered_targets.append(target)

    def process_landing_seq_toggle(self, switch_state):
        """
        Executes target cycling based on the physical LANDING SEQ 1 toggle behavior.
        Flipping UP cycles vectors until the CNTL light turns ON and PWR drops OFF.
        """
        if not self.filtered_targets:
            print("[SYSTEM] No valid target signatures found in active vector space.")
            return {"CNTL_LIGHT": "OFF", "PWR_LIGHT": "ON", "target": None}

        if switch_state == "UP":
            # Cycle to the next target index within the verified tube list
            self.active_index = (self.active_index + 1) % len(self.filtered_targets)
            selected = self.filtered_targets[self.active_index]
            
            print(f"\n[STEP INDEX] LANDING SEQ 1 flipped UP. Cycling to index {self.active_index}...")
            print(f"[LIGHT STATUS] ---> **SEQ LIGHTS CNTL: ON** | **SEQ LIGHTS PWR: OFF**")
            print(f"[LOCK ACQUIRED] Vector ID {selected['id']} ({selected['shape']}) selected at Range {selected['range']}m.")
            
            return {
                "CNTL_LIGHT": "ON",
                "PWR_LIGHT": "OFF",
                "target": selected
            }
        
        elif switch_state == "DOWN":
            # Pilot snaps the switch back immediately to confirm the track
            confirmed_target = self.filtered_targets[self.active_index]
            print(f"[EXECUTION] LANDING SEQ 1 toggled immediately back to OFF. Lock confirmed on Target ID {confirmed_target['id']}.")
            return {"CNTL_LIGHT": "OFF", "PWR_LIGHT": "ON", "target": confirmed_target}

class Friendship7SensorArray:
    def __init__(self):
        print("[INIT] Initializing 36-Digit High-Precision Cockpit Sensor Array...")
        
        # Exact calibration coefficients for physical environmental thermistors
        self.pilot_cabin_oxy_coeff = Decimal("0.209463829102485736192847561029384756")
        self.animal_cabin_oxy_coeff = Decimal("0.209461110029384756102938475610293847")
        self.hull_thermal_scaler    = Decimal("1.800000000000000000000000000000000000")

    def stack_sensor_digits(self, computed_decimal):
        """Packs a 36-decimal sensor factor calculation into three standard UNIVAC registers."""
        raw_digits = f"{computed_decimal:.36f}".split(".")[-1][:36]
        return raw_digits[0:12], raw_digits[12:24], raw_digits[24:36]

    def monitor_cabin_environment(self, raw_analog_voltage_l, raw_analog_voltage_r):
        """
        Parses fine sensor telemetry voltages to capture atmospheric stability 
        inside both cabin seats simultaneously.
        """
        v_left  = Decimal(str(raw_analog_voltage_l))
        v_right = Decimal(str(raw_analog_voltage_r))
        
        # Ultra-precise oxygen and environmental compound computations
        calc_pilot_o2  = v_left * self.pilot_cabin_oxy_coeff
        calc_animal_o2 = v_right * self.animal_cabin_oxy_coeff
        
        p_high, p_mid, p_low = self.stack_sensor_digits(calc_pilot_o2)
        a_high, a_mid, a_low = self.stack_sensor_digits(calc_animal_o2)
        
        return {
            "PILOT_O2_LEVEL": calc_pilot_o2,
            "PILOT_WORDS": (p_high, p_mid, p_low),
            "ANIMAL_O2_LEVEL": calc_animal_o2,
            "ANIMAL_WORDS": (a_high, a_mid, a_low)
        }

if __name__ == "__main__":
    # Self-test block for diagnostic trace verification
    sensors = Friendship7SensorArray()
    
    # Injecting test voltages from the dual environmental line connections
    pilot_line_v  = "0.784512394857"
    animal_line_v = "0.784210029384"
    
    report = sensors.monitor_cabin_environment(pilot_line_v, animal_line_v)
    
    print("\n--- ENVIRONMENTAL TELEMETRY SCAN RANGE ---")
    print(f"Pilot Seat O2 Value:  {report['PILOT_O2_LEVEL']}")
    print(f" -> Packed Registers: High: {report['PILOT_WORDS'][0]} | Mid: {report['PILOT_WORDS'][1]} | Low: {report['PILOT_WORDS'][2]}")
    print(f"Animal Seat O2 Value: {report['ANIMAL_O2_LEVEL']}")
    print(f" -> Packed Registers: High: {report['ANIMAL_WORDS'][0]} | Mid: {report['ANIMAL_WORDS'][1]} | Low: {report['ANIMAL_WORDS'][2]}")

    engine = ModernVectorEngine()
    
    print("\n--- Initiating Cockpit Step Selection Loop ---")
    # Step 1: Pilot flips LANDING SEQ 1 UP to advance the target list
    telemetry_state = engine.process_landing_seq_toggle("UP")
    
    # Step 2: System satisfies indicators (CNTL ON, PWR OFF). Pilot immediately reverts the toggle down
    time.sleep(0.5)
    if telemetry_state["CNTL_LIGHT"] == "ON" and telemetry_state["PWR_LIGHT"] == "OFF":
        engine.process_landing_seq_toggle("DOWN")
