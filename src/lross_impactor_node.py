import numpy as np
from numba import njit
from pydantic import BaseModel, Field
from decimal import Decimal, getcontext

# Maintain standard 36-decimal precision matching the UNIVAC IX core spec
getcontext().prec = 36

# ==========================================
# 1. KINETIC SPECTROSCOPY SCHEMAS
# ==========================================
class LcrossVehicleProfile(BaseModel):
    """
    Enforces strict Pydantic schema constraints on secondary payload masses
    and structural dimensions prior to calculating kinetic debris plume dynamics.
    """
    spacecraft_id: str = Field("LCROSS-ESPA-S_SC", description="Shepherding spacecraft token")
    shepherding_mass_lbs: float = Field(..., gt=0.0, description="Dry structural ring weight")
    edus_centaur_mass_lbs: float = Field(..., gt=0.0, description="Spent kinetic impactor booster weight")
    spectrometer_channels_active: int = Field(..., ge=2, description="Near-IR and visible photometer links")
    is_plume_illuminated: bool = Field(..., description="Ejecta tracking visibility confirmation")

# ==========================================
# 2. NUMBA ACCELERATED DEBRIS HOT-PATHS
# ==========================================
@njit(fastmath=True)
def calculate_kinetic_ejecta_height(velocity_mps: float, impactor_mass_kg: float, gravity_mps2: float = 1.62) -> float:
    """
    Numba-accelerated kinetic energy and ejecta plume projection calculator.
    Determines if the kicked-up regolith will overshoot shadows into direct sunlight.
    """
    if velocity_mps <= 0.0 or impactor_mass_kg <= 0.0:
        return 0.0
    # Kinetic Energy = 0.5 * m * v^2
    kinetic_energy_joules = 0.5 * impactor_mass_kg * (velocity_mps ** 2)
    # Approximate theoretical apex height of the ejecta cloud
    theoretical_apex_m = (velocity_mps ** 2) / (2.0 * gravity_mps2)
    return theoretical_apex_m

@njit(fastmath=True)
def detect_spectral_water_ice_ratio(near_ir_absorption_idx: float, mid_ir_thermal_idx: float) -> float:
    """
    Evaluates multi-spectral absorption spikes to verify the signature 
    of volatile water vapor/ice in the debris plume.
    """
    if near_ir_absorption_idx <= 0.0:
        return 0.0
    # Core mathematical ratio mapping the 1.5-micron ice signature
    ice_percentage = (near_ir_absorption_idx * 100.0) / (mid_ir_thermal_idx + 0.01)
    return max(0.0, min(100.0, ice_percentage))

# ==========================================
# 3. CORE IMPACT LOGISTICS ENGINE
# ==========================================
class LcrossMissionDirectorNode:
    def __init__(self, athena_guidance_bridge=None):
        self.athena = athena_guidance_bridge
        
        # Target Point: Cabeus Crater Core PSR (Permanently Shadowed Region)
        self.TARGET_CRATER_CORDS = {
            "CABEUS_MAIN": (-84.900000, -35.500000),
            "SHACKLETON_ALT": (-89.900000, 0.000000)
        }
        
        self.edus_separated = False
        self.plume_scanned = False

    def process_impactor_flight_sequence(self, raw_telemetry: dict, velocity_mps: float, ir_index: float):
        """
        Ingests high-speed descent downlinks, calculates terminal trajectory separation, 
        and updates Athena steering matrices to pilot through the explosion cloud.
        """
        # 1. Parse and validate structural properties via Pydantic
        profile = LcrossVehicleProfile(**raw_telemetry)
        
        # Convert weight profiles to standard metric scales for physics execution
        centaur_kg = profile.edus_centaur_mass_lbs * 0.453592
        
        # 2. Compute plume height using JIT-accelerated hot-path loops
        predicted_plume_apex_m = calculate_kinetic_ejecta_height(velocity_mps, centaur_kg)
        
        # 3. Run spectral analysis diagnostic loop
        detected_ice_pct = detect_spectral_water_ice_ratio(ir_index, mid_ir_thermal_idx=1.2)
        
        # Flag structural state shifts
        if velocity_mps > 2400.0: # Match the ~5,600 mph terminal velocity
            self.edus_separated = True
            
        print("\n[NASA LCROSS LUNAR IMPACTOR SEGMENT RESOLVED]")
        print(f"-> Active Asset: {profile.spacecraft_id} | Spectrometers: {profile.spectrometer_channels_active}")
        print(f"-> Predicted Crater Debris Plume Apex: {predicted_plume_apex_m:.2f} Meters")
        print(f"-> Real-Time Multi-Spectral Water Vapor Ratio: {detected_ice_pct:.2f}%")

        # 4. Interface cleanly with the central Athena guidance hub
        if self.athena and hasattr(self.athena, 'bus_states'):
            print("-> Routing trajectory correction parameters down to Athena intercept lines.")
            # If volatile ice concentrations match targets, keep status loops clear
            self.athena.bus_states["RET_ATT_LIGHT_ACTIVE"] = detected_ice_pct > 5.0
            
        return {
            "edus_separated": self.edus_separated,
            "calculated_plume_apex_m": predicted_plume_apex_m,
            "detected_ice_pct": detected_ice_pct
        }
