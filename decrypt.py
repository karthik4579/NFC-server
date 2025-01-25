import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.asymmetric import rsa

# Function to decrypt AES-encrypted data
def decrypt_password(encrypted_data, key):
    # Decode the Base64-encoded AES key
    decoded_key = base64.b64decode(key)

    # Decode the Base64-encoded encrypted data
    decoded_encrypted_data = base64.b64decode(encrypted_data)

    # Initialize AES cipher with the provided key
    cipher = Cipher(algorithms.AES(decoded_key), modes.ECB())
    decryptor = cipher.decryptor()

    # Decrypt the data
    decrypted_data = decryptor.update(decoded_encrypted_data) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return decrypted_data.decode('utf-8')