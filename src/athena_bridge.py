import numpy as np
from numba import njit
from pydantic import BaseModel, Field
from decimal import Decimal, getcontext

# Maintain full 36-digit arbitrary-precision compatibility with UNIVAC IX
getcontext().prec = 36

# ==========================================
# 1. ATHENA TARGETING TRACKING SCHEMAS
# ==========================================
class AthenaTargetPacket(BaseModel):
    """
    Enforces strict Pydantic parsing on incoming target coordinate blocks
    before injecting variables into high-frequency flight calculations.
    """
    target_id: str = Field(..., description="Unique structural threat identification string")
    heading_error_feet: float = Field(..., ge=0.0, description="Absolute linear guidance track error")
    is_firing_authorized: bool = Field(..., description="Master command override status vector")

# ==========================================
# 2. NUMBA ACCELERATED TELEMETRY HOT-PATHS
# ==========================================
@njit(fastmath=True)
def calculate_rcs_lamp_lux(error_feet: float, target_window_feet: float = 65.0) -> float:
    """
    Numba-accelerated cockpit indicator lamp intensity calculator.
    Scales voltage levels: glows dimly at 65 feet, blindingly bright when dead-centered.
    """
    if error_feet > target_window_feet:
        return 0.0
    # Linear voltage ratio: 1.0 (Full Brightness) down to 0.0 (Extinguished)
    intensity = 1.0 - (error_feet / target_window_feet)
    return max(0.0, min(1.0, intensity))

# ==========================================
# 3. ATHENA PIPELINE ENGINE
# ==========================================
class AthenaGuidanceBridge:
    def __init__(self, integrated_flight_director=None):
        self.flight_director = integrated_flight_director
        
        # Real-Time Telemetry Bus Registers
        self.bus_states = {
            "RCS_TARGET_LIGHT_V": 0.0,    # 0.0V to 1.0V Analog Panel Signal
            "RET_ATT_LIGHT_ACTIVE": False, # Command firing state link
            "ATHENA_HANDSHAKE_LIVE": True
        }

    def process_athena_telemetry_frame(self, raw_athena_packet: dict, flight_attitude_dict: dict):
        """
        Processes high-frequency target updates from Athena. Updates panel indicators
        and feeds correction trim commands directly into flight controls.
        """
        # 1. Validate data integrity via Pydantic schemas
        target = AthenaTargetPacket(**raw_athena_packet)
        
        # 2. Compute indicator light brightness natively using accelerated hot-paths
        lux_percentage = calculate_rcs_lamp_lux(target.heading_error_feet)
        self.bus_states["RCS_TARGET_LIGHT_V"] = lux_percentage
        
        # 3. Map execution lighting triggers
        if target.is_firing_authorized:
            self.bus_states["RET_ATT_LIGHT_ACTIVE"] = True
        else:
            self.bus_states["RET_ATT_LIGHT_ACTIVE"] = False

        # 4. Inject guidance corrections to the flight control system
        if self.flight_director:
            if target.heading_error_feet > 0.05 and not self.flight_director.capsule_separated:
                # Adjust booster engine vector trim to compensate for track drift
                print(f"[ATHENA LINK] Injecting dynamic trim adjustment to Booster Core.")
                self.flight_director.relays["BOOSTER_IGNITION_BUS"] = True
            elif self.flight_director.capsule_separated:
                # Direct capsule attitude control corrections based on target position
                print(f"[ATHENA LINK] Steering capsule attitude using target guidance parameters.")
                self.flight_director.process_actual_flight_corrections(
                    flight_attitude_dict, 
                    target_heading_deg=0.0 # Align along the resolved targeting vector
                )
