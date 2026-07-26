import numpy as np
from numba import njit, prange

# Hexadecimal Voltage Level Constants (0.0V - 1.0V in 0.0625V increments)
VOLTAGE_SAFE     = 0.0000  # State 0x0
VOLTAGE_ARMED    = 0.5000  # State 0x8
VOLTAGE_FIRE     = 1.0000  # State 0xF
VOLTAGE_ABORT    = 0.9375  # State 0xE
VOLTAGE_JETTISON = 0.6250  # State 0xA

@njit(parallel=True, fastmath=True)
def process_telemetry_grid(sensor_matrix):
    """
    Parallel processing of multi-channel nose cone sensor arrays.
    Maps analog voltages directly to autonomous ignition triggers.
    """
    rows, cols = sensor_matrix.shape
    output_triggers = np.zeros(rows, dtype=np.float64)
    
    for i in prange(rows):
        critical_sum = 0.0
        for j in range(cols):
            critical_sum += sensor_matrix[i, j]
        
        # Heuristic threshold tracking for absolute structural safety
        average_voltage = critical_sum / cols
        if average_voltage > 0.85:
            output_triggers[i] = VOLTAGE_ABORT
        else:
            output_triggers[i] = VOLTAGE_SAFE
            
    return output_triggers

class MercuryRedstoneFlightController:
    def __init__(self):
        self.escape_tower_status = VOLTAGE_SAFE
        self.retro_pack_status = VOLTAGE_SAFE
        self.system_ready = True

    def evaluate_escape_tower(self, booster_telemetry):
        """
        Monitors manual sequencing loops and automatic boost parameters.
        Handles emergency separation sequence for the two-seat custom hull.
        """
        # Process multi-channel inputs via Numba parallel carver loop
        triggers = process_telemetry_grid(booster_telemetry)
        
        if np.any(triggers == VOLTAGE_ABORT):
            self.escape_tower_status = VOLTAGE_FIRE
            return "EMERGENCY ABORT: Escape Tower Rocket Ignited. Capsule Separating."
        
        return "Escape Tower Nominal. Monitoring Boost Insert Loops."

    def execute_retro_sequence(self, sequence_voltage, squib_arm_voltage):
        """
        Validates dual-stage physical switch positions for reentry.
        Executes manual retro-rocket squib fire protocols.
        """
        # Enforce exact hexadecimal cross-talk matching constraints
        if sequence_voltage == VOLTAGE_ARMED and squib_arm_voltage == VOLTAGE_ARMED:
            self.retro_pack_status = VOLTAGE_FIRE
            return "RETRO SEQ ACTIVE: Three solid-fuel retro-rockets fired sequentially."
        
        if sequence_voltage == VOLTAGE_JETTISON:
            self.retro_pack_status = VOLTAGE_SAFE
            return "RETRO JETTISON: Retro-rocket strap-on pack discarded from heat shield."
            
        return "Retro-Rocket Pack Standby. Squibs Disarmed."

# --- Hardware System Validation Run ---
if __name__ == "__main__":
    controller = MercuryRedstoneFlightController()
    
    # Simulate an 8-layer telemetry grid tracking structural anomalies
    simulated_nosecone_sensors = np.array([
        [0.125, 0.250, 0.1875, 0.125],   # Nominal telemetry line
        [0.9375, 1.000, 0.8750, 0.9375]   # Critical pressure spike detected
    ])
    
    print("--- ESCAPE TOWER CHECK ---")
    abort_check = controller.evaluate_escape_tower(simulated_nosecone_sensors)
    print(abort_check)
    
    print("\n--- RETRO-ROCKET PACK CHECK ---")
    # Simulate manual toggle validation via control board switch arrays
    reentry_action = controller.execute_retro_sequence(VOLTAGE_ARMED, VOLTAGE_ARMED)
    print(reentry_action)
