# Cryptography Bill of Materials (CBoM) Utilities

This repository contains utilities for generating, parsing, and evaluating Cryptography Bill of Materials (CBoM) in the CycloneDX format, as well as tools for identifying cryptographic primitives in GPG environments.

## Tools Overview

### 1. `parse_cbom.py`
A Python script designed to parse CycloneDX CBoM JSON files and extract relevant cryptographic components. It has been enhanced to:
- Identify cryptographic primitives directly from `algorithmProperties` or fallback to extracting them from generic component `properties` (useful for GPG keys and other related crypto materials).
- Automatically evaluate and flag whether a cryptographic primitive or algorithm is **PQC Safe** (Post-Quantum Cryptography). Classical public-key algorithms (like RSA, DSA, ECC) will be flagged as vulnerable (`No`), while algorithms like Kyber, Dilithium, and Falcon will be flagged as safe (`Yes`).

#### Usage:
```bash
# Basic usage against a default bom.json
./parse_cbom.py

# Specify a specific CBoM JSON file
./parse_cbom.py -f ubuntu_bom.json

# Filter for specific algorithms
./parse_cbom.py -a RSA -a ECC

# Filter by specific asset type
./parse_cbom.py -t certificate
```

#### Example Output:
```text
COMPONENT NAME                           | ASSET TYPE                | PRIMITIVE       | PQC SAFE   | TRUST STORE     | PUBLIC ROOT 
--------------------------------------------------------------------------------------------------------------------------------
ubuntu-archive-keyring.gpg               | certificate               | unknown         | Unknown    | N/A             | No          
ubuntu-archive-removed-keys.gpg          | certificate               | unknown         | Unknown    | N/A             | No          
ubuntu-cloudimage-keyring.gpg            | certificate               | unknown         | Unknown    | N/A             | No          
ubuntu-cloudimage-removed-keys.gpg       | certificate               | unknown         | Unknown    | N/A             | No          
ubuntu-keyring-2012-cdimage.gpg          | certificate               | unknown         | Unknown    | N/A             | No          
ubuntu-keyring-2018-archive.gpg          | certificate               | unknown         | Unknown    | N/A             | No          
ubuntu-master-keyring.gpg                | certificate               | unknown         | Unknown    | N/A             | No          
ubuntu-keyring-2012-cdimage.gpg          | related-crypto-material   | RSA-4096        | No         | apt             | No          
ubuntu-keyring-2018-archive.gpg          | related-crypto-material   | RSA-4096        | No         | apt             | No          
ubuntu-archive-keyring.gpg               | related-crypto-material   | RSA-4096        | No         | apt             | No          
ubuntu-archive-removed-keys.gpg          | related-crypto-material   | DSA-1024        | No         | apt             | No          
ubuntu-cloudimage-keyring.gpg            | related-crypto-material   | RSA-4096        | No         | apt             | No          
ubuntu-cloudimage-removed-keys.gpg       | related-crypto-material   | N/A             | Unknown    | apt             | No          
ubuntu-master-keyring.gpg                | related-crypto-material   | RSA-4096        | No         | apt             | No          
```

#### Example Output (Filtering for ECC):
```bash
./parse_cbom.py -a ECC -f tomcat_bom.json
```
```text
COMPONENT NAME                           | ASSET TYPE                | PRIMITIVE       | PQC SAFE   | TRUST STORE     | PUBLIC ROOT 
--------------------------------------------------------------------------------------------------------------------------------
AffirmTrust Premium ECC                  | certificate               | ECDSA           | No         | ca-store        | Yes         
Atos TrustedRoot Root CA ECC TLS 2021    | certificate               | ECDSA           | No         | ca-store        | Yes         
COMODO ECC Certification Authority       | certificate               | ECDSA           | No         | ca-store        | Yes         
CommScope Public Trust ECC Root-01       | certificate               | ECDSA           | No         | ca-store        | Yes         
CommScope Public Trust ECC Root-02       | certificate               | ECDSA           | No         | ca-store        | Yes         
DigiCert TLS ECC P384 Root G5            | certificate               | ECDSA           | No         | ca-store        | Yes         
HARICA TLS ECC Root CA 2021              | certificate               | ECDSA           | No         | ca-store        | Yes         
Hellenic Academic and Research Ins...    | certificate               | ECDSA           | No         | ca-store        | Yes         
Microsoft ECC Root Certificate Aut...    | certificate               | ECDSA           | No         | ca-store        | Yes         
SSL.com EV Root Certification Auth...    | certificate               | ECDSA           | No         | ca-store        | Yes         
SSL.com Root Certification Authori...    | certificate               | ECDSA           | No         | ca-store        | Yes         
SSL.com TLS ECC Root CA 2022             | certificate               | ECDSA           | No         | ca-store        | Yes         
Security Communication ECC RootCA1       | certificate               | ECDSA           | No         | ca-store        | Yes         
Trustwave Global ECC P256 Certific...    | certificate               | ECDSA           | No         | ca-store        | Yes         
Trustwave Global ECC P384 Certific...    | certificate               | ECDSA           | No         | ca-store        | Yes         
USERTrust ECC Certification Authority    | certificate               | ECDSA           | No         | ca-store        | Yes         
emSign ECC Root CA - C3                  | certificate               | ECDSA           | No         | ca-store        | Yes         
emSign ECC Root CA - G3                  | certificate               | ECDSA           | No         | ca-store        | Yes         
vTrus ECC Root CA                        | certificate               | ECDSA           | No         | ca-store        | Yes         
```

