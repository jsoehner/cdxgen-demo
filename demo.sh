#!/bin/bash

# Exit on error
set -e

EXTRACT_MODE=0
IMAGE_NAME="alpine:latest"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -e|--extract) EXTRACT_MODE=1 ;;
        *) IMAGE_NAME="$1" ;;
    esac
    shift
done

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
jq -r '.components[]? | "\(.name | .[0:29]) \t| \(.version | .[0:14]) \t| \(.type)"' "$BOM_FILE" | awk -F'\t\\| ' '{printf "%-30s | %-15s | %-10s\n", $1, $2, $3}'

echo "--------------------------------------------------------"
echo "Done! The full JSON CBoM is available in $BOM_FILE"

if [ "$EXTRACT_MODE" -eq 1 ]; then
    echo ""
    echo "[Step 3] Interactive Certificate Extraction"
    
    cert_names=()
    while IFS= read -r name; do
        if [ -n "$name" ]; then
            cert_names+=("$name")
        fi
    done < <(jq -r '.components[]? | select(.cryptoProperties.assetType == "certificate") | select(.properties[]?.name == "SrcFile") | .name' "$BOM_FILE")

    if [ ${#cert_names[@]} -eq 0 ]; then
        echo "No extractable certificates found."
        exit 0
    fi

    echo "Select a certificate to extract (or press Ctrl+C to exit):"
    
    PS3="Enter the number of the certificate to extract: "
    select SELECTED_CERT in "${cert_names[@]}"; do
        if [ -n "$SELECTED_CERT" ]; then
            echo "You selected: $SELECTED_CERT"
            FILE_PATH=$(jq -r --arg name "$SELECTED_CERT" '.components[]? | select(.name == $name) | .properties[]? | select(.name == "SrcFile") | .value' "$BOM_FILE" | head -n 1)
            
            if [ -z "$FILE_PATH" ] || [ "$FILE_PATH" == "null" ]; then
                echo "Error: Could not find SrcFile for $SELECTED_CERT"
            else
                echo "Extracting $FILE_PATH from container $IMAGE_NAME..."
                CONTAINER=$(docker create "$IMAGE_NAME")
                
                FILENAME=$(basename "$FILE_PATH")
                docker cp "${CONTAINER}:${FILE_PATH}" "./$FILENAME"
                docker rm "$CONTAINER" >/dev/null
                
                echo "Successfully extracted to ./$FILENAME"
                
                echo "Certificate details:"
                openssl x509 -in "./$FILENAME" -text -noout | head -n 15
                echo "..."
            fi
            break
        else
            echo "Invalid selection. Please try again."
        fi
    done
fi
