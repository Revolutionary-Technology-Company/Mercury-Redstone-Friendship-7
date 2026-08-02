import numpy as np
from numba import njit
from pydantic import BaseModel, Field
from typing import Dict, Tuple

# ==========================================
# 1. PYDANTIC PROTOCOL SCHEMA VALIDATION
# ==========================================
class VehicleMassProfile(BaseModel):
    """
    Enforces strict Pydantic telemetry structural parsing prior to loading
    aerodynamic matrix parameters into active execution loops.
    """
    asset_id: str = Field(..., description="Unique vehicle structural tracking identification string")
    dry_mass_lbs: float = Field(..., gt=0, description="Structural empty vehicle mass")
    max_allowable_g_load: float = Field(..., gt=0, description="Maximum airframe yield structural limit")

# ==========================================
# 2. NUMBA ACCELERATED PHYSICS HOT-PATHS
# ==========================================
@njit(fastmath=True)
def calculate_haversine_clearance(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Accelerated hot-path geographic clearance calculator. Calculates straight-line
    distance gaps over the earth sphere to find target vectors.
    """
    # Convert degrees to radians natively
    rad_lat1 = np.radians(lat1)
    rad_lon1 = np.radians(lon1)
    rad_lat2 = np.radians(lat2)
    rad_lon2 = np.radians(lon2)
    
    dlon = rad_lon2 - rad_lon1
    dlat = rad_lat2 - rad_lat1
    
    a = np.sin(dlat / 2.0)**2 + np.cos(rad_lat1) * np.cos(rad_lat2) * np.sin(dlon / 2.0)**2
    c = 2.0 * np.arcsin(np.sqrt(a))
    
    # Earth radius in nautical miles
    nm_radius = 3440.065
    return c * nm_radius

@njit(fastmath=True)
def verify_safe_kinetic_envelope(current_altitude_ft: float, speed_knots: float, safe_buffer_nm: float) -> bool:
    """
    Evaluates kinetic states to determine if the vehicle can execute operations safely.
    Ensures sufficient potential-to-kinetic energy conversion bounds.
    """
    if current_altitude_ft < 15000.0:
        return False
    if speed_knots < 250.0:
        return False
    return True

# ==========================================
# 3. TACTICAL CORE LOGISTICS CONTROLLER
# ==========================================
class TacticalTrajectoryOrchestrator:
    def __init__(self):
        # Established Texas Recovery Baseline Terminal Points
        self.TEXAS_RECOVERY_PORTALS = {
            "CADDO_LAKE_DEEP_PIER": (32.698600, -94.112500),
            "OPLIN_ATLAS_SILO_578_5": (32.161720, -99.552690),
            "LAWN_ATLAS_SILO_578_6": (32.140350, -99.703210)
        }
        
        # Primary Target Positions Dictionary Matrix
        self.active_targets: Dict[str, Tuple[float, float]] = {}

    def register_mission_target(self, target_id: str, latitude: float, longitude: float):
        """
        Locks target threat vectors into the coordinate tracking cache.
        """
        self.active_targets[target_id] = (latitude, longitude)
        print(f"[TACTICAL NODE] Locked target coordinate track for ID: {target_id}")

    def evaluate_engagement_profile(self, config_data: dict, current_gps: Tuple[float, float], 
                                    altitude_ft: float, current_speed_knots: float, target_id: str) -> dict:
        """
        Processes structural inputs, checks standoff distances, and calculates
        safe firing vectors before mapping return pathways.
        """
        # 1. Validate structural schema properties via Pydantic
        profile = VehicleMassProfile(**config_data)
        
        if target_id not in self.active_targets:
            return {"status": "REJECTED_UNKNOWN_TARGET", "action": "HOLD_POSITION"}
            
        t_lat, t_lon = self.active_targets[target_id]
        c_lat, c_lon = current_gps
        
        # 2. Run fast JIT clearance evaluations
        distance_to_target_nm = calculate_haversine_clearance(c_lon, c_lat, t_lon, t_lat)
        is_envelope_safe = verify_safe_kinetic_envelope(altitude_ft, current_speed_knots, distance_to_target_nm)
        
        # Strict Safe Fire Condition Check: Must maintain 65 nautical miles minimum standoff clearance
        SAFE_FIRE_STANDOFF_NM = 65.0
        
        if is_envelope_safe and (distance_to_target_nm >= SAFE_FIRE_STANDOFF_NM):
            print(f"\n[ENGAGEMENT AREA CLEARED] Asset {profile.asset_id} is in a safe firing envelope.")
            print(f"-> Target Standoff: {distance_to_target_nm:.2f} NM (Required: >={SAFE_FIRE_STANDOFF_NM} NM)")
            print("-> COMMAND STATE: WEAPON STAGING AUTHORIZED.")
            
            # Resolve closest recovery landing vector across Texas rings
            recovery_destination = "CADDO_LAKE_DEEP_PIER"
            r_lat, r_lon = self.TEXAS_RECOVERY_PORTALS[recovery_destination]
            distance_to_recovery = calculate_haversine_clearance(c_lon, c_lat, r_lon, r_lat)
            
            return {
                "status": "ENGAGEMENT_SUCCESS_DEPLOYED",
                "action": "INITIATE_TEXAS_TRANSIT",
                "target_standoff_nm": distance_to_target_nm,
                "assigned_landing_portal": recovery_destination,
                "recovery_distance_nm": distance_to_recovery
            }
        else:
            print(f"\n[TACTICAL ABORT ENVELOPE INDETERMINATE]")
            print(f"-> Threat Standoff: {distance_to_target_nm:.2f} NM. Kinetic Buffer Clear: {is_envelope_safe}")
            print("-> COMMAND STATE: DIVERT AND EXECUTE S-TURN ENERGY MANAGEMENT LOOPS.")
            return {
                "status": "INSUFFICIENT_SAFETY_MARGIN",
                "action": "EXECUTE_S_TURN_MANEUVER",
                "target_standoff_nm": distance_to_target_nm
            }
