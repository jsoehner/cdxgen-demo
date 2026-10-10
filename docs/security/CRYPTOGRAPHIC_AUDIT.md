## 🛡️ Cryptographic Bill of Materials (CBOM) & PQC Migration Assessment

**Format**: CycloneDX (v1.6) | **Total Components**: 13 | **Crypto Assets**: 13

### 📊 Post-Quantum Migration Scorecard

| Metric | Count | Migration Status |
|---|---|---|
| **Post-Quantum Ready (PQC)** | **3** | 🟢 Quantum-Resistant (NIST FIPS 203/204/205) |
| **Quantum-Vulnerable (Backlog)** | **5** | 🔴 At Risk of 'Harvest Now, Decrypt Later' |
| **Classical Symmetric / Hashing** | **5** | 🟡 Classical Security (Requires AES-256 / SHA-256+) |
| **Asymmetric PQC Migration Progress** | **37.5%** | (3 of 8 asymmetric primitives migrated) |

### ✅ Post-Quantum Cryptography Migrated Assets

| Component Name | Primitive | Key/Parameter Set | PQC Standard | Location(s) |
|---|---|---|---|---|
| `ML-KEM-768` | kem | N/A | NIST FIPS 203 (ML-KEM) | `pqc_hybrid_service.py:6`<br>`pqc_hybrid_service.py:30`<br>`pqc_hybrid_service.py:46`<br>`pqc_hybrid_service.py:50`<br>`parse_cbom.py:83` |
| `ML-DSA-65` | signature | N/A | NIST FIPS 204 (ML-DSA) | `pqc_hybrid_service.py:7`<br>`pqc_hybrid_service.py:31`<br>`pqc_hybrid_service.py:74`<br>`pqc_hybrid_service.py:77`<br>`parse_cbom.py:83` |
| `SLH-DSA` | signature | N/A | NIST FIPS 204 (ML-DSA) | `parse_cbom.py:83` |

### ⚠️ Quantum-Vulnerable Assets & Remediation Plan

