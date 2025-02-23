# post-quantum-hybrid-encryption


This repository demonstrates a hybrid encryption approach that combines a post-quantum key encapsulation mechanism (KEM) with symmetric AES encryption. The example is implemented in Python using the [liboqs](https://github.com/open-quantum-safe/liboqs) library for post‑quantum algorithms and [cryptography](https://cryptography.io/en/latest/) for AES encryption. It utilises and is inspired by the Python bindings from the Open Quantum Safe (OQS) project.

## Overview

The main file in this repository is:
**`post_quantum_hybrid_encryption.py`**

This file performs the following steps:

1. **Post-Quantum Key Exchange**  
   - Both the client and server use liboqs's `ML-KEM-512` algorithm.
   - The client generates its key pair.
   - The server encapsulates a shared secret using the client's public key.
   - The client decapsulates the ciphertext to obtain the same shared secret.
   - The script verifies that both shared secrets match.

2. **Symmetric Encryption with AES**  
   - The shared secret is used (or derived) as a 32-byte AES-256 key.
   - A plaintext message is encrypted using AES in CFB mode with a randomly generated IV.
   - The encrypted message is then decrypted back to the original plaintext.

This hybrid approach leverages quantum-resistant key exchange to secure the symmetric key, while using a well-established encryption algorithm (AES) for bulk data encryption.

## Prerequisites

- [Python 3](https://www.python.org/)
- [liboqs](https://github.com/open-quantum-safe/liboqs) and [liboqs-python](https://github.com/open-quantum-safe/liboqs/tree/main/python)
  - Will be installed automatically.
- [git](https://git-scm.com/)
- [CMake](https://cmake.org/)
- C compiler, e.g., [gcc](https://gcc.gnu.org/), [clang](https://clang.llvm.org), [MSVC](https://visualstudio.microsoft.com/vs/) etc.


## Installation

Possibly the easiest way to install the Python and C libraries to get everything up and running, is via a virtual environment, as below:

Execute in a Terminal/Console/Administrator Command Prompt

```shell
python3 -m venv venv
. venv/bin/activate
python3 -m ensurepip --upgrade
```

On Windows, replace the line

```shell
. venv/bin/activate
```

by

```shell
venv\Scripts\activate.bat
```

If `liboqs` is not found at runtime by `liboqs-python`, it will be automatically downloaded, configured, and installed as a shared library. This one-time process occurs when the `liboqs-python` wrapper is loaded. The `liboqs` source directory will be removed upon completion.

Other methods of installation, including utilising Docker, and building the C library from source, can be observed by visiting the liboqs Python bindings repository [here](https://github.com/open-quantum-safe/liboqs-python).

### Install this application and dependencies

Execute in a Terminal/Console/Administrator Command Prompt

```shell
git clone --depth=1 https://github.com/semsion/post-quantum-hybrid-encryption
cd post-quantum-hybrid-encryption
pip install .
```

### Running the Example

To run the hybrid encryption process, execute the following command in your terminal:

```bash
python post_quantum_hybrid_encryption.py
```

Upon execution, the script will:

- Log liboqs and liboqs-python version details.
- List all enabled KEM mechanisms.
- Perform the key exchange and verify if the shared secrets match.
- Encrypt an arbitrary message using AES.
- Decrypt the message and display the decrypted text.

### How It Works

1. **Key Exchange Using KEM:**
- The client generates a key pair.
- The server uses the client's public key to encapsulate a secret and produce a ciphertext.
- The client decapsulates the ciphertext to recover the shared secret.
- The script verifies that the shared secrets between the client and server are identical.

2. **Symmetric Encryption Using AES:**
- The shared secret is truncated (or properly derived) to form a 32-byte key.
- A random 16-byte IV (Initialization Vector) is generated.
- The plaintext message is encrypted using AES in CFB mode.
- The ciphertext is decrypted back to plaintext using the same AES key and IV.

### Acknowledgements

- [Open Quantum Safe Project](https://openquantumsafe.org/) for the liboqs library and Python bindings.
- [cryptography](https://cryptography.io/) for providing a simple-to-use cryptographic interface.
