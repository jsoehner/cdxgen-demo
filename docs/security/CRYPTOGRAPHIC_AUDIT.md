## 🛡️ Cryptographic Bill of Materials (CBOM) & PQC Migration Assessment

**Format**: CycloneDX (v1.6) | **First-Party Code Crypto Assets**: 8 | **Total Tracked Crypto Assets**: 10

### 📊 Post-Quantum Migration Scorecard

| Metric | Count | Migration Status |
|---|---|---|
| **Post-Quantum Ready (PQC)** | **2** | 🟢 Quantum-Resistant (NIST FIPS 203/204/205) |
| **Quantum-Vulnerable (Backlog)** | **4** | 🔴 At Risk of 'Harvest Now, Decrypt Later' |
| **Classical Symmetric / Digest** | **4** | 🟡 Classical Security (Requires AES-256 / SHA-256+) |
| **Asymmetric PQC Migration Progress** | **33.3%** | (2 of 6 asymmetric primitives migrated) |

### 🎯 Cryptographic Supply Chain Coverage & Confidence

| Evaluation Layer | Coverage / Status | Audit Confidence Assessment |
|---|---|---|
| **First-Party Code (`src/`, `scripts/`)** | **100% Audited** (8 Crypto Primitive(s) Inventoried) | 🟢 **HIGH** (Direct AST & SAST verified) |
| **Third-Party Supply Chain** | **16.9%** (14 of 83 dependencies cataloged) | 🔴 LOW (Known profiles assimilated) |
| **Overall Audit Confidence Score** | **17.9%** | 🔴 LOW (69 unassimilated supply chain dependencies) |

| **System OS Inventory** | **Pending Update** | 🟡 **Warning** (Local OS crypto components not yet inventoried) |

### ✅ Post-Quantum Ready Assets

| Component Name | Primitive | Key/Parameter Set | PQC Standard | Provenance / Location(s) |
|---|---|---|---|---|
| `ML-KEM-768` | kem | N/A | ML-KEM-768 (FIPS 203) | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:30`<br>`pqc_hybrid_service.py:50` |
| `ML-DSA-65` | signature | N/A | ML-DSA-65 (FIPS 204) | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:31`<br>`pqc_hybrid_service.py:77` |

### ⚠️ Quantum-Vulnerable Assets & Remediation Plan

| Component / Algorithm | Type / Primitive | Key Length / Curve | Recommended Target | Provenance / Context |
|---|---|---|---|---|
| **`RSA-2048`**<br><sub>RSA-2048</sub> | algorithm / pke | 2048 | **ML-KEM-768 / Kyber (FIPS 203)** | First-Party Code (SAST/AST)<br>`python_test/ssl_test.py`<br><br>`pqc_hybrid_service.py:36`<br><sub><code>self.legacy_sig_algorithm = "RSA-2048"</code></sub><br><br>`pqc_hybrid_service.py:80`<br><sub><code>legacy_sig = os.urandom(256)  # 2048-bit RSA signature</code></sub> |
| **`ECDSA-P256`**<br><sub>ECDSA-P256</sub> | algorithm / signature | secp256r1 | **ML-DSA-65 / Dilithium (FIPS 204)** | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:37`<br><sub><code>self.legacy_ecdsa_curve = "ECDSA-P256"</code></sub> |
| **`ECDH-X25519`**<br><sub>ECDH-X25519</sub> | algorithm / key-agreement | 25519 | **ML-KEM-768 / Kyber (FIPS 203)** | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:38`<br><sub><code>self.legacy_ecdh_curve = "X25519"</code></sub> |
| **`cryptography (PyCA OpenSSL Asymmetric Primitives (RSA / ECDSA / Ed25519 / X25519))`**<br><sub>RSA-2048 / ECDSA-P256 / Ed25519 / X25519</sub> | signature / signature | 2048 / 256 | **Migrate asymmetric PKI/JWT workflows to OpenSSL 3.5+ ML-KEM (FIPS 203) and ML-DSA (FIPS 204)** | Assimilated Upstream CBOM: PyCA Cryptography / OpenSSL 3.x EVP Reference CBOM<br>`Dependency: cryptography@50.0.2` |

