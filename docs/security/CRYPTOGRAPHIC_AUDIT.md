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

| Component Name | Primitive | Key/Parameter Set | PQC Standard | Location(s) |
|---|---|---|---|---|
| `ML-KEM-768` | kem | N/A | PQC Algorithm | `pqc_hybrid_service.py:30`<br>`pqc_hybrid_service.py:50` |
| `ML-DSA-65` | signature | N/A | PQC Algorithm | `pqc_hybrid_service.py:31`<br>`pqc_hybrid_service.py:77` |
| `SLH-DSA` | signature | N/A | NIST FIPS 205 (SLH-DSA) | Dependencies / External |

### ⚠️ Quantum-Vulnerable Assets & Remediation Plan

| Component / Algorithm | Type / Primitive | Key Length / Curve | Recommended Target | Source Location(s) & Code Context |
|---|---|---|---|---|
| **`RSA-2048`**<br><sub>RSA</sub> | algorithm / signature | 2048 | **ML-KEM-768 / Kyber (FIPS 203)** | `pqc_hybrid_service.py:36`<br><sub><code>self.legacy_sig_algorithm = "RSA-2048"</code></sub><br><br>`pqc_hybrid_service.py:80`<br><sub><code>legacy_sig = os.urandom(256)  # 2048-bit RSA signature</code></sub> |
| **`ECDSA-P256`**<br><sub>ECDSA</sub> | algorithm / signature | secp256r1 | **ML-DSA-65 / Dilithium (FIPS 204)** | `pqc_hybrid_service.py:37`<br><sub><code>self.legacy_ecdsa_curve = "ECDSA-P256"</code></sub> |
| **`ECDH-X25519`**<br><sub>ECDH</sub> | algorithm / key-agreement | 25519 | **ML-KEM-768 / Kyber (FIPS 203)** | `pqc_hybrid_service.py:38`<br><sub><code>self.legacy_ecdh_curve = "X25519"</code></sub> |
| **`Ed25519`**<br><sub>Ed25519</sub> | algorithm / signature | 25519 | **ML-DSA-65 / Dilithium (FIPS 204)** | Dependencies / External |
| **`Diffie-Hellman`**<br><sub>Diffie</sub> | algorithm / key-agreement | N/A | **ML-KEM (KEM) or ML-DSA (Signatures)** | Dependencies / External |

### 🔒 Classical Symmetric & Digest Assets

| Component Name | Primitive | Key Length | Quantum Resistance Assessment | Location(s) |
|---|---|---|---|---|
| `Stateful-Hash-Signature` | signature | N/A | Review key length for Grover resistance | Dependencies / External |
| `AES-256-GCM` | block-cipher | 256 | Quantum-Resistant (Grover's proof) | `pqc_hybrid_service.py:13`<br>`pqc_hybrid_service.py:41`<br>`pqc_hybrid_service.py:61` |
| `SHA-256` | hash | 256 | Quantum-Resistant (Grover's proof) | `pqc_hybrid_service.py:14` |
| `SHA-384` | hash | 384 | Review key length for Grover resistance | `pqc_hybrid_service.py:14`<br>`pqc_hybrid_service.py:42`<br>`pqc_hybrid_service.py:58` |
| `ChaCha20-Poly1305` | stream-cipher | 256 | Quantum-Resistant (Grover's proof) | `scripts/analyze_cbom.py:30` |
| `SHA-512` | hash | 512 | Review key length for Grover resistance | `scripts/analyze_cbom.py:30` |
