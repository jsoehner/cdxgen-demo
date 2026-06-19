#!/usr/bin/env python3
import subprocess
import sys
import argparse

ALGO_MAP = {
    "1": "RSA",
    "2": "RSA (Encrypt Only)",
    "3": "RSA (Sign Only)",
    "16": "Elgamal",
    "17": "DSA",
    "18": "ECDH",
    "19": "ECDSA",
    "20": "Elgamal (Encrypt/Sign)",
    "22": "EdDSA",
    "23": "AEDSA"
}

def get_primitive(algo_id, length, curve_name):
    algo_name = ALGO_MAP.get(algo_id, f"Unknown({algo_id})")
    # For Elliptic Curves, the primitive is usually the curve name itself (e.g. ed25519)
    if algo_id in ("18", "19", "22", "23") and curve_name:
        return curve_name
    # For others like RSA/DSA, we append the key length
    elif algo_name != f"Unknown({algo_id})" and length:
        return f"{algo_name}-{length}"
    else:
        return algo_name

def parse_gpg_colons(output):
    results = []
    lines = output.strip().split('\n')
    for line in lines:
        parts = line.split(':')
        # Check if the record is a public master key (pub) or public subkey (sub)
        # The output has many fields, at least 17 are needed to get the curve name
        if len(parts) >= 17 and parts[0] in ("pub", "sub"):
            record_type = parts[0]
            length = parts[2]
            algo_id = parts[3]
            key_id = parts[4]
            # Field 17 is index 16 (0-indexed)
            curve_name = parts[16]
            
            primitive = get_primitive(algo_id, length, curve_name)
            
            results.append({
                "type": record_type,
                "key_id": key_id,
                "length": length,
                "algorithm": ALGO_MAP.get(algo_id, f"ID {algo_id}"),
                "curve": curve_name,
                "primitive": primitive
            })
    return results

def main():
    parser = argparse.ArgumentParser(description="Parse GPG --with-colons output to identify cryptographic primitives.")
    parser.add_argument("key_id", nargs="?", help="Key ID or Email to query. If omitted, queries all keys.", default="")
    parser.add_argument("--file", help="Read colon-separated output from a file instead of running GPG.")
    
    args = parser.parse_args()
    
    if args.file:
        try:
            with open(args.file, 'r') as f:
                output = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)
    else:
        cmd = ["gpg", "--list-options", "show-unusable-keys", "--list-keys", "--with-colons"]
        if args.key_id:
            cmd.append(args.key_id)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error running GPG: {e}\n(Is the key missing?)")
            sys.exit(1)
        except FileNotFoundError:
            print("Error: gpg command not found. Is GnuPG installed?")
            sys.exit(1)
            
    parsed_keys = parse_gpg_colons(output)
    
    if not parsed_keys:
        print("No public keys (pub/sub) found.")
        sys.exit(0)
        
    print(f"{'TYPE':<5} | {'KEY ID':<16} | {'LENGTH':<6} | {'ALGORITHM':<10} | {'CURVE':<15} | {'PRIMITIVE':<15}")
    print("-" * 78)
    for key in parsed_keys:
        print(f"{key['type']:<5} | {key['key_id']:<16} | {key['length']:<6} | {key['algorithm']:<10} | {key['curve']:<15} | {key['primitive']:<15}")

if __name__ == "__main__":
    main()
