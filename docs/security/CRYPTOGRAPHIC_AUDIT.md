## 🛡️ Cryptographic Bill of Materials (CBOM) & PQC Migration Assessment

**Format**: CycloneDX (v1.6) | **Total Components**: 8 | **Crypto Assets**: 8

### 📊 Post-Quantum Migration Scorecard

| Metric | Count | Migration Status |
|---|---|---|
| **Post-Quantum Ready (PQC)** | **2** | 🟢 Quantum-Resistant (NIST FIPS 203/204/205) |
| **Quantum-Vulnerable (Backlog)** | **3** | 🔴 At Risk of 'Harvest Now, Decrypt Later' |
| **Classical Symmetric / Hashing** | **3** | 🟡 Classical Security (Requires AES-256 / SHA-256+) |
| **Asymmetric PQC Migration Progress** | **40.0%** | (2 of 5 asymmetric primitives migrated) |

### ✅ Post-Quantum Cryptography Migrated Assets

| Component Name | Primitive | Key/Parameter Set | PQC Standard | Location(s) |
|---|---|---|---|---|
| `ML-KEM-768` | kem | N/A | NIST FIPS 203 (ML-KEM) | `pqc_hybrid_service.py:30`<br>`pqc_hybrid_service.py:50` |
| `ML-DSA-65` | signature | N/A | NIST FIPS 204 (ML-DSA) | `pqc_hybrid_service.py:31`<br>`pqc_hybrid_service.py:77` |

### ⚠️ Quantum-Vulnerable Assets & Remediation Plan

| Component / Algorithm | Type / Primitive | Key Length / Curve | Recommended Target | Source Location(s) & Code Context |
|---|---|---|---|---|
| **`RSA-2048`**<br><sub>RSA-2048</sub> | algorithm / pke | 2048 | **ML-KEM-768 / Kyber (FIPS 203)** | `python_test/ssl_test.py`<br><br>`pqc_hybrid_service.py:36`<br><sub><code>self.legacy_sig_algorithm = "RSA-2048"</code></sub><br><br>`pqc_hybrid_service.py:80`<br><sub><code>legacy_sig = os.urandom(256)  # 2048-bit RSA signature</code></sub> |
| **`ECDSA-P256`**<br><sub>ECDSA-P256</sub> | algorithm / signature | secp256r1 | **ML-DSA-65 / Dilithium (FIPS 204)** | `pqc_hybrid_service.py:37`<br><sub><code>self.legacy_ecdsa_curve = "ECDSA-P256"</code></sub> |
| **`ECDH-X25519`**<br><sub>ECDH-X25519</sub> | algorithm / key-agreement | 25519 | **ML-KEM-768 / Kyber (FIPS 203)** | `pqc_hybrid_service.py:38`<br><sub><code>self.legacy_ecdh_curve = "X25519"</code></sub> |

### 🔒 Classical Symmetric & Digest Assets

| Component Name | Primitive | Key Length | Quantum Resistance Assessment | Location(s) |
|---|---|---|---|---|
| `private-key@6a4f2146-df32-4fe8-929e-0ec7541320b8` | unknown | N/A | Review key length for Grover resistance | `python_test/ssl_test.py` |
| `AES-256-GCM` | block-cipher | 256 | Quantum-Resistant (Grover's proof) | `pqc_hybrid_service.py:41`<br>`pqc_hybrid_service.py:61` |
| `SHA-384` | hash | 384 | Quantum-Resistant (Grover's proof) | `pqc_hybrid_service.py:42`<br>`pqc_hybrid_service.py:58` |
