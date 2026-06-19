import json

with open('tomcat_bom.json', 'r') as f:
    bom = json.load(f)

# Inject an example of a cryptographic algorithm that cdxgen would detect in Java
bom['components'].append({
  "name": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
  "type": "cryptographic-asset",
  "cryptoProperties": {
    "assetType": "algorithm",
    "algorithmProperties": {
      "primitive": "ae",
      "cryptoFunctions": ["keygen", "encrypt", "decrypt"],
      "executionEnvironment": "software-plain-ram"
    }
  }
})
bom['components'].append({
  "name": "RSA",
  "type": "cryptographic-asset",
  "cryptoProperties": {
    "assetType": "algorithm",
    "algorithmProperties": {
      "primitive": "public-key",
      "cryptoFunctions": ["sign", "verify"]
    }
  }
})

with open('tomcat_demo_bom.json', 'w') as f:
    json.dump(bom, f, indent=2)
