"""
Point operations on elliptic curves.

Implements:
- Point addition: P + Q
- Point doubling: 2P = P + P
- Handling of special cases (point at infinity, additive inverses)

Mathematical background:

For an elliptic curve E: y² = x³ + ax + b (mod p)

ADDITION (P ≠ Q):
  λ = (y₂ - y₁) / (x₂ - x₁) mod p
  x₃ = λ² - x₁ - x₂ mod p
  y₃ = λ(x₁ - x₃) - y₁ mod p

DOUBLING (P = Q and y₁ ≠ 0):
  λ = (3x₁² + a) / (2y₁) mod p
  x₃ = λ² - 2x₁ mod p
  y₃ = λ(x₁ - x₃) - y₁ mod p

SPECIAL CASES:
  P + O = P (O is identity)
  P + (-P) = O (inverse)
  P + P = 2P (doubling)
"""

from src.point import Point, Point_At_Infinity
from src.arithmetic import mod_inverse, mod_div


def add_points(P, Q) -> "Point | Point_At_Infinity":
    """
    Add two points on an elliptic curve.

    Implements: R = P + Q on curve E: y² = x³ + ax + b (mod p)

    Args:
        P: First point (Point or Point_At_Infinity)
        Q: Second point (Point or Point_At_Infinity)

    Returns:
        P + Q as a Point or Point_At_Infinity

    Raises:
        ValueError: If points are on different curves
    """
    # Handle point at infinity cases
    if isinstance(P, Point_At_Infinity):
        return Q
    if isinstance(Q, Point_At_Infinity):
        return P

    # Both are regular points
    assert isinstance(P, Point) and isinstance(Q, Point)

    # Verify same curve
    if P.curve != Q.curve:
        raise ValueError("Cannot add points on different curves")

    curve = P.curve
    p = curve.p

    # Case 1: Same x-coordinate
    if P.x == Q.x:
        # Case 1a: P = Q (use doubling formula)
        if P.y == Q.y:
            return double_point(P)
        # Case 1b: P = -Q (points are inverses)
        else:
            return Point_At_Infinity(curve)

    # Case 2: Different x-coordinates (use addition formula)
    # λ = (y₂ - y₁) / (x₂ - x₁) mod p
    dx = (Q.x - P.x) % p
    dy = (Q.y - P.y) % p

    dx_inv = mod_inverse(dx, p)
    lam = (dy * dx_inv) % p

    # x₃ = λ² - x₁ - x₂ mod p
    x3 = (lam * lam - P.x - Q.x) % p

    # y₃ = λ(x₁ - x₃) - y₁ mod p
    y3 = (lam * (P.x - x3) - P.y) % p

    return Point(curve, x3, y3)


def double_point(P) -> "Point | Point_At_Infinity":
    """
    Double a point on an elliptic curve.

    Implements: R = 2P = P + P on curve E: y² = x³ + ax + b (mod p)

    Args:
        P: Point to double (Point or Point_At_Infinity)

    Returns:
        2P as a Point or Point_At_Infinity

    Raises:
        ValueError: If point is at infinity or has y-coordinate 0
    """
    # Point at infinity case
    if isinstance(P, Point_At_Infinity):
        return P

    # Ensure P is a Point (not Point_At_Infinity)
    if not isinstance(P, Point):
        return P  # Return as-is if it's something unexpected

    curve = P.curve
    p = curve.p

    # Special case: y-coordinate is 0
    # 2P = (x, 0) + (x, 0) = point at infinity
    if P.y == 0:
        return Point_At_Infinity(curve)

    # Doubling formula:
    # λ = (3x₁² + a) / (2y₁) mod p
    numerator = (3 * P.x * P.x + curve.a) % p
    denominator = (2 * P.y) % p

    denominator_inv = mod_inverse(denominator, p)
    lam = (numerator * denominator_inv) % p

    # x₃ = λ² - 2x₁ mod p
    x3 = (lam * lam - 2 * P.x) % p

    # y₃ = λ(x₁ - x₃) - y₁ mod p
    y3 = (lam * (P.x - x3) - P.y) % p

    return Point(curve, x3, y3)


