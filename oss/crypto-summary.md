## 🛡️ Cryptographic Bill of Materials (CBOM) & PQC Migration Assessment

**Format**: CycloneDX (v1.7) | **First-Party Code Crypto Assets**: 85 | **Total Tracked Crypto Assets**: 14

### 📊 Post-Quantum Migration Scorecard

| Metric | Count | Migration Status |
|---|---|---|
| **Post-Quantum Ready (PQC)** | **3** | 🟢 Quantum-Resistant (NIST FIPS 203/204/205) |
| **Quantum-Vulnerable (Backlog)** | **5** | 🔴 At Risk of 'Harvest Now, Decrypt Later' |
| **Classical Symmetric / Hashing** | **6** | 🟡 Classical Security (Requires AES-256 / SHA-256+) |
| **Asymmetric PQC Migration Progress** | **37.5%** | (3 of 8 asymmetric primitives migrated) |

### 🎯 Cryptographic Supply Chain Coverage & Confidence

| Evaluation Layer | Coverage / Status | Audit Confidence Assessment |
|---|---|---|
| **First-Party Code (`src/`)** | **100% Audited** (0 Custom Primitives) | 🟢 **HIGH** (Direct AST & SAST verified clean) |
| **Third-Party Supply Chain** | **0.0%** (0 of 72 dependencies cataloged) | 🔴 LOW (Known profiles assimilated) |
| **Overall Audit Confidence Score** | **1.4%** | **🔴 LOW** (72 unassimilated supply chain dependencies) |

### ✅ Post-Quantum Cryptography Migrated Assets

| Component Name | Primitive | Key/Parameter Set | PQC Standard | Provenance / Location(s) |
|---|---|---|---|---|
| `ML-KEM-768` | kem | N/A | PQC Algorithm | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:30`<br>`pqc_hybrid_service.py:50` |
| `ML-DSA-65` | signature | N/A | PQC Algorithm | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:31`<br>`pqc_hybrid_service.py:77` |
| `SLH-DSA` | signature | N/A | NIST FIPS 205 (SLH-DSA) | First-Party Code (SAST/AST)<br>Dependencies / External |

### ⚠️ Quantum-Vulnerable Assets & Remediation Plan

| Component / Algorithm | Type / Primitive | Key Length / Curve | Recommended Target | Provenance / Context |
|---|---|---|---|---|
| **`RSA-2048`**<br><sub>RSA</sub> | algorithm / signature | 2048 | **ML-KEM-768 / Kyber (FIPS 203)** | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:36`<br><sub><code>self.legacy_sig_algorithm = "RSA-2048"</code></sub><br><br>`pqc_hybrid_service.py:80`<br><sub><code>legacy_sig = os.urandom(256)  # 2048-bit RSA signature</code></sub> |
| **`ECDSA-P256`**<br><sub>ECDSA</sub> | algorithm / signature | secp256r1 | **ML-DSA-65 / Dilithium (FIPS 204)** | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:37`<br><sub><code>self.legacy_ecdsa_curve = "ECDSA-P256"</code></sub> |
| **`ECDH-X25519`**<br><sub>ECDH</sub> | algorithm / key-agreement | 25519 | **ML-KEM-768 / Kyber (FIPS 203)** | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:38`<br><sub><code>self.legacy_ecdh_curve = "X25519"</code></sub> |
| **`Ed25519`**<br><sub>Ed25519</sub> | algorithm / signature | 25519 | **ML-DSA-65 / Dilithium (FIPS 204)** | First-Party Code (SAST/AST)<br>External Dependency |
| **`Diffie-Hellman`**<br><sub>Diffie</sub> | algorithm / key-agreement | N/A | **ML-KEM (KEM) or ML-DSA (Signatures)** | First-Party Code (SAST/AST)<br>External Dependency |

### 🔒 Classical Symmetric & Digest Assets

| Component Name | Primitive | Key Length | Quantum Resistance Assessment | Provenance / Location(s) |
|---|---|---|---|---|
| `Stateful-Hash-Signature` | signature | N/A | Review key length for Grover resistance | First-Party Code (SAST/AST)<br>Dependencies / External |
| `AES-256-GCM` | block-cipher | 256 | Quantum-Resistant (Grover's proof) | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:13`<br>`pqc_hybrid_service.py:41`<br>`pqc_hybrid_service.py:61` |
| `SHA-256` | hash | 256 | Quantum-Resistant (Grover's proof) | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:14` |
| `SHA-384` | hash | 384 | Review key length for Grover resistance | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:14`<br>`pqc_hybrid_service.py:42`<br>`pqc_hybrid_service.py:58` |
| `ChaCha20-Poly1305` | stream-cipher | 256 | Quantum-Resistant (Grover's proof) | First-Party Code (SAST/AST)<br>`scripts/analyze_cbom.py:30` |
| `SHA-512` | hash | 512 | Review key length for Grover resistance | First-Party Code (SAST/AST)<br>`scripts/analyze_cbom.py:30` |

### ⚠️ Unassimilated Third-Party Binaries & Cryptographic Blind Spots

> ℹ️ *The following third-party dependencies do not have verified upstream CBOM attestations in the catalog. They lower the audit confidence score until explicit CBOMs or attestations are published.* 

| Dependency Name | Version | Package URL (purl) | Status |
|---|---|---|---|
| `express` | 5.2.1 | `pkg:npm/express@5.2.1` | 🟡 Unassimilated (No upstream CBOM) |
| `accepts` | 2.0.0 | `pkg:npm/accepts@2.0.0` | 🟡 Unassimilated (No upstream CBOM) |
| `mime-types` | 3.0.2 | `pkg:npm/mime-types@3.0.2` | 🟡 Unassimilated (No upstream CBOM) |
| `mime-db` | 1.54.0 | `pkg:npm/mime-db@1.54.0` | 🟡 Unassimilated (No upstream CBOM) |
| `negotiator` | 1.0.0 | `pkg:npm/negotiator@1.0.0` | 🟡 Unassimilated (No upstream CBOM) |
| `body-parser` | 2.3.0 | `pkg:npm/body-parser@2.3.0` | 🟡 Unassimilated (No upstream CBOM) |
| `bytes` | 3.1.2 | `pkg:npm/bytes@3.1.2` | 🟡 Unassimilated (No upstream CBOM) |
| `content-type` | 2.0.0 | `pkg:npm/content-type@2.0.0` | 🟡 Unassimilated (No upstream CBOM) |
| `debug` | 4.4.3 | `pkg:npm/debug@4.4.3` | 🟡 Unassimilated (No upstream CBOM) |
| `ms` | 2.1.3 | `pkg:npm/ms@2.1.3` | 🟡 Unassimilated (No upstream CBOM) |
| `http-errors` | 2.0.1 | `pkg:npm/http-errors@2.0.1` | 🟡 Unassimilated (No upstream CBOM) |
| `depd` | 2.0.0 | `pkg:npm/depd@2.0.0` | 🟡 Unassimilated (No upstream CBOM) |
| `inherits` | 2.0.4 | `pkg:npm/inherits@2.0.4` | 🟡 Unassimilated (No upstream CBOM) |
| `setprototypeof` | 1.2.0 | `pkg:npm/setprototypeof@1.2.0` | 🟡 Unassimilated (No upstream CBOM) |
| `statuses` | 2.0.2 | `pkg:npm/statuses@2.0.2` | 🟡 Unassimilated (No upstream CBOM) |
| *... and 57 more unassimilated dependencies* | | | |
