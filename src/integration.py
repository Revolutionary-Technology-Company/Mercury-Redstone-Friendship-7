import time
from timers import HighRiskSafetyOrchestrator
from squibs import RetroSquibEvasionController
from sensors import ModernVectorEngine
from jettison import NoseTowerJettisonController
from retro_seq import RetroDescentSequenceController
from comm_relay import CommunicationsRelayController
from parachute import ParachuteRecoveryController
from boost_insert import BoostInsertionController

class MercuryComprehensiveIntegrator:
    def __init__(self):
        # Master hardware interface maps
        self.safety_timer = HighRiskSafetyOrchestrator()
        self.evasion_unit = RetroSquibEvasionController()
        self.vector_engine = ModernVectorEngine()
        self.jett_unit = NoseTowerJettisonController()
        self.descent_unit = RetroDescentSequenceController()
        self.comms_unit = CommunicationsRelayController()
        self.recovery_unit = ParachuteRecoveryController()
        self.boost_unit = BoostInsertionController()
        
        self.system_active = True
        self.escape_sequence_completed = False

    def process_global_tick(self, simulate_blast=False, pilot_switch_action=None):
        """
        Processes a single unified system tick across all connected console components.
        """
        if not self.system_active:
            return

        print("\n=== SYSTEM CORE DATA TELEMETRY LOOP ===")
        if pilot_actions is None:
            pilot_actions = {}

        # 1. Check for incoming environmental threats / detonation signatures
        if simulate_blast:
            self.safety_timer.register_nuclear_detection(signature_detected=True)
            
            # Automated Safety Interlock: A BRIGHT alert triggers immediate evasion maneuvers
            if self.safety_timer.seq_lights_bright:
                print("[SYSTEM BUS] Interrupt vector triggered by SEQ LIGHTS BRIGHT status.")
                # Query sensors for the threat coordinates (simulating blast at Pitch: 60, Yaw: -45)
                threat_coordinates = (30.0, -120.0)
                self.evasion_unit.execute_emergency_burn(threat_coordinates)
                self.escape_sequence_completed = True
                self.system_active = False
                return

        # 2. Process Row 1: Communications Configurations
        if "AUDIO_UHF" in pilot_actions:
            self.comms_unit.set_audio_uhf_mode(pilot_actions["AUDIO_UHF"])
        if "TONE_VOX" in pilot_actions:
            self.comms_unit.configure_vox_loop(pilot_actions["TONE_VOX"])
        if "DIPLF" in pilot_actions:
            self.comms_unit.set_diplf_switch(pilot_actions["DIPLF"])

        # 3. Process Row 2 & 3: Threat Mitigation Timers & Step Targets
        if "ELECT_TIMER" in pilot_actions:
            self.safety_timer.process_elect_timer_toggle(pilot_actions["ELECT_TIMER"])
        if "LANDING_SEQ" in pilot_actions:
            self.vector_engine.process_landing_seq_toggle(pilot_actions["LANDING_SEQ"])
        if "TM_256" in pilot_actions:
            self.comms_unit.configure_frequency_divider(pilot_actions["TM_256"])
        if "PARA_CNTL" in pilot_actions:
            self.recovery_unit.set_parachute_control(pilot_actions["PARA_CNTL"])

        # 3. Row 3 & 4 Processing: Descent Staging, Booster Cuts, and Recovery Signals
        if "BOOST_PWR" in pilot_actions:
            self.boost_unit.set_boost_pwr_rail(pilot_actions["BOOST_PWR"])
        if "BOOST_INS_1" in pilot_actions:
            self.boost_unit.evaluate_insertion_toggles(1, pilot_actions["BOOST_INS_1"])
        if "BOOST_INS_2" in pilot_actions:
            self.boost_unit.evaluate_insertion_toggles(2, pilot_actions["BOOST_INS_2"])
        if "ATT_IND" in pilot_actions:
            self.recovery_unit.set_attitude_indicator_source(pilot_actions["ATT_IND"])

        # 4. Process Row 3 & 4: Descent Sequencing & Physical Jettisons
        if "RETRO_PWR" in pilot_actions:
            self.descent_unit.process_retro_pwr(pilot_actions["RETRO_PWR"])
        if "RETRO_SEQ_1" in pilot_actions:
            self.descent_unit.process_retro_seq_toggles(1, pilot_actions["RETRO_SEQ_1"])
        if "RETRO_SEQ_2" in pilot_actions:
            self.descent_unit.process_retro_seq_toggles(2, pilot_actions["RETRO_SEQ_2"])
        if "RETRO_JETT" in pilot_actions:
            self.descent_unit.trigger_manual_separation(pilot_actions["RETRO_JETT"])
        if "TOWER_JETT" in pilot_actions:
            self.jett_unit.process_jett_switch_toggle(
                switch_state=pilot_actions["TOWER_JETT"], 
                escape_burn_completed=self.escape_sequence_completed
            )

        # 5. Core Chronometer Ticks
        tick_status = self.safety_timer.process_system_tick()
        if tick_status == "DETONATION":
            print("[CRITICAL] Structural termination protocol complete. Halting engine.")
            self.system_active = False

        # 6. Process physical pilot inputs for the manual JETT toggle
        if pilot_jett_action:
            self.jett_unit.process_jett_switch_toggle(
                switch_state=pilot_jett_action, 
                escape_burn_completed=self.escape_sequence_completed
            )

        # 7. Process any physical manual pilot inputs from the console boards
        if pilot_switch_action:
            print(f"[COCKPIT INPUT] Pilot toggled ELECT TIMER to: {pilot_switch_action}")
            self.safety_timer.process_elect_timer_toggle(pilot_switch_action)

        # 8. Advance the primary chronological clock and evaluate amber windows
        tick_status = self.safety_timer.process_system_tick()
        
        # Terminate loop if an un-authorized disarm forces structural termination
        if tick_status == "DETONATION":
            print("[SYSTEM BUS] Terminal loop closed. Halting integration engine.")
            self.system_active = False

