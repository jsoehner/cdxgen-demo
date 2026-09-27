## 🛡️ Cryptographic Bill of Materials (CBOM) & PQC Migration Assessment

**Format**: CycloneDX (v1.7) | **Total Components**: 85 | **Crypto Assets**: 14

### 📊 Post-Quantum Migration Scorecard

| Metric | Count | Migration Status |
|---|---|---|
| **Post-Quantum Ready (PQC)** | **3** | 🟢 Quantum-Resistant (NIST FIPS 203/204/205) |
| **Quantum-Vulnerable (Backlog)** | **5** | 🔴 At Risk of 'Harvest Now, Decrypt Later' |
| **Classical Symmetric / Hashing** | **6** | 🟡 Classical Security (Requires AES-256 / SHA-256+) |
| **Asymmetric PQC Migration Progress** | **37.5%** | (3 of 8 asymmetric primitives migrated) |

### ✅ Post-Quantum Cryptography Migrated Assets

| Component Name | Primitive | Key/Parameter Set | PQC Standard |
|---|---|---|---|
| `ML-KEM-768` | kem | N/A | PQC Algorithm |
| `ML-DSA-65` | signature | N/A | PQC Algorithm |
| `SLH-DSA` | signature | N/A | NIST FIPS 205 (SLH-DSA) |

### ⚠️ Quantum-Vulnerable Assets (Action Required)

| Component / Asset Name | Asset Type | Primitive / Algorithm | Key Length / Curve | Recommended PQC Replacement |
|---|---|---|---|---|
| `RSA-2048` | algorithm | RSA | 2048 | **ML-KEM-768 / Kyber (FIPS 203)** |
| `ECDSA-P256` | algorithm | ECDSA | secp256r1 | **ML-DSA-65 / Dilithium (FIPS 204)** |
| `ECDH-X25519` | algorithm | ECDH | 25519 | **ML-KEM-768 / Kyber (FIPS 203)** |
| `Ed25519` | algorithm | Ed25519 | 25519 | **ML-DSA-65 / Dilithium (FIPS 204)** |
| `Diffie-Hellman` | algorithm | Diffie | N/A | **ML-KEM (KEM) or ML-DSA (Signatures)** |

### 🔒 Classical Symmetric & Digest Assets

| Component Name | Primitive | Key Length | Quantum Resistance Assessment |
|---|---|---|---|
| `Stateful-Hash-Signature` | signature | N/A | Review key length for Grover resistance |
| `AES-256-GCM` | block-cipher | 256 | Quantum-Resistant (Grover's proof) |
| `SHA-256` | hash | 256 | Quantum-Resistant (Grover's proof) |
| `SHA-384` | hash | 384 | Review key length for Grover resistance |
| `ChaCha20-Poly1305` | stream-cipher | 256 | Quantum-Resistant (Grover's proof) |
| `SHA-512` | hash | 512 | Review key length for Grover resistance |
