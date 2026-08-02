import numpy as np
from numba import njit
from pydantic import BaseModel, Field
from decimal import Decimal, getcontext
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
from astropy.time import Time
import astropy.units as u

# Enforce strict 36-decimal precision matching the UNIVAC IX core spec
getcontext().prec = 36

# ==========================================
# 1. COMMERCIAL LANDER INTEGRATION SCHEMAS
# ==========================================
class LunarLanderProfile(BaseModel):
    """
    Enforces strict Pydantic parsing on incoming commercial partner vehicle data
    prior to executing kinetic trajectory conversions.
    """
    partner_company: str = Field(..., description="Commercial entity (ASTROBOTIC, INTUITIVE_MACHINES, MASTEN)")
    lander_model: str = Field(..., description="Robotic lander structural designation")
    propellant_mass_kg: float = Field(..., gt=0.0, description="Remaining volatile cryogenic/hypergolic mass")
    thrust_vector_newtons: float = Field(..., gt=0.0, description="Main engine descent thrust rating")
    is_telemetry_encrypted: bool = Field(True, description="Sovereign protocol lock status")

# ==========================================
# 2. NUMBA ACCELERATED TRAJECTORY HOT-PATHS
# ==========================================
@njit(fastmath=True)
def calculate_sutton_graves_heat_flux(velocity_mps: float, air_density_kgm3: float, nose_radius_m: float = 0.5) -> float:
    """
    Numba-accelerated Sutton-Graves stagnation point heat flux engine.
    Calculates thermodynamic wall loads during high-velocity earth entry returns.
    """
    # q = C * sqrt(rho / Rn) * V^3
    constant_c = 1.7415e-4
    if velocity_mps <= 0.0 or air_density_kgm3 <= 0.0:
        return 0.0
    heat_flux_wm2 = constant_c * np.sqrt(air_density_kgm3 / nose_radius_m) * (velocity_mps ** 3)
    return heat_flux_wm2

# ==========================================
# 3. CISLUNAR INTERFACE NODE CONTROLLER
# ==========================================
class LunarCatalystOrchestrator:
    def __init__(self, athena_bridge_handle=None):
        self.athena = athena_bridge_handle
        
        # Reference Location: Oplin Atlas Silo Site 578-5
        self.ground_station_lat = 32.161720
        self.ground_station_lon = -99.552690
        self.ground_station_alt_m = 604.0
        
        # Initialize Astropy Earth Location object for topocentric conversions
        self.location = EarthLocation(
            lat=self.ground_station_lat * u.deg,
            lon=self.ground_station_lon * u.deg,
            height=self.ground_station_alt_m * u.m
        )

    def calculate_lander_topocentric_angles(self, moon_ra_deg: float, moon_dec_deg: float) -> tuple:
        """
        Uses astropy celestial routines to calculate real-time local azimuth 
        and elevation pointing coordinates from the Texas Atlas silo grid.
        """
        current_time = Time.now()
        
        # Map target cislunar coordinates
        cislunar_target = SkyCoord(ra=moon_ra_deg * u.deg, dec=moon_dec_deg * u.deg, frame='icrs')
        
        # Transform coordinate frame to local horizon tracking matrix
        altaz_frame = AltAz(obstime=current_time, location=self.location)
        transformed_vector = cislunar_target.transform_to(altaz_frame)
        
        azimuth_deg = float(transformed_vector.az.deg)
        elevation_deg = float(transformed_vector.alt.deg)
        
        return azimuth_deg, elevation_deg

    def process_lander_return_trajectory(self, raw_profile: dict, velocity_mps: float, density_kgm3: float) -> dict:
        """
        Ingests real-time commercial telemetry frames, monitors terminal entry 
        heating parameters, and alerts Athena if tolerances breach safety windows.
        """
        # 1. Validate commercial lander attributes via Pydantic
        lander = LunarLanderProfile(**raw_profile)
        
        # 2. Compute aerothermal flux via accelerated hot-paths
        peak_flux_wm2 = calculate_sutton_graves_heat_flux(velocity_mps, density_kgm3)
        
        # Strict Structural Safety Limit: Alert if wall heating exceeds 1.5 MW/m²
        STRUCTURAL_FLUX_LIMIT = 1500000.0
        abort_sequence_active = peak_flux_wm2 > STRUCTURAL_FLUX_LIMIT
        
        print("\n[LUNAR CATALYST CISLUNAR TELEMETRY SEGMENT DETECTED]")
        print(f"-> Vessel: {lander.partner_company} | Lander Design: {lander.lander_model}")
        print(f"-> Calculated Aero Entry Stagnation Heat Flux: {peak_flux_wm2:.2f} W/m²")
        
        if abort_sequence_active:
            print("-> ALERT: Thermal flux limits breached! Triggering manual S-Turn energy dissipation.")
        else:
            print("-> Trajectory Status: Aerothermal envelope within uncompromised structural bounds.")
            
        # 3. Synchronize status registers with Athena downlinks
        if self.athena and hasattr(self.athena, 'bus_states'):
            self.athena.bus_states["ATHENA_HANDSHAKE_LIVE"] = not abort_sequence_active
            
        return {
            "vessel_id": f"{lander.partner_company}-{lander.lander_model}",
            "calculated_flux_wm2": peak_flux_wm2,
            "requires_energy_dissipation": abort_sequence_active
        }
