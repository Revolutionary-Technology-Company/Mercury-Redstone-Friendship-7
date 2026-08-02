import sys
import socket
import json
import time
from decimal import Decimal, getcontext

"""Enforce strict 36-decimal digit precision across the math unit"""
getcontext().prec = 36

class LeftPanelSwitchboard:
    def __init__(self):
        print("[INIT] Initializing 36-Digit High-Precision Left Panel Array...")
        
       """16-state hexadecimal thresholds mapped to exact 36-digit Decimals"""
        self.pins = {
            "L_ASCS_AUTO":      Decimal("0.062500000000000000000000000000000000"),
            "L_MANUAL_PROPR":   Decimal("0.125000000000000000000000000000000000"),
            "L_YAW_THRUSTER":   Decimal("0.187500000000000000000000000000000000"),
            "L_PITCH_COMMAND":  Decimal("0.250000000000000000000000000000000000"),
            "L_ROLL_COMMAND":   Decimal("0.312500000000000000000000000000000000"),
            "L_CABIN_PRESS":    Decimal("0.375000000000000000000000000000000000"),
            "L_SUIT_FAN_1":     Decimal("0.437500000000000000000000000000000000"),
            "L_SUIT_FAN_2":     Decimal("0.500000000000000000000000000000000000"),
            "L_O2_PRIMARY":     Decimal("0.562500000000000000000000000000000000"),
            "L_O2_EMERGENCY":   Decimal("0.625000000000000000000000000000000000"),
            "L_TELEMETRY_TX":   Decimal("0.687500000000000000000000000000000000"),
            "L_BEACON_MODE":    Decimal("0.750000000000000000000000000000000000"),
            "L_AUDIO_INTER":    Decimal("0.812500000000000000000000000000000000"),
            "L_EARTH_PATH_CAL": Decimal("0.875000000000000000000000000000000000"),
            "L_MASTER_ARM":     Decimal("0.937500000000000000000000000000000000")
        }

    def stack_into_univac_words(self, precise_value):
        """Splits a 36-decimal calculation into three 12-digit UNIVAC memory registers."""
        raw_digits = f"{precise_value:.36f}".split(".")[-1][:36]
        return raw_digits[0:12], raw_digits[12:24], raw_digits[24:36]

    def resolve_precise_switch(self, raw_analog_voltage):
        """Matches fine board input voltages against exact Left Panel switch lines."""
        target_input = Decimal(str(raw_analog_voltage))
        resolved_pin = "UNKNOWN_LEFT_STATE"
        
        for pin_name, target_voltage in self.pins.items():
            if abs(target_input - target_voltage) < Decimal("0.0001"):
                resolved_pin = pin_name
                break
                
       """Calculate dynamic left-side trajectory adjustments"""
        drift_factor = target_input * Decimal("0.987654321098765432109876543210987654")
        w_high, w_mid, w_low = self.stack_into_univac_words(drift_factor)
        
        return {
            "PIN_NAME": resolved_pin,
            "DRIFT_CALC": drift_factor,
            "UNIVAC_STKS": (w_high, w_mid, w_low)
        }

class CockpitSwitchInterface:
    def __init__(self, target_host='127.0.0.1', target_port=8080):
        self.target_host = target_host
        self.target_port = target_port
        
        # Nominal default voltages (Centered/Neutral or Safe)
        self.switch_states = {
            "ANT_CNTL": 0.5000,
            "IND_LT_TEST": 0.0625  # Default down/off
        }

    def update_switch_voltage(self, switch_name, voltage):
        """Updates the physical voltage registration for a specific toggle."""
        if switch_name in self.switch_states:
            # Rounding to the nearest 16-state hexadecimal step (0.0625V)
            calibrated_voltage = round(voltage / 0.0625) * 0.0625
            self.switch_states[switch_name] = max(0.0, min(1.0, calibrated_voltage))
            self.transmit_telemetry(switch_name)

    def transmit_telemetry(self, switch_name):
        """Transmits the 36-decimal precision telemetry packet to UNIVAC IX."""
        voltage_val = self.switch_states[switch_name]
        
        # Formatting state logic commands based on calibrated voltages
        action_flag = "STANDBY"
        if switch_name == "ANT_CNTL" and voltage_val == 0.0625:
            action_flag = "ENGAGE_FASTEST_TARGET"
        elif switch_name == "IND_LT_TEST":
            action_flag = "AIM_ALIGN_ON" if voltage_val == 0.9375 else "AIM_ALIGN_OFF"

        payload = {
            "node": "LEFT_BOARD",
            "switch": switch_name,
            "voltage": f"{voltage_val:.4f}",
            "execution_flag": action_flag,
            "timestamp": time.time()
        }

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.target_host, self.target_port))
                # Format string message matching the main backplane engine expectations
                message = f"LEFT_BOARD:{switch_name}:{voltage_val:.4f}:{action_flag}"
                sock.sendall(message.encode('utf-8'))
                print(f"[TRANSMIT] {switch_name} -> {voltage_val:.4f}V | Flag: {action_flag}")
        except Exception as e:
            print(f"[BUS ERROR] Failed to stream switch state to backplane: {e}")

