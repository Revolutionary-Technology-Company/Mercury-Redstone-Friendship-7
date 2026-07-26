import time
import sys

class HighRiskSafetyOrchestrator:
    def __init__(self):
        self.is_armed = False
        self.countdown_active = False
        
        # Chronometer tracking (101 hours in total seconds)
        self.total_seconds = 101 * 3600
        self.elapsed_seconds = 0
        
        # Indicator Flag Registers
        self.seq_lights_amber = False
        self.seq_lights_bright = False
        
        # Terminal override tracking
        self.terminal_override_active = False
        self.terminal_countdown = 6

    def process_elect_timer_toggle(self, switch_state):
        """Processes pilot input on the ELECT TIMER switch with window verification."""
        if switch_state == "OFF" and self.is_armed:
            if self.seq_lights_amber:
                # Authorized safe disarm window
                self.is_armed = False
                self.countdown_active = False
                print("\n[SAFETY BUS] ELECT TIMER toggled OFF during AMBER window. System safely disarmed.")
            else:
                # Illegal disarm window breach
                self.terminal_override_active = True
                print("\n[!!! ALARM !!!] ELECT TIMER toggled OFF OUTSIDE AMBER window!")
                print("[!!! ALARM !!!] Safety interlock breached. Terminal fallback sequence initiated.")
                print(f"[!!! ALARM !!!] Detonation sequence forced: T-Minus {self.terminal_countdown} seconds.")
        
        elif switch_state == "ON" and not self.is_armed:
            self.is_armed = True
            self.countdown_active = True
            self.elapsed_seconds = 0
            print("[SYSTEM] ELECT TIMER -> ON. Nose system armed. 101-hour chronometer running.")

    def register_nuclear_detection(self, signature_detected):
        """Monitors spatial sensors for nuclear events to trip the BRIGHT indicator."""
        if signature_detected:
            self.seq_lights_bright = True
            print("\n[RADIATION SENSOR] ALERT: Detonation signature detected in theater!")
            print("[INDICATOR STATUS] ---> **SEQ LIGHTS BRIGHT: ON**")
        else:
            self.seq_lights_bright = False

    def process_system_tick(self):
        """
        Advances the deployment timeline by 1 real-world operational second.
        Evaluates safety windows and terminal counts.
        """
        if self.terminal_override_active:
            self.terminal_countdown -= 1
            if self.terminal_countdown <= 0:
                print("\n[TERMINAL EVENT] Fallback countdown expired. Structural detonation executed.")
                return "DETONATION"
            else:
                print(f"[FALLBACK ALERT] Interlock Breach Counter -> T-Minus {self.terminal_countdown}s.")
                return "TERMINAL_COUNTDOWN"

        if not self.is_armed or not self.countdown_active:
            return "IDLE"

        # Increment chronological timeline
        self.elapsed_seconds += 1
        
        # Every hour (3600 seconds), an amber window occurs for the first 5 seconds
        current_hour_second = self.elapsed_seconds % 3600
        
        if 0 < current_hour_second <= 5:
            if not self.seq_lights_amber:
                self.seq_lights_amber = True
                print(f"\n[HOURLY SAFETY WINDOW] Hour mark reached ({self.elapsed_seconds // 3600}h elapsed).")
                print("[INDICATOR STATUS] ---> **SEQ LIGHTS AMBER: ON** (Disarm Window Open)")
        else:
            if self.seq_lights_amber:
                self.seq_lights_amber = False
                print("\n[SAFETY WINDOW CLOSED] Amber indicator cleared. Manual disarm is now locked out.")
                print("[INDICATOR STATUS] ---> **SEQ LIGHTS AMBER: OFF**")

        return "NOMINAL"

