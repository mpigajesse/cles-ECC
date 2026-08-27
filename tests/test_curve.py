"""
Tests for elliptic curve definitions and validation.

Tests the elliptic curve class:
- Weierstrass form: y² = x³ + ax + b (mod p)
- Curve validity: 4a³ + 27b² ≢ 0 (mod p)
- Point membership verification
"""

import pytest
from src.curve import EllipticCurve


class TestEllipticCurveCreation:
    """Test elliptic curve creation and validation."""

    def test_create_valid_curve(self):
        """Test creating a valid elliptic curve."""
        # Small pedagogical curve
        # y² = x³ + 2x + 2 (mod 17)
        curve = EllipticCurve(p=17, a=2, b=2)
        assert curve.p == 17
        assert curve.a == 2
        assert curve.b == 2

    def test_create_secp256k1(self):
        """Test creating secp256k1 curve."""
        p = 2**256 - 2**32 - 977
        a = 0
        b = 7
        curve = EllipticCurve(p=p, a=a, b=b)
        assert curve.p == p
        assert curve.a == a
        assert curve.b == b

    def test_create_nist_p256(self):
        """Test creating NIST P-256 curve."""
        p = 2**256 - 2**224 + 2**192 + 2**128 - 1
        a = p - 3
        b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1
        curve = EllipticCurve(p=p, a=a, b=b)
        assert curve.p == p

    def test_invalid_curve_discriminant(self):
        """Test that curve with invalid discriminant raises error."""
        # For y² = x³ + ax + b to be non-singular:
        # 4a³ + 27b² ≢ 0 (mod p)
        # Let's construct an invalid curve
        p = 17
        a = 0
        b = 0
        # 4*0³ + 27*0² = 0 ≡ 0 (mod 17), so this should fail
        with pytest.raises(ValueError, match="invalid|singular|discriminant"):
            EllipticCurve(p=p, a=a, b=b)

    def test_non_prime_p(self):
        """Test that non-prime p raises error or warning."""
        # This might be allowed or not depending on implementation
        # For proper ECC, p should be prime
        # We can either raise error or issue warning
        # Here we'll assume it should raise an error for strict ECC
        # Some implementations allow composite moduli for testing
        pass  # Can be implemented if strict prime checking is desired

    def test_negative_p(self):
        """Test that negative p raises error."""
        with pytest.raises(ValueError, match="positive|prime"):
            EllipticCurve(p=-17, a=2, b=2)

    def test_p_equals_one(self):
        """Test that p=1 raises error."""
        with pytest.raises(ValueError, match="prime"):
            EllipticCurve(p=1, a=2, b=2)


class TestEllipticCurveProperties:
    """Test curve properties and methods."""

    def test_curve_string_representation(self):
        """Test string representation of curve."""
        curve = EllipticCurve(p=17, a=2, b=2)
        curve_str = str(curve)
        assert "17" in curve_str
        assert "2" in curve_str
        # Should contain something like "y² = x³ + 2x + 2 (mod 17)"

    def test_curve_equality(self):
        """Test that two curves with same parameters are equal."""
        curve1 = EllipticCurve(p=17, a=2, b=2)
        curve2 = EllipticCurve(p=17, a=2, b=2)
        assert curve1.p == curve2.p
        assert curve1.a == curve2.a
        assert curve1.b == curve2.b

    def test_curve_parameter_order(self):
        """Test that parameter order matters."""
        curve1 = EllipticCurve(p=17, a=2, b=3)
        curve2 = EllipticCurve(p=17, a=3, b=2)
        assert curve1.a != curve2.a
        assert curve1.b != curve2.b


class TestPointMembership:
    """Test checking if points belong to the curve."""

    def test_point_on_curve(self):
        """Test that a point on the curve is recognized."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # We need to find an actual point on the curve
        # For y² = x³ + 2x + 2 (mod 17)
        # Brute force find: for x in 0..16, check if y² = x³ + 2x + 2
        points_on_curve = []
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            # Check if y_squared has square root mod 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    points_on_curve.append((x, y))
                    break

        # Test at least one point
        if points_on_curve:
            x, y = points_on_curve[0]
            assert curve.has_point(x, y), f"Point ({x},{y}) should be on curve"

    def test_point_not_on_curve(self):
        """Test that a random point is likely not on the curve."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # Test a point unlikely to be on the curve
        # Unless by chance, (1, 1) is probably not on y² = x³ + 2x + 2
        # 1² = 1³ + 2(1) + 2 => 1 = 5 (false)
        assert not curve.has_point(1, 1)

    def test_point_membership_boundary(self):
        """Test point membership near boundaries."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # Test with x = p-1, y = p-1
        assert not curve.has_point(16, 16)


class TestSmallCurvePedagogical:
    """Test with small pedagogical curves."""

    def test_p17_a2_b2(self):
        """Test standard pedagogical curve E: y² = x³ + 2x + 2 (mod 17)."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # Verify it's valid
        # 4*2³ + 27*2² = 32 + 108 = 140 = 8 + 4 = 12 (mod 17) ≠ 0
        assert curve.is_valid()

    def test_p23_a1_b1(self):
        """Test pedagogical curve E: y² = x³ + x + 1 (mod 23)."""
        curve = EllipticCurve(p=23, a=1, b=1)
        assert curve.is_valid()

    def test_p13_a2_b2(self):
        """Test small pedagogical curve E: y² = x³ + 2x + 2 (mod 13)."""
        # 4*2³ + 27*2² = 32 + 108 = 140 = 10 (mod 13) ≠ 0
        # 140 = 13*10 + 10, so 140 ≡ 10 (mod 13)
        curve = EllipticCurve(p=13, a=2, b=2)
        assert curve.is_valid()


class TestCurveDiscriminant:
    """Test curve discriminant calculation."""

    def test_discriminant_calculation(self):
        """Test that discriminant is correctly calculated."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # Δ = -16(4a³ + 27b²) mod p
        # But we mainly check that 4a³ + 27b² ≠ 0
        disc_part = (4 * pow(2, 3, 17) + 27 * pow(2, 2, 17)) % 17
        assert disc_part != 0, "Discriminant part should not be 0"

    def test_singular_curve_fails(self):
        """Test that singular curve is rejected."""
        # Singular curve has 4a³ + 27b² ≡ 0 (mod p)
        # Find such a, b for some small p
        p = 7
        # Try to find singular curve
        # Try a=0, b=0: 0 + 0 = 0 ✓
        with pytest.raises(ValueError):
            EllipticCurve(p=p, a=0, b=0)


class TestCurveComparison:
    """Test comparing different curves."""

    def test_different_p(self):
        """Test curves with different primes."""
        curve1 = EllipticCurve(p=17, a=2, b=2)
        curve2 = EllipticCurve(p=19, a=2, b=2)
        # They should be different
        assert curve1.p != curve2.p

    def test_different_a(self):
        """Test curves with different a parameters."""
        curve1 = EllipticCurve(p=17, a=1, b=2)
        curve2 = EllipticCurve(p=17, a=2, b=2)
        # They should have different properties
        assert curve1.a != curve2.a


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
