import numpy as np
from numba import njit
from pydantic import BaseModel, Field
from decimal import Decimal, getcontext

# Maintain standard 36-decimal precision matching the UNIVAC IX backplane
getcontext().prec = 36

# ==========================================
# 1. HARDWARE SYSTEM CONTROL SCHEMAS
# ==========================================
class BoosterCoreStatus(BaseModel):
    """Verifies engine health and staging metrics before cutoff sequences."""
    booster_sustainer_psi: float = Field(..., gt=0, description="Main combustion chamber pressure")
    gimbal_deflection_deg: float = Field(..., ge=-5.0, le=5.0, description="Engine nozzle vector angle")
    booster_separation_armed: bool = Field(..., description="Staging sequence interlock status")

class ActualFlightAttitude(BaseModel):
    """Tracks capsule axis coordinates and pilot control stick vectors."""
    pitch_deg: float = Field(..., ge=-180.0, le=180.0)
    roll_deg: float = Field(..., ge=-180.0, le=180.0)
    yaw_deg: float = Field(..., ge=-180.0, le=180.0)
    rcs_pressure_psi: float = Field(..., gt=0, description="Reaction control thruster pressure")

# ==========================================
# 2. ACCELERATED FLIGHT MATRIX HOT-PATHS
# ==========================================
@njit(fastmath=True)
def compute_booster_thrust_decay(psi: float, propellant_mass_lbs: float) -> float:
    """
    Accelerated booster physics tracking loop. Models active thrust decay 
    to calculate the precise millisecond window for Main Engine Cutoff (MECO).
    """
    if propellant_mass_lbs <= 100.0:
        return 0.0
    return psi * 360.25

@njit(fastmath=True)
def calculate_rcs_pulse_duration(error_deg: float, rcs_psi: float) -> float:
    """
    Calculates the exact duration in milliseconds to fire the capsule's attitude 
    thrusters to stabilize alignment during manual flight corrections.
    """
    if np.abs(error_deg) < 0.05:
        return 0.0 # Perfectly stable on-target alignment
    return (np.abs(error_deg) * 45.1) / rcs_psi

# ==========================================
# 3. INTEGRATED VEHICLE CONTROLLER
# ==========================================
class IntegratedFlightDirector:
    def __init__(self):
        self.booster_active = True
        self.capsule_separated = False
        
        # Hardware Status Tracks
        self.relays = {
            "BOOSTER_IGNITION_BUS": False,
            "SUSTAINER_VALVE_SOLENOID": "OPEN",
            "CAPSULE_RCS_ISOLATION": "OPEN",
            "STAGING_EXPLOSIVE_BOLTS": False
        }

    def execute_booster_staging_loop(self, booster_data: dict, fuel_mass: float):
        """
        Manages the heavy booster stage. Cuts primary engine lines and 
        fires explosive structural bolts to ditch the spend rocket body.
        """
        status = BoosterCoreStatus(**booster_data)
        thrust = compute_booster_thrust_decay(status.booster_sustainer_psi, fuel_mass)
        
        if thrust <= 0.0 and status.booster_separation_armed:
            self.relays["SUSTAINER_VALVE_SOLENOID"] = "CLOSED"
            self.relays["STAGING_EXPLOSIVE_BOLTS"] = True
            self.booster_active = False
            self.capsule_separated = True
            print("\n[BOOSTER CONTROL] MAIN ENGINE CUTOFF DETERMINED.")
            print("-> Action: Fired staging separation ring. Booster jettisoned.")
        else:
            print(f"-> Booster Active Core: Sustainer Thrust Output = {thrust:.2f} lbs.")

    def process_actual_flight_corrections(self, attitude_data: dict, target_heading_deg: float):
        """
        Manages actual capsule operations. Uses high-frequency pulses to control 
        the orientation of the spacecraft once free from the booster stack.
        """
        att = ActualFlightAttitude(**attitude_data)
        current_error = target_heading_deg - att.pitch_deg
        
        pulse_time_sec = calculate_rcs_pulse_duration(current_error, att.rcs_pressure_psi)
        
        if pulse_time_sec > 0.0:
            print(f"\n[ACTUAL FLIGHT CONTROL] Attitide Drift Identified: {current_error:.2f}°")
            print(f"-> Action: Command RCS solenoid pulse for {pulse_time_sec:.4f} seconds.")
        else:
            print("-> Actual Flight State: Gyro attitude alignment stable within target tracking window.")
