"""
Tests for modular arithmetic operations.

Tests the fundamental operations needed for ECC:
- Modular inverse (extended Euclidean algorithm)
- Modular exponentiation
- Modular division
"""

import pytest
from src.arithmetic import mod_inverse, mod_pow, mod_gcd


class TestModularInverse:
    """Test modular inverse calculation."""

    def test_mod_inverse_basic(self):
        """Test basic modular inverse."""
        # 3 * 3 ≡ 1 (mod 11)
        # So inverse of 3 mod 11 is 3
        result = mod_inverse(3, 11)
        assert result == 4
        assert (3 * result) % 11 == 1

    def test_mod_inverse_simple(self):
        """Test simple modular inverse."""
        # 2 * 6 ≡ 1 (mod 11)
        result = mod_inverse(2, 11)
        assert result == 6
        assert (2 * result) % 11 == 1

    def test_mod_inverse_large_numbers(self):
        """Test modular inverse with large numbers."""
        p = 17
        for a in range(1, p):
            inv = mod_inverse(a, p)
            assert (a * inv) % p == 1, f"Failed for a={a}, p={p}"

    def test_mod_inverse_prime_field(self):
        """Test modular inverse in large prime field."""
        p = 10**9 + 7  # Large prime
        a = 12345
        inv = mod_inverse(a, p)
        assert (a * inv) % p == 1

    def test_mod_inverse_no_inverse(self):
        """Test that modular inverse raises error when gcd(a,p) != 1."""
        # 4 and 6 are not coprime
        with pytest.raises(ValueError, match="does not exist|no modular inverse"):
            mod_inverse(4, 6)

    def test_mod_inverse_zero(self):
        """Test that 0 has no modular inverse."""
        with pytest.raises(ValueError, match="does not exist|no modular inverse"):
            mod_inverse(0, 11)

    def test_mod_inverse_identity(self):
        """Test that 1 is its own inverse."""
        for p in [7, 11, 13, 17, 19, 23]:
            result = mod_inverse(1, p)
            assert result == 1


class TestModularPower:
    """Test modular exponentiation."""

    def test_mod_pow_basic(self):
        """Test basic modular exponentiation."""
        # 2^3 = 8 ≡ 3 (mod 5)
        result = mod_pow(2, 3, 5)
        assert result == 3

    def test_mod_pow_zero_exponent(self):
        """Test modular power with exponent 0."""
        # a^0 ≡ 1 (mod p) for any a
        assert mod_pow(5, 0, 7) == 1
        assert mod_pow(10, 0, 13) == 1

    def test_mod_pow_one_base(self):
        """Test modular power with base 1."""
        # 1^n ≡ 1 (mod p) for any n
        assert mod_pow(1, 100, 7) == 1
        assert mod_pow(1, 999, 13) == 1

    def test_mod_pow_fermat(self):
        """Test Fermat's Little Theorem: a^(p-1) ≡ 1 (mod p)."""
        p = 17
        for a in range(1, p):
            result = mod_pow(a, p - 1, p)
            assert result == 1, f"Fermat failed for a={a}, p={p}"

    def test_mod_pow_large_exponent(self):
        """Test modular power with large exponent."""
        result = mod_pow(2, 10**9, 10**9 + 7)
        assert 0 <= result < 10**9 + 7

    def test_mod_pow_consistency(self):
        """Test that mod_pow is consistent with naive calculation for small numbers."""
        for base in range(2, 10):
            for exp in range(1, 10):
                for mod in [7, 11, 13, 17]:
                    result = mod_pow(base, exp, mod)
                    expected = pow(base, exp, mod)
                    assert result == expected


class TestModularGCD:
    """Test greatest common divisor calculation."""

    def test_gcd_basic(self):
        """Test basic GCD calculation."""
        assert mod_gcd(12, 8) == 4
        assert mod_gcd(48, 18) == 6

    def test_gcd_coprime(self):
        """Test GCD of coprime numbers."""
        assert mod_gcd(5, 7) == 1
        assert mod_gcd(11, 13) == 1

    def test_gcd_one_divides_other(self):
        """Test GCD when one number divides the other."""
        assert mod_gcd(12, 4) == 4
        assert mod_gcd(25, 5) == 5

    def test_gcd_zero(self):
        """Test GCD with zero."""
        assert mod_gcd(5, 0) == 5
        assert mod_gcd(0, 7) == 7

    def test_gcd_same_number(self):
        """Test GCD of same number."""
        assert mod_gcd(7, 7) == 7
        assert mod_gcd(100, 100) == 100

    def test_gcd_order_independent(self):
        """Test that GCD(a,b) = GCD(b,a)."""
        assert mod_gcd(12, 8) == mod_gcd(8, 12)
        assert mod_gcd(48, 18) == mod_gcd(18, 48)


class TestModularArithmetic:
    """Integration tests for modular arithmetic."""

    def test_modular_division(self):
        """Test modular division (multiplication by inverse)."""
        p = 17
        a = 5
        b = 3
        # (a / b) mod p = (a * b^-1) mod p
        b_inv = mod_inverse(b, p)
        result = (a * b_inv) % p
        # Verify: result * b ≡ a (mod p)
        assert (result * b) % p == a

    def test_chain_operations(self):
        """Test chaining multiple modular operations."""
        p = 23
        # ((5 * 3) + (7 * 11)) mod p
        result = (5 * 3 + 7 * 11) % p
        assert 0 <= result < p

    def test_inverse_of_inverse(self):
        """Test that inverse of inverse returns original number."""
        p = 19
        a = 5
        inv_a = mod_inverse(a, p)
        inv_inv_a = mod_inverse(inv_a, p)
        assert inv_inv_a == a


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