def scalar_mult_naive(P, d: int) -> "Point | Point_At_Infinity":
    """
    Multiply a point by a scalar using naive method.

    Computes: R = d × P = P + P + ... + P (d times)

    This is the simplest but slowest method: O(d) operations.
    Used for educational purposes to understand the concept.

    Args:
        P: Point to multiply
        d: Scalar (non-negative integer)

    Returns:
        d × P

    Example:
        >>> R = scalar_mult_naive(G, 5)  # R = G + G + G + G + G
    """
    if isinstance(P, Point_At_Infinity):
        return P

    if d == 0:
        return Point_At_Infinity(P.curve)

    if d < 0:
        # For negative scalars, use inverse of point
        P_neg = P.negate()
        return scalar_mult_naive(P_neg, -d)

    # Naive method: repeated addition
    result = Point_At_Infinity(P.curve)
    for _ in range(d):
        result = add_points(result, P)

    return result


def scalar_mult_binary(P, d: int) -> "Point | Point_At_Infinity":
    """
    Multiply a point by a scalar using binary (double-and-add) method.

    Computes: R = d × P using binary decomposition.

    This is much faster: O(log d) group operations.
    Used for realistic cryptography applications.

    Algorithm:
    1. Write d in binary: d = d_n...d_1d_0
    2. Result starts at O (point at infinity)
    3. For each bit (from high to low):
       - Double current result
       - If bit is 1, add P

    Example:
        d = 13 = 1101₂
        13·P = (((P + P) + P) + P) + P)
        = (((2P + P)·2) + P)
        = ((3P·2) + P)
        = (6P + P)
        = 7P

    Better breakdown:
        13 = 8 + 4 + 1
        13·P = 8P + 4P + P

    Args:
        P: Point to multiply
        d: Scalar (non-negative integer)

    Returns:
        d × P

    Complexity:
        Time: O(log d) point operations
        Space: O(1)
    """
    if isinstance(P, Point_At_Infinity):
        return P

    if d == 0:
        return Point_At_Infinity(P.curve)

    if d < 0:
        P_neg = P.negate()
        return scalar_mult_binary(P_neg, -d)

    # Convert d to binary
    binary = bin(d)[2:]  # Remove '0b' prefix

    # Start with first bit
    result = Point_At_Infinity(P.curve)

    # Process each bit
    for i, bit in enumerate(binary):
        # For the first bit (i=0)
        if i == 0:
            # If first bit is 1, result = P
            if bit == "1":
                result = P
            # If first bit is 0, result stays as Point_At_Infinity
        else:
            # For subsequent bits: always double first
            result = double_point(result)

            # If bit is 1, add P
            if bit == "1":
                result = add_points(result, P)

    return result


def scalar_mult(P, d: int, use_binary: bool = True) -> "Point | Point_At_Infinity":
    """
    Multiply a point by a scalar.

    Chooses between naive and binary methods based on parameters.

    Args:
        P: Point to multiply
        d: Scalar (integer)
        use_binary: If True, use fast binary method; if False, use naive method

    Returns:
        d × P

    Example:
        >>> G = Point(curve, Gx, Gy)
        >>> Q = scalar_mult(G, 12345)  # Q = 12345·G
    """
    if use_binary:
        return scalar_mult_binary(P, d)
    else:
        return scalar_mult_naive(P, d)


def scalar_mult_with_steps(P, d: int, verbose: bool = True) -> tuple:
    """
    Multiply a point by a scalar and return intermediate steps.

    Useful for educational purposes to see how scalar multiplication works.

    Args:
        P: Point to multiply
        d: Scalar
        verbose: If True, print steps

    Returns:
        Tuple (result, steps) where steps is list of intermediate results
    """
    if isinstance(P, Point_At_Infinity):
        return P, [P]

    if d == 0:
        O = Point_At_Infinity(P.curve)
        return O, [O]

    if d < 0:
        P_neg = P.negate()
        return scalar_mult_with_steps(P_neg, -d, verbose)

    # Use binary method with tracking
    binary = bin(d)[2:]
    steps = []

    result = Point_At_Infinity(P.curve)
    steps.append(result)

    for i, bit in enumerate(binary):
        # Double
        if not isinstance(result, Point_At_Infinity):
            result = double_point(result)
        steps.append(result)

        if verbose:
            power = d // (2 ** (len(binary) - i - 1))
            print(f"  {power:6d}P = {result}")

        # Add if bit is 1
        if bit == "1":
            result = add_points(result, P)
            steps.append(result)
            if verbose:
                power = d // (2 ** (len(binary) - i - 1))
                print(f"  +    P")
                print(f"  ------")
                next_power = power + 1
                print(f"  {next_power:6d}P = {result}")

    return result, steps
