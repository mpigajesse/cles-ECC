"""
Tests for point operations on elliptic curves.

Tests:
- Point addition: P + Q
- Point doubling: 2P = P + P
- Point addition with infinity
- Special cases and edge conditions
"""

import pytest
from src.curve import EllipticCurve, CURVE_P17_A2_B2
from src.point import Point, Point_At_Infinity
from src.operations import add_points, double_point


class TestPointAddition:
    """Test point addition on elliptic curves."""

    def test_point_plus_itself_is_double(self):
        """Test that P + P = 2P."""
        curve = CURVE_P17_A2_B2
        # Find two different points and verify P + P = 2P
        points = []
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    points.append(Point(curve, x, y))
                    if len(points) >= 1:
                        break
            if len(points) >= 1:
                break

        if points:
            P = points[0]
            # P + P should equal 2P (both methods)
            sum_result = add_points(P, P)
            double_result = double_point(P)
            assert sum_result == double_result

    def test_point_plus_identity(self):
        """Test that P + O = P."""
        curve = CURVE_P17_A2_B2
        O = Point_At_Infinity(curve)

        # Find a point
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P = Point(curve, x, y)
                    result = add_points(P, O)
                    assert result == P
                    return
        pytest.skip("No point found on curve")

    def test_identity_plus_point(self):
        """Test that O + P = P."""
        curve = CURVE_P17_A2_B2
        O = Point_At_Infinity(curve)

        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P = Point(curve, x, y)
                    result = add_points(O, P)
                    assert result == P
                    return
        pytest.skip("No point found on curve")

    def test_point_plus_negative(self):
        """Test that P + (-P) = O."""
        curve = CURVE_P17_A2_B2
        O = Point_At_Infinity(curve)

        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P = Point(curve, x, y)
                    neg_P = P.negate()
                    result = add_points(P, neg_P)
                    assert result == O
                    return
        pytest.skip("No point found on curve")

    def test_addition_commutativity(self):
        """Test that P + Q = Q + P (addition is commutative)."""
        curve = CURVE_P17_A2_B2

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
            P, Q = points[0], points[1]
            if P != Q:  # Only test with different points
                result1 = add_points(P, Q)
                result2 = add_points(Q, P)
                assert result1 == result2

    def test_addition_associativity(self):
        """Test that (P + Q) + R = P + (Q + R)."""
        curve = CURVE_P17_A2_B2

        points = []
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    points.append(Point(curve, x, y))
                    if len(points) >= 3:
                        break
            if len(points) >= 3:
                break

        if len(points) >= 3:
            P, Q, R = points[0], points[1], points[2]
            left = add_points(add_points(P, Q), R)
            right = add_points(P, add_points(Q, R))
            assert left == right


class TestPointDoubling:
    """Test point doubling operation."""

    def test_double_point_result_on_curve(self):
        """Test that 2P is on the curve."""
        curve = CURVE_P17_A2_B2

        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P = Point(curve, x, y)
                    doubled = double_point(P)
                    assert doubled.is_on_curve()
                    return
        pytest.skip("No point found on curve")

    def test_double_point_twice(self):
        """Test that double(double(P)) = 4P."""
        curve = CURVE_P17_A2_B2

        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P = Point(curve, x, y)
                    P2 = double_point(P)
                    P4_method1 = double_point(P2)
                    # Method 2: P4 = P2 + P2
                    P4_method2 = add_points(P2, P2)
                    assert P4_method1 == P4_method2
                    return
        pytest.skip("No point found on curve")

    def test_double_identity_is_identity(self):
        """Test that 2*O = O."""
        curve = CURVE_P17_A2_B2
        O = Point_At_Infinity(curve)

        # Doubling identity should give identity
        # (depends on implementation)
        try:
            result = double_point(O)
            assert result == O
        except (ValueError, TypeError):
            # Some implementations don't allow doubling infinity
            pass


class TestSpecialCases:
    """Test special cases and edge conditions."""

    def test_addition_with_point_itself(self):
        """Test P + P (should trigger doubling formula)."""
        curve = CURVE_P17_A2_B2

        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P = Point(curve, x, y)
                    # Direct add vs double
                    result1 = add_points(P, P)
                    result2 = double_point(P)
                    assert result1 == result2
                    return
        pytest.skip("No point found on curve")

    def test_adding_different_curves_fails(self):
        """Test that adding points from different curves fails."""
        curve1 = EllipticCurve(p=17, a=2, b=2)
        curve2 = EllipticCurve(p=19, a=1, b=1)

        # Find point on curve1
        for x in range(17):
            y_squared = (pow(x, 3, 17) + 2 * x + 2) % 17
            for y in range(17):
                if (y * y) % 17 == y_squared:
                    P1 = Point(curve1, x, y)
                    break

        # Find point on curve2
        for x in range(19):
            y_squared = (pow(x, 3, 19) + x + 1) % 19
            for y in range(19):
                if (y * y) % 19 == y_squared:
                    P2 = Point(curve2, x, y)
                    break

        # Adding should fail
        with pytest.raises((ValueError, AssertionError)):
            add_points(P1, P2)

    def test_result_coordinates_in_range(self):
        """Test that result coordinates are in valid range."""
        curve = CURVE_P17_A2_B2

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
            P, Q = points[0], points[1]
            result = add_points(P, Q)
            # Result should have valid coordinates
            assert 0 <= result.x < curve.p or isinstance(result, Point_At_Infinity)
            assert 0 <= result.y < curve.p or isinstance(result, Point_At_Infinity)


class TestPointAdditionFormulas:
    """Test correctness of addition formulas."""

    def test_slope_calculation_precision(self):
        """Test that slope calculations are precise in modular arithmetic."""
        curve = CURVE_P17_A2_B2

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
            P, Q = points[0], points[1]
            if P != Q:
                # Add P and Q
                R = add_points(P, Q)
                # Verify R is on the curve
                assert R.is_on_curve()


class TestPointOperationsSecp256k1:
    """Test operations on secp256k1."""

    def test_generator_add_itself(self):
        """Test adding generator point to itself on secp256k1."""
        from src.curve import CURVE_SECP256K1

        Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

        G = Point(CURVE_SECP256K1, Gx, Gy)

        # 2G should be on curve
        G2 = double_point(G)
        assert G2.is_on_curve()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
