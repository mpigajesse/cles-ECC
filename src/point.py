"""
Points on elliptic curves.

Represents points on curves of the form:
    E: y² ≡ x³ + ax + b (mod p)

Includes the point at infinity (identity element for point addition).
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.curve import EllipticCurve


class Point:
    """
    A point on an elliptic curve.

    Represents a point (x, y) on the curve E: y² = x³ + ax + b (mod p)

    Attributes:
        curve: The elliptic curve this point is on
        x: x-coordinate
        y: y-coordinate
    """

    def __init__(self, curve: "EllipticCurve", x: int, y: int):
        """
        Create a point on the curve.

        Validates that the point is on the curve.

        Args:
            curve: The elliptic curve
            x: x-coordinate
            y: y-coordinate

        Raises:
            ValueError: If the point is not on the curve
        """
        self.curve = curve
        self.x = x % curve.p
        self.y = y % curve.p

        # Verify the point is on the curve
        if not self.is_on_curve():
            raise ValueError(
                f"Point ({x}, {y}) is not on curve {curve}: "
                f"{self.y}² ≠ {self.x}³ + {self.curve.a}·{self.x} + {self.curve.b} (mod {self.curve.p})"
            )

    def is_on_curve(self) -> bool:
        """
        Check if this point is on its curve.

        Verifies: y² ≡ x³ + ax + b (mod p)

        Returns:
            True if point is on the curve, False otherwise
        """
        return self.curve.has_point(self.x, self.y)

    def is_at_infinity(self) -> bool:
        """
        Check if this point is the point at infinity.

        Regular points are never at infinity.

        Returns:
            False (regular points are not at infinity)
        """
        return False

    def negate(self) -> "Point":
        """
        Return the additive inverse of this point.

        On an elliptic curve, the inverse of P = (x, y) is -P = (x, -y).

        Returns:
            Point(-P)
        """
        neg_y = (-self.y) % self.curve.p
        return Point(self.curve, self.x, neg_y)

    def __eq__(self, other) -> bool:
        """
        Check if two points are equal.

        Two points are equal if they have the same coordinates and are on the same curve.

        Args:
            other: Point to compare with

        Returns:
            True if points are equal, False otherwise
        """
        if not isinstance(other, Point):
            return False
        return (
            self.curve == other.curve
            and self.x == other.x
            and self.y == other.y
        )

    def __ne__(self, other) -> bool:
        """Check if two points are not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """
        Hash a point for use in sets and dicts.

        Allows points to be used as dictionary keys.

        Returns:
            Hash value
        """
        return hash((self.curve.p, self.curve.a, self.curve.b, self.x, self.y))

    def __str__(self) -> str:
        """Return string representation of point."""
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        """Return detailed representation of point."""
        return f"Point({self.x}, {self.y}) on {self.curve}"


class Point_At_Infinity:
    """
    The point at infinity (identity element for point addition).

    In projective coordinates, the point at infinity serves as the identity:
        P + O = P for all P
        P + (-P) = O

    For a given curve, there is exactly one point at infinity.
    """

    def __init__(self, curve: "EllipticCurve"):
        """
        Create the point at infinity on a curve.

        Args:
            curve: The elliptic curve
        """
        self.curve = curve

    def is_on_curve(self) -> bool:
        """
        Check if point at infinity is on the curve.

        By definition, it is.

        Returns:
            True
        """
        return True

    def is_at_infinity(self) -> bool:
        """
        Check if this is the point at infinity.

        Returns:
            True
        """
        return True

    def negate(self) -> "Point_At_Infinity":
        """
        Return the additive inverse of the point at infinity.

        -O = O (it's its own inverse).

        Returns:
            Self
        """
        return self

    def __eq__(self, other) -> bool:
        """
        Check if two points at infinity are equal.

        Point at infinity is only equal to other points at infinity on the same curve.

        Args:
            other: Object to compare with

        Returns:
            True if both are points at infinity on the same curve
        """
        if not isinstance(other, Point_At_Infinity):
            return False
        return self.curve == other.curve

    def __ne__(self, other) -> bool:
        """Check if not equal."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """
        Hash the point at infinity.

        Allows it to be used in sets and dicts.

        Returns:
            Hash value
        """
        return hash(("Point_At_Infinity", self.curve.p, self.curve.a, self.curve.b))

    def __str__(self) -> str:
        """Return string representation."""
        return "O (point at infinity)"

    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"Point_At_Infinity on {self.curve}"


def is_point(obj) -> bool:
    """
    Check if an object is a point (either regular or at infinity).

    Args:
        obj: Object to check

    Returns:
        True if obj is a Point or Point_At_Infinity
    """
    return isinstance(obj, (Point, Point_At_Infinity))