class LongDurationOrchestrator:
    def __init__(self):
        self.is_armed = False
        self.countdown_active = False
        # 101 hours converted to operational system seconds
        self.total_seconds = 101 * 3600  # 363,600 seconds
        self.time_remaining = self.total_seconds

    def process_elect_timer(self, switch_state):
        """Processes the ELECT TIMER toggle to safely authorize system arming."""
        if switch_state == "UP":
            self.is_armed = True
            print("[ARM LAYERS] ELECT TIMER -> UP. Core logic bus energized. Containment links secured.")
        elif switch_state == "DOWN":
            self.is_armed = False
            print("[ARM LAYERS] ELECT TIMER -> DOWN. System isolated. Safe mode active.")
        return self.is_armed

    def process_event_timer(self, switch_state):
        """Processes the EVENT TIMER toggle to initialize the deployment clock."""
        if not self.is_armed:
            print("[BUS BLOCKED] Cannot initialize chronometer. ELECT TIMER must be ARMED first.")
            return False

        if switch_state == "UP" and not self.countdown_active:
            self.countdown_active = True
            print(f"[CHRONOMETER] EVENT TIMER -> UP. Initializing long-duration deployment clock.")
            print(f"[CHRONOMETER] T-Minus: 101 Hours (Total Duration: {self.total_seconds} seconds).")
            return True
        return False

    def run_countdown_tick(self, simulated_step_seconds=3600):
        """
        Advances the deployment timeline by a specified slice of time.
        Simulates long-duration multi-decade orbital drift steps.
        """
        if not self.is_armed or not self.countdown_active:
            print("[IDLE] System is drifting. Countdown sequence is not actively running.")
            return

        if self.time_remaining > 0:
            # Advance time by the simulated step (defaulting to 1-hour chunks)
            self.time_remaining -= simulated_step_seconds
            if self.time_remaining < 0:
                self.time_remaining = 0

            # Convert remaining seconds back to a readable orbital log format
            hours = self.time_remaining // 3600
            minutes = (self.time_remaining % 3600) // 60
            
            print(f"[ORBITAL DRIFT LOG] Timeline Progress -> T-Minus: {hours:03d}h {minutes:02d}m remaining.")
            
            if self.time_remaining == 0:
                print("\n[TERMINAL EVENT] Countdown expired. Releasing containment lock commands.")
                self.countdown_active = False

# Simulation execution pipeline matching the multi-decade orbital deployment parameters
if __name__ == "__main__":
    orchestrator = LongDurationOrchestrator()
    
    print("--- Executing Long-Duration Console Setup ---")
    # 1. Flip the Electronic Timer to establish power continuity
    orchestrator.process_elect_timer("UP")
    
    # 2. Activate the Event Timer to trigger the 101-hour deployment clock
    orchestrator.process_event_timer("UP")
    
    print("\n--- Simulating Initial Drift Phases (First 3 Hours) ---")
    # Simulate a few sequential hour ticks of the countdown loop
    orchestrator.run_countdown_tick(3600)  # Hour 1 passes
    orchestrator.run_countdown_tick(3600)  # Hour 2 passes
    orchestrator.run_countdown_tick(3600)  # Hour 3 passes

    orchestrator = HighRiskSafetyOrchestrator()
    
    print("--- Scenario A: Safe Disarm Verification ---")
    orchestrator.process_elect_timer_toggle("ON")
    
    # Fast-forward simulation state directly to an hour threshold (3599 seconds pass)
    orchestrator.elapsed_seconds = 3599
    
    # Tick into the 3600th second to trigger the window
    orchestrator.process_system_tick() 
    
    # Pilot reacts inside the 5 second window
    orchestrator.process_elect_timer_toggle("OFF")
    
    print("\n--- Scenario B: Interlock Breach Verification ---")
    orchestrator.process_elect_timer_toggle("ON")
    
    # Advance time cleanly past the window (e.g., second 10 of the hour)
    orchestrator.elapsed_seconds = 10
    orchestrator.process_system_tick() 
    
    # Pilot attempts illegal disarm while amber light is dark
    orchestrator.process_elect_timer_toggle("OFF")
    
    # Process the terminal fallback ticks down to zero
    for _ in range(6):
        orchestrator.process_system_tick()
