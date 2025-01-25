from cryptography.fernet import Fernet
key = Fernet.generate_key()
fernet = Fernet(key)

def ncrypt(a):
    temp1 = fernet.encrypt(a.encode())
    b = temp1.decode()
    return b