# Maintain uniform 36-decimal precision matching the UNIVAC IX backplane
getcontext().prec = 36

# Hardware Logic & Operational Status Codes
CLAMP_LOCKED   = Decimal("0.000000000000000000000000000000000000") # 0x00
CAPSULE_FLOAT  = Decimal("0.875000000000000000000000000000000000") # 0x0E

class LeftPanelCoaxController:
    def __init__(self, integrated_flight_director=None):
        self.flight_director = integrated_flight_director
        
        # State Monitor Variables
        self.retro_man_depressed = False
        self.retro_seq_1_active = False
        self.retro_seq_2_active = False
        
        # Hardware Relay Triggers
        self.relays = {
            "RETRO_BOOSTER_IGNITION_BUS": False,
            "CAPSULE_STRUCTURAL_CLAMP": CLAMP_LOCKED,
            "ZERO_G_FLOAT_INDICATOR": False
        }

    def press_retro_man_button(self):
        """
        Action: Depresses the RETRO MAN manual override push button.
        Arms the internal safety bypass network for mechanical staging.
        """
        self.retro_man_depressed = True
        print("[COCKPIT CONTROL] RETRO MAN button depressed. Safety bypass armed.")

    def toggle_retro_sequences(self, seq_1_state: bool, seq_2_state: bool, execution_window_ms: float = 0.0):
        """
        Action: Handles simultaneous flips of RETRO SEQ 1 and RETRO SEQ 2 toggles.
        If executed at exactly the same time, it drops booster buses and releases clamps.
        """
        self.retro_seq_1_active = seq_1_state
        self.retro_seq_2_active = seq_2_state

        # Check for immediate structural detachment parameters
        if self.retro_man_depressed and self.retro_seq_1_active and self.retro_seq_2_active:
            if execution_window_ms == 0.0:
                print("\n[CRITICAL MANUAL INTERRUPT: CAPSULE DETACHMENT]")
                print("-> Simultaneous step verified: RETRO SEQ 1 & 2 engaged in same window.")
                print("-> Action: Bypassing standard booster rocket ignition loops.")
                
                # Force booster ignition lines to remain completely dead
                self.relays["RETRO_BOOSTER_IGNITION_BUS"] = False
                
                # Apply instantaneous voltage drop to release structural attachment clamps
                self.relays["CAPSULE_STRUCTURAL_CLAMP"] = CAPSULE_FLOAT
                self.relays["ZERO_G_FLOAT_INDICATOR"] = True
                
                # Communicate separation directly to the active flight director
                if self.flight_director:
                    self.flight_director.capsule_separated = True
                    self.flight_director.relays["STAGING_EXPLOSIVE_BOLTS"] = True
                    print("-> Success: Core flight director informed. Spacecraft is now floating free.")
            else:
                print("-> Verification Failure: Toggle synchronization mismatch out of acceptable window.")

    def reset_retro_panel_safeties(self):
        """Resets panel switches to default tracking states."""
        self.retro_man_depressed = False
        self.retro_seq_1_active = False
        self.retro_seq_2_active = False
        print("[COCKPIT CONTROL] Left panel retro safeties returned to baseline standby.")


# Example operational loop simulating cockpit panel interaction
if __name__ == "__main__":
    panel = CockpitSwitchInterface()
    
    print("--- Simulating Cockpit Toggle Activations ---")
    # 1. Pilot flips IND LT TEST switch UP to turn on alignment verification
    panel.update_switch_voltage("IND_LT_TEST", 0.9375)
    time.sleep(1)
    
    # 2. Pilot presses ANT CNTL switch DOWN to trigger engagement on fastest target vector
    panel.update_switch_voltage("ANT_CNTL", 0.0625)
