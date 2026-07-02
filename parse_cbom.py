#!/usr/bin/env python3
import json
import argparse
import sys
import csv

def parse_cbom(bom_file, asset_types, exclude_asset_types, algorithms, exclude_roots=False):
    try:
        with open(bom_file, 'r') as f:
            bom = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{bom_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File '{bom_file}' is not a valid JSON.")
        sys.exit(1)

    components = bom.get("components", [])
    filtered_components = []

    for comp in components:
        crypto_props = comp.get("cryptoProperties")
        
        # Only process components that have cryptographic properties
        if not crypto_props:
            continue
        
        asset_type = crypto_props.get("assetType", "unknown")
        
        # 1. Apply exclusions first
        if exclude_asset_types and asset_type in exclude_asset_types:
            continue
            
        # 2. Apply inclusions
        if asset_types and asset_type not in asset_types:
            continue

        # 3. Filter by algorithm (searches in both the component name and the primitive properties)
        name = comp.get("name", "unknown")
        alg_props = crypto_props.get("algorithmProperties")
        primitive = alg_props.get("primitive", "unknown") if alg_props else ""
        
        properties = comp.get("properties", [])

        # Fallback primitive parsing using component properties (e.g., for GPG keys)
        if not primitive or primitive == "unknown":
            algo = ""
            strength = ""
            for prop in properties:
                if prop.get("name") == "cdx:crypto:algorithm":
                    algo = str(prop.get("value", ""))
                elif prop.get("name") == "cdx:crypto:keyStrength":
                    strength = str(prop.get("value", ""))
            if algo:
                primitive = f"{algo}-{strength}" if strength else algo

        if algorithms:
            match = False
            for alg in algorithms:
                if alg.lower() in name.lower() or alg.lower() in primitive.lower():
                    match = True
                    break
            if not match:
                continue

        # 4. Extract Trust Store and Public Root status
        trust_store = "N/A"
        public_root = "No"
        
        for prop in properties:
            name_prop = prop.get("name")
            val_prop = prop.get("value")
            if name_prop == "cdx:crypto:trustDomain":
                trust_store = val_prop
            elif name_prop == "cdx:crypto:isCA" and str(val_prop).lower() == "true":
                public_root = "Yes"

        if exclude_roots and public_root == "Yes":
            continue

        # 5. Check if it's PQC-Safe
        pqc_safe = "Unknown"
        pqc_keywords = ["kyber", "dilithium", "falcon", "sphincs", "ml-kem", "ml-dsa", "slh-dsa", "mceliece", "ntru", "saber", "frodokem", "bike", "hqc", "lms", "xmss"]
        vulnerable_keywords = ["rsa", "dsa", "ecc", "ecdh", "ecdsa", "eddsa", "dh", "diffie-hellman", "ed25519", "x25519", "curve25519", "nistp", "secp", "cv25519"]
        
        lower_primitive = primitive.lower() if primitive else ""
        lower_name = name.lower() if name else ""
        
        is_vulnerable = any(k in lower_primitive or k in lower_name for k in vulnerable_keywords)
        is_pqc = any(k in lower_primitive or k in lower_name for k in pqc_keywords)
        
        if is_pqc:
            pqc_safe = "Yes"
        elif is_vulnerable:
            pqc_safe = "No"

        filtered_components.append({
            "name": name,
            "asset_type": asset_type,
            "primitive": primitive if primitive else "N/A",
            "trust_store": trust_store,
            "public_root": public_root,
            "pqc_safe": pqc_safe
        })

    return filtered_components

def main():
    parser = argparse.ArgumentParser(
        description="Parse and filter CBoM (CycloneDX Cryptography Bill of Materials)",
        epilog="Examples:\n"
               "  ./parse_cbom.py -e certificate\n"
               "  ./parse_cbom.py -t algorithm -a RSA -a ECC\n"
               "  ./parse_cbom.py --file bom.json --exclude-asset-type related-crypto-material",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("-f", "--file", default="bom.json", 
                        help="Path to the CBoM json file (default: bom.json)")
    parser.add_argument("-t", "--asset-type", action="append", 
                        help="Include only specific crypto asset types (e.g., 'algorithm', 'certificate', 'related-crypto-material'). Can be specified multiple times.")
    parser.add_argument("-e", "--exclude-asset-type", action="append", 
                        help="Exclude specific crypto asset types. Can be specified multiple times.")
    parser.add_argument("-a", "--algorithm", action="append", 
                        help="Filter by specific algorithm name or primitive (e.g., 'RSA', 'ECC'). Can be specified multiple times.")
    parser.add_argument("--exclude-roots", action="store_true",
                        help="Exclude public root certificates from the output.")
    parser.add_argument("--format", choices=["table", "csv", "json"], default="table",
                        help="Output format (default: table)")
    
    args = parser.parse_args()
    
    results = parse_cbom(args.file, args.asset_type, args.exclude_asset_type, args.algorithm, args.exclude_roots)
    
    if not results:
        print(f"No cryptographic assets found matching the given filters in '{args.file}'.")
        return

    if args.format == "json":
        print(json.dumps(results, indent=2))
        return
    elif args.format == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=["name", "asset_type", "primitive", "pqc_safe", "trust_store", "public_root"])
        writer.writeheader()
        writer.writerows(results)
        return

    # Print results as a formatted table
    print(f"{'COMPONENT NAME':<40} | {'ASSET TYPE':<25} | {'PRIMITIVE':<15} | {'PQC SAFE':<10} | {'TRUST STORE':<15} | {'PUBLIC ROOT':<12}")
    print("-" * 128)
    
    for res in results:
        name = res['name']
        
        # Truncate long names for the table display
        if len(name) > 37:
            name = name[:34] + "..."
            
        print(f"{name:<40} | {str(res['asset_type']):<25} | {str(res['primitive']):<15} | {str(res['pqc_safe']):<10} | {str(res['trust_store']):<15} | {str(res['public_root']):<12}")

if __name__ == "__main__":
    main()
