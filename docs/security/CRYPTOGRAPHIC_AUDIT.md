## 🛡️ Cryptographic Bill of Materials (CBOM) & PQC Migration Assessment

**Format**: CycloneDX (v1.6) | **First-Party Code Crypto Assets**: 11 | **Total Tracked Crypto Assets**: 16

### 📊 Post-Quantum Migration Scorecard

| Metric | Count | Migration Status |
|---|---|---|
| **Post-Quantum Ready (PQC)** | **2** | 🟢 Quantum-Resistant (NIST FIPS 203/204/205) |
| **Quantum-Vulnerable (Backlog)** | **7** | 🔴 At Risk of 'Harvest Now, Decrypt Later' |
| **Classical Symmetric / Digest** | **7** | 🟡 Classical Security (Requires AES-256 / SHA-256+) |
| **Asymmetric PQC Migration Progress** | **22.2%** | (2 of 9 asymmetric/vulnerable primitives migrated) |

### 🎯 Cryptographic Supply Chain Coverage & Confidence

| Evaluation Layer | Coverage / Status | Audit Confidence Assessment |
|---|---|---|
| **First-Party Code (`src/`, `scripts/`)** | **100% Audited** (11 Crypto Primitive(s) Inventoried across Configuration (163), PKI/Certificate (1), Python (12), Shell (4)) | 🟢 **HIGH** (Direct AST & SAST verified) |
| **Third-Party Supply Chain** | **98.8%** (79 of 80 dependencies cataloged) | 🟢 HIGH (Known profiles assimilated) |
| **Overall Audit Confidence Score** | **98.8%** | 🟢 HIGH (1 unassimilated supply chain dependencies) |

| **System OS Inventory** | **Pending Update** | 🟡 **Warning** (Local OS crypto components not yet inventoried) |

### ✅ Post-Quantum Ready Assets

| Component Name | Primitive | Key/Parameter Set | PQC Standard | Provenance / Location(s) |
|---|---|---|---|---|
| `ML-KEM-768` | kem | 768 | ML-KEM (FIPS 203) | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:30`<br>`pqc_hybrid_service.py:50` |
| `ML-DSA-65` | signature | 65 | ML-DSA (FIPS 204) | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:31`<br>`pqc_hybrid_service.py:77` |

### ⚠️ Quantum-Vulnerable Assets & Remediation Plan

