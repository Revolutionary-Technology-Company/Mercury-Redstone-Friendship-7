import unittest
import numpy as np
from src.flight_control_dynamics import IntegratedFlightDirector
from src.left_panel import LeftPanelCoaxController
from src.abort_interlock import AsynchronousAbortInterlock

# Mock class simulating the physical 17-missile mechanical barrel line
class MockNikeBatteryController:
    def __init__(self):
        self.relays = {
            "DOOR_MOTOR_SOLENOID": "OPENING",
            "AXLE_HYDRAULIC_VALVE": "EXTENDED_78_DEG",
            "HOUSING_CAP_ACTUATOR": "ROTATING_OPEN"
        }

class TestAbortPurgePipeline(unittest.TestCase):
    def setUp(self):
        self.battery = MockNikeBatteryController()
        self.left_panel = LeftPanelCoaxController()
        self.director = IntegratedFlightDirector()
        
        # Build unified execution interlock node
        self.interlock = AsynchronousAbortInterlock(
            battery_controller=self.battery,
            left_panel_handle=self.left_panel,
            flight_director=self.director
        )
        
        # Raw packet payload passing tracking variables
        self.hazard_packet = {
            "asset_id": "MA6-GLENN-COMBINED-FLIGHT-STACK",
            "detonation_detected": True,
            "current_gyro_heading": [0.04, -0.01, 0.02],
            "target_gyro_heading": [0.00, 0.00, 0.00]
        }

    def test_forceful_housing_purge_before_separation(self):
        """Verifies that all side bays are shut flush before structural disconnect ring activates."""
        result = self.interlock.execute_asynchronous_abort_purge(self.hazard_packet)
        
        # Mechanical bay lines must report completely closed
        self.assertEqual(self.battery.relays["DOOR_MOTOR_SOLENOID"], "CLOSED")
        self.assertEqual(self.battery.relays["AXLE_HYDRAULIC_VALVE"], "RETRACTED")
        self.assertEqual(self.battery.relays["HOUSING_CAP_ACTUATOR"], "CAP_FULLY_ENGAGED")
        
        # Separation lines must register high voltage
        self.assertTrue(result["capsule_separated"])
        self.assertTrue(result["hull_integrity_sealed"])
        self.assertTrue(self.interlock.abort_sequence_complete)

if __name__ == "__main__":
    unittest.main()
