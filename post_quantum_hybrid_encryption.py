"""
Hybrid encryption process combining a post-quantum key encapsulation mechanism (KEM) for key exchange and AES for symmetric encryption.

Steps:
1. Both client and server use liboqs's ML-KEM-512.
2. The client generates its key pair.
3. The server encapsulates a shared secret using the client's public key.
4. The client decapsulates the ciphertext to obtain the same shared secret.
5. We then take the shared secret (or a derived key) to encrypt/decrypt an arbitrary text message using AES.
"""

import logging
from pprint import pformat
from sys import stdout
import os
import oqs

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stdout))

# Log liboqs details
logger.info("liboqs version: %s", oqs.oqs_version())
logger.info("liboqs-python version: %s", oqs.oqs_python_version())
logger.info(
    "Enabled KEM mechanisms:\n%s",
    pformat(oqs.get_enabled_kem_mechanisms(), compact=True),
)

# Set the chosen KEM algorithm
kemalg = "ML-KEM-512"

# Perform KEM key exchange to generate a shared secret:
with oqs.KeyEncapsulation(kemalg) as client:
    with oqs.KeyEncapsulation(kemalg) as server:
        logger.info("Key encapsulation details:\n%s", pformat(client.details))

        # Client generates its keypair.
        public_key_client = client.generate_keypair()

        # Server encapsulates its secret using the client's public key.
        ciphertext, shared_secret_server = server.encap_secret(public_key_client)

        # Client decapsulates the ciphertext to recover the shared secret.
        shared_secret_client = client.decap_secret(ciphertext)

        if shared_secret_client == shared_secret_server:
            logger.info("Shared secrets match. Proceeding with symmetric encryption.")
        else:
            logger.error("Shared secrets do not match!")
            exit(1)

# Use the shared secret as a symmetric key for AES encryption.
# Make sure the key is the proper length for AES-256 (32 bytes). If the shared secret isn't long enough,
# a key derivation function should be used.
key = shared_secret_client[:32]

# Set up the plaintext message to be encrypted.
plaintext = b"Hello, this is a secret message from quantum-resistant hybrid encryption!"

# logger.info("Message to be encrypted: %s", plaintext)

# Generate a random IV for AES. AES block size is 16 bytes.
iv = os.urandom(16)

# Encrypt the plaintext using AES in CFB mode.
encryptor = Cipher(
    algorithms.AES(key), modes.CFB(iv), backend=default_backend()
).encryptor()

ciphertext_text = encryptor.update(plaintext) + encryptor.finalize()

logger.info("Encrypted message (hex): %s", ciphertext_text.hex())

# To decrypt, use the same key and IV.
decryptor = Cipher(
    algorithms.AES(key), modes.CFB(iv), backend=default_backend()
).decryptor()

decrypted_text = decryptor.update(ciphertext_text) + decryptor.finalize()

logger.info("Decrypted message: %s", decrypted_text.decode())