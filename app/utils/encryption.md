

`app/utils/encryption.py` is a Python module that provides utility functions for encryption and decryption of data. Here's a breakdown of the code:

**Importing dependencies**

The module starts by importing necessary dependencies:

* `Fernet` from `cryptography.fernet`: a symmetric encryption algorithm that provides secure encryption and decryption of data.
* `os`: a built-in Python module for interacting with the operating system.
* `base64`: a built-in Python module for encoding and decoding binary data using base64.

**Loading the encryption key**

The module loads an encryption key from an environmental variable named `ENCRYPTION_KEY`. If the key is not set, a `ValueError` is raised.

**Creating a Fernet cipher suite**

The module creates a Fernet cipher suite using the loaded encryption key. The cipher suite is an instance of the `Fernet` class, which provides methods for encryption and decryption.

**Defining the `encrypt_data` function**

The `encrypt_data` function takes in a piece of data to be encrypted and returns the encrypted data. Here's what the function does:

1. If the input data is `None`, the function returns `None`.
2. If the input data is already bytes, the function assumes it's already encrypted and returns the input unchanged.
3. If the input data is not bytes, the function converts it to a string using the `str()` function.
4. The function encrypts the string data using the Fernet cipher suite's `encrypt()` method.
5. The function returns the encrypted data as bytes.

**Defining the `decrypt_data` function**

The `decrypt_data` function takes in a piece of encrypted data and returns the decrypted data. Here's what the function does:

1. If the input data is `None`, the function returns `None`.
2. If the input data is a string, the function encodes it as bytes using the `encode()` method.
3. The function decrypts the bytes data using the Fernet cipher suite's `decrypt()` method.
4. The function decodes the decrypted bytes data as a string using the `decode()` method.
5. The function returns the decrypted string data.

**Error handling**

The `decrypt_data` function catches any exceptions that occur during decryption and raises a `ValueError` with a message indicating that decryption failed.

Overall, `app/utils/encryption.py` provides a simple and secure way to encrypt and decrypt data using the Fernet algorithm. The module can be used throughout the application to protect sensitive data.