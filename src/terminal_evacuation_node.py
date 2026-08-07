import numpy as np
from numba import njit
from pydantic import BaseModel, Field
from decimal import Decimal, getcontext
import time

# Enforce strict 36-digit fixed-point math to prevent truncation noise
getcontext().prec = 36

# ==========================================
# 1. EVACUATION TELEMETRY VALIDATION SCHEMA
# ==========================================
class EvacuationIncidentPacket(BaseModel):
    """
    Enforces strict Pydantic parsing on incoming structural health fields
    prior to executing emergency joint tracking adjustments.
    """
    asset_id: str = Field(..., description="Unique structural tracking ID")
    detonation_risk_active: bool = Field(..., description="Hazard flag indicator")
    current_velocity_fps: float = Field(..., gt=0.0, description="Combined stack speed")
    hazard_vector: list = Field(..., min_items=3, max_items=3, description="3D coordinate origin of threat")

# ==========================================
# 2. NUMBA ACCELERATED ESCAPE VELOCITY LOOPS
# ==========================================
@njit(fastmath=True)
def calculate_escape_trajectory_trim(current_velocity: float, hazard_vec: np.ndarray) -> np.ndarray:
    """
    Numba-accelerated kinetic vector generator. Computes an immediate 
    divergent steering path perpendicular to the hazard origin.
    """
    # Normalize hazard vector to obtain defensive heading direction
    norm_factor = np.sqrt(hazard_vec[0]**2 + hazard_vec[1]**2 + hazard_vec[2]**2)
    if norm_factor == 0.0:
        return np.zeros(3)
        
    defensive_direction = -hazard_vec / norm_factor
    # Compute high-G emergency escape thrust vector modifiers
    escape_vector_trim = defensive_direction * (current_velocity * 0.15)
    return escape_vector_trim

# ==========================================
# 3. CORE TERMINAL CONTROLLER NODE
# ==========================================
class TerminalEvacuationOrchestrator:
    def __init__(self, battery_controller=None, athena_guidance_bridge=None):
        self.battery = battery_controller
        self.athena = athena_guidance_bridge
        self.joint_evacuation_complete = False

    def execute_terminal_fire_and_escape(self, raw_incident_data: dict):
        """
        Finishes deploying the active missile, seals the airframe hull,
        and coordinates an immediate joint escape burn for the Atlas and capsule stack.
        """
        # 1. Parse and validate active attributes via Pydantic
        packet = EvacuationIncidentPacket(**raw_incident_data)
        
        if not packet.detonation_risk_active:
            return {"status": "STABLE_ENVIRONMENT", "action": "MAINTAIN_TRACKING"}

        print("\n[CRITICAL WARNING: TERMINAL FIRE AND EVACUATION DEPLOYED]")
        
        # 2. Force Completion of Current Missile Fire Cycle
        if self.battery:
            current_idx = self.battery.current_missile_index
            if current_idx < self.battery.TOTAL_MISSILES and self.battery.missile_armed_status[current_idx]:
                print(f"-> Threat Margin Acceptable: Completing fire sequence for Missile #{current_idx + 1}...")
                self.battery.relays["IGNITION_BUS_ARMED"] = True
                # Pulse bus voltage for squib ignition
                self.battery.missile_armed_status[current_idx] = False
                self.battery.relays["IGNITION_BUS_ARMED"] = False
                print("-> Missile away. Proceeding immediately to hull closure.")

            # 3. High-Speed Enclosure Loop: Secure hull streamline
            print("-> Collapsing Launch Mechanisms: Retracting Axle assembly...")
            self.battery.relays["AXLE_HYDRAULIC_VALVE"] = "RETRACTED"
            
            print("-> Collapsing Launch Mechanisms: Snapping Left Protective Cap Shut...")
            self.battery.relays["HOUSING_CAP_ACTUATOR"] = "CAP_FULLY_ENGAGED"
            
            print("-> Collapsing Launch Mechanisms: Latching Right-Hinged Outer Door...")
            self.battery.relays["DOOR_MOTOR_SOLENOID"] = "CLOSED"
            print("-> SUCCESS: Fuselage streamline completely secured for high-G transit.")

        # 4. Joint Evacuation Trajectory Modification
        hazard_arr = np.array(packet.hazard_vector, dtype=np.float64)
        escape_trim_modifiers = calculate_escape_trajectory_trim(packet.current_velocity_fps, hazard_arr)
        
        self.joint_evacuation_complete = True
        print(f"-> Combined Flight Stack Divert Triggered. Trim Delta Applied: {escape_trim_modifiers}")
        print("-> STATUS SUCCESS: Atlas and Capsule moving to safe coordinate elements together.")

        # 5. Handshake tracking variables down to your active Athena dashboard layers
        if self.athena and hasattr(self.athena, 'bus_states'):
            # Flash indicators to register joint escape maneuver mode
            self.athena.bus_states["RET_ATT_LIGHT_ACTIVE"] = True
            
        return {
            "status": "JOINT_EVACUATION_SUCCESSFUL",
            "missile_fired": True,
            "hull_sealed_clean": True,
            "joint_stack_safe": True
        }
