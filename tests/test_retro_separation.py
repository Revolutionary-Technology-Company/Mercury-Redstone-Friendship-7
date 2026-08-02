import unittest
from src.flight_control_dynamics import IntegratedFlightDirector
from src.left_panel import LeftPanelCoaxController

class TestManualRetroSeparation(unittest.TestCase):
    def setUp(self):
        # Instantiate flight hardware simulation modules
        self.director = IntegratedFlightDirector()
        self.controller = LeftPanelCoaxController(integrated_flight_director=self.director)

    def test_nominal_simultaneous_detachment_pass(self):
        """Verifies that the capsule breaks away cleanly into a float state without firing engines."""
        # 1. Arm system via push button
        self.controller.press_retro_man_button()
        
        # 2. Command simultaneous sequence flips
        self.controller.toggle_retro_sequences(seq_1_state=True, seq_2_state=True, execution_window_ms=0.0)
        
        # 3. Assert structural clamps released and capsule is drifting un-boosted
        self.assertEqual(self.controller.relays["CAPSULE_STRUCTURAL_CLAMP"], str(0.875))
        self.assertFalse(self.controller.relays["RETRO_BOOSTER_IGNITION_BUS"])
        self.assertTrue(self.director.capsule_separated)

    def test_missing_retro_man_inhibit(self):
        """Ensures that toggling the sequences without pressing RETRO MAN blocks structural separation."""
        # Toggle sequences without arming the push button first
        self.controller.toggle_retro_sequences(seq_1_state=True, seq_2_state=True, execution_window_ms=0.0)
        
        self.assertEqual(self.controller.relays["CAPSULE_STRUCTURAL_CLAMP"], str(0.0))
        self.assertFalse(self.director.capsule_separated)

if __name__ == "__main__":
    unittest.main()
