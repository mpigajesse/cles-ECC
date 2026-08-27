"""
ECC Key Generator - Educational cryptography implementation

Modules:
    - arithmetic: Modular arithmetic operations
    - curve: Elliptic curve definitions and validation
    - point: Point representation on elliptic curves
    - operations: Point addition, doubling, scalar multiplication
    - key_generation: Key pair generation
"""

__version__ = "0.1.0"
__author__ = "Jesse"

# Lazy imports to avoid circular dependencies
__all__ = [
    "arithmetic",
    "curve",
    "point",
    "operations",
    "key_generation",
]