### 🔒 Classical Symmetric & Digest Assets

| Component Name | Primitive | Key Length | Quantum Resistance Assessment | Provenance / Location(s) |
|---|---|---|---|---|
| `private-key@b1943c37-75c8-48b9-b415-3ffbefd454a8` | unknown | N/A | Review key length for Grover resistance | First-Party Code (SAST/AST)<br>`python_test/ssl_test.py` |
| `AES-256-GCM` | block-cipher | 256 | Quantum-Resistant (Grover's proof) | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:41`<br>`pqc_hybrid_service.py:61` |
| `SHA-384` | hash | 384 | Quantum-Resistant (Grover's proof) | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:42`<br>`pqc_hybrid_service.py:58` |
| `cryptography (PyCA OpenSSL EVP Symmetric & AEAD Suite (AES-256-GCM / ChaCha20-Poly1305 / Fernet))` | block-cipher | 256 | Quantum-Resistant (Grover's proof) | Assimilated Upstream CBOM: PyCA Cryptography / OpenSSL 3.x EVP Reference CBOM<br>`Dependency: cryptography@50.0.2` |

### ⚠️ Unassimilated Third-Party Binaries & Cryptographic Blind Spots

> ℹ️ *The following third-party dependencies do not have verified upstream CBOM attestations in the catalog. They lower the audit confidence score until explicit CBOMs or attestations are published.* 

| Dependency Name | Version | Package URL (purl) | Status |
|---|---|---|---|
| `accepts` | 2.0.0 | `pkg:npm/accepts@2.0.0` | 🟡 Unassimilated (No upstream CBOM) |
| `body-parser` | 2.4.0 | `pkg:npm/body-parser@2.4.0` | 🟡 Unassimilated (No upstream CBOM) |
| `bytes` | 3.1.2 | `pkg:npm/bytes@3.1.2` | 🟡 Unassimilated (No upstream CBOM) |
| `call-bind-apply-helpers` | 1.0.2 | `pkg:npm/call-bind-apply-helpers@1.0.2` | 🟡 Unassimilated (No upstream CBOM) |
| `call-bound` | 1.0.4 | `pkg:npm/call-bound@1.0.4` | 🟡 Unassimilated (No upstream CBOM) |
| `content-disposition` | 1.1.0 | `pkg:npm/content-disposition@1.1.0` | 🟡 Unassimilated (No upstream CBOM) |
| `content-type` | 1.0.5 | `pkg:npm/content-type@1.0.5` | 🟡 Unassimilated (No upstream CBOM) |
| `content-type` | 2.0.0 | `pkg:npm/content-type@2.0.0` | 🟡 Unassimilated (No upstream CBOM) |
| `content-type` | 2.1.0 | `pkg:npm/content-type@2.1.0` | 🟡 Unassimilated (No upstream CBOM) |
| `cookie` | 0.7.2 | `pkg:npm/cookie@0.7.2` | 🟡 Unassimilated (No upstream CBOM) |
| `cookie-signature` | 1.2.2 | `pkg:npm/cookie-signature@1.2.2` | 🟡 Unassimilated (No upstream CBOM) |
| `debug` | 4.4.3 | `pkg:npm/debug@4.4.3` | 🟡 Unassimilated (No upstream CBOM) |
| `depd` | 2.0.0 | `pkg:npm/depd@2.0.0` | 🟡 Unassimilated (No upstream CBOM) |
| `dunder-proto` | 1.0.1 | `pkg:npm/dunder-proto@1.0.1` | 🟡 Unassimilated (No upstream CBOM) |
| `ee-first` | 1.1.1 | `pkg:npm/ee-first@1.1.1` | 🟡 Unassimilated (No upstream CBOM) |
| *... and 54 more unassimilated dependencies* | | | |