### 2. `parse_gpg.py`
A lightweight script that interfaces directly with GnuPG's machine-readable output (`--with-colons`) to identify the exact cryptographic primitives used for both master keys and subkeys (e.g., `RSA-4096`, `ed25519`).

#### Usage:
```bash
# Parse all keys in your GPG keyring
./parse_gpg.py

# Query a specific key ID or email
./parse_gpg.py user@example.com

# Parse from a saved output file
./parse_gpg.py --file gpg_output.txt
```

### 3. `demo.sh`
A bash script that orchestrates the generation of a CBoM from a Docker container image using `cdxgen` and demonstrates parsing it dynamically with `jq`. It also features an interactive extraction mode.

#### Usage:
```bash
# Run against a default alpine image
./demo.sh

# Run against a specific image
./demo.sh ubuntu:latest

# Run interactively to extract a certificate from the container
./demo.sh -e tomcat:latest
```

### 4. Enterprise SBOM & CBOM Automation Pipeline (`scripts/`)
A production-ready suite of automation, analysis, and verification scripts:

- **`scripts/generate_boms.sh`**: Generates both standard SBOM (`sbom.cyclonedx.json`) and cryptographic bill of materials (`cbom.json`) for source repositories or container images. Supports OCI 1.1 referrer discovery and automatic fallback to `npx @cyclonedx/cdxgen`.
  ```bash
  # Scan current source repository
  bash scripts/generate_boms.sh .

  # Scan a container image
  bash scripts/generate_boms.sh -t docker my-app:latest
  ```

- **`scripts/analyze_cbom.py`**: Analyzes generated CBOMs against standard software inventories, evaluating:
  - **PQC Readiness**: Identifies quantum-vulnerable primitives (RSA, ECDSA, ECDH) vs migrated NIST standards (ML-KEM-768, ML-DSA-65, SLH-DSA).
  - **Grover Resistance**: Verifies symmetric key lengths (AES-256, SHA-384+).
  - **Supply Chain Confidence**: Quantifies verified dependencies vs unassimilated supply chain blind spots.
  - **OS Inventory Verification**: Tracks system-level cryptographic packages.
  ```bash
  python3 scripts/analyze_cbom.py oss/cbom.json --sbom oss/sbom.cyclonedx.json --markdown docs/security/CRYPTOGRAPHIC_AUDIT.md
  ```

- **`scripts/scan_crypto_ast.py`**: Performs dual-engine semantic AST scanning across Python, JavaScript/TypeScript, Go, Java, Rust, C#, and C/C++ source code to discover cryptographic call sites and reconcile them 100% against the CBOM.
  ```bash
  python3 scripts/scan_crypto_ast.py . --cbom oss/cbom.json
  ```

- **`scripts/test_boms.sh`**: Automated verification test harness asserting JSON syntax, CycloneDX schema conformance, and non-empty crypto asset discovery.
  ```bash
  bash scripts/test_boms.sh oss
  ```

- **`scripts/update_os_inventory.py`**: Scans host OS package managers (`dpkg`, `rpm`) for installed cryptographic runtime components and updates `known_cbom_catalog.json`.
  ```bash
  python3 scripts/update_os_inventory.py
  ```

- **`scripts/fetch_oci_cbom.py` & `scripts/attach_oci_bom.sh`**: Query OCI 1.1 referrers without pulling image layers, and attach generated CBOM artifacts to OCI registries via ORAS.
  ```bash
  python3 scripts/fetch_oci_cbom.py <IMAGE_REF> -o oss/upstream_cbom.json
  bash scripts/attach_oci_bom.sh oss/cbom.json <IMAGE_REF>
  ```

### 5. `pqc_hybrid_service.py`
Demonstration of a hybrid Post-Quantum Cryptographic service architecture designed for transition-era systems:
- **Quantum-Resistant Key Encapsulation**: Uses **ML-KEM-768** (NIST FIPS 203) combined with classical **ECDH-X25519** via SHA-384 key derivation to establish **AES-256-GCM** session encryption.
- **Dual Digital Signatures**: Signs transactions simultaneously using **ML-DSA-65** (NIST FIPS 204) and legacy **RSA-2048** / **ECDSA-P256** for backwards compatibility.