| Component / Algorithm | Type / Primitive | Key Length / Curve | Recommended Target | Source Location(s) & Code Context |
|---|---|---|---|---|
| **`RSA-2048`**<br><sub>RSA-2048</sub> | algorithm / pke | 2048 | **ML-KEM-768 / Kyber (FIPS 203)** | `python_test/ssl_test.py`<br><br>`pqc_hybrid_service.py:9`<br><sub><code>- RSA-2048: Legacy client auth and backward-compatible certificate validation.</code></sub><br><br>`pqc_hybrid_service.py:36`<br><sub><code>self.legacy_sig_algorithm = "RSA-2048"</code></sub><br><br>`pqc_hybrid_service.py:74`<br><sub><code>Dual-sign payload using ML-DSA-65 (Post-Quantum) and RSA-2048 (Legacy).</code></sub><br><br>`pqc_hybrid_service.py:80`<br><sub><code>legacy_sig = os.urandom(256)  # 2048-bit RSA signature</code></sub><br><br>`parse_gpg.py:7`<br><sub><code>"1": "RSA",</code></sub><br><br>`parse_gpg.py:8`<br><sub><code>"2": "RSA (Encrypt Only)",</code></sub><br><br>`parse_gpg.py:9`<br><sub><code>"3": "RSA (Sign Only)",</code></sub><br><br>`parse_cbom.py:84`<br><sub><code>vulnerable_keywords = ["rsa", "dsa", "ecc", "ecdh", "ecdsa", "eddsa", "dh", "diffie-hellman", "ed25519", "x25519", "curv</code></sub><br><br>`parse_cbom.py:113`<br><sub><code>"  ./parse_cbom.py -t algorithm -a RSA -a ECC\n"</code></sub><br><br>`parse_cbom.py:125`<br><sub><code>help="Filter by specific algorithm name or primitive (e.g., 'RSA', 'ECC'). Can be specified multiple times.")</code></sub><br><br>`inject_algo.py:20`<br><sub><code>"name": "RSA",</code></sub><br><br>`python_test/ssl_test.py:3`<br><sub><code>from cryptography.hazmat.primitives.asymmetric import rsa</code></sub><br><br>`python_test/ssl_test.py:8`<br><sub><code>context.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384')</code></sub><br><br>`python_test/ssl_test.py:10`<br><sub><code>private_key = rsa.generate_private_key(</code></sub> |
| **`ECDSA-P256`**<br><sub>ECDSA-P256</sub> | algorithm / signature | secp256r1 | **ML-DSA-65 / Dilithium (FIPS 204)** | `pqc_hybrid_service.py:10`<br><sub><code>- ECDSA-P256 (secp256r1): Legacy mobile device signature verification.</code></sub><br><br>`pqc_hybrid_service.py:37`<br><sub><code>self.legacy_ecdsa_curve = "ECDSA-P256"</code></sub><br><br>`parse_gpg.py:13`<br><sub><code>"19": "ECDSA",</code></sub><br><br>`parse_cbom.py:84`<br><sub><code>vulnerable_keywords = ["rsa", "dsa", "ecc", "ecdh", "ecdsa", "eddsa", "dh", "diffie-hellman", "ed25519", "x25519", "curv</code></sub> |
| **`ECDH-X25519`**<br><sub>ECDH-X25519</sub> | algorithm / key-agreement | 25519 | **ML-KEM-768 / Kyber (FIPS 203)** | `pqc_hybrid_service.py:11`<br><sub><code>- ECDH-X25519: Classical key exchange component in hybrid mode.</code></sub><br><br>`pqc_hybrid_service.py:38`<br><sub><code>self.legacy_ecdh_curve = "X25519"</code></sub><br><br>`pqc_hybrid_service.py:46`<br><sub><code>Simulate hybrid key encapsulation combining ML-KEM-768 with classical ECDH-X25519.</code></sub><br><br>`parse_gpg.py:12`<br><sub><code>"18": "ECDH",</code></sub><br><br>`parse_cbom.py:84`<br><sub><code>vulnerable_keywords = ["rsa", "dsa", "ecc", "ecdh", "ecdsa", "eddsa", "dh", "diffie-hellman", "ed25519", "x25519", "curv</code></sub> |
| **`Ed25519`**<br><sub>Ed25519</sub> | algorithm / signature | 25519 | **ML-DSA-65 / Dilithium (FIPS 204)** | `parse_cbom.py:84`<br><sub><code>vulnerable_keywords = ["rsa", "dsa", "ecc", "ecdh", "ecdsa", "eddsa", "dh", "diffie-hellman", "ed25519", "x25519", "curv</code></sub> |
| **`Diffie-Hellman`**<br><sub>Diffie-Hellman</sub> | algorithm / key-agreement | N/A | **ML-KEM (KEM) or ML-DSA (Signatures)** | `parse_cbom.py:84`<br><sub><code>vulnerable_keywords = ["rsa", "dsa", "ecc", "ecdh", "ecdsa", "eddsa", "dh", "diffie-hellman", "ed25519", "x25519", "curv</code></sub><br><br>`python_test/ssl_test.py:8`<br><sub><code>context.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384')</code></sub> |

### 🔒 Classical Symmetric & Digest Assets

| Component Name | Primitive | Key Length | Quantum Resistance Assessment | Location(s) |
|---|---|---|---|---|
| `private-key@765cf23a-11c3-49a3-92a1-da9c7c0a0a67` | unknown | N/A | Review key length for Grover resistance | `python_test/ssl_test.py` |
| `AES-256-GCM` | block-cipher | 256 | Quantum-Resistant (Grover's proof) | `pqc_hybrid_service.py:13`<br>`pqc_hybrid_service.py:41`<br>`pqc_hybrid_service.py:61`<br>`python_test/ssl_test.py:8` |
| `SHA-256` | hash | 256 | Quantum-Resistant (Grover's proof) | `pqc_hybrid_service.py:14` |
| `SHA-384` | hash | 384 | Quantum-Resistant (Grover's proof) | `pqc_hybrid_service.py:14`<br>`pqc_hybrid_service.py:42`<br>`pqc_hybrid_service.py:47`<br>`pqc_hybrid_service.py:58`<br>`python_test/ssl_test.py:8` |
| `Stateful-Hash-Signature` | signature | N/A | Review key length for Grover resistance | `parse_cbom.py:83` |
