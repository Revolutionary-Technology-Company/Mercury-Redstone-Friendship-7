import unittest
from src.flight_control_dynamics import IntegratedFlightDirector
from src.athena_bridge import AthenaGuidanceBridge

class TestAthenaSystemIntegration(unittest.TestCase):
    def setUp(self):
        # Fire up the unified hardware simulation layers
        self.director = IntegratedFlightDirector()
        self.bridge = AthenaGuidanceBridge(integrated_flight_director=self.director)
        
        # Reference Telemetry Profiles
        self.mock_athena_packet = {
            "target_id": "STATIONARY-TARGET-TEXAS-RING",
            "heading_error_feet": 15.0, # Well within the 65-foot window
            "is_firing_authorized": True
        }
        self.mock_attitude = {
            "pitch_deg": 2.5,
            "roll_deg": 0.0,
            "yaw_deg": 0.0,
            "rcs_pressure_psi": 250.0
        }

    def test_athena_panel_light_scaling(self):
        """Verifies that the target light scales correctly based on guidance precision."""
        self.bridge.process_athena_telemetry_frame(self.mock_athena_packet, self.mock_attitude)
        
        # Heading error is 15ft / 65ft, light should be partially illuminated
        self.assertGreater(self.bridge.bus_states["RCS_TARGET_LIGHT_V"], 0.0)
        self.assertTrue(self.bridge.bus_states["RET_ATT_LIGHT_ACTIVE"])

    def test_capsule_separated_athena_guidance(self):
        """Confirms that the system correctly pathways guidance updates once the booster is gone."""
        # Force booster staging cutoff criteria
        self.director.capsule_separated = True
        
        # Execute guidance framework pass
        self.bridge.process_athena_telemetry_frame(self.mock_athena_packet, self.mock_attitude)
        self.assertEqual(self.director.relays["STAGING_EXPLOSIVE_BOLTS"], False)

if __name__ == "__main__":
    unittest.main()
