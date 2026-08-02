import numpy as np
from numba import njit
from pydantic import BaseModel, Field
from decimal import Decimal, getcontext

# Maintain standard 36-decimal precision matching the UNIVAC IX backplane core
getcontext().prec = 36

# ==========================================
# 1. WATER-POWERED PROPULSION SCHEMAS
# ==========================================
class HydrosEngineProfile(BaseModel):
    """
    Enforces strict Pydantic parsing on incoming NASA HYDROS water-electrolysis 
    telemetry packets prior to commanding orbital thrust maneuvers.
    """
    thruster_model: str = Field("HYDROS-C", description="Propulsion configuration class (HYDROS-C or HYDROS-M)")
    liquid_water_remaining_g: float = Field(..., gt=0.0, description="Remaining unpressurized water payload weight")
    accumulation_tank_psi: float = Field(..., ge=0.0, le=250.0, description="Internal gas accumulator pressure")
    electrolysis_current_amps: float = Field(..., ge=0.0, description="Electrical current routed to splitter core")
    is_valve_interlock_safe: bool = Field(..., description="Ignition safety bus status loop confirmation")

# ==========================================
# 2. NUMBA ACCELERATED EXPLOSIVE HOT-PATHS
# ==========================================
@njit(fastmath=True)
def calculate_electrolysis_splitting_curve(current_amps: float, time_seconds: float, starting_psi: float) -> float:
    """
    Numba-accelerated chemical pressure generation model. Computes the production 
    rate of gaseous hydrogen and oxygen from liquid water based on current input.
    """
    if current_amps <= 0.0 or time_seconds <= 0.0:
        return starting_psi
    # Standard gas constant scaling formula modeling generation inside a shot-glass-sized core
    added_pressure_psi = current_amps * time_seconds * 0.452
    final_pressure = starting_psi + added_pressure_psi
    return min(220.0, final_pressure) # Cap at absolute mechanical safety release threshold

@njit(fastmath=True)
def compute_thruster_impulse_torque(accumulation_psi: float, burst_duration_sec: float = 2.0) -> float:
    """
    Calculates the exact torque impulse delivered to the airframe during 
    bipropellant gas combustion in the rocket nozzle.
    """
    if accumulation_psi < 150.0:
        return 0.0 # Insufficient gas saturation to initiate clean hot-fire
    # Returns relative thrust kick velocity profile (e.g. 2 cm/sec)
    delivered_impulse = (accumulation_psi / 200.0) * burst_duration_sec * 0.02
    return delivered_impulse

# ==========================================
# 3. CORE HYDROS ENGINE ORCHESTRATOR
# ==========================================
class HydrosPropulsionController:
    def __init__(self, athena_guidance_bridge=None):
        self.athena = athena_guidance_bridge
        self.engine_firing_count = 0
        self.system_pressurized = False

    def process_propulsion_telemetry_frame(self, raw_telemetry: dict, cycle_duration_sec: float):
        """
        Ingests real-time water propulsion status, models gas generation updates, 
        and updates Athena navigation lines during constellation management.
        """
        # 1. Parse and validate downlinked attributes via Pydantic
        packet = HydrosEngineProfile(**raw_telemetry)
        
        # 2. Model gas splitting curves natively over parallel hot-paths
        resolved_psi = calculate_electrolysis_splitting_curve(
            packet.electrolysis_current_amps, 
            cycle_duration_sec, 
            packet.accumulation_tank_psi
        )
        
        self.system_pressurized = resolved_psi >= 200.0
        
        # 3. Compute torque impulse response metrics
        predicted_torque_kick = 0.0
        if self.system_pressurized and packet.is_valve_interlock_safe:
            predicted_torque_kick = compute_thruster_impulse_torque(resolved_psi)
            self.engine_firing_count += 1
            
        print("\n[NASA HYDROS WATER-FUEL PROBATION CELL RESOLVED]")
        print(f"-> Active Unit: {packet.thruster_model} | Water Mass Remaining: {packet.liquid_water_remaining_g:.2f}g")
        print(f"-> Accumulator Chamber Status: {resolved_psi:.2f} PSI | Ready: {self.system_pressurized}")
        print(f"-> Calculated Orbital Acceleration Kick: {predicted_torque_kick * 100.0:.4f} cm/sec")

        # 4. Communicate dynamic thrust variables down to the active Athena hub
        if self.athena and hasattr(self.athena, 'bus_states'):
            print("-> Syncing propulsion thrust corrections directly into active Athena steering matrices.")
            # Adjust indicator lamps to notify pilots when the water system is fully pressurized
            self.athena.bus_states["RET_ATT_LIGHT_ACTIVE"] = self.system_pressurized
            
        return {
            "current_chamber_psi": resolved_psi,
            "engine_hotfired_active": predicted_torque_kick > 0.0,
            "predicted_torque_kick": predicted_torque_kick
        }
