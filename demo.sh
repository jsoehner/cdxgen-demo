#!/bin/bash

# Exit on error
set -e

# Default to alpine:latest if no image name is provided
IMAGE_NAME=${1:-"alpine:latest"}
BOM_FILE="bom.json"

echo "========================================================"
echo " CBoM Generation and Parsing Demo with cdxgen and jq"
echo "========================================================"
echo "Target Image : $IMAGE_NAME"
echo "Output File  : $BOM_FILE"
echo "========================================================"
echo ""

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install jq to run this demo."
    exit 1
fi

echo "[Step 1] Generating CBoM (CycloneDX Bill of Materials) using cdxgen..."
# Using npx to run cdxgen without requiring manual global installation
# If you have cdxgen installed globally, you can replace this with:
# cdxgen -t container "$IMAGE_NAME" -o "$BOM_FILE" --include-crypto --component-type cryptographic-asset
npx -y @cyclonedx/cdxgen -t container "$IMAGE_NAME" -o "$BOM_FILE" --include-crypto --component-type cryptographic-asset

if [ ! -f "$BOM_FILE" ]; then
    echo "Error: Failed to generate $BOM_FILE"
    exit 1
fi

echo ""
echo "[Step 2] Parsing the CBoM using jq to itemize components..."
echo "--------------------------------------------------------"
printf "%-30s | %-15s | %-10s\n" "COMPONENT NAME" "VERSION" "TYPE"
echo "--------------------------------------------------------"

# Parse the CycloneDX JSON with jq
# -r outputs raw strings instead of JSON strings
# .components[]? safely iterates over components if the array exists
# We extract name, version, and type for each component
jq -r '.components[]? | "\(.name | .[0:29]) \t| \(.version | .[0:14]) \t| \(.type)"' "$BOM_FILE" | awk -F'\t\\| ' '{printf "%-30s | %-15s | %-10s\n", $1, $2, $3}'

# Alternative simpler jq formatting without awk if preferred:
# jq -r '.components[]? | "- \(.name) (\(.version)) [\(.type)]"' "$BOM_FILE"

echo "--------------------------------------------------------"
echo "Done! The full JSON CBoM is available in $BOM_FILE"
