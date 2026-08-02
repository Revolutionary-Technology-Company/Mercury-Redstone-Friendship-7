import unittest
from src.shrew_rover_node import ShrewRoverInterfaceNode
from src.athena_bridge import AthenaGuidanceBridge

class TestShrewRoverMobilityPipeline(unittest.TestCase):
    def setUp(self):
        # Establish integrated software handles
        self.bridge = AthenaGuidanceBridge()
        self.node = ShrewRoverInterfaceNode(athena_bridge_handle=self.bridge)
        
        # Valid Mock SHREW Rover Packet matching Dartmouth's structural layout
        self.valid_rover_data = {
            "rover_id": "SHREW-MODULAR-EXPLORER-04",
            "wheel_compliance_factor": 0.85,
            "chassis_mass_kg": 45.2,
            "active_payloads_count": 3,
            "battery_charge_pct": 92.4
        }

    def test_nominal_surface_mobility_pass(self):
        """Verifies stable surface rolling evaluates as nominal without tripping hazards."""
        result = self.node.log_rover_surface_status(
            raw_telemetry=self.valid_rover_data,
            rpm=120.0,          # Moderate motor execution speed
            v_mps=1.8           # Smooth, unhindered forward progress
        )
        self.assertFalse(result["hazard_tripped"])
        self.assertLess(result["slip_gradient"], 0.20)

    def test_regolith_slip_abort_trigger(self):
        """Ensures extreme motor spinning with zero velocity throws a critical traction hazard."""
        result = self.node.log_rover_surface_status(
            raw_telemetry=self.valid_rover_data,
            rpm=450.0,          # High wheel spinning
            v_mps=0.1           # Minimal forward progress (stuck in fine crater regolith)
        )
        self.assertTrue(result["hazard_tripped"])

if __name__ == "__main__":
    unittest.main()
