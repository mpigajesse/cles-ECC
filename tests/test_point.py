"""
Tests for points on elliptic curves.

Tests the Point class:
- Point representation (x, y)
- Point at infinity (identity element)
- Point equality
- Membership verification
"""

import pytest
from src.curve import EllipticCurve
from src.point import Point, Point_At_Infinity


class TestPointCreation:
    """Test point creation and validation."""

    def test_create_valid_point(self):
        """Test creating a valid point on the curve."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # Find a point on the curve by brute force
        # For y² = x³ + 2x + 2 (mod 17)
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    point = Point(curve, x, y)
                    assert point.x == x
                    assert point.y == y
                    assert point.curve == curve
                    return
        pytest.skip("No point found on test curve")

    def test_create_invalid_point(self):
        """Test that invalid point raises error."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # (1, 1) is not on y² = x³ + 2x + 2 (mod 17)
        # 1² = 1 but 1³ + 2(1) + 2 = 5
        with pytest.raises(ValueError, match="not on curve"):
            Point(curve, 1, 1)

    def test_point_coordinates_normalized(self):
        """Test that coordinates are normalized to [0, p)."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # Find a point on curve
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    # Create point with coordinates outside [0, p)
                    point = Point(curve, x + 17, y + 34)
                    assert 0 <= point.x < curve.p
                    assert 0 <= point.y < curve.p
                    return
        pytest.skip("No point found on test curve")

    def test_point_zero_coordinate(self):
        """Test point with zero coordinates."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # Check if (0, y) is on curve for some y
        # y² = 0³ + 2(0) + 2 = 2
        # Need to find sqrt(2) mod 17
        for y in range(17):
            if (y * y) % 17 == 2:
                point = Point(curve, 0, y)
                assert point.x == 0
                assert point.y == y
                return
        pytest.skip("No point with x=0 found")


class TestPointAtInfinity:
    """Test the point at infinity (identity element)."""

    def test_point_at_infinity_creation(self):
        """Test creating the point at infinity."""
        curve = EllipticCurve(p=17, a=2, b=2)
        O = Point_At_Infinity(curve)
        assert O.curve == curve
        assert O.is_at_infinity()

    def test_point_at_infinity_uniqueness(self):
        """Test that point at infinity is unique for a curve."""
        curve = EllipticCurve(p=17, a=2, b=2)
        O1 = Point_At_Infinity(curve)
        O2 = Point_At_Infinity(curve)
        assert O1 == O2

    def test_point_at_infinity_equality(self):
        """Test equality with point at infinity."""
        curve = EllipticCurve(p=17, a=2, b=2)
        O = Point_At_Infinity(curve)
        assert O.is_at_infinity()

    def test_point_at_infinity_string(self):
        """Test string representation of point at infinity."""
        curve = EllipticCurve(p=17, a=2, b=2)
        O = Point_At_Infinity(curve)
        s = str(O)
        assert "infinity" in s.lower() or "O" in s


class TestPointEquality:
    """Test point equality and comparison."""

    def test_equal_points(self):
        """Test that identical points are equal."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # Find a point
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P1 = Point(curve, x, y)
                    P2 = Point(curve, x, y)
                    assert P1 == P2
                    return
        pytest.skip("No point found on test curve")

    def test_different_x_not_equal(self):
        """Test that points with different x are not equal."""
        curve = EllipticCurve(p=17, a=2, b=2)
        points = []
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    points.append(Point(curve, x, y))
                    if len(points) >= 2:
                        break
            if len(points) >= 2:
                break

        if len(points) >= 2:
            assert points[0] != points[1]

    def test_different_y_not_equal(self):
        """Test that points with different y are not equal."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # Find a point with two different y values (should be rare)
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            y_coords = []
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    y_coords.append(y)
            if len(y_coords) == 2:
                P1 = Point(curve, x, y_coords[0])
                P2 = Point(curve, x, y_coords[1])
                assert P1 != P2
                return
        pytest.skip("No point with two y coordinates found")

    def test_point_not_equal_to_other_types(self):
        """Test point not equal to non-point types."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # Find a point
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P = Point(curve, x, y)
                    assert P != (x, y)
                    assert P != [x, y]
                    assert P != "point"
                    return
        pytest.skip("No point found on test curve")


class TestPointRepresentation:
    """Test string representation of points."""

    def test_point_string_format(self):
        """Test point string representation."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # Find a point
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P = Point(curve, x, y)
                    s = str(P)
                    assert str(x) in s
                    assert str(y) in s
                    return
        pytest.skip("No point found on test curve")

    def test_point_repr(self):
        """Test point repr."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # Find a point
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P = Point(curve, x, y)
                    r = repr(P)
                    assert "Point" in r or "(" in r
                    return
        pytest.skip("No point found on test curve")


class TestPointProperties:
    """Test point properties and methods."""

    def test_point_on_curve_property(self):
        """Test is_on_curve method."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # Find a point
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P = Point(curve, x, y)
                    assert P.is_on_curve()
                    return
        pytest.skip("No point found on test curve")

    def test_point_not_at_infinity_by_default(self):
        """Test that regular points are not at infinity."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # Find a point
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P = Point(curve, x, y)
                    assert not P.is_at_infinity()
                    return
        pytest.skip("No point found on test curve")

    def test_point_curve_property(self):
        """Test point's curve attribute."""
        curve = EllipticCurve(p=17, a=2, b=2)
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P = Point(curve, x, y)
                    assert P.curve == curve
                    return
        pytest.skip("No point found on test curve")


class TestPointNegation:
    """Test point negation (additive inverse)."""

    def test_point_negation(self):
        """Test negating a point."""
        curve = EllipticCurve(p=17, a=2, b=2)
        # Find a point
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P = Point(curve, x, y)
                    neg_P = P.negate()
                    # Negation should flip y-coordinate
                    assert neg_P.x == P.x
                    assert neg_P.y == (-P.y) % curve.p
                    return
        pytest.skip("No point found on test curve")

    def test_negation_of_negation(self):
        """Test that negating twice gives the original."""
        curve = EllipticCurve(p=17, a=2, b=2)
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P = Point(curve, x, y)
                    assert P == P.negate().negate()
                    return
        pytest.skip("No point found on test curve")


class TestPointSecp256k1:
    """Test points on secp256k1."""

    def test_generator_secp256k1(self):
        """Test known generator point of secp256k1."""
        from src.curve import CURVE_SECP256K1

        Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

        # This should not raise
        G = Point(CURVE_SECP256K1, Gx, Gy)
        assert G.x == Gx
        assert G.y == Gy


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
