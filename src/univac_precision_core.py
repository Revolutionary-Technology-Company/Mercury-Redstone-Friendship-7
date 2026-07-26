import sys
from decimal import Decimal, getcontext

# Set global execution context to exactly 36 decimal digits
getcontext().prec = 36

class Univac36DigitStacker:
    def __init__(self):
        print("[INIT] Initializing UNIVAC IX 36-Decimal Precision Extension Core...")

    def format_to_univac_words(self, decimal_value):
        """
        Takes a 36-digit Decimal value and splits it into three 
        distinct 12-digit words to mimic physical hardware stacking.
        """
        # Ensure string representation is exactly 36 digits (excluding the decimal point)
        raw_str = f"{decimal_value:.36f}".replace(".", "")[:36]
        
        # Slice into 3 distinct 12-character UNIVAC registers
        word_high = raw_str[0:12]
        word_mid  = raw_str[12:24]
        word_low  = raw_str[24:36]
        
        return word_high, word_mid, word_low

    def process_high_precision_telemetry(self, raw_voltage_input):
        """
        Calculates ultra-precise trajectory tracking from the 
        capsule's physical panel resistor arrays.
        """
        # Example: Simulating a deep fractional orbital math calculation
        base_constant = Decimal("3.141592653589793238462643383279502884")
        multiplier = Decimal(str(raw_voltage_input))
        
        # Core mathematical execution
        precise_result = base_constant * multiplier
        return precise_result

if __name__ == "__main__":
    stacker = Univac36DigitStacker()
    
    # Simulate a highly precise switch voltage read (e.g., from the Center Panel Abort line)
    test_voltage = 0.812562512345
    
    print(f"\n--- [36-DIGIT CORE ENGINE ACTIVE] ---")
    result = stacker.process_high_precision_telemetry(test_voltage)
    print(f"[MATH RESULT] Calculated 36-Digit Float: {result}")
    
    # Stack into memory blocks
    w1, w2, w3 = stacker.format_to_univac_words(result)
    print(f"[UNIVAC STACK] WORD 1 (HIGH): {w1}")
    print(f"[UNIVAC STACK] WORD 2 (MID) : {w2}")
    print(f"[UNIVAC STACK] WORD 3 (LOW) : {w3}")
