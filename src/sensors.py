import sys
from decimal import Decimal, getcontext

# Standardize context execution rules to exactly 36 positions
getcontext().prec = 36

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