| Component / Algorithm | Type / Primitive | Key Length / Curve | Recommended Target | Provenance / Context |
|---|---|---|---|---|
| **`private-key@a1de0bf0-7212-41a0-a856-faf8a17376c5`**<br><sub>private-key@a1de0bf0-7212-41a0-a856-faf8a17376c5</sub> | related-crypto-material / private-key | 2048 | **ML-DSA-65 / SLH-DSA X.509 Certificate & KMS Key Rotation** | First-Party Code (SAST/AST)<br>`python_test/ssl_test.py` |
| **`RSA-2048`**<br><sub>RSA-2048</sub> | algorithm / pke | 2048 | **ML-KEM-768 / Kyber (FIPS 203)** | First-Party Code (SAST/AST)<br>`python_test/ssl_test.py`<br><br>`ubuntu_bom.json:1`<br><sub><code>{"bomFormat":"CycloneDX","specVersion":"1.7","serialNumber":"urn:uuid:3ac3954a-8cf4-4363-9ad1-a9ff6a4fcbec","version":2,</code></sub><br><br>`demo.sh:135`<br><sub><code>echo "Filtering tomcat_bom.json for 'RSA' algorithms only:"</code></sub><br><br>`demo.sh:136`<br><sub><code>python3 ./parse_cbom.py -f "tomcat_bom.json" -a RSA \| head -n 15</code></sub><br><br>`demo.sh:146`<br><sub><code>echo "Parsing the injected CBoM for 'RSA':"</code></sub><br><br>`demo.sh:147`<br><sub><code>python3 ./parse_cbom.py -f "tomcat_demo_bom.json" -a RSA \| head -n 15</code></sub><br><br>`pqc_hybrid_service.py:36`<br><sub><code>self.legacy_sig_algorithm = "RSA-2048"</code></sub><br><br>`pqc_hybrid_service.py:80`<br><sub><code>legacy_sig = os.urandom(256)  # 2048-bit RSA signature</code></sub><br><br>`python_test/python-usages.slices.json:1`<br><sub><code>{"objectSlices":[{"code":"","fullName":"ssl_test.py:<module>","signature":"","fileName":"ssl_test.py","lineNumber":1,"co</code></sub> |
| **`RSA-4096`**<br><sub>RSA-4096</sub> | algorithm / signature | 4096 | **ML-KEM-768 / Kyber (FIPS 203)** | First-Party Code (SAST/AST)<br>`bom.json:1`<br><sub><code>{"bomFormat":"CycloneDX","specVersion":"1.7","serialNumber":"urn:uuid:1a8d61c0-f598-4e94-8411-4430b498eee0","version":2,</code></sub><br><br>`tomcat_deep_bom.json:1`<br><sub><code>{"bomFormat":"CycloneDX","specVersion":"1.7","serialNumber":"urn:uuid:248749a8-c3e5-4230-997b-b12297daf504","version":2,</code></sub><br><br>`tomcat_bom.json:1`<br><sub><code>{"bomFormat":"CycloneDX","specVersion":"1.7","serialNumber":"urn:uuid:e6f0d6c1-f499-4f95-b899-1801b40383f6","version":2,</code></sub> |
| **`ECDSA-P256`**<br><sub>ECDSA-P256</sub> | algorithm / signature | secp256r1 | **ML-DSA-65 / Dilithium (FIPS 204)** | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:37`<br><sub><code>self.legacy_ecdsa_curve = "ECDSA-P256"</code></sub> |
| **`ECDH-X25519`**<br><sub>ECDH-X25519</sub> | algorithm / key-agreement | 25519 | **ML-KEM-768 / Kyber (FIPS 203)** | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:38`<br><sub><code>self.legacy_ecdh_curve = "X25519"</code></sub> |
| **`cryptography (PyCA OpenSSL Asymmetric Primitives (RSA / ECDSA / Ed25519 / X25519))`**<br><sub>RSA-2048 / ECDSA-P256 / Ed25519 / X25519</sub> | signature / signature | 2048 / 256 | **Migrate asymmetric PKI/JWT workflows to OpenSSL 3.5+ ML-KEM (FIPS 203) and ML-DSA (FIPS 204)** | Assimilated Upstream CBOM: PyCA Cryptography / OpenSSL 3.x EVP Reference CBOM<br>`Dependency: cryptography@50.0.2` |
| **`pycryptodome (Python Asymmetric & Key Exchange Primitives (RSA / ECDSA / Ed25519 / X25519))`**<br><sub>RSA-2048 / ECDSA-P256 / Ed25519 / X25519</sub> | signature / signature | 2048 / 256 | **Transition asymmetric signatures and key exchanges to ML-KEM-768 and ML-DSA-65** | Assimilated Upstream CBOM: Python Cryptographic & SSH/JOSE Library Specification<br>`Dependency: pycryptodome@4.4.0` |

### 🔒 Classical Symmetric & Digest Assets

| Component Name | Primitive | Key Length | Quantum Resistance Assessment | Provenance / Location(s) |
|---|---|---|---|---|
| `X.509-Certificate` | certificate | X.509 | Review key length for Grover resistance | First-Party Code (SAST/AST)<br>`ePKI_Root_Certification_Authority.crt:1` |
| `SHA-256` | hash | 256 | Quantum-Resistant (Grover's proof) | First-Party Code (SAST/AST)<br>`bom.json:1`<br>`tomcat_demo_bom.json:12683`<br>`tomcat_demo_bom.json:12684`<br>`tomcat_demo_bom.json:12685`<br>`tomcat_demo_bom.json:12686`<br>`tomcat_demo_bom.json:12687`<br>`tomcat_demo_bom.json:12688`<br>`tomcat_demo_bom.json:12689`<br>`tomcat_demo_bom.json:12690`<br>`tomcat_demo_bom.json:12691`<br>`tomcat_demo_bom.json:12692`<br>`tomcat_demo_bom.json:12693`<br>`tomcat_demo_bom.json:12694`<br>`tomcat_demo_bom.json:12695`<br>`tomcat_demo_bom.json:12696`<br>`tomcat_demo_bom.json:12697`<br>`tomcat_demo_bom.json:12698`<br>`tomcat_demo_bom.json:12699`<br>`tomcat_demo_bom.json:12700`<br>`tomcat_demo_bom.json:12701`<br>`tomcat_demo_bom.json:12702`<br>`tomcat_demo_bom.json:12703`<br>`tomcat_demo_bom.json:12704`<br>`tomcat_demo_bom.json:12705`<br>`tomcat_demo_bom.json:12706`<br>`tomcat_demo_bom.json:12707`<br>`tomcat_demo_bom.json:12708`<br>`tomcat_demo_bom.json:12709`<br>`tomcat_demo_bom.json:12710`<br>`tomcat_demo_bom.json:12711`<br>`tomcat_demo_bom.json:12712`<br>`tomcat_demo_bom.json:12713`<br>`tomcat_demo_bom.json:12714`<br>`tomcat_demo_bom.json:12715`<br>`tomcat_demo_bom.json:12716`<br>`tomcat_demo_bom.json:12717`<br>`tomcat_demo_bom.json:12718`<br>`tomcat_demo_bom.json:12719`<br>`tomcat_demo_bom.json:12720`<br>`tomcat_demo_bom.json:12721`<br>`tomcat_demo_bom.json:12722`<br>`tomcat_demo_bom.json:12723`<br>`tomcat_demo_bom.json:12724`<br>`tomcat_demo_bom.json:12725`<br>`tomcat_demo_bom.json:12726`<br>`tomcat_demo_bom.json:12727`<br>`tomcat_demo_bom.json:12728`<br>`tomcat_demo_bom.json:12729`<br>`tomcat_demo_bom.json:12730`<br>`tomcat_demo_bom.json:12731`<br>`tomcat_demo_bom.json:12732`<br>`tomcat_demo_bom.json:12733`<br>`tomcat_demo_bom.json:12734`<br>`tomcat_demo_bom.json:12735`<br>`tomcat_demo_bom.json:12736`<br>`tomcat_demo_bom.json:12737`<br>`tomcat_demo_bom.json:12738`<br>`tomcat_demo_bom.json:12739`<br>`tomcat_demo_bom.json:12740`<br>`tomcat_demo_bom.json:12741`<br>`tomcat_demo_bom.json:12742`<br>`tomcat_demo_bom.json:12743`<br>`tomcat_demo_bom.json:12744`<br>`tomcat_demo_bom.json:12745`<br>`tomcat_demo_bom.json:12746`<br>`tomcat_demo_bom.json:12747`<br>`tomcat_demo_bom.json:12748`<br>`tomcat_demo_bom.json:12749`<br>`tomcat_demo_bom.json:12750`<br>`tomcat_demo_bom.json:12751`<br>`tomcat_demo_bom.json:12752`<br>`tomcat_demo_bom.json:12753`<br>`tomcat_demo_bom.json:12754`<br>`tomcat_demo_bom.json:12755`<br>`tomcat_demo_bom.json:12756`<br>`tomcat_demo_bom.json:12757`<br>`tomcat_demo_bom.json:12758`<br>`tomcat_demo_bom.json:12759`<br>`tomcat_demo_bom.json:12760`<br>`tomcat_demo_bom.json:12761`<br>`tomcat_demo_bom.json:12762`<br>`tomcat_demo_bom.json:12763`<br>`tomcat_demo_bom.json:12764`<br>`tomcat_demo_bom.json:12765`<br>`tomcat_demo_bom.json:12766`<br>`tomcat_demo_bom.json:12767`<br>`tomcat_demo_bom.json:12768`<br>`tomcat_demo_bom.json:12769`<br>`tomcat_demo_bom.json:12770`<br>`tomcat_demo_bom.json:12771`<br>`tomcat_demo_bom.json:12772`<br>`tomcat_demo_bom.json:12773`<br>`tomcat_demo_bom.json:12774`<br>`tomcat_demo_bom.json:12775`<br>`tomcat_demo_bom.json:12776`<br>`tomcat_demo_bom.json:12777`<br>`tomcat_demo_bom.json:12778`<br>`tomcat_demo_bom.json:12779`<br>`tomcat_demo_bom.json:12780`<br>`tomcat_demo_bom.json:12781`<br>`tomcat_demo_bom.json:12782`<br>`tomcat_demo_bom.json:12783`<br>`tomcat_demo_bom.json:12784`<br>`tomcat_demo_bom.json:12785`<br>`tomcat_demo_bom.json:12786`<br>`tomcat_demo_bom.json:12787`<br>`tomcat_demo_bom.json:12788`<br>`tomcat_demo_bom.json:12789`<br>`tomcat_demo_bom.json:12790`<br>`tomcat_demo_bom.json:12791`<br>`tomcat_demo_bom.json:12792`<br>`tomcat_demo_bom.json:12793`<br>`tomcat_demo_bom.json:12794`<br>`tomcat_demo_bom.json:12795`<br>`tomcat_demo_bom.json:12796`<br>`tomcat_demo_bom.json:12797`<br>`tomcat_demo_bom.json:12798`<br>`tomcat_demo_bom.json:12799`<br>`tomcat_demo_bom.json:12800`<br>`tomcat_demo_bom.json:12801`<br>`tomcat_demo_bom.json:12802`<br>`tomcat_demo_bom.json:12803`<br>`tomcat_demo_bom.json:12804`<br>`tomcat_demo_bom.json:12805`<br>`tomcat_demo_bom.json:12806`<br>`tomcat_demo_bom.json:12807`<br>`tomcat_demo_bom.json:12808`<br>`tomcat_demo_bom.json:12809`<br>`tomcat_demo_bom.json:12810`<br>`tomcat_demo_bom.json:12811`<br>`tomcat_demo_bom.json:12812`<br>`tomcat_demo_bom.json:12813`<br>`tomcat_demo_bom.json:12814`<br>`tomcat_demo_bom.json:12815`<br>`tomcat_demo_bom.json:12816`<br>`tomcat_demo_bom.json:12817`<br>`tomcat_demo_bom.json:12818`<br>`tomcat_demo_bom.json:12819`<br>`tomcat_demo_bom.json:12820`<br>`tomcat_demo_bom.json:12821`<br>`tomcat_demo_bom.json:12822`<br>`tomcat_demo_bom.json:12823`<br>`tomcat_demo_bom.json:12824`<br>`tomcat_demo_bom.json:12825`<br>`tomcat_demo_bom.json:12826`<br>`tomcat_demo_bom.json:12827`<br>`tomcat_demo_bom.json:12828`<br>`tomcat_demo_bom.json:12829`<br>`tomcat_demo_bom.json:12830`<br>`tomcat_demo_bom.json:12831`<br>`tomcat_demo_bom.json:12832`<br>`tomcat_demo_bom.json:12833`<br>`tomcat_demo_bom.json:12834`<br>`tomcat_demo_bom.json:12835`<br>`tomcat_demo_bom.json:12849`<br>`ubuntu_bom.json:1`<br>`tomcat_deep_bom.json:1`<br>`tomcat_bom.json:1` |
| `AES-256-GCM` | block-cipher | 256 | Quantum-Resistant (Grover's proof) | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:41`<br>`pqc_hybrid_service.py:61` |
| `SHA-384` | hash | 384 | Quantum-Resistant (Grover's proof) | First-Party Code (SAST/AST)<br>`pqc_hybrid_service.py:42`<br>`pqc_hybrid_service.py:58` |
| `cookie-signature (Express Signed Cookie HMAC-SHA256 MAC)` | mac | 256 | Quantum-Resistant (Grover's proof) | Assimilated Upstream CBOM: Express Cookie HMAC-SHA256 Signing Specification<br>`Dependency: cookie-signature@1.2.2` |
| `cryptography (PyCA OpenSSL EVP Symmetric & AEAD Suite (AES-256-GCM / ChaCha20-Poly1305 / Fernet))` | block-cipher | 256 | Quantum-Resistant (Grover's proof) | Assimilated Upstream CBOM: PyCA Cryptography / OpenSSL 3.x EVP Reference CBOM<br>`Dependency: cryptography@50.0.2` |
| `pycryptodome (Python Symmetric AEAD & Digest Suite (AES-256-GCM / ChaCha20-Poly1305 / SHA-256))` | block-cipher | 256 | Quantum-Resistant (Grover's proof) | Assimilated Upstream CBOM: Python Cryptographic & SSH/JOSE Library Specification<br>`Dependency: pycryptodome@4.4.0` |

### ⚠️ Unassimilated Third-Party Binaries & Cryptographic Blind Spots

> ℹ️ *The following third-party dependencies do not have verified upstream CBOM attestations in the catalog. They lower the audit confidence score until explicit CBOMs or attestations are published.* 

| Dependency Name | Version | Package URL (purl) | Status |
|---|---|---|---|
| `node_test` | 1.0.0 | `pkg:npm/node_test@1.0.0` | 🟡 Unassimilated (No upstream CBOM) |

### ⚛️ Post-Quantum Cryptography (PQC) Modernization Roadmap

NIST finalized the principal post-quantum cryptography standards in August 2024: **FIPS 203** (ML-KEM), **FIPS 204** (ML-DSA), and **FIPS 205** (SLH-DSA). Below is the recommended migration path for replacing quantum-vulnerable public key algorithms and hardening symmetric ciphers against Grover's algorithm.

#### 🗺️ Cryptographic Algorithm Replacement Matrix

| Classical Primitive | Threat Mechanism | Post-Quantum Replacement | NIST Security Level | Migration Guidance |
|---|---|---|---|---|
| **RSA / Diffie-Hellman / ECDH / X25519** (Key Exchange / KEM) | Broken by Shor's algorithm | **ML-KEM-768 / ML-KEM-1024** (FIPS 203) or Hybrid **X25519MLKEM768** | Level 3 (AES-192 equiv) / Level 5 (AES-256 equiv) | Primary general-purpose key encapsulation. For TLS 1.3 and SSH, deploy hybrid `X25519MLKEM768` for seamless interoperability. |
| **RSA-PSS / ECDSA / Ed25519** (Digital Signatures) | Broken by Shor's algorithm | **ML-DSA-65 / ML-DSA-87** (FIPS 204) | Level 3 / Level 5 | Primary general-purpose lattice signatures for PKI, X.509 certs, code signing, and API tokens. |
| **High-Assurance Root / CA Signatures** | Broken by Shor's algorithm | **SLH-DSA** (FIPS 205 / SPHINCS+) | Level 1, 3, 5 | Stateless hash-based signatures with zero lattice assumptions; ideal for long-lived root trust stores. |
| **Firmware / Secure Boot Signing** | Broken by Shor's algorithm | **LMS / XMSS** (RFC 8554 / RFC 8391, NIST SP 800-208) | Level 3 / Level 5 | Stateful hash-based signatures with minimal memory/code overhead; optimal for microcontrollers. |
| **AES-128 (Symmetric Encryption)** | Halved by Grover's (effective 64-bit security) | **AES-256-GCM** or **ChaCha20-Poly1305** | Level 5 (effective 128-bit quantum security) | Upgrade symmetric key lengths from 128-bit to 256-bit to preserve Grover resistance. |
| **SHA-1 / MD5 (Hash Functions)** | Broken classical collisions + quantum Grover | **SHA-256 / SHA-384 / SHA-512 / SHA-3-256** | Level 3 - 5 | Deprecate weak digests immediately. Use SHA-256 or SHA-3-256 as quantum-safe baseline. |

#### 💻 Multi-Language PQC Implementation Recipes

<details>
<summary><b>Swift (iOS, macOS, Server-side Swift)</b></summary>

```swift
import CryptoKit
// 1. Symmetric Grover resistance (use 256-bit keys)
let symmetricKey = SymmetricKey(size: .bits256)
let sealedBox = try AES.GCM.seal(data, using: symmetricKey)

// 2. Post-Quantum KEM via SwiftCrypto / liboqs-swift:
#if canImport(OQS)
import OQS
let kem = OQSKEM(algorithm: .mlkem768)
let (publicKey, secretKey) = try kem.generateKeyPair()
let (ciphertext, sharedSecretSender) = try kem.encapsulate(publicKey: publicKey)
let sharedSecretReceiver = try kem.decapsulate(ciphertext: ciphertext, secretKey: secretKey)
#endif
```
</details>

<details>
<summary><b>Go (Go 1.24+ crypto/mlkem & Hybrid TLS)</b></summary>

```go
package main

import (
    "crypto/mlkem" // Standard library in Go 1.24+
    "crypto/tls"
)

func main() {
    // 1. FIPS 203 ML-KEM-768 Key Encapsulation
    decapsKey, _ := mlkem.GenerateKey768()
    encapsKey := decapsKey.EncapsulationKey()
    ciphertext, sharedSecretClient := encapsKey.Encapsulate()
    sharedSecretServer, _ := decapsKey.Decapsulate(ciphertext)
    _ = sharedSecretServer

    // 2. Hybrid Post-Quantum TLS 1.3 Client
    tlsConfig := &tls.Config{
        MinVersion:       tls.VersionTLS13,
        CurvePreferences: []tls.CurveID{tls.X25519MLKEM768, tls.X25519},
    }
    _ = tlsConfig
}
```
</details>

<details>
<summary><b>Python (cryptography 44.0+ & liboqs-python)</b></summary>

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# 1. Grover-resistant 256-bit symmetric AEAD
key = AESGCM.generate_key(bit_length=256)
aesgcm = AESGCM(key)

# 2. FIPS 203 ML-KEM-768 via liboqs-python
import oqs
with oqs.KeyEncapsulation('ML-KEM-768') as kem:
    public_key = kem.generate_keypair()
    ciphertext, shared_secret_sender = kem.encap_secret(public_key)
    shared_secret_receiver = kem.decap_secret(ciphertext)
    assert shared_secret_sender == shared_secret_receiver
```
</details>

<details>
<summary><b>Rust (pqcrypto / aws-lc-rs)</b></summary>

```rust
use pqcrypto_kyber::kyber768; // FIPS 203 ML-KEM-768
use pqcrypto_traits::kem::{PublicKey, SecretKey, SharedSecret};

fn main() {
    let (pk, sk) = kyber768::keypair();
    let (ss_sender, ct) = kyber768::encapsulate(&pk);
    let ss_receiver = kyber768::decapsulate(&ct, &sk);
    assert_eq!(ss_sender.as_bytes(), ss_receiver.as_bytes());
}
```
</details>

<details>
<summary><b>Java / Kotlin (Bouncy Castle 1.78+)</b></summary>

```java
import org.bouncycastle.pqc.jcajce.provider.BouncyCastlePQCProvider;
import org.bouncycastle.pqc.jcajce.spec.MLKEMParameterSpec;
import java.security.*;

Security.addProvider(new BouncyCastlePQCProvider());
KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-KEM", "BCPQC");
kpg.initialize(MLKEMParameterSpec.ml_kem_768);
KeyPair kp = kpg.generateKeyPair();
```
</details>

<details>
<summary><b>TypeScript / Node.js</b></summary>

```typescript
import { mlkem768 } from '@noble/post-quantum/ml-kem';

const [aliceKeys, alicePub] = mlkem768.keygen();
const [ciphertext, sharedBob] = mlkem768.encapsulate(alicePub);
const sharedAlice = mlkem768.decapsulate(ciphertext, aliceKeys);
```
</details>

### 🌐 Open Source CBOM Intelligence & Supply Chain Attestation Locators

Third-party dependencies account for the vast majority of cryptographic attack surfaces. When upstream packages do not ship with explicit CBOM files, use the following sources and methods to uncover cryptographic metadata:

1. **OCI 1.1 / Sigstore Cosign Attestations (`application/vnd.cyclonedx+json`)**:
   - Many open-source container images and libraries attach CycloneDX CBOM attestations via Sigstore Cosign.
   - Query attestations using Cosign:
     ```bash
     cosign download attestation --predicate-type https://cyclonedx.org/bom ghcr.io/<org>/<image>:<tag> | jq -r .payload | base64 -d | jq .
     ```
2. **OpenSSF Security Insights (`SECURITY-INSIGHTS.yml`)**:
   - Repositories implementing OpenSSF Security Insights declare encryption standards and key management under `/.github/SECURITY-INSIGHTS.yml`.
3. **Package Registry Provenance & Hash Attestations**:
   - **PyPI (PEP 740)**: Inspect cryptographic provenance via `https://pypi.org/pypi/<package>/json`.
   - **npm Provenance**: Verify build provenance and sign-offs with `npm view <package> --json`.
   - **Swift Package Index**: Discover cryptography framework dependencies directly from SwiftPM manifests and DocC documentation.
4. **Direct Assimilation with `--external-cbom`**:
   - Ingest any vendor or upstream CycloneDX CBOM file directly into `jsi-bom-actions`:
     ```bash
     python scripts/analyze_cbom.py build/cbom.cyclonedx.json --sbom build/sbom.cyclonedx.json --external-cbom vendor.cbom.json
     ```
   - This directly credits verified dependencies and elevates the repository's **Audit Confidence Score**.