# Simulation execution pipeline demonstrating different operational states
if __name__ == "__main__":
    master_loop = MercuryComprehensiveIntegrator()
    
    # Run full end-to-end telemetry check simulating a complete flight envelope loop
    print("\n--- PHASE 1: ORBITAL INSERTION VALIDATION ---")
    master_loop.process_global_tick(pilot_actions={"BOOST_PWR": "UP", "BOOST_INS_1": "UP", "BOOST_INS_2": "UP"})
    
    print("\n--- PHASE 2: THREAT ALERT LOGIC G-LIMIT BURN ---")
    master_loop.process_global_tick(pilot_actions={"ELECT_TIMER": "ON"})
    master_loop.process_global_tick(simulate_blast=True)
    master_loop.process_global_tick(pilot_actions={"TOWER_JETT": "UP"})
    
    print("\n--- PHASE 3: LOW-ALTITUDE STABILIZATION AND DESCENT ---")
    master_loop.process_global_tick(pilot_actions={"PARA_CNTL": "UP", "ATT_IND": "DOWN"})
    
    # Simulate a comprehensive, nominal mission-to-descent timeline update
    master_loop.process_global_tick(pilot_actions={"AUDIO_UHF": "1", "TONE_VOX": "UP", "ELECT_TIMER": "ON"})
    master_loop.process_global_tick(simulate_blast=True)
    master_loop.process_global_tick(pilot_actions={"TOWER_JETT": "UP"})
    
    # Enter reentry phase parameters
    master_loop.process_global_tick(pilot_actions={"RETRO_PWR": "UP", "RETRO_SEQ_1": "UP", "RETRO_SEQ_2": "UP"})
    master_loop.process_global_tick(pilot_actions={"RETRO_JETT": "UP"})
    
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
