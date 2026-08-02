import unittest
from src.lunar_catalyst_node import LunarCatalystOrchestrator
from src.athena_bridge import AthenaGuidanceBridge

class TestLunarCatalystCislunarPipeline(unittest.TestCase):
    def setUp(self):
        # Set up active hardware translation mock structures
        self.bridge = AthenaGuidanceBridge()
        self.orchestrator = LunarCatalystOrchestrator(athena_bridge_handle=self.bridge)
        
        # Valid Mock Telemetry Profile matching Astrobotic's lander parameters
        self.valid_lander_data = {
            "partner_company": "ASTROBOTIC",
            "lander_model": "GRIFFIN-HEAVY-DUTY",
            "propellant_mass_kg": 1850.5,
            "thrust_vector_newtons": 32000.0,
            "is_telemetry_encrypted": True
        }

    def test_topocentric_angle_resolution(self):
        """Verifies that astropy successfully outputs standard horizon tracking coordinates."""
        az, el = self.orchestrator.calculate_lander_topocentric_angles(moon_ra_deg=42.5, moon_dec_deg=12.2)
        self.assertTrue(0.0 <= az <= 360.0)
        self.assertTrue(-90.0 <= el <= 90.0)

    def test_nominal_entry_heat_flux(self):
        """Confirms Sutton-Graves loop correctly tracks standard hypersonic entry values."""
        result = self.orchestrator.process_lander_return_trajectory(
            raw_profile=self.valid_lander_data,
            velocity_mps=3500.0,    # Normal atmospheric entry transition speed
            density_kgm3=0.0015     # Outer thin altitude air density profile
        )
        self.assertFalse(result["requires_energy_dissipation"])
        self.assertGreater(result["calculated_flux_wm2"], 0.0)

    def test_extreme_flux_abort_condition(self):
        """Verifies high kinetic entries trigger system alerts to initialize S-Turn loops."""
        result = self.orchestrator.process_lander_return_trajectory(
            raw_profile=self.valid_lander_data,
            velocity_mps=11200.0,   # High-velocity direct lunar return footprint
            density_kgm3=0.0850     # Thick compression layer crossing
        )
        self.assertTrue(result["requires_energy_dissipation"])

if __name__ == "__main__":
    unittest.main()
