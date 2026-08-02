import numpy as np
from numba import njit
from pydantic import BaseModel, Field
from decimal import Decimal, getcontext
import csv

# Maintain standard 36-decimal precision matching the UNIVAC IX backplane framework
getcontext().prec = 36

# ==========================================
# 1. SHREW ROVER TYPOLOGY SCHEMA VALIDATION
# ==========================================
class ShrewRoverProfile(BaseModel):
    """
    Enforces strict Pydantic parsing on incoming Dartmouth SHREW rover telemetry
    prior to injecting mobility kinematics into active mapping matrices.
    """
    rover_id: str = Field(..., description="Unique exploratory asset tracking designation")
    wheel_compliance_factor: float = Field(..., gt=0.0, le=1.0, description="Structural tire flexibility rating")
    chassis_mass_kg: float = Field(..., gt=0.0, description="Total modular mass configuration")
    active_payloads_count: int = Field(..., ge=0, description="Number of mounted sensor units")
    battery_charge_pct: float = Field(..., ge=0.0, le=100.0)

# ==========================================
# 2. NUMBA ACCELERATED MOBILITY HOT-PATHS
# ==========================================
@njit(fastmath=True)
def calculate_wheel_slip_gradient(motor_rpm: float, forward_velocity_mps: float, wheel_radius_m: float = 0.15) -> float:
    """
    Numba-accelerated wheel slippage diagnostic engine. 
    Identifies if a modular rover is losing traction on steep lunar crater slopes.
    """
    if motor_rpm <= 0.0:
        return 0.0
    # Expected linear velocity vs actual forward ground speed
    theoretical_velocity = (motor_rpm * (2.0 * np.pi / 60.0)) * wheel_radius_m
    if theoretical_velocity == 0.0:
        return 0.0
    
    slip_ratio = (theoretical_velocity - forward_velocity_mps) / theoretical_velocity
    return max(0.0, min(1.0, slip_ratio))

# ==========================================
# 3. CORE ROVER LOGISTICS ORCHESTRATOR
# ==========================================
class ShrewRoverInterfaceNode:
    def __init__(self, athena_bridge_handle=None):
        self.athena = athena_bridge_handle
        self.active_rovers = {}

    def log_rover_surface_status(self, raw_telemetry: dict, rpm: float, v_mps: float) -> dict:
        """
        Ingests real-time exploratory rover downlinks, flags high traction loss, 
        and updates the central Athena target acquisition engine to maintain lock.
        """
        # 1. Parse and validate structural properties via Pydantic
        rover = ShrewRoverProfile(**raw_telemetry)
        
        # 2. Compute wheel traction dynamics via accelerated hot-path
        slip_gradient = calculate_wheel_slip_gradient(rpm, v_mps)
        
        # Hazard Condition: Flag if traction loss drops below a critical 65% safe threshold
        CRITICAL_SLIP_LIMIT = 0.65
        traction_hazard_active = slip_gradient > CRITICAL_SLIP_LIMIT
        
        status_string = "TRACTION_HAZARD_STUCK" if traction_hazard_active else "NOMINAL_EXPLORATION"
        
        self.active_rovers[rover.rover_id] = {
            "profile": rover,
            "slip_ratio": slip_gradient,
            "status": status_string
        }
        
        print("\n[NASA SHREW PROJECT ROVER TELEMETRY SYNCHRONIZED]")
        print(f"-> Asset Identified: {rover.rover_id} (Compliance Factor: {rover.wheel_compliance_factor})")
        print(f"-> Mechanical Slip Diagnostic: {slip_gradient * 100.0:.2f}% | Mode: {status_string}")
        
        # 3. Route positioning safeguards down to your Athena loop if available
        if self.athena and hasattr(self.athena, 'bus_states'):
            print("-> Syncing rover terrain parameters with active Athena tracking matrices.")
            # Drop handshake state line if the rover becomes completely immobilized
            self.athena.bus_states["ATHENA_HANDSHAKE_LIVE"] = not traction_hazard_active
            
        return {
            "asset_id": rover.rover_id,
            "slip_gradient": slip_gradient,
            "hazard_tripped": traction_hazard_active
        }

    def export_rover_visio_layer(self, output_csv_path="visio_rover_mapping.csv"):
        """
        Exports active rover mechanical parameters to a Visio-compliant format.
        Allows data graphics layers to visually color rovers based on ground traction risks.
        """
        headers = ["ProcessID", "RoverID", "OperationalStatus", "SlipRatio", "BatteryLevel"]
        with open(output_csv_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for idx, (rover_id, data) in enumerate(self.active_rovers.items()):
                writer.writerow([
                    f"SHREW-{2000 + idx}",
                    rover_id,
                    data["status"],
                    f"{data['slip_ratio']:.4f}",
                    f"{data['profile'].battery_charge_pct:.1f}%"
                ])
        print(f"[FILE EXPORT SUCCESS] Rover status arrays written to: {output_csv_path}")
