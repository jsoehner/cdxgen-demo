"""
pqc_hybrid_service.py - Hybrid Post-Quantum Cryptographic Service Architecture

Demonstrates a dual-stack cryptographic service during the PQC transition era:
1. Migrated PQC Primitives:
   - ML-KEM-768 (NIST FIPS 203 / Crystals-Kyber): Quantum-resistant key encapsulation.
   - ML-DSA-65 (NIST FIPS 204 / Crystals-Dilithium): Quantum-resistant digital signatures.
2. Legacy Quantum-Vulnerable Primitives (Migration Backlog):
   - RSA-2048: Legacy client auth and backward-compatible certificate validation.
   - ECDSA-P256 (secp256r1): Legacy mobile device signature verification.
   - ECDH-X25519: Classical key exchange component in hybrid mode.
3. Quantum-Resistant Classical Primitives:
   - AES-256-GCM: Bulk payload symmetric encryption (Grover-safe).
   - SHA-384 / SHA-256: Quantum-resistant cryptographic hashing.
"""

import os
import hashlib
from typing import Tuple, Dict, Any


class HybridPQCEngine:
    """
    Hybrid Post-Quantum Cryptographic Engine.
    Executes hybrid key encapsulation and dual-signing.
    """

    def __init__(self):
        # 1. Migrated Post-Quantum Cryptographic Primitives (FIPS 203 & FIPS 204)
        self.kem_algorithm = "ML-KEM-768"
        self.dsa_algorithm = "ML-DSA-65"
        self.kem_parameter_set = "768"
        self.dsa_parameter_set = "65"

        # 2. Legacy Asymmetric Primitives (Requires Migration Plan)
        self.legacy_sig_algorithm = "RSA-2048"
        self.legacy_ecdsa_curve = "ECDSA-P256"
        self.legacy_ecdh_curve = "X25519"

        # 3. Classical Symmetric / Hash Primitives (Quantum-Resistant)
        self.bulk_cipher = "AES-256-GCM"
        self.hash_digest = "SHA-384"

    def encapsulate_hybrid_key(self, peer_pqc_pk: bytes, peer_ecdh_pk: bytes) -> Dict[str, Any]:
        """
        Simulate hybrid key encapsulation combining ML-KEM-768 with classical ECDH-X25519.
        Both shared secrets are hashed together using SHA-384 to derive the session key.
        """
        # Post-quantum KEM shared secret (NIST FIPS 203)
        pqc_ciphertext = os.urandom(1088)  # ML-KEM-768 ciphertext length
        pqc_shared_secret = os.urandom(32)

        # Classical X25519 ECDH shared secret (Quantum-vulnerable component)
        classical_ephemeral_pub = os.urandom(32)
        classical_shared_secret = os.urandom(32)

        # Hybrid Key Derivation via SHA-384
        h = hashlib.sha384()
        h.update(pqc_shared_secret)
        h.update(classical_shared_secret)
        session_key = h.digest()[:32]  # 256-bit AES key

        return {
            "pqc_algorithm": self.kem_algorithm,
            "classical_algorithm": self.legacy_ecdh_curve,
            "pqc_ciphertext": pqc_ciphertext.hex()[:32] + "...",
            "classical_public": classical_ephemeral_pub.hex()[:32] + "...",
            "derived_session_cipher": self.bulk_cipher,
            "session_key_len_bits": len(session_key) * 8
        }

    def sign_hybrid_payload(self, message: bytes) -> Dict[str, str]:
        """
        Dual-sign payload using ML-DSA-65 (Post-Quantum) and RSA-2048 (Legacy).
        """
        # 1. PQC Signature (FIPS 204 ML-DSA-65)
        pqc_sig = os.urandom(3309)  # ML-DSA-65 signature length

        # 2. Legacy RSA Signature (PKCS#1 v1.5 with SHA-256)
        legacy_sig = os.urandom(256)  # 2048-bit RSA signature

        return {
            "pqc_signature_algorithm": self.dsa_algorithm,
            "pqc_signature": pqc_sig.hex()[:32] + "...",
            "legacy_signature_algorithm": self.legacy_sig_algorithm,
            "legacy_signature": legacy_sig.hex()[:32] + "..."
        }


if __name__ == "__main__":
    engine = HybridPQCEngine()
    session = engine.encapsulate_hybrid_key(b"peer_pqc_pk", b"peer_ecdh_pk")
    sigs = engine.sign_hybrid_payload(b"Critical Financial Transaction")

    print("=== Hybrid PQC Session Established ===")
    print(f"KEM: {session['pqc_algorithm']} (PQC) + {session['classical_algorithm']} (Classical)")
    print(f"Bulk Encryption: {session['derived_session_cipher']}")
    print(f"Dual Signatures: {sigs['pqc_signature_algorithm']} (PQC) & {sigs['legacy_signature_algorithm']} (Legacy)")
