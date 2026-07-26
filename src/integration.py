import time
from timers import HighRiskSafetyOrchestrator
from squibs import RetroSquibEvasionController
from sensors import ModernVectorEngine
from jettison import NoseTowerJettisonController

class MercurySystemIntegrator:
    def __init__(self):
        self.safety_timer = HighRiskSafetyOrchestrator()
        self.evasion_unit = RetroSquibEvasionController()
        self.vector_engine = ModernVectorEngine()
        self.jett_unit = NoseTowerJettisonController()
        
        self.system_active = True
        self.escape_sequence_completed = False

    def process_global_tick(self, simulate_blast=False, pilot_switch_action=None):
        """
        Processes a single unified system tick across all connected console components.
        """
        if not self.system_active:
            return

        print("\n--- NEW TELEMETRY CYCLE ---")

        # 1. Check for incoming environmental threats / detonation signatures
        if simulate_blast:
            self.safety_timer.register_nuclear_detection(signature_detected=True)
            
            # Automated Safety Interlock: A BRIGHT alert triggers immediate evasion maneuvers
            if self.safety_timer.seq_lights_bright:
                print("[SYSTEM BUS] Interrupt vector triggered by SEQ LIGHTS BRIGHT status.")
                # Query sensors for the threat coordinates (simulating blast at Pitch: 60, Yaw: -45)
                threat_coordinates = (60.0, -45.0)
                self.evasion_unit.execute_emergency_burn(threat_coordinates)
                self.escape_sequence_completed = True
                self.system_active = False
                return
        # 2. Process physical pilot inputs for the manual JETT toggle
        if pilot_jett_action:
            self.jett_unit.process_jett_switch_toggle(
                switch_state=pilot_jett_action, 
                escape_burn_completed=self.escape_sequence_completed
            )

        # 3. Process any physical manual pilot inputs from the console boards
        if pilot_switch_action:
            print(f"[COCKPIT INPUT] Pilot toggled ELECT TIMER to: {pilot_switch_action}")
            self.safety_timer.process_elect_timer_toggle(pilot_switch_action)

        # 4. Advance the primary chronological clock and evaluate amber windows
        tick_status = self.safety_timer.process_system_tick()
        
        # Terminate loop if an un-authorized disarm forces structural termination
        if tick_status == "DETONATION":
            print("[SYSTEM BUS] Terminal loop closed. Halting integration engine.")
            self.system_active = False

# Simulation execution pipeline demonstrating different operational states
if __name__ == "__main__":
    master_loop = MercurySystemIntegrator()
    
    print("====================================================")
    print("FULL FLIGHT THREAT ANALYSIS AND EVASION SIMULATION")
    print("====================================================")
    # Start tracking system
    master_loop.process_global_tick(pilot_switch_action="ON")
    
    # 1. Radar detects signature -> Fires evasive thrusters under safe G-limits
    master_loop.process_global_tick(simulate_blast=True)
    
    # 2. Threat clear -> Pilot toggles the JETT switch UP to cast off the nose apparatus
    master_loop.process_global_tick(pilot_jett_action="UP")
    
    print("====================================================")
    print("SCENARIO 1: SYSTEM INITIALIZATION AND ARMING SEQUENCE")
    print("====================================================")
    # Turn the core electronic timer system on
    integrator.process_global_tick(pilot_switch_action="ON")
    
    print("\n====================================================")
    print("SCENARIO 2: ILLEGAL DISARM WINDOW OVERRIDE BREACH")
    print("====================================================")
    # Advance time slightly to ensure we are outside the 0-5s hourly window
    integrator.safety_timer.elapsed_seconds = 45
    # Pilot attempts to shut off the system when the amber sequence indicator is dark
    integrator.process_global_tick(pilot_switch_action="OFF")
    
    # Process the subsequent terminal ticks to demonstrate the 6-second interlock sequence
    for _ in range(3):
        if integrator.system_active:
            integrator.process_global_tick()

    print("\n====================================================")
    print("SCENARIO 3: AUTOMATED EMERGENCY ESCAPE EVASION")
    print("====================================================")
    # Reset the integration controller for a fresh threat assessment test
    escape_test_integrator = MercurySystemIntegrator()
    escape_test_integrator.safety_timer.process_elect_timer_toggle("ON")
    
    # Simulate an immediate external blast detection signature
    escape_test_integrator.process_global_tick(simulate_blast=True)
