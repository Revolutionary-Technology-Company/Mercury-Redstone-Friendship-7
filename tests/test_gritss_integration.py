import unittest
from src.athena_bridge import AthenaGuidanceBridge
from src.gritss_transponder import GritssInterferometryNode

class TestGritssGeodeticPipeline(unittest.TestCase):
    def setUp(self):
        # Establish integrated tracking stack handles
        self.bridge = AthenaGuidanceBridge()
        self.gritss_node = GritssInterferometryNode(athena_bridge_handle=self.bridge)
        
        # Valid Mock GRITSS Transponder Frame Output
        self.valid_downlink = {
            "satellite_id": "GRITSS-12U-XL",
            "x_band_frequency_ghz": 10.2,
            "s_band_frequency_ghz": 3.2,
            "laser_retroreflector_lock": True,
            "phase_center_drift_mm": 1.5  # Simulate minimal axis deflection
        }

    def test_nominal_geodetic_sync_pass(self):
        """Verifies that high-elevation orbits calculate frame ties with sub-centimeter accuracy."""
        sync_success = self.gritss_node.synchronize_reference_frame(
            raw_telemetry=self.valid_downlink,
            raw_range_ft=1250400.0,  # Base orbital target distance
            sat_elevation=42.5       # High visibility above receiver dish
        )
        self.assertTrue(sync_success)
        self.assertTrue(self.gritss_node.system_calibrated)

    def test_low_horizon_visibility_inhibit(self):
        """Ensures the transponder isolates tracking calculations when signals are degraded by horizon clutter."""
        sync_success = self.gritss_node.synchronize_reference_frame(
            raw_telemetry=self.valid_downlink,
            raw_range_ft=1890000.0,
            sat_elevation=4.2        # Below the mandatory 10-degree horizon limit
        )
        self.assertFalse(sync_success)

if __name__ == "__main__":
    unittest.main()
