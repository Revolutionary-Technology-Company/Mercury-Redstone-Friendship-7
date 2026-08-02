import unittest
from src.artemis_egress_node import ArtemisEgressOrchestrator
from src.athena_bridge import AthenaGuidanceBridge

class TestArtemisEgressKinematics(unittest.TestCase):
    def setUp(self):
        # Set up active hardware simulation pipeline layers
        self.bridge = AthenaGuidanceBridge()
        self.node = ArtemisEgressOrchestrator(athena_guidance_bridge=self.bridge)
        
        # Valid Mock Egress Basket Packet matching Pad 39B hardware parameters
        self.valid_basket_data = {
            "basket_id": "BASKET-02",
            "personnel_count": 5,
            "cable_length_feet": 1335.0,
            "magnetic_brake_armed": True,
            "chassis_mass_lbs": 3200.0 # SUV-sized basket structural weight configuration
        }

    def test_nominal_egress_acceleration_zone(self):
        """Verifies steady speed accumulation along the initial gravity gravity-drop runway."""
        result = self.node.process_emergency_descent_frame(
            raw_telemetry=self.valid_basket_data,
            current_distance_ft=500.0 # Halfway down the clear acceleration track
        )
        self.assertFalse(result["evacuation_complete"])
        self.assertGreater(result["live_speed_knots"], 15.0)

    def test_magnetic_braking_zone_deceleration(self):
        """Confirms eddy current equations safely decay momentum down to a complete stop."""
        # Query at terminal footprint gate limit
        result = self.node.process_emergency_descent_frame(
            raw_telemetry=self.valid_basket_data,
            current_distance_ft=1335.0
        )
        self.assertTrue(result["evacuation_complete"])
        self.assertEqual(result["live_speed_knots"], 0.0)

if __name__ == "__main__":
    unittest.main()
