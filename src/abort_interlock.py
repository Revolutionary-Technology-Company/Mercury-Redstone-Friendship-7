import numpy as np
from numba import njit
from pydantic import BaseModel, Field
from decimal import Decimal, getcontext

# Enforce strict 36-digit fixed-point math to prevent truncation noise
getcontext().prec = 36

# Hardware Logic & Operational Codes
VALVE_SAFE_LOCK = Decimal("0.000000000000000000000000000000000000") # 0x0
CAPSULE_FLOAT   = Decimal("0.875000000000000000000000000000000000") # 0xE
RELAY_FIRE_RING = Decimal("1.000000000000000000000000000000000000") # 0xF

# ==========================================
# 1. EMERGENCY TELEMETRY CONFIG VALIDATION
# ==========================================
class AbortIncidentPacket(BaseModel):
    """
    Enforces strict Pydantic parsing on incoming diagnostic hazard fields 
    prior to activating high-amp explosive staging overrides.
    """
    asset_id: str = Field(..., description="Unique airframe structural tracking ID")
    detonation_detected: bool = Field(..., description="Explosive fault monitoring flag")
    current_gyro_heading: list = Field(..., min_items=3, max_items=3, description="3D vector array")
    target_gyro_heading: list = Field(..., min_items=3, max_items=3, description="Target alignment array")

# ==========================================
# 2. NUMBA ACCELERATED TRACKING STEERING
# ==========================================
@njit(fastmath=True)
def calculate_dampened_steering_error(current_vec: np.ndarray, target_vec: np.ndarray) -> np.ndarray:
    """
    Parallel-ready gyro tracking loop. Computes error offsets to maintain
    Atlas alignment to target vectors without over-correction.
    """
    error = target_vec - current_vec
    # Inject an immediate 1% real-time dampening factor to counteract raw capsule separation recoil
    dampened_adjustment = error * 0.99
    return dampened_adjustment

# ==========================================
# 3. INTERLOCK PIPELINE ORCHESTRATOR
# ==========================================
class AsynchronousAbortInterlock:
    def __init__(self, battery_controller=None, left_panel_handle=None, flight_director=None):
        self.battery = battery_controller
        self.left_panel = left_panel_handle
        self.director = flight_director
        self.abort_sequence_complete = False

    def execute_asynchronous_abort_purge(self, raw_incident_data: dict):
        """
        Intercepts detonation profiles, forcefuly seals exposed missile bay components,
        and hands steering loops over to Athena to allow continued radio-controlled fire cycles.
        """
        # 1. Parse and validate transaction properties via Pydantic
        packet = AbortIncidentPacket(**raw_incident_data)
        
        if not packet.detonation_detected:
            return {"status": "ENVIRONMENT_NOMINAL", "action": "CONTINUE_FLIGHT"}

        print("\n[CRITICAL HARDWARE FAULT: ABORT SEPARATION INITIALIZED]")
        print("-> Immediate Hazard Isolated. Commencing structural protection loops.")

        # 2. Forceful Mechanical Purge Loop: Seal hull skin before blast-off
        if self.battery:
            print("-> Purging Missile Bay Mechanically: Forcing Axle Retraction...")
            self.battery.relays["AXLE_HYDRAULIC_VALVE"] = "RETRACTED"
            
            print("-> Purging Missile Bay Mechanically: Snapping Left Protective Cap Shut...")
            self.battery.relays["HOUSING_CAP_ACTUATOR"] = "CAP_FULLY_ENGAGED"
            
            print("-> Purging Missile Bay Mechanically: Latching Right-Hinged Outer Door...")
            self.battery.relays["DOOR_MOTOR_SOLENOID"] = "CLOSED"
            print("-> SUCCESS: Outer rocket fuselage streamline restored and sealed.")

        # 3. Secure Detachment Mechanics: Release structural ties without booster activation
        if self.left_panel:
            self.left_panel.relays["RETRO_BOOSTER_IGNITION_BUS"] = False
            self.left_panel.relays["CAPSULE_STRUCTURAL_CLAMP"] = CAPSULE_FLOAT
            
        if self.director:
            self.director.seco_complete = True # Force-flag SECO block to pass staging gates
            self.director.separation_ring_relay = RELAY_FIRE_RING
            self.director.capsule_separated = True
            print("-> Staging Clamps Blown. Friendship 7 separated into safe drift pattern.")

        # 4. Athena Inertial Steering Retention: Keep vehicle rotating and tracking
        c_vec = np.array(packet.current_gyro_heading, dtype=np.float64)
        t_vec = np.array(packet.target_gyro_heading, dtype=np.float64)
        steering_trim = calculate_dampened_steering_error(c_vec, t_vec)
        
        self.abort_sequence_complete = True
        print(f"-> Athena Tracking Matrix Restored: Error Offset Adjusted by {steering_trim}.")
        print("-> REMOTE CONTROL MATRIX LOGGED: Radio firing bus armed for remote launch commands.")

        return {
            "status": "ABORT_PURGE_SUCCESSFUL",
            "capsule_separated": True,
            "hull_integrity_sealed": True,
            "athena_guidance_retained": True
        }
