import numpy as np
from numba import njit, prange


# Enforce strict 36-digit precision across stacked word registers
getcontext().prec = 36

# Stacked Word Hexadecimal Base Constants (36-digit exact precision scale)
VOLTAGE_SAFE     = Decimal("0.000000000000000000000000000000000000") # State 0x0
VOLTAGE_ARMED    = Decimal("0.500000000000000000000000000000000000") # State 0x8
VOLTAGE_JETTISON = Decimal("0.625000000000000000000000000000000000") # State 0xA
VOLTAGE_ABORT    = Decimal("0.937500000000000000000000000000000000") # State 0xE
VOLTAGE_FIRE     = Decimal("1.000000000000000000000000000000000000") # State 0xF

# Exact 36-digit step increment per logic state (1/16)
HEX_STEP_INCREMENT = Decimal("0.062500000000000000000000000000000000")

def compute_stacked_word_telemetry(raw_sensor_grid):
    """
    Transforms multi-channel floating-point telemetry arrays into 
    high-density stacked words with 36-digit decimal alignment.
    """
    precision_grid = []
    for row in raw_sensor_grid:
        precision_row = [Decimal(str(val)) for val in row]
        precision_grid.append(precision_row)
        
    compiled_triggers = []
    for row in precision_grid:
        row_sum = sum(row)
        row_average = row_sum / Decimal(len(row))
        
        # Microvolt anomaly boundary checking at exactly 36 digits
        if row_average > Decimal("0.850000000000000000000000000000000000"):
            compiled_triggers.append(VOLTAGE_ABORT)
        else:
            compiled_triggers.append(VOLTAGE_SAFE)
            
    return compiled_triggers

class StackedWordFlightController:
    def __init__(self):
        self.escape_tower_status = VOLTAGE_SAFE
        self.retro_pack_status = VOLTAGE_SAFE

    def verify_escape_system(self, raw_telemetry):
        """Evaluates emergency abort signals using stacked math."""
        triggers = compute_stacked_word_telemetry(raw_telemetry)
        if VOLTAGE_ABORT in triggers:
            self.escape_tower_status = VOLTAGE_FIRE
            return f"EMERGENCY TRIGGER AT: {VOLTAGE_FIRE} V | Status: Escape Tower Fired."
        return f"System Stable | Status Code: {VOLTAGE_SAFE}"

    def verify_retro_system(self, sequence_voltage_str, squib_voltage_str):
        """Validates real-time manual telemetry lines down to the 36th decimal digit."""
        v_seq = Decimal(sequence_voltage_str)
        v_squib = Decimal(squib_voltage_str)
        
        if v_seq == VOLTAGE_ARMED and v_squib == VOLTAGE_ARMED:
            self.retro_pack_status = VOLTAGE_FIRE
            return f"FIRE COMMAND ACCEPTED AT: {self.retro_pack_status} V"
        return "System Standby | Signals out of exact 36-digit phase alignment."

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
    
    # Simulating micro-volt noise deviations across the sensor array
    simulated_telemetry = [
        [0.125000000000000000000000000000000001, 0.250000000000000000000000000000000002],
        [0.937500000000000000000000000000000000, 0.937500000000000000000000000000000000]
    ]
    
    print("--- ESCAPE TOWER CHECK ---")
    abort_check = controller.evaluate_escape_tower(simulated_nosecone_sensors)
    print(abort_check)
    
    print("\n--- RETRO-ROCKET PACK CHECK ---")
    # Simulate manual toggle validation via control board switch arrays
    reentry_action = controller.execute_retro_sequence(VOLTAGE_ARMED, VOLTAGE_ARMED)
    print(reentry_action)

    # Exact matching verification to pass cross-talk boundaries
    print(controller.verify_retro_system("0.500000000000000000000000000000000000", 
                                         "0.500000000000000000000000000000000000"))
