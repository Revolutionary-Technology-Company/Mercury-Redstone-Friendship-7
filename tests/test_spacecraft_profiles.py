import unittest
import os
from src.schema_validator import SpacecraftProfileLoader

class TestSpacecraftProfilesAndSchemas(unittest.TestCase):
    def setUp(self):
        # Establish testing baseline configuration profile paths
        self.config_path = "src/config/spacecraft_profiles.json"
        self.loader = SpacecraftProfileLoader(config_json_path=self.config_path)

    def test_profile_parsing_bounds(self):
        """Validates that all 3 custom profiles ingest without triggering exception breaks."""
        self.assertIn("MERCURY_FRIENDSHIP_7_SOLO", self.loader.profiles)
        self.assertIn("MERCURY_ATLAS_BOOSTER_SOLO", self.loader.profiles)
        self.assertIn("MERCURY_ATLAS_FRIENDSHIP_7_STACK", self.loader.profiles)

    def test_integrated_stack_mass_precision(self):
        """Verifies that the combined structural weight parses cleanly into 36 decimals."""
        stack_mass = self.loader.fetch_precise_mass("MERCURY_ATLAS_FRIENDSHIP_7_STACK")
        
        # Combined weight should match 14,587 lbs exactly
        expected_mass = "14587.000000000000000000000000000000000000"
        self.assertEqual(str(stack_mass), expected_mass)
        
    def test_eclss_chamber_allocations(self):
        """Confirms life-support checks match the dual-chamber design."""
        solo_capsule = self.loader.profiles["MERCURY_FRIENDSHIP_7_SOLO"]
        booster_solo = self.loader.profiles["MERCURY_ATLAS_BOOSTER_SOLO"]
        
        # Capsule requires 2 compartments (Pilot and service animal), booster requires 0
        self.assertEqual(solo_capsule.eclss_chamber_count, 2)
        self.assertEqual(booster_solo.eclss_chamber_count, 0)

if __name__ == "__main__":
    unittest.main()
