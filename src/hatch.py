import sys
from decimal import Decimal, getcontext

# Enforce strict 36-decimal digit precision across the safety loop
getcontext().prec = 36

class Friendship7HatchController:
    def __init__(self):
        print("[INIT] Initializing 36-Digit High-Precision Capsule Hatch Sequencer...")
        
        # Exact electronic latch status coefficients
        self.pressure_equilibrium_k = Decimal("1.000000000000000000000000000000000000")
        self.latch_engage_voltage   = Decimal("0.937500000000000000000000000000000000") # Hex F matching Master Arm

    def split_hatch_digits(self, internal_decimal):
        """Splits the lock alignment metric into three standard 12-digit UNIVAC registers."""
        raw_digits = f"{internal_decimal:.36f}".split(".")[-1][:36]
        return raw_digits[0:12], raw_digits[12:24], raw_digits[24:36]

    def verify_and_actuate_hatch(self, cabin_pressure, master_arm_v, manual_plunger_throw):
        """
        Safety interlock loop: Validates that pressure is equalized and master arm 
        is hot before triggering the door actuators.
        """
        press_val   = Decimal(str(cabin_pressure))
        arm_v       = Decimal(str(master_arm_v))
        plunger_v   = Decimal(str(manual_plunger_throw))
        
        # 36-Digit cross-multiplication matrix to check door seal drift
        structural_alignment = (press_val * arm_v) + (plunger_v * Decimal("0.012345678901234567890123456789012345"))
        h_high, h_mid, h_low = self.split_hatch_digits(structural_alignment)
        
        # Enforcing mechanical logic constraints before updating solenoids
        if press_val != self.pressure_equilibrium_k:
            return {
                "HATCH_STATUS": "LOCKED_LATCH_PRESSURE_WARNING",
                "ACTUATOR_RELAY": False,
                "UNIVAC_WORDS": (h_high, h_mid, h_low)
            }
            
        if arm_v >= self.latch_engage_voltage and plunger_v > Decimal("0.50"):
            return {
                "HATCH_STATUS": "ACTUATING_EXPLOSIVE_HATCH_EMERGENCY_RELEASE",
                "ACTUATOR_RELAY": True,
                "UNIVAC_WORDS": (h_high, h_mid, h_low)
            }
            
        return {
            "HATCH_STATUS": "SECURED_FLIGHT_READY",
            "ACTUATOR_RELAY": False,
            "UNIVAC_WORDS": (h_high, h_mid, h_low)
        }

if __name__ == "__main__":
    # Internal component terminal verification run
    controller = Friendship7HatchController()
    
    # Simulation 1: Blocked door trigger due to atmospheric pressure lock
    print("\n--- TEST RUN 1: RUNNING FLIGHT PRESSURE VERIFICATION ---")
    fail_report = controller.verify_and_actuate_hatch("0.102394857123", "0.937500000000", "0.937500000000")
    print(f"Action Code:   {fail_report['HATCH_STATUS']}")
    print(f"Solenoid Fire: {fail_report['ACTUATOR_RELAY']}")
    print(f"Hatch Memory:  {fail_report['UNIVAC_WORDS']}")
    
    # Simulation 2: Successful lock release on the pad (pressure equalized at 1.0)
    print("\n--- TEST RUN 2: EQUALIZED PAD ESCAPE RELEASE TRIGGER ---")
    pass_report = controller.verify_and_actuate_hatch("1.000000000000", "0.937500000000", "0.937500000000")
    print(f"Action Code:   {pass_report['HATCH_STATUS']}")
    print(f"Solenoid Fire: {pass_report['ACTUATOR_RELAY']}")
    print(f"Hatch Memory:  {pass_report['UNIVAC_WORDS']}")
