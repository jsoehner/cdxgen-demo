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
A bash script that orchestrates the generation of a CBoM from a Docker container image using `cdxgen` and demonstrates parsing it dynamically with `jq`.

#### Usage:
```bash
# Run against a default alpine image
./demo.sh

# Run against a specific image
./demo.sh ubuntu:latest
```

## Features
- **PQC Readiness Identification**: Easily audit your software components and cryptographic assets for classical algorithms that are vulnerable to quantum computing threats.
- **Deep CycloneDX Inspection**: Extracts embedded cryptography metadata, such as algorithm strength, trust domains, and CA root attributes.
- **GPG Key Primitive Extraction**: Translates raw GPG algorithm IDs and elliptic curve parameters into human-readable primitive strings.

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
