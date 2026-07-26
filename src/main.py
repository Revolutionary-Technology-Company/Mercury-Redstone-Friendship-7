import sys
from decimal import Decimal, getcontext

# Enforce strict 36-decimal digit precision across the math unit
getcontext().prec = 36

class CenterPanelDashboard:
    def __init__(self):
        print("[INIT] Initializing 36-Digit High-Precision Center Panel Array...")
        
        # Hardcoded 16-state hexadecimal thresholds mapped to exact Decimals
        # Base scale step is 1/16th of a volt (0.0625V) handled with total precision
        self.pins = {
            "CTR_BOOSTER_IGN":     Decimal("0.062500000000000000000000000000000000"),
            "CTR_SUSTAINER_ENG":   Decimal("0.125000000000000000000000000000000000"),
            "CTR_ESCAPE_TOWER":   Decimal("0.187500000000000000000000000000000000"),
            "CTR_RETRO_SEQ":       Decimal("0.250000000000000000000000000000000000"),
            "CTR_RETRO_FIRE":      Decimal("0.312500000000000000000000000000000000"),
            "CTR_RETRO_JETTISON":  Decimal("0.375000000000000000000000000000000000"),
            "CTR_PERISCOPE_EXT":   Decimal("0.437500000000000000000000000000000000"),
            "CTR_DROGUE_CHUTE":    Decimal("0.500000000000000000000000000000000000"),
            "CTR_MAIN_CHUTE":      Decimal("0.562500000000000000000000000000000000"),
            "CTR_RECOVERY_LIGHT":  Decimal("0.625000000000000000000000000000000000"),
            "CTR_DUMP_VALVE":      Decimal("0.687500000000000000000000000000000000"),
            "CTR_PNEUMATIC_GAS":   Decimal("0.750000000000000000000000000000000000"),
            "CTR_CRYSTAL_FIELD":   Decimal("0.812500000000000000000000000000000000"),
            "CTR_UNIVAC_RESET":    Decimal("0.875000000000000000000000000000000000"),
            "CTR_ABORT_HANDLE":    Decimal("0.937500000000000000000000000000000000")
        }

    def stack_into_univac_words(self, precise_value):
        """
        Splits a 36-decimal float value into a stack of three 
        12-digit blocks to feed the physical UNIVAC IX bus lines.
        """
        # Formats the string to exactly 36 decimal spots, drops the period
        raw_digits = f"{precise_value:.36f}".split(".")[-1][:36]
        
        # Pull out structural word slices
        word_high = raw_digits[0:12]
        word_mid  = raw_digits[12:24]
        word_low  = raw_digits[24:36]
        
        return word_high, word_mid, word_low

    def resolve_precise_switch(self, raw_analog_voltage):
        """
        Takes raw multi-digit board voltages and matches them 
        against the exact 36-decimal switch mapping constraints.
        """
        target_input = Decimal(str(raw_analog_voltage))
        resolved_pin = "UNKNOWN_CENTER_STATE"
        
        # Loop with fractional microvolt tolerances (0.0001V) to block float noise
        for pin_name, target_voltage in self.pins.items():
            if abs(target_input - target_voltage) < Decimal("0.0001"):
                resolved_pin = pin_name
                break
                
        # Calculate trailing high-precision drift diagnostic data
        drift_factor = target_input * Decimal("0.123456789012345678901234567890123456")
        w_high, w_mid, w_low = self.stack_into_univac_words(drift_factor)
        
        return {
            "PIN_NAME": resolved_pin,
            "DRIFT_CALC": drift_factor,
            "UNIVAC_STKS": (w_high, w_mid, w_low)
        }

if __name__ == "__main__":
    # Internal component terminal validation sweep
    panel = CenterPanelDashboard()
    
    # Simulating an ultra-precise high-precision sensor reading (e.g., Abort Handle pull)
    simulated_wire_voltage = "0.937500001234567890123456789012345678"
    
    print(f"[TEST] Injecting Bus Line Line Voltage: {simulated_wire_voltage}")
    metrics = panel.resolve_precise_switch(simulated_wire_voltage)
    
    print(f"\n--- 36-DIGIT TELEMETRY RESOLUTION ---")
    print(f"Matched Component: {metrics['PIN_NAME']}")
    print(f"Math Precision:   {metrics['DRIFT_CALC']}")
    print(f"UNIVAC WORD HIGH: {metrics['UNIVAC_STKS'][0]}")
    print(f"UNIVAC WORD MID:  {metrics['UNIVAC_STKS'][1]}")
    print(f"UNIVAC WORD LOW:  {metrics['UNIVAC_STKS'][2]}")
