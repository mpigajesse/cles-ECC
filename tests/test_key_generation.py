"""
Tests for ECC key generation.

Tests:
- Random private key generation
- Public key computation (Q = d·G)
- Key pair generation
- Validation of key pairs
"""

import pytest
from src.curve import CURVE_P17_A2_B2, CURVE_SECP256K1, CURVE_NIST_P256
from src.point import Point, Point_At_Infinity
from src.key_generation import (
    generate_private_key,
    compute_public_key,
    generate_keypair,
    validate_keypair,
    KeyPair,
)


class TestPrivateKeyGeneration:
    """Test random private key generation."""

    def test_generate_private_key_in_range(self):
        """Test that generated private key is in valid range [1, n-1]."""
        curve = CURVE_P17_A2_B2
        n = 20  # Example order (not actual secp256k1 order)

        d = generate_private_key(n)
        assert 1 <= d < n

    def test_generate_private_key_randomness(self):
        """Test that multiple calls generate different keys (probabilistic)."""
        curve = CURVE_P17_A2_B2
        n = 20

        keys = set()
        for _ in range(10):
            d = generate_private_key(n)
            keys.add(d)

        # Should have multiple different keys (very unlikely to have duplicates)
        assert len(keys) > 1

    def test_generate_private_key_never_zero(self):
        """Test that generated private key is never 0."""
        n = 100
        for _ in range(50):
            d = generate_private_key(n)
            assert d != 0

    def test_generate_private_key_never_n(self):
        """Test that generated private key is never n."""
        n = 50
        for _ in range(50):
            d = generate_private_key(n)
            assert d != n

    def test_generate_private_key_large_n(self):
        """Test private key generation with large n."""
        n = 2**256
        d = generate_private_key(n)
        assert 1 <= d < n


class TestPublicKeyComputation:
    """Test public key computation Q = d·G."""

    def test_public_key_from_private_key(self):
        """Test computing public key from private key."""
        curve = CURVE_P17_A2_B2
        # Use a known generator point
        Gx, Gy = 13, 7  # Example point on P17 curve
        G = Point(curve, Gx, Gy)

        # Private key
        d = 3

        # Compute public key
        Q = compute_public_key(d, G)

        # Public key should be on the curve
        assert Q.is_on_curve()

    def test_different_private_keys_different_public_keys(self):
        """Test that different private keys produce different public keys."""
        curve = CURVE_P17_A2_B2
        Gx, Gy = 13, 7
        G = Point(curve, Gx, Gy)

        Q1 = compute_public_key(1, G)
        Q2 = compute_public_key(2, G)

        assert Q1 != Q2

    def test_private_key_one_gives_generator(self):
        """Test that d=1 gives public key Q=G."""
        curve = CURVE_P17_A2_B2
        Gx, Gy = 13, 7
        G = Point(curve, Gx, Gy)

        Q = compute_public_key(1, G)
        assert Q == G

    def test_public_key_zero_scalar(self):
        """Test that d=0 gives point at infinity."""
        curve = CURVE_P17_A2_B2
        Gx, Gy = 13, 7
        G = Point(curve, Gx, Gy)

        Q = compute_public_key(0, G)
        assert isinstance(Q, Point_At_Infinity)

    def test_public_key_secp256k1_generator(self):
        """Test public key computation with secp256k1 generator."""
        Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

        G = Point(CURVE_SECP256K1, Gx, Gy)

        # Use a small private key for testing
        d = 2
        Q = compute_public_key(d, G)

        # Should be on curve
        assert Q.is_on_curve()


