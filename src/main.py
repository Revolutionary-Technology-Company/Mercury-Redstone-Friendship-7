import sys
import time
from src.left_panel import LeftPanelSwitchboard
from src.right_panel import RightPanelSwitchboard
from src.center_panel import CenterPanelDashboard

class UnivacIXCoreOrchestrator:
    def __init__(self):
        print("[BOOT] UNIVAC IX Architecture Online. Initializing 3VL Evaluation Engine...")
        self.left_board = LeftPanelSwitchboard()
        self.right_board = RightPanelSwitchboard()
        self.center_board = CenterPanelDashboard()
        self.athena_export_ready = False

    def process_3vl_state(self, left_v, right_v, center_v):
        """Evaluates inputs across all boards using Kleene indeterminate parameters."""
        l_action = self.left_board.read_left_matrix(left_v)
        r_action = self.right_board.read_right_matrix(right_v)
        c_action = self.center_board.read_center_matrix(center_v)
        
        print(f"[3VL LOGIC] LEFT: {l_action} | RIGHT: {r_action} | CENTER: {c_action}")
        return l_action, r_action, c_action

    def drive_round_diagnostic_ports(self, l_act, r_act, c_act):
        """Pushes current active variables out to the round window display tubes."""
        print(f"[ROUND DISPLAY] Updating terminal windows behind unmasked nose panels.")
        if c_act == "CTR_UNIVAC_RESET":
            print("[MAINFRAME] Flashing initialization parameters across nose crystal layers.")
            self.athena_export_ready = True

    def export_to_athena_bus(self):
        """Prepares the old salvaged UNIVAC nose block to stream data to the Athena system."""
        if self.athena_export_ready:
            print("[ATHENA] Old UNIVAC core decoupled. Packaging telemetry buffer to Athena supercomputing bus link.")
            return "ATHENA_SYNC_COMPLETE"
        return "ATHENA_WAITING"

if __name__ == "__main__":
    univac_ix = UnivacIXCoreOrchestrator()
    
    # Simulating simultaneous pilot input actions across all switch blocks
    test_hardware_sweeps = [
        (0.9375, 0.9375, 0.0625),  # Master Arm toggles + Booster Ignition throw
        (0.1875, 0.375,  0.75),    # Yaw thrusters + Gas Valve adjustments
        (0.0625, 0.0625, 0.875)    # Univac Reset command execution sequence
    ]
    
    for cycle, (lv, rv, cv) in enumerate(test_hardware_sweeps):
        print(f"\n--- [CLOCK FRAME {cycle}] Processing Panel Buses ---")
        la, ra, ca = univac_ix.process_3vl_state(lv, rv, cv)
        univac_ix.drive_round_diagnostic_ports(la, ra, ca)
        
        athena_status = univac_ix.export_to_athena_bus()
        print(f"[ATHENA LINK]: {athena_status}")
        time.sleep(0.5)
