import os
import binascii
 
# Generate a 24-byte random key and convert it to a hexadecimal string
secret_key = binascii.hexlify(os.urandom(24)).decode()
print(secret_key)