class TestKeyPairGeneration:
    """Test complete key pair generation."""

    def test_generate_keypair(self):
        """Test generating a complete key pair."""
        curve = CURVE_P17_A2_B2
        Gx, Gy = 13, 7
        G = Point(curve, Gx, Gy)
        n = 20  # Order

        keypair = generate_keypair(G, n)

        assert isinstance(keypair, KeyPair)
        assert keypair.private_key is not None
        assert keypair.public_key is not None
        assert keypair.curve == curve
        assert keypair.generator == G

    def test_keypair_private_key_in_range(self):
        """Test that private key in keypair is in valid range."""
        curve = CURVE_P17_A2_B2
        Gx, Gy = 13, 7
        G = Point(curve, Gx, Gy)
        n = 20

        for _ in range(10):
            keypair = generate_keypair(G, n)
            assert 1 <= keypair.private_key < n

    def test_keypair_public_key_on_curve(self):
        """Test that public key in keypair is on the curve."""
        curve = CURVE_P17_A2_B2
        Gx, Gy = 13, 7
        G = Point(curve, Gx, Gy)
        n = 20

        keypair = generate_keypair(G, n)
        assert keypair.public_key.is_on_curve()

    def test_keypair_reproducible_with_private_key(self):
        """Test that keypair is reproducible with given private key."""
        curve = CURVE_P17_A2_B2
        Gx, Gy = 13, 7
        G = Point(curve, Gx, Gy)

        private_key = 5
        Q1 = compute_public_key(private_key, G)

        keypair = KeyPair(curve, private_key, Q1, G)
        assert keypair.private_key == private_key
        assert keypair.public_key == Q1


class TestKeyPairValidation:
    """Test key pair validation."""

    def test_validate_valid_keypair(self):
        """Test validation of a valid key pair."""
        curve = CURVE_P17_A2_B2
        Gx, Gy = 13, 7
        G = Point(curve, Gx, Gy)

        d = 5
        Q = compute_public_key(d, G)

        keypair = KeyPair(curve, d, Q, G)
        assert validate_keypair(keypair)

    def test_validate_wrong_public_key(self):
        """Test validation fails with wrong public key."""
        curve = CURVE_P17_A2_B2
        Gx, Gy = 13, 7
        G = Point(curve, Gx, Gy)

        d = 5
        Q_correct = compute_public_key(d, G)

        # Find a different point on the curve
        d_wrong = 6
        Q_wrong = compute_public_key(d_wrong, G)

        if Q_wrong == Q_correct:
            # If they happen to be same, use d_wrong = 1 instead
            Q_wrong = G

        keypair = KeyPair(curve, d, Q_wrong, G)
        assert not validate_keypair(keypair)

    def test_validate_point_at_infinity_fails(self):
        """Test validation fails if public key is point at infinity."""
        curve = CURVE_P17_A2_B2
        Gx, Gy = 13, 7
        G = Point(curve, Gx, Gy)

        d = 0  # This gives Q = O
        Q = compute_public_key(d, G)

        keypair = KeyPair(curve, d, Q, G)
        # Public key should not be at infinity for valid keypair
        assert not validate_keypair(keypair)


class TestKeyPairClass:
    """Test the KeyPair class."""

    def test_keypair_string_representation(self):
        """Test string representation of keypair."""
        curve = CURVE_P17_A2_B2
        Gx, Gy = 13, 7
        G = Point(curve, Gx, Gy)

        d = 5
        Q = compute_public_key(d, G)

        keypair = KeyPair(curve, d, Q, G)
        s = str(keypair)
        # Should contain some identifying information
        assert "key" in s.lower() or "pair" in s.lower()

    def test_keypair_attributes(self):
        """Test keypair attributes."""
        curve = CURVE_P17_A2_B2
        Gx, Gy = 13, 7
        G = Point(curve, Gx, Gy)

        d = 5
        Q = compute_public_key(d, G)

        keypair = KeyPair(curve, d, Q, G)
        assert keypair.private_key == d
        assert keypair.public_key == Q
        assert keypair.generator == G
        assert keypair.curve == curve

    def test_keypair_multiple_instances_different(self):
        """Test that multiple generated keypairs are different."""
        curve = CURVE_P17_A2_B2
        Gx, Gy = 13, 7
        G = Point(curve, Gx, Gy)
        n = 20

        keypair1 = generate_keypair(G, n)
        keypair2 = generate_keypair(G, n)

        # Keys should be different (with high probability)
        assert keypair1.private_key != keypair2.private_key


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_private_key_equals_one(self):
        """Test edge case where d=1."""
        curve = CURVE_P17_A2_B2
        Gx, Gy = 13, 7
        G = Point(curve, Gx, Gy)

        Q = compute_public_key(1, G)
        assert Q == G

    def test_large_private_key(self):
        """Test with very large private key."""
        Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

        G = Point(CURVE_SECP256K1, Gx, Gy)

        # Large private key
        d = 12345678901234567890

        # Should compute without error
        Q = compute_public_key(d, G)
        assert Q.is_on_curve()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
