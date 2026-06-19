import ssl
import socket
from cryptography.hazmat.primitives.asymmetric import rsa

def setup_ssl():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    context.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384')
    
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return context
