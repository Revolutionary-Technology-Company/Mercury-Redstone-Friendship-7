# src/build_hex_board_atx_breaker.py
import os

class EATXBreakerBoardGenerator:
    def __init__(self):
        # E-ATX Form Factor dimensions in mm (Largest ATX spec)
        self.board_width = 330.0  
        self.board_height = 305.0
        self.layer_count = 8  # 8-layer micro-via routing scheme
        self.copper_thickness_oz = 3.0  # RT Rule 1: 3oz copper for high-draw amp loads
        
    def initialize_rt_infrastructure(self):
        print(f"Initializing E-ATX Hardware Frame: {self.board_width}mm x {self.board_height}mm")
        print(f"Enforcing RT Fabrication Standards: {self.layer_count}-Layers with {self.copper_thickness_oz}oz Copper Armor.")
        
    def build_breaker_nodes(self):
        """
        Maps physical breaker loops directly behind the seats to isolate 
        0.0V - 1.0V native hexadecimal logic buses.
        """
        breakers = {
            "CB_LEFT_PILOT_NAV": {
                "pin_input": "A1_PILOT_IN",
                "voltage_max": 1.0,  # Max hex state
                "guard_ring": True,  # RT Rule 2: Guard ring isolation
                "layer": 1,          # Component layer
                "description": "Primary pilot stabilization circuit protection"
            },
            "CB_RIGHT_COPILOT_NAV": {
                "pin_input": "B1_COPILOT_IN",
                "voltage_max": 1.0,
                "guard_ring": True,
                "layer": 3,          # Isolated on layer 3 to prevent crosstalk
                "description": "Co-pilot/Animal chamber control loop protection"
            },
            "CB_CENTER_COUNTDOWN": {
                "pin_input": "C1_CENTER_IN",
                "voltage_max": 0.5,  # Nominal static sync
                "guard_ring": False,
                "layer": 5,
                "description": "Booster ignition and abort handshake line breaker"
            },
            "CB_ECLSS_HATCH": {
                "pin_input": "D1_SAFETY_IN",
                "voltage_max": 1.0,  # Vacuum equilibrium latch power
                "guard_ring": True,
                "layer": 7,          # Deep routing layer
                "description": "Dual-chamber suit fan and explosive hatch solenoid barrier"
            }
        }
        return breakers

    def generate_kicad_netlist(self, output_path="hardware/eatx_breaker_board.net"):
        self.initialize_rt_infrastructure()
        breakers = self.build_breaker_nodes()
        
        print("\n--- Compiling Hardware Matrix Nets ---")
        netlist_content = []
        netlist_content.append(f"(export (version D)\n  (design (components")
        
        for name, spec in breakers.items():
            print(f"Routing {name} on Layer {spec['layer']}... [GuardRing: {spec['guard_ring']}]")
            # Enforce RT Rule 3: Use multi-layer micro-vias instead of crossing traces
            netlist_content.append(
                f"    (comp (ref {name})\n"
                f"      (value Circuit_Breaker_16State)\n"
                f"      (footprint RT_Footprints:HighAmp_Relay_Guard)\n"
                f"      (property (name 'Copper_Weight') (value '{self.copper_thickness_oz}oz'))\n"
                f"      (property (name 'Layer_Assignment') (value 'Layer_{spec['layer']}')))"
            )
            
        netlist_content.append("  )\n)")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write("\n".join(netlist_content))
            
        print(f"\n[SUCCESS] E-ATX KiCad Netlist compiled successfully to: {output_path}")

if __name__ == "__main__":
    # Execute generation sequence matching repository deployment steps
    generator = EATXBreakerBoardGenerator()
    generator.generate_kicad_netlist()
