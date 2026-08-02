import unittest
from src.lross_impactor_node import LcrossMissionDirectorNode
from src.athena_bridge import AthenaGuidanceBridge

class TestLcrossMissionKinematics(unittest.TestCase):
    def setUp(self):
        # Set up active software engine pipelines
        self.bridge = AthenaGuidanceBridge()
        self.node = LcrossMissionDirectorNode(athena_guidance_bridge=self.bridge)
        
        # Valid Mock LCROSS Profile matching Northrop Grumman ESPA hardware specs
        self.valid_spacecraft_data = {
            "spacecraft_id": "LCROSS-ESPA-S_SC",
            "shepherding_mass_lbs": 1286.0,
            "edus_centaur_mass_lbs": 5070.0, # Spent upper stage impact block
            "spectrometer_channels_active": 4,
            "is_plume_illuminated": True
        }

    def test_nominal_booster_impact_plume(self):
        """Verifies that high-velocity kinetic impacts return predictable plume expansion heights."""
        result = self.node.process_impactor_flight_sequence(
            raw_telemetry=self.valid_spacecraft_data,
            velocity_mps=2500.0,    # Lunar impact speed (~5,600 mph)
            ir_index=0.85           # Simulate clear near-IR water absorption dip
        )
        self.assertTrue(result["edus_separated"])
        self.assertGreater(result["calculated_plume_apex_m"], 1000.0)
        self.assertGreater(result["detected_ice_pct"], 0.0)

    def test_zero_velocity_standby_loop(self):
        """Ensures the JIT physics engine returns clean neutral properties when parked in parking orbits."""
        result = self.node.process_impactor_flight_sequence(
            raw_telemetry=self.valid_spacecraft_data,
            velocity_mps=0.0,
            ir_index=0.0
        )
        self.assertEqual(result["calculated_plume_apex_m"], 0.0)
        self.assertEqual(result["detected_ice_pct"], 0.0)

if __name__ == "__main__":
    unittest.main()
