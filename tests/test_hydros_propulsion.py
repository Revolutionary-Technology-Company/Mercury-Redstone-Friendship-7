import unittest
from src.hydros_propulsion_node import HydrosPropulsionController
from src.athena_bridge import AthenaGuidanceBridge

class TestHydrosPropulsionPhysics(unittest.TestCase):
    def setUp(self):
        # Establish hardware simulation pipeline layers
        self.bridge = AthenaGuidanceBridge()
        self.node = HydrosPropulsionController(athena_guidance_bridge=self.bridge)
        
        # Valid Mock HYDROS Packet matching Tethers Unlimited hardware baselines
        self.valid_engine_data = {
            "thruster_model": "HYDROS-C",
            "liquid_water_remaining_g": 585.5, # Mapped from standard ~600g water canister
            "accumulation_tank_psi": 120.0,     # Incomplete starting gas saturation
            "electrolysis_current_amps": 4.5,   # Active current running through core splitter
            "is_valve_interlock_safe": True
        }

    def test_nominal_electrolysis_gas_generation(self):
        """Verifies that electrical water splitting calculations properly scale pressure."""
        result = self.node.process_propulsion_telemetry_frame(
            raw_telemetry=self.valid_engine_data,
            cycle_duration_sec=180.0 # Run simulation across a 3-minute tracking window
        )
        # Pressure should ramp up to maximum operational levels
        self.assertGreaterEqual(result["current_chamber_psi"], 200.0)
        self.assertTrue(result["engine_hotfired_active"])
        self.assertGreater(result["predicted_torque_kick"], 0.0)

    def test_insufficient_pressure_standby_loop(self):
        """Ensures the bipropellant nozzle does not fire if accumulation bounds sit under 150 PSI."""
        self.valid_engine_data["accumulation_tank_psi"] = 10.0
        self.valid_engine_data["electrolysis_current_amps"] = 0.0 # No current active
        
        result = self.node.process_propulsion_telemetry_frame(
            raw_telemetry=self.valid_engine_data,
            cycle_duration_sec=10.0
        )
        self.assertEqual(result["current_chamber_psi"], 10.0)
        self.assertFalse(result["engine_hotfired_active"])
        self.assertEqual(result["predicted_torque_kick"], 0.0)

if __name__ == "__main__":
    unittest.main()
