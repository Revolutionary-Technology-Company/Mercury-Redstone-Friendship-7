import math
import time

class RetroSquibEvasionController:
    def __init__(self):
        # Maximum safe structural/biological G-force constraint for human pilots
        self.MAX_SAFE_G = 5.4 
        # Standard Earth gravitational acceleration constant (m/s^2)
        self.G_CONSTANT = 9.81  
        self.squibs_fired = False

    def calculate_evasion_vector(self, blast_vector):
        """
        Computes the exact opposite heading (180 degrees) from the detected detonation vector.
        Expects blast_vector as a tuple of (pitch, yaw) angles in degrees.
        """
        pitch, yaw = blast_vector
        
        # Calculate safer facing vector by inverting the coordinates
        safe_pitch = (pitch + 180) % 360
        safe_yaw = (yaw + 180) % 360
        
        # Normalize negative rotations back to positive space
        if safe_pitch > 180: safe_pitch -= 360
        if safe_yaw > 180: safe_yaw -= 360
            
        return (round(safe_pitch, 2), round(safe_yaw, 2))

    def execute_emergency_burn(self, blast_vector):
        """
        Orchestrates capsule re-orientation and commands maximum safe squib acceleration.
        """
        if self.squibs_fired:
            print("[SQUIBS] Emergency burn already expended.")
            return

        print("\n[EVASION PROTOCOL] Initiating automated defensive response...")
        
        # 1. Determine safest direction
        safe_pitch, safe_yaw = self.calculate_evasion_vector(blast_vector)
        print(f"[RE-ORIENTATION] Detonation detected at Pitch: {blast_vector[0]}°, Yaw: {blast_vector[1]}°")
        print(f"[RE-ORIENTATION] Adjusting reaction control system (RCS) to safe vector: Pitch: {safe_pitch}°, Yaw: {safe_yaw}°")
        
        # 2. Enforce safety limit on the thrust profiles
        target_acceleration = self.MAX_SAFE_G * self.G_CONSTANT
        print(f"[THRUST ENGINE] Calibrating ignition profile to structural pilot limit: {self.MAX_SAFE_G}g")
        print(f"[THRUST ENGINE] Target Linear Acceleration Vector: {target_acceleration:.2f} m/s²")
        
        # 3. Fire squib pathways
        self.squibs_fired = True
        print("[INDICATOR STATUS] ---> **RETRO ROCKET SQUIBS ARM & JETT LIGHTS: FLASHING AMBER**")
        print("[THRUST ENGINE] !!! FIRE RETRO ROCKET SQUIBS !!! Sustaining evasive escape velocity...")

# Simulation pipeline connecting the blast detection alert to the escape maneuver
if __name__ == "__main__":
    controller = RetroSquibEvasionController()
    
    # Simulate a scenario where a detonation signature is detected off the front starboard quarter
    # Pitch: 45.0 degrees, Yaw: 30.0 degrees
    detected_blast_coordinates = (45.0, 30.0)
    
    # Trigger the automated safe escape sequence
    controller.execute_emergency_burn(detected_blast_coordinates)
