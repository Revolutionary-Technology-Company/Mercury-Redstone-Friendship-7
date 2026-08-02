import numpy as np
from numba import njit
from pydantic import BaseModel, Field
from decimal import Decimal, getcontext

# Maintain full 36-digit arbitrary-precision compatibility with UNIVAC IX
getcontext().prec = 36

# ==========================================
# 1. PAD EMERGENCY SAFETIES SCHEMAS
# ==========================================
class EgressBasketProfile(BaseModel):
    """
    Enforces strict Pydantic parsing on incoming pad evacuation variables
    prior to calculating velocity decay during emergency descent profiles.
    """
    basket_id: str = Field(..., description="Designation of active SUV-sized wire basket (1 through 4)")
    personnel_count: int = Field(..., ge=1, le=7, description="Number of evacuating crew members onboard")
    cable_length_feet: float = Field(1335.0, ge=1330.0, le=1340.0, description="Total run of Pad 39B cable system")
    magnetic_brake_armed: bool = Field(..., description="Eddy current permanent magnet interlock status")
    chassis_mass_lbs: float = Field(..., gt=0.0, description="Total empty mass of the egress basket vehicle")

# ==========================================
# 2. NUMBA ACCELERATED KINETIC HOT-PATHS
# ==========================================
@njit(fastmath=True)
def calculate_basket_pov_velocity(distance_traveled_ft: float, total_cable_ft: float = 1335.0) -> float:
    """
    Numba-accelerated gravity descent velocity engine. Computes the instantaneous
    First-Person Point-of-View speed (in knots) along the 1,335-foot slide.
    """
    if distance_traveled_ft >= total_cable_ft:
        return 0.0
        
    # Gravity incline descent profile modeling an average slope on Pad 39B
    gravity_acceleration = 32.174
    sine_slope_angle = np.sin(np.radians(11.5))
    
    # Magnetic brake engagement zone occupies the final 235 feet of the line
    braking_zone_start_ft = total_cable_ft - 235.0
    
    if distance_traveled_ft < braking_zone_start_ft:
        # Standard unhindered velocity: V = sqrt(2 * g * sin(theta) * d)
        velocity_fps = np.sqrt(2.0 * gravity_acceleration * sine_slope_angle * distance_traveled_ft)
    else:
        # Peak velocity at braking zone boundary
        peak_velocity_fps = np.sqrt(2.0 * gravity_acceleration * sine_slope_angle * braking_zone_start_ft)
        # Apply exponential velocity decay profile driven by eddy current magnetic forces
        braking_distance = distance_traveled_ft - braking_zone_start_ft
        decay_factor = np.exp(-0.025 * braking_distance)
        velocity_fps = peak_velocity_fps * decay_factor
        if velocity_fps < 2.0:
            velocity_fps = 0.0 # Basket successfully halted at terminal bumper
            
    # Convert feet per second directly into aviation standard knots
    return velocity_fps * 0.592484

# ==========================================
# 3. CORE PAD SAFETIES OVERSEER NODE
# ==========================================
class ArtemisEgressOrchestrator:
    def __init__(self, athena_guidance_bridge=None):
        self.athena = athena_guidance_bridge
        self.evacuation_complete = False
        self.peak_speed_witnessed_knots = 0.0

    def process_emergency_descent_frame(self, raw_telemetry: dict, current_distance_ft: float):
        """
        Ingests rapid egress data packages, calculates live First-Person POV velocity profiles,
        and manages the safety handshakes down to your active Athena dashboard layers.
        """
        # 1. Parse and validate active basket metrics via Pydantic
        basket = EgressBasketProfile(**raw_telemetry)
        
        # 2. Compute live POV speed metrics using JIT-accelerated hot-paths
        live_speed_knots = calculate_basket_pov_velocity(current_distance_ft, basket.cable_length_feet)
        
        if live_speed_knots > self.peak_speed_witnessed_knots:
            self.peak_speed_witnessed_knots = live_speed_knots
            
        # Terminal state determination
        if current_distance_ft >= basket.cable_length_feet and live_speed_knots == 0.0:
            self.evacuation_complete = True
            
        print("\n[ARTEMIS EMERGENCY EGRESS INTERCEPT NODE ACTIVE]")
        print(f"-> Tracking Vessel: Basket {basket.basket_id} | Evacuating Manifest: {basket.personnel_count} Crew")
        print(f"-> Live POV Kinematic Speed: {live_speed_knots:.2f} Knots | Distance Down Line: {current_distance_ft:.1f} FT")
        
        if self.evacuation_complete:
            print("-> STATUS SUCCESS: Basket safely halted at Pad 39B bunker terminal perimeter.")
        elif current_distance_ft >= (basket.cable_length_feet - 235.0) and not basket.magnetic_brake_armed:
            print("-> CRITICAL HAZARD ALERT: Magnetic braking system failed to report active lock during descent!")

        # 3. Route status registers down to the central Athena guidance hub
        if self.athena and hasattr(self.athena, 'bus_states'):
            # Light up cockpit indicator alert lamps to flag a live pad abort condition
            self.athena.bus_states["RET_ATT_LIGHT_ACTIVE"] = not self.evacuation_complete
            
        return {
            "live_speed_knots": live_speed_knots,
            "peak_speed_knots": self.peak_speed_witnessed_knots,
            "evacuation_complete": self.evacuation_complete
        }
