"""
Elliptic curve class for Weierstrass curves.

Implements elliptic curves of the form:
    E: y² ≡ x³ + ax + b (mod p)

where p is prime and the curve is non-singular (4a³ + 27b² ≢ 0 mod p).
"""

from src.arithmetic import mod_gcd


class EllipticCurve:
    """
    Elliptic curve in Weierstrass form over a prime field.

    Represents a curve: y² = x³ + ax + b (mod p)

    Attributes:
        p: Prime modulus (field characteristic)
        a: Curve parameter a
        b: Curve parameter b
    """

    def __init__(self, p: int, a: int, b: int):
        """
        Create an elliptic curve.

        Validates that:
        - p is positive
        - Curve is non-singular: 4a³ + 27b² ≢ 0 (mod p)

        Args:
            p: Prime modulus
            a: Curve parameter a
            b: Curve parameter b

        Raises:
            ValueError: If p is not positive or curve is singular
        """
        if p <= 0:
            raise ValueError(f"Prime p must be positive, got {p}")

        if not self._is_probably_prime(p):
            raise ValueError(f"p must be prime or composite for testing, got {p}")

        self.p = p
        self.a = a % p  # Normalize to [0, p)
        self.b = b % p  # Normalize to [0, p)

        # Check curve is non-singular
        if not self.is_valid():
            raise ValueError(
                f"Curve y² = x³ + {self.a}x + {self.b} (mod {p}) is singular: "
                f"discriminant 4a³ + 27b² ≡ 0 (mod {p})"
            )

    @staticmethod
    def _is_probably_prime(n: int, k: int = 5) -> bool:
        """
        Miller-Rabin primality test.

        Returns True if n is probably prime, False if definitely composite.

        Args:
            n: Number to test
            k: Number of test rounds (higher = more confident)

        Returns:
            True if probably prime, False if composite
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False

        # Write n-1 as 2^r * d where d is odd
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        # Witness loop
        import random
        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)

            if x == 1 or x == n - 1:
                continue

            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False

        return True

    def is_valid(self) -> bool:
        """
        Check if curve is non-singular (valid).

        A Weierstrass curve is non-singular iff 4a³ + 27b² ≢ 0 (mod p)

        Returns:
            True if curve is non-singular, False otherwise
        """
        # Calculate 4a³ + 27b² (mod p)
        discriminant_part = (4 * pow(self.a, 3, self.p) + 27 * pow(self.b, 2, self.p)) % self.p
        return discriminant_part != 0

    def has_point(self, x: int, y: int) -> bool:
        """
        Check if point (x, y) is on the curve.

        A point (x, y) is on the curve iff y² ≡ x³ + ax + b (mod p)

        Args:
            x: x-coordinate
            y: y-coordinate

        Returns:
            True if (x, y) is on the curve, False otherwise
        """
        x = x % self.p
        y = y % self.p

        # Check: y² ≡ x³ + ax + b (mod p)
        left = (y * y) % self.p
        right = (pow(x, 3, self.p) + self.a * x + self.b) % self.p

        return left == right

    def __str__(self) -> str:
        """Return string representation of curve."""
        return f"E: y² = x³ + {self.a}x + {self.b} (mod {self.p})"

    def __repr__(self) -> str:
        """Return detailed representation of curve."""
        return f"EllipticCurve(p={self.p}, a={self.a}, b={self.b})"

    def __eq__(self, other) -> bool:
        """Check if two curves are equal."""
        if not isinstance(other, EllipticCurve):
            return False
        return self.p == other.p and self.a == other.a and self.b == other.b


# Common pedagogical curves

CURVE_P17_A2_B2 = EllipticCurve(p=17, a=2, b=2)
"""Small pedagogical curve: y² = x³ + 2x + 2 (mod 17)"""

CURVE_P23_A1_B1 = EllipticCurve(p=23, a=1, b=1)
"""Small pedagogical curve: y² = x³ + x + 1 (mod 23)"""

CURVE_P13_A2_B2 = EllipticCurve(p=13, a=2, b=2)
"""Very small pedagogical curve: y² = x³ + 2x + 2 (mod 13)"""


# secp256k1 curve (Bitcoin/Ethereum)
SECP256K1_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
SECP256K1_A = 0x0000000000000000000000000000000000000000000000000000000000000000
SECP256K1_B = 0x0000000000000000000000000000000000000000000000000000000000000007
CURVE_SECP256K1 = EllipticCurve(p=SECP256K1_P, a=SECP256K1_A, b=SECP256K1_B)
"""secp256k1: Bitcoin/Ethereum curve"""


# NIST P-256 curve
NIST_P256_P = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
NIST_P256_A = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
NIST_P256_B = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
CURVE_NIST_P256 = EllipticCurve(p=NIST_P256_P, a=NIST_P256_A, b=NIST_P256_B)
"""NIST P-256: Standard curve"""
