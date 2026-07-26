import sys
from decimal import Decimal, getcontext

"""Enforce strict 36-decimal digit precision across the math unit"""
getcontext().prec = 36

class RightPanelSwitchboard:
    def __init__(self):
        print("[INIT] Initializing 36-Digit High-Precision Right Panel Array...")
        
       """16-state hexadecimal thresholds mapped to exact 36-digit Decimals (Co-Pilot/Animal Cabin)"""
        self.pins = {
            "R_ASCS_MONITOR":    Decimal("0.062500000000000000000000000000000000"),
            "R_MANUAL_OVER":     Decimal("0.125000000000000000000000000000000000"),
            "R_AUX_THRUSTER":    Decimal("0.187500000000000000000000000000000000"),
            "R_PITCH_MONITOR":   Decimal("0.250000000000000000000000000000000000"),
            "R_ROLL_MONITOR":    Decimal("0.312500000000000000000000000000000000"),
            "R_ANIMAL_PRESS":    Decimal("0.375000000000000000000000000000000000"),
            "R_CHAMBER_FAN_1":   Decimal("0.437500000000000000000000000000000000"),
            "R_CHAMBER_FAN_2":   Decimal("0.500000000000000000000000000000000000"),
            "R_SECONDARY_O2":    Decimal("0.562500000000000000000000000000000000"),
            "R_ANIMAL_O2_EMER":  Decimal("0.625000000000000000000000000000000000"),
            "R_DATA_RECORDER":   Decimal("0.687500000000000000000000000000000000"),
            "R_UHF_SQUELCH":     Decimal("0.750000000000000000000000000000000000"),
            "R_AUDIO_MONITOR":   Decimal("0.812500000000000000000000000000000000"),
            "R_ORBIT_RECOVERY":  Decimal("0.875000000000000000000000000000000000"),
            "R_CABIN_ARM":       Decimal("0.937500000000000000000000000000000000")
        }

    def stack_into_univac_words(self, precise_value):
        """Splits a 36-decimal calculation into three 12-digit UNIVAC memory registers."""
        raw_digits = f"{precise_value:.36f}".split(".")[-1][:36]
        return raw_digits[0:12], raw_digits[12:24], raw_digits[24:36]

    def resolve_precise_switch(self, raw_analog_voltage):
        """Matches fine board input voltages against exact Right Panel switch lines."""
        target_input = Decimal(str(raw_analog_voltage))
        resolved_pin = "UNKNOWN_RIGHT_STATE"
        
        for pin_name, target_voltage in self.pins.items():
            if abs(target_input - target_voltage) < Decimal("0.0001"):
                resolved_pin = pin_name
                break
                
       """Calculate dynamic right-side status indicators"""
        drift_factor = target_input * Decimal("0.555555555555555555555555555555555555")
        w_high, w_mid, w_low = self.stack_into_univac_words(drift_factor)
        
        return {
            "PIN_NAME": resolved_pin,
            "DRIFT_CALC": drift_factor,
            "UNIVAC_STKS": (w_high, w_mid, w_low)
        }
