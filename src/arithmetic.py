"""
Modular arithmetic operations for elliptic curve cryptography.

This module implements fundamental arithmetic operations needed for ECC:
- Extended Euclidean algorithm
- Modular inverse
- Modular exponentiation
- Greatest common divisor
"""


def mod_gcd(a: int, b: int) -> int:
    """
    Calculate greatest common divisor using Euclidean algorithm.

    Args:
        a: First integer
        b: Second integer

    Returns:
        GCD of a and b

    Example:
        >>> mod_gcd(48, 18)
        6
    """
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> tuple:
    """
    Extended Euclidean algorithm.

    Returns (gcd, x, y) such that: a*x + b*y = gcd(a, b)

    Args:
        a: First integer
        b: Second integer

    Returns:
        Tuple (gcd, x, y) where a*x + b*y = gcd(a, b)

    Example:
        >>> gcd, x, y = extended_gcd(10, 6)
        >>> gcd
        2
        >>> 10*x + 6*y == 2
        True
    """
    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = extended_gcd(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return gcd, x, y


def mod_inverse(a: int, m: int) -> int:
    """
    Calculate modular multiplicative inverse.

    Finds x such that: a * x ≡ 1 (mod m)

    Uses extended Euclidean algorithm.
    Only works if gcd(a, m) = 1 (a and m are coprime).

    Args:
        a: The number to find inverse of
        m: The modulus (usually a prime p)

    Returns:
        x such that (a * x) % m == 1

    Raises:
        ValueError: If no modular inverse exists (gcd(a, m) != 1)

    Example:
        >>> mod_inverse(3, 11)
        4
        >>> (3 * 4) % 11
        1
    """
    if a == 0:
        raise ValueError(f"Modular inverse of 0 mod {m} does not exist: gcd(0, {m}) != 1")

    gcd, x, _ = extended_gcd(a % m, m)

    if gcd != 1:
        raise ValueError(
            f"Modular inverse of {a} mod {m} does not exist: gcd({a}, {m}) = {gcd} != 1"
        )

    return x % m


def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Fast modular exponentiation.

    Calculate base^exp mod mod efficiently using binary exponentiation.

    Args:
        base: The base
        exp: The exponent
        mod: The modulus

    Returns:
        (base^exp) mod mod

    Example:
        >>> mod_pow(2, 10, 1000)
        24
        >>> 2**10 % 1000
        24
    """
    # Python's built-in pow is highly optimized
    # Using it instead of re-implementing binary exponentiation
    return pow(base, exp, mod)


def mod_add(a: int, b: int, mod: int) -> int:
    """
    Modular addition.

    Args:
        a: First number
        b: Second number
        mod: The modulus

    Returns:
        (a + b) mod mod
    """
    return (a + b) % mod


def mod_sub(a: int, b: int, mod: int) -> int:
    """
    Modular subtraction.

    Args:
        a: First number
        b: Second number
        mod: The modulus

    Returns:
        (a - b) mod mod
    """
    return (a - b) % mod


def mod_mul(a: int, b: int, mod: int) -> int:
    """
    Modular multiplication.

    Args:
        a: First number
        b: Second number
        mod: The modulus

    Returns:
        (a * b) mod mod
    """
    return (a * b) % mod


def mod_div(a: int, b: int, mod: int) -> int:
    """
    Modular division.

    Calculate a / b mod mod = a * b^(-1) mod mod

    Args:
        a: Dividend
        b: Divisor (must be coprime with mod)
        mod: The modulus

    Returns:
        (a / b) mod mod = (a * b^(-1)) mod mod

    Raises:
        ValueError: If b and mod are not coprime
    """
    b_inv = mod_inverse(b, mod)
    return (a * b_inv) % mod


class ModularArithmetic:
    """
    Helper class for modular arithmetic operations with a fixed modulus.

    This class encapsulates a prime modulus and provides methods for
    arithmetic operations in that field.
    """

    def __init__(self, prime: int):
        """
        Initialize with a prime modulus.

        Args:
            prime: The prime modulus for all operations
        """
        if not self._is_prime(prime):
            raise ValueError(f"{prime} is not prime")
        self.prime = prime

    @staticmethod
    def _is_prime(n: int, k: int = 10) -> bool:
        """
        Miller-Rabin primality test.

        Args:
            n: Number to test
            k: Number of test iterations

        Returns:
            True if probably prime, False if definitely composite
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False

        # Write n-1 as 2^r * d
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

    def add(self, a: int, b: int) -> int:
        """Add two numbers modulo prime."""
        return mod_add(a, b, self.prime)

    def sub(self, a: int, b: int) -> int:
        """Subtract two numbers modulo prime."""
        return mod_sub(a, b, self.prime)

    def mul(self, a: int, b: int) -> int:
        """Multiply two numbers modulo prime."""
        return mod_mul(a, b, self.prime)

    def div(self, a: int, b: int) -> int:
        """Divide two numbers modulo prime."""
        return mod_div(a, b, self.prime)

    def inv(self, a: int) -> int:
        """Calculate modular inverse."""
        return mod_inverse(a, self.prime)

    def pow(self, base: int, exp: int) -> int:
        """Calculate modular exponentiation."""
        return mod_pow(base, exp, self.prime)
