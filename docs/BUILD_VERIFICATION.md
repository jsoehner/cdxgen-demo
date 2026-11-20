# Build & Functional Verification

- **Date:** 2026-11-20
- **Verified By:** Jeffs' Automated build and deploy agent
- **Repository:** `jsoehner/cdxgen-demo`
- **Status:** VERIFIED

## Trusted OSS Split-Horizon Configuration

- **Local Development (LAN):** Configured via local git-excluded `uv.toml` and `.env` pointing to the Trusted OSS virtual PyPI registry (`--mode virtual`).
- **CI / GitHub Actions (WAN):** Configured repository variables (`TRUSTED_OSS_CACHE_URL=https://jsigroup-oss.duckdns.org`, `TRUSTED_OSS_MODE=virtual`, `TRUSTED_OSS_GPG_EMAIL=oss-signing@the-techy.com`) and mTLS client certificate secrets (`OSS_MTLS_CLIENT_CERT`, `OSS_MTLS_CLIENT_KEY`).
- **Git Hygiene:** Local `.env`, `uv.toml`, `.mvn/settings.xml`, `.mvn/maven.config`, and `.npmrc` are excluded via `.git/info/exclude`.
- **Ecosystem Note:** Python dependencies (`cffi==2.1.1`, `cryptography==50.0.2`, `pycparser==3.12`, `pycryptodome==4.5.0`) resolved cleanly from the Trusted OSS virtual PyPI index. The optional `node_test` fixture was verified with deterministic `npm ci` (Trusted OSS `/npm/` proxy endpoint is not yet enabled, returning HTTP `404`).

## Build & Verification Commands

```bash
# 1. Create isolated Python virtual environment and install dependencies via Trusted OSS PyPI
export PYTHONPYCACHEPREFIX=/tmp/pycache-cdxgen-demo
uv venv /tmp/venv-cdxgen-demo
uv pip install --python /tmp/venv-cdxgen-demo/bin/python \
  --index-url http://oss.jsigroup.local:8080/pypi/virtual/simple \
  -r requirements.txt

# 2. Syntax verification (Python & Bash)
find . -maxdepth 3 -name '*.py' -not -path '*/.git/*' -not -path '*/node_modules/*' -print0 \
  | xargs -0 /tmp/venv-cdxgen-demo/bin/python -m py_compile
bash -n demo.sh scripts/attach_oci_bom.sh scripts/generate_boms.sh scripts/test_boms.sh

# 3. Functional CLI & BOM verification
/tmp/venv-cdxgen-demo/bin/python pqc_hybrid_service.py
/tmp/venv-cdxgen-demo/bin/python parse_cbom.py -f ubuntu_bom.json
/tmp/venv-cdxgen-demo/bin/python parse_cbom.py -a ECC -f tomcat_bom.json
/tmp/venv-cdxgen-demo/bin/python parse_gpg.py --help
/tmp/venv-cdxgen-demo/bin/python -c "import sys; sys.path.insert(0, 'python_test'); import ssl_test; ctx = ssl_test.setup_ssl(); print(type(ctx).__name__)"
/tmp/venv-cdxgen-demo/bin/python scripts/scan_crypto_ast.py . --cbom oss/cbom.json --output-json /tmp/cdxgen-demo-callsites.json
bash scripts/test_boms.sh oss

# 4. Isolated Node.js fixture verification (node_test/)
npm ci --no-audit --no-fund && node --check server.js
```

## Functional Verification Results

| Check | Scope | Result | Evidence |
| :--- | :--- | :--- | :--- |
| **Python Dependency Install** | `requirements.txt` via Trusted OSS PyPI | PASS | Installed `cffi==2.1.1`, `cryptography==50.0.2`, `pycparser==3.12`, `pycryptodome==4.5.0` |
| **Python & Shell Syntax** | All `*.py` and `*.sh` scripts | PASS | `py_compile` and `bash -n` exited `0` |
| **Hybrid PQC Service** | `pqc_hybrid_service.py` | PASS | Established `ML-KEM-768` + `X25519`, `AES-256-GCM`, dual `ML-DSA-65` & `RSA-2048` signatures |
| **CBOM Parser** | `parse_cbom.py` (`ubuntu_bom.json`, `tomcat_bom.json`) | PASS | Parsed GPG keyrings and filtered `ECC` CA certificates (`ECDSA`, PQC Safe: `No`) |
| **GPG Parser CLI** | `parse_gpg.py --help` | PASS | CLI help and argument parsing verified |
| **Python TLS Fixture** | `python_test/ssl_test.py` (`setup_ssl()`) | PASS | Generated 2048-bit RSA key and returned valid `SSLContext` |
| **AST Crypto Reconciliation** | `scripts/scan_crypto_ast.py` | PASS | Found 12 crypto call sites; 100% reconciled against 83 CBOM assets |
| **BOM Test Harness** | `bash scripts/test_boms.sh oss` | PASS | 4/4 checks passed (SBOM JSON, CBOM JSON, CycloneDX v1.7 schema, PQC audit) |
| **Node.js Fixture** | `node_test/` (`npm ci` + `node --check`) | PASS | Installed 67 packages cleanly; `server.js` syntax valid |
| **Web UI / HTTP API** | N/A | N/A | CLI/BOM analysis toolkit (no standalone web UI or API server) |
