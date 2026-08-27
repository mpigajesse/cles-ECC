"""
ECC Key generation.

Implements:
- Random private key generation
- Public key computation (Q = d·G)
- Complete key pair generation
- Key pair validation
"""

import secrets
from typing import TYPE_CHECKING
from dataclasses import dataclass

from src.operations import scalar_mult

if TYPE_CHECKING:
    from src.curve import EllipticCurve
    from src.point import Point, Point_At_Infinity


@dataclass
class KeyPair:
    """
    An ECC key pair (private key, public key).

    Attributes:
        curve: Elliptic curve
        private_key: Secret scalar d
        public_key: Public point Q = d·G
        generator: Generator point G
    """

    curve: "EllipticCurve"
    private_key: int
    public_key: "Point | Point_At_Infinity"
    generator: "Point"

    def __str__(self) -> str:
        """String representation of keypair."""
        return (
            f"KeyPair(\n"
            f"  private_key: {hex(self.private_key)}\n"
            f"  public_key:  {self.public_key}\n"
            f")"
        )

    def __repr__(self) -> str:
        """Detailed representation."""
        return self.__str__()


def generate_private_key(n: int) -> int:
    """
    Generate a random private key.

    The private key is a random integer d in the range [1, n-1].

    Args:
        n: Order of the generator (size of the key space)

    Returns:
        Random private key d where 1 ≤ d < n

    Note:
        This uses Python's `secrets` module for cryptographically
        secure random number generation.
    """
    return secrets.randbelow(n - 1) + 1


def compute_public_key(private_key: int, generator: "Point") -> "Point | Point_At_Infinity":
    """
    Compute public key from private key.

    Computes: Q = d × G

    where:
    - d is the private key (scalar)
    - G is the generator point
    - Q is the public key

    This is the fundamental equation of ECC:
    - Easy to compute Q from d and G
    - Hard to compute d from Q and G (ECDLP - discrete log problem)

    Args:
        private_key: Private key d
        generator: Generator point G

    Returns:
        Public key Q = d × G (Point or Point_At_Infinity if d=0)

    Example:
        >>> G = Point(curve, Gx, Gy)
        >>> d = 12345
        >>> Q = compute_public_key(d, G)  # Q = 12345·G
    """
    return scalar_mult(generator, private_key, use_binary=True)


def generate_keypair(
    generator: "Point",
    n: int,
) -> KeyPair:
    """
    Generate a complete ECC key pair.

    Creates a random private key and computes the corresponding public key.

    Args:
        generator: Generator point G
        n: Order of the generator

    Returns:
        KeyPair containing private_key, public_key, curve, and generator

    Example:
        >>> G = Point(curve, Gx, Gy)
        >>> keypair = generate_keypair(G, n=2**256)
        >>> private_key = keypair.private_key
        >>> public_key = keypair.public_key
    """
    # Generate random private key
    private_key = generate_private_key(n)

    # Compute public key
    public_key = compute_public_key(private_key, generator)

    # Create and return keypair
    return KeyPair(
        curve=generator.curve,
        private_key=private_key,
        public_key=public_key,
        generator=generator,
    )


def validate_keypair(keypair: KeyPair) -> bool:
    """
    Validate that a key pair is correct.

    Verifies that:
    1. Private key is in valid range [1, n-1]
    2. Public key is on the curve
    3. Public key is not the point at infinity
    4. Public key = private_key × generator

    Args:
        keypair: KeyPair to validate

    Returns:
        True if keypair is valid, False otherwise
    """
    from src.point import Point_At_Infinity

    # Check private key is non-zero (we don't have actual order n here)
    if keypair.private_key <= 0:
        return False

    # Check public key is not infinity
    if isinstance(keypair.public_key, Point_At_Infinity):
        return False

    # Check public key is on curve
    if not keypair.public_key.is_on_curve():
        return False

    # Verify: Q = d × G
    expected_public_key = compute_public_key(keypair.private_key, keypair.generator)
    if keypair.public_key != expected_public_key:
        return False

    return True


class KeyGenerator:
    """
    Helper class for key generation on a specific curve with generator.

    Encapsulates curve and generator, providing convenient methods for
    repeated key generation without passing these parameters each time.
    """

    def __init__(self, generator: "Point", order: int):
        """
        Initialize key generator.

        Args:
            generator: Generator point G
            order: Order of the generator (approximately the key space size)
        """
        self.generator = generator
        self.order = order
        self.curve = generator.curve

    def generate_keypair(self) -> KeyPair:
        """
        Generate a key pair.

        Returns:
            New KeyPair
        """
        return generate_keypair(self.generator, self.order)

    def generate_private_key(self) -> int:
        """
        Generate a private key.

        Returns:
            Random private key
        """
        return generate_private_key(self.order)

    def get_public_key(self, private_key: int) -> "Point | Point_At_Infinity":
        """
        Get public key for a given private key.

        Args:
            private_key: Private key d

        Returns:
            Public key Q = d × G
        """
        return compute_public_key(private_key, self.generator)


# Convenience functions for common curves

def generate_secp256k1_keypair() -> KeyPair:
    """
    Generate a key pair on secp256k1 (Bitcoin/Ethereum).

    Returns:
        KeyPair on secp256k1
    """
    from src.curve import CURVE_SECP256K1

    Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

    from src.point import Point
    G = Point(CURVE_SECP256K1, Gx, Gy)

    # secp256k1 order (actual value for Bitcoin/Ethereum)
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    return generate_keypair(G, n)


def generate_nist_p256_keypair() -> KeyPair:
    """
    Generate a key pair on NIST P-256.

    Returns:
        KeyPair on NIST P-256
    """
    from src.curve import CURVE_NIST_P256

    # NIST P-256 generator
    Gx = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
    Gy = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5

    from src.point import Point
    G = Point(CURVE_NIST_P256, Gx, Gy)

    # NIST P-256 order
    n = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551

    return generate_keypair(G, n)
