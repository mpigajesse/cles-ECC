#!/usr/bin/env python3
"""
ECC Key Generator - Main entry point

Educational program for generating ECC key pairs with mathematical transparency.
Shows the step-by-step calculation of Q = dG on elliptic curves.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

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
    print(f"\n{Fore.BLUE}[PEDAGOGICAL MODE]")
    print(f"{Fore.BLUE}Using small curve for educational purposes\n")
    print(f"This mode will show all intermediate calculations.")
    print(f"\n[PHASE 2-7 in development...]")
    print(f"Currently not implemented - Phase 1 infrastructure only\n")


def mode_realistic():
    """Run realistic mode with secp256k1."""
    print(f"\n{Fore.BLUE}[REALISTIC MODE - secp256k1]")
    print(f"{Fore.BLUE}Using Bitcoin/Ethereum curve\n")
    print(f"\n[PHASE 8+ in development...]")
    print(f"Currently not implemented - Phase 1 infrastructure only\n")


def mode_nist():
    """Run NIST P-256 mode."""
    print(f"\n{Fore.BLUE}[NIST MODE - P-256]")
    print(f"{Fore.BLUE}Using NIST P-256 standard curve\n")
    print(f"\n[PHASE 8+ in development...]")
    print(f"Currently not implemented - Phase 1 infrastructure only\n")


def run_tests():
    """Run test suite."""
    print(f"\n{Fore.BLUE}[RUNNING TESTS]")
    print(f"Executing pytest...\n")
    import subprocess
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
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
