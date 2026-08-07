import unittest
import numpy as np
from src.flight_control_dynamics import IntegratedFlightDirector
from src.athena_bridge import AthenaGuidanceBridge
from src.terminal_evacuation_node import TerminalEvacuationOrchestrator

# Mock class matching your 17-missile hardware tracking registries
class MockNikeBatteryController:
    def __init__(self):
        self.TOTAL_MISSILES = 17
        self.current_missile_index = 3
        self.missile_armed_status = [True] * self.TOTAL_MISSILES
        self.relays = {
            "IGNITION_BUS_ARMED": False,
            "DOOR_MOTOR_SOLENOID": "FULLY_OPEN",
            "AXLE_HYDRAULIC_VALVE": "EXTENDED_78_DEG",
            "HOUSING_CAP_ACTUATOR": "ROTATING_OPEN"
        }

class TestTerminalEvacuationSubsystem(unittest.TestCase):
    def setUp(self):
        self.battery = MockNikeBatteryController()
        self.bridge = AthenaGuidanceBridge()
        
        # Build unified sequence interlock node
        self.orchestrator = TerminalEvacuationOrchestrator(
            battery_controller=self.battery,
            athena_guidance_bridge=self.bridge
        )
        
        # Hazard payload matching Pydantic parsing bounds
        self.incident_data = {
            "asset_id": "MA6-GLENN-COMBINED-FLIGHT-STACK",
            "detonation_risk_active": True,
            "current_velocity_fps": 18500.0,
            "hazard_vector": [150.0, -20.0, 45.0]
        }

    def test_complete_fire_and_joint_closure_sequence(self):
        """Confirms that the vehicle completes the live launch before locking the hull down."""
        target_index = self.battery.current_missile_index
        result = self.orchestrator.execute_terminal_fire_and_escape(self.incident_data)
        
        # Current missile should register as spent
        self.assertFalse(self.battery.missile_armed_status[target_index])
        
        # Fuselage bay lines must report completely closed and locked flush
        self.assertEqual(self.battery.relays["DOOR_MOTOR_SOLENOID"], "CLOSED")
        self.assertEqual(self.battery.relays["AXLE_HYDRAULIC_VALVE"], "RETRACTED")
        self.assertEqual(self.battery.relays["HOUSING_CAP_ACTUATOR"], "CAP_FULLY_ENGAGED")
        
        # Flight tracking should reflect safe joint evacuation status
        self.assertTrue(result["joint_stack_safe"])
        self.assertTrue(self.orchestrator.joint_evacuation_complete)

if __name__ == "__main__":
    unittest.main()
