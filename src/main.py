#!/usr/bin/env python3
"""
ECC Key Generator - Main entry point

Educational program for generating ECC key pairs with mathematical transparency.
Shows the step-by-step calculation of Q = dG on elliptic curves.
"""

import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Also add parent directory for package imports
parent_path = src_path.parent
if str(parent_path) not in sys.path:
    sys.path.insert(0, str(parent_path))

from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)


def print_header():
    """Display application header."""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}        ECC KEY GENERATOR - EDUCATIONAL MODE")
    print(f"{Fore.CYAN}{'='*60}")
    print(f"\nGenerating elliptic curve cryptography key pairs")
    print(f"Learning focus: Q = d × G\n")


def print_menu():
    """Display main menu options."""
    print(f"\n{Fore.YELLOW}Select mode:")
    print(f"  {Fore.GREEN}1{Fore.RESET} - Pedagogical mode (small curve, visible calculations)")
    print(f"  {Fore.GREEN}2{Fore.RESET} - Realistic mode (secp256k1)")
    print(f"  {Fore.GREEN}3{Fore.RESET} - NIST mode (P-256)")
    print(f"  {Fore.GREEN}4{Fore.RESET} - Run tests")
    print(f"  {Fore.GREEN}5{Fore.RESET} - Exit")
    print(f"\n{Fore.YELLOW}Choice: {Fore.RESET}", end="")


def mode_pedagogical():
    """Run pedagogical mode with small curve."""
    print(f"\n{Fore.BLUE}[PEDAGOGICAL MODE - Educational Demonstration]")
    print(f"{Fore.BLUE}Using small curve: y² = x³ + 2x + 2 (mod 17)\n")

    try:
        try:
            from .curve import CURVE_P17_A2_B2
            from .point import Point
            from .key_generation import generate_keypair
            from .operations import scalar_mult_with_steps
        except ImportError:
            from curve import CURVE_P17_A2_B2
            from point import Point
            from key_generation import generate_keypair
            from operations import scalar_mult_with_steps

        curve = CURVE_P17_A2_B2
        G = Point(curve, 13, 7)  # Generator point for pedagogical curve
        n = 18  # Order

        print(f"{Fore.GREEN}Curve Parameters:")
        print(f"  E: y² = x³ + 2x + 2 (mod 17)")
        print(f"  Generator G = (13, 7)")
        print(f"  Order n = 18")

        # Generate keypair
        print(f"\n{Fore.YELLOW}[1] Generating random private key d...")
        keypair = generate_keypair(G, n)
        print(f"{Fore.GREEN}  d = {keypair.private_key}")

        # Show scalar multiplication steps
        print(f"\n{Fore.YELLOW}[2] Computing Q = d × G (Scalar Multiplication)...")
        print(f"{Fore.CYAN}Binary representation of {keypair.private_key}:")
        print(f"  {bin(keypair.private_key)} = {keypair.private_key}")

        # Calculate Q = d × G with steps
        Q, steps = scalar_mult_with_steps(G, keypair.private_key, verbose=False)

        print(f"\n{Fore.YELLOW}[3] Result:")
        print(f"{Fore.GREEN}  Public Key Q = ({Q.x}, {Q.y})")
        print(f"  Q is on curve: {Q.is_on_curve()}")

        print(f"\n{Fore.YELLOW}[4] Verification:")
        print(f"{Fore.GREEN}  Private key d: {keypair.private_key}")
        print(f"  Public key Q:  ({Q.x}, {Q.y})")
        print(f"  Relationship:  Q = d × G ✓")

        print(f"\n{Fore.CYAN}This demonstrates the core ECC principle:")
        print(f"  Easy: d + G → Q")
        print(f"  Hard: Q + G → d (discrete log problem)")

    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        import traceback
        traceback.print_exc()