```bash
python3 pqc_hybrid_service.py
```

## Features
- **PQC Readiness Identification**: Easily audit your software components and cryptographic assets for classical algorithms that are vulnerable to quantum computing threats.
- **Dual-Engine AST Scanning**: Validates first-party cryptographic usage in source code directly against the generated CBOM inventory.
- **Deep CycloneDX Inspection**: Extracts embedded cryptography metadata, such as algorithm strength, trust domains, and CA root attributes.
- **GPG Key Primitive Extraction**: Translates raw GPG algorithm IDs and elliptic curve parameters into human-readable primitive strings.
- **CI/CD Integration**: Pre-configured GitHub Actions workflow (`.github/workflows/sbom.yml`) to automatically generate, verify, and track BOM artifacts on push and PR.

## Advanced Example: Carving Artifacts from Container Images

You can dynamically parse a CBoM to locate a specific cryptographic asset (such as a certificate) and extract it directly from the original Docker image layer. 

Here is an example demonstrating how to carve out the `ePKI_Root_Certification_Authority.crt` certificate from a `tomcat:latest` image based on its CBoM, and then parse it using `openssl`:

```bash
# 1. Define your target image and artifact
IMAGE="tomcat:latest"
BOM_FILE="tomcat_demo_bom.json"
ARTIFACT="ePKI_Root_Certification_Authority.crt"

# 2. Extract the file's internal location from the CBoM using jq
FILE_PATH=$(jq -r --arg name "$ARTIFACT" '.components[]? | select(.name == $name) | .properties[]? | select(.name == "SrcFile") | .value' "$BOM_FILE" | head -n 1)

# 3. Create a temporary container to extract the physical file
CONTAINER=$(docker create "$IMAGE")
docker cp "${CONTAINER}:${FILE_PATH}" "./$ARTIFACT"
docker rm "$CONTAINER" >/dev/null

# 4. Parse and display the certificate values
openssl x509 -in "./$ARTIFACT" -text -noout
```

## Gotchas

When working with CBoMs and these utilities, keep the following in mind:

1. **Unpredictable CBoM Filenames**: CBoM files do not have a rigidly enforced naming convention (e.g., they aren't always named `bom.json` or `*_bom.json`). When scanning a repository or container for existing CBoMs, do not rely on filenames. Instead, dynamically search for files containing the `"cryptoProperties"` JSON attribute, which is a reliable indicator of CBoM data.
2. **Missing Dependencies (`cdxgen`)**: If `cdxgen` is not installed globally on your system, running it directly will fail. It is recommended to use `npx -y @cyclonedx/cdxgen` to guarantee it runs smoothly without manual installation.
3. **Extraction Mode Requires Docker**: The interactive certificate extraction feature in `demo.sh` relies on `docker create` and `docker cp`. This means a local Docker daemon must be running and accessible to the user executing the script.
4. **JSON Formatting Issues**: Ensure that any injected algorithms or manual modifications (such as those performed by `inject_algo.py`) maintain valid JSON structure, or `parse_cbom.py` will fail to parse the file.


## 🛡️ Security & Cryptographic Posture
This project tracks Software & Cryptographic Bill of Materials (SBOM & CBOM) and Post-Quantum Cryptography (PQC) readiness.

| Metric | Status / Value | Standard / Target |
| :--- | :--- | :--- |
| **BOM Format** | CycloneDX v1.7 | OWASP CycloneDX CBOM Specification |
| **PQC Migration Progress** | **37.5%** | NIST FIPS 203 / 204 / 205 |
| **Post-Quantum Ready Assets** | **3** (`ML-KEM-768`, `ML-DSA-65`, `SLH-DSA`) | Quantum-Resistant Algorithms |
| **Quantum-Vulnerable Backlog** | **5** (`RSA-2048`, `ECDSA-P256`, `ECDH-X25519`, `Ed25519`, `DH`) | Harvest-Now-Decrypt-Later Backlog |
| **Classical Symmetric / Digests** | **4** (`AES-256-GCM`, `SHA-256`, `SHA-384`, `Stateful-Hash`) | Grover Resistance Verified |
| **First-Party Code Coverage** | **100% AST Reconciled** | Zero unvetted custom crypto |

- 📊 **Detailed Audit Report**: See the latest [Cryptographic Audit & PQC Migration Report](docs/security/CRYPTOGRAPHIC_AUDIT.md).
- 📜 **Policy Standard**: Governed by the [Hybrid Post-Quantum Cryptography Migration and CBOM Audit Standard](file:///home/jsoehner/memory_system/knowledge/okf/cbom_pqc_migration_and_hybrid_cryptography_standard.md).

