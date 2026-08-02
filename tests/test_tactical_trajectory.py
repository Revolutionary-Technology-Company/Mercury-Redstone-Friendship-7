import unittest
from src.tactical_trajectory_node import TacticalTrajectoryOrchestrator

class TestTacticalTrajectoryPipeline(unittest.TestCase):
    def setUp(self):
        self.orchestrator = TacticalTrajectoryOrchestrator()
        # Mock target tracking array station
        self.orchestrator.register_mission_target("OFFSHORE-VEHICLE-ALPHA", 27.500000, -85.200000)
        
        # Valid structural input data dictionary matching Pydantic requirements
        self.valid_config = {
            "asset_id": "MERCURY-REDSTONE-TACTICAL-CORE-01",
            "dry_mass_lbs": 12500.0,
            "max_allowable_g_load": 11.5
        }

    def test_nominal_safe_fire_and_landing_route(self):
        """
        Verifies that high-altitude, long-range configurations correctly authorize
        weapon deployment and transition directly to the Texas recovery zone.
        """
        # Current Position outside target envelope (Providing 70+ NM safe standoff)
        current_gps = (28.439440, -80.564170) 
        altitude = 45000.0
        speed = 420.0
        
        result = self.orchestrator.evaluate_engagement_profile(
            config_data=self.valid_config,
            current_gps=current_gps,
            altitude_ft=altitude,
            current_speed_knots=speed,
            target_id="OFFSHORE-VEHICLE-ALPHA"
        )
        
        self.assertEqual(result["status"], "ENGAGEMENT_SUCCESS_DEPLOYED")
        self.assertEqual(result["action"], "INITIATE_TEXAS_TRANSIT")
        self.assertEqual(result["assigned_landing_portal"], "CADDO_LAKE_DEEP_PIER")

    def test_unsafe_envelope_abort_trigger(self):
        """
        Confirms that low-altitude or insufficient standoff triggers a structural abort,
        forcing energy management routines to execute.
        """
        # Low altitude close proximity position (Triggers emergency clearance logic)
        current_gps = (27.600000, -85.100000)
        altitude = 8000.0
        speed = 180.0
        
        result = self.orchestrator.evaluate_engagement_profile(
            config_data=self.valid_config,
            current_gps=current_gps,
            altitude_ft=altitude,
            current_speed_knots=speed,
            target_id="OFFSHORE-VEHICLE-ALPHA"
        )
        
        self.assertEqual(result["status"], "INSUFFICIENT_SAFETY_MARGIN")
        self.assertEqual(result["action"], "EXECUTE_S_TURN_MANEUVER")

if __name__ == "__main__":
    unittest.main()