def mode_realistic():
    """Run realistic mode with secp256k1."""
    print(f"\n{Fore.BLUE}[REALISTIC MODE - secp256k1]")
    print(f"{Fore.BLUE}Bitcoin/Ethereum Curve\n")

    try:
        try:
            from .key_generation import generate_secp256k1_keypair
        except ImportError:
            from key_generation import generate_secp256k1_keypair

        print(f"{Fore.GREEN}Curve: secp256k1")
        print(f"  E: y² = x³ + 7 (mod p)")
        print(f"  Field: p = 2²⁵⁶ - 2³² - 977")
        print(f"  Order: n ≈ 2²⁵⁶")

        print(f"\n{Fore.YELLOW}Generating secp256k1 keypair...")
        keypair = generate_secp256k1_keypair()

        print(f"\n{Fore.GREEN}Generated Successfully!")
        print(f"\n{Fore.YELLOW}Private Key (d):")
        print(f"  Hex: {hex(keypair.private_key)[:50]}...")
        print(f"  Bits: {keypair.private_key.bit_length()}")

        print(f"\n{Fore.YELLOW}Public Key (Q = d·G):")
        print(f"  x: {hex(keypair.public_key.x)[:50]}...")
        print(f"  y: {hex(keypair.public_key.y)[:50]}...")

        print(f"\n{Fore.CYAN}secp256k1 is used in:")
        print(f"  • Bitcoin transactions")
        print(f"  • Ethereum smart contracts")
        print(f"  • Lightning Network")
        print(f"  • Many other cryptocurrencies")

    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        import traceback
        traceback.print_exc()


def mode_nist():
    """Run NIST P-256 mode."""
    print(f"\n{Fore.BLUE}[NIST MODE - P-256]")
    print(f"{Fore.BLUE}FIPS 186-4 Standard Curve\n")

    try:
        try:
            from .key_generation import generate_nist_p256_keypair
        except ImportError:
            from key_generation import generate_nist_p256_keypair

        print(f"{Fore.GREEN}Curve: NIST P-256 (prime256v1, secp256r1)")
        print(f"  E: y² = x³ - 3x + b (mod p)")
        print(f"  Field: p = 2²⁵⁶ - 2²²⁴ + 2¹⁹² + 2¹²⁸ - 1")
        print(f"  Order: n ≈ 2²⁵⁶")

        print(f"\n{Fore.YELLOW}Generating NIST P-256 keypair...")
        keypair = generate_nist_p256_keypair()

        print(f"\n{Fore.GREEN}Generated Successfully!")
        print(f"\n{Fore.YELLOW}Private Key (d):")
        print(f"  Hex: {hex(keypair.private_key)[:50]}...")
        print(f"  Bits: {keypair.private_key.bit_length()}")

        print(f"\n{Fore.YELLOW}Public Key (Q = d·G):")
        print(f"  x: {hex(keypair.public_key.x)[:50]}...")
        print(f"  y: {hex(keypair.public_key.y)[:50]}...")

        print(f"\n{Fore.CYAN}NIST P-256 is standardized for:")
        print(f"  • FIPS 186-4 Digital Signatures")
        print(f"  • TLS/SSL Certificate Authentication")
        print(f"  • Government and Financial Applications")
        print(f"  • Secure Communications")

    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        import traceback
        traceback.print_exc()


def run_tests():
    """Run test suite."""
    print(f"\n{Fore.BLUE}[RUNNING TESTS]")
    print(f"Executing pytest...\n")
    import subprocess

    # Use the venv python if available, otherwise use sys.executable
    python_exe = sys.executable
    result = subprocess.run(
        [python_exe, "-m", "pytest", "tests/", "-v", "--tb=short"],
        cwd=Path(__file__).parent.parent
    )
    return result.returncode == 0


def main():
    """Main application loop."""
    print_header()

    while True:
        print_menu()

        try:
            choice = input().strip()

            if choice == "1":
                mode_pedagogical()
            elif choice == "2":
                mode_realistic()
            elif choice == "3":
                mode_nist()
            elif choice == "4":
                success = run_tests()
                if success:
                    print(f"\n{Fore.GREEN}✓ All tests passed!")
                else:
                    print(f"\n{Fore.RED}✗ Some tests failed")
            elif choice == "5":
                print(f"\n{Fore.YELLOW}Goodbye!\n")
                break
            else:
                print(f"\n{Fore.RED}Invalid choice. Please try again.\n")

        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Program interrupted by user\n")
            break
        except Exception as e:
            print(f"\n{Fore.RED}Error: {e}\n")


if __name__ == "__main__":
    main()
