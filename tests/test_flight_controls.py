import unittest
from src.flight_control_dynamics import IntegratedFlightDirector

class TestFlightControlSubsystems(unittest.TestCase):
    def setUp(self):
        self.director = IntegratedFlightDirector()
        
        # Reference Telemetry Profiles
        self.booster_telemetry = {
            "booster_sustainer_psi": 15.0, # Post-burn drop
            "gimbal_deflection_deg": 1.2,
            "booster_separation_armed": True
        }
        self.actual_telemetry = {
            "pitch_deg": 42.5,
            "roll_deg": 0.0,
            "yaw_deg": -1.5,
            "rcs_pressure_psi": 250.0
        }

    def test_booster_cutoff_and_jettison(self):
        """Confirms the booster core isolates fuel lines and commands staging at low pressure."""
        self.director.execute_booster_staging_loop(self.booster_telemetry, fuel_mass=50.0)
        self.assertTrue(self.director.capsule_separated)
        self.assertEqual(self.director.relays["STAGING_EXPLOSIVE_BOLTS"], True)

    def test_actual_attitude_thruster_pulse(self):
        """Verifies actual capsule loops command a defensive RCS pulse when drift occurs."""
        # Intentionally introduce a 5-degree off-target drift error
        self.director.process_actual_flight_corrections(self.actual_telemetry, target_heading_deg=47.5)
        self.assertEqual(self.director.relays["CAPSULE_RCS_ISOLATION"], "OPEN")

if __name__ == "__main__":
    unittest.main()
