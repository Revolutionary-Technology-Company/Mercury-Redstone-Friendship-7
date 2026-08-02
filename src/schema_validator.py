import json
from decimal import Decimal, getcontext
from pydantic import BaseModel, Field

# Match the UNIVAC IX precision standard natively
getcontext().prec = 36

class SpacecraftTelemetrySchema(BaseModel):
    """
    Enforces strict structural boundaries on mass, surface areas, and 
    G-load parameters before passing inputs to Numba physics JIT hot-paths.
    """
    asset_id: str = Field(..., description="Unique structural asset registration tracking label")
    description: str = Field(..., description="Historical configuration summary string")
    dry_mass_lbs: float = Field(..., gt=0, description="Total empty mass of structure")
    max_allowable_g_load: float = Field(..., gt=0, description="Maximum airframe structural breaking point")
    aerodynamic_surface_area_sqft: float = Field(..., gt=0, description="Total atmospheric cross-sectional area")
    ballistic_coefficient_beta: float = Field(..., gt=0, description="Hypersonic drag decay multiplier")
    eclss_chamber_count: int = Field(..., ge=0, description="Active isolated oxygen support volumes")
    voltage_bus_step_v: float = Field(..., ge=0, description="potentiometer step intervals")

class SpacecraftProfileLoader:
    def __init__(self, config_json_path="src/config/spacecraft_profiles.json"):
        self.profiles = {}
        self.load_and_validate_profiles(config_json_path)

    def load_and_validate_profiles(self, path):
        with open(path, "r") as file:
            raw_data = json.load(file)
            
        for key, raw_profile in raw_data.items():
            # Validate structural bounds using your Pydantic core engine
            validated_profile = SpacecraftTelemetrySchema(**raw_profile)
            self.profiles[key] = validated_profile
            
        print(f"[SCHEMA VALIDATOR] Successfully mapped and verified {len(self.profiles)} high-precision spacecraft profiles.")

    def fetch_precise_mass(self, profile_key: str) -> Decimal:
        """Returns the high-precision decimal representation of structural mass."""
        if profile_key not in self.profiles:
            raise KeyError(f"Profile {profile_key} missing from configuration database.")
        return Decimal(str(self.profiles[profile_key].dry_mass_lbs))
