import random
import string
import hashlib
from cryptography.fernet import Fernet
import base64

# Greet the user in a playful manner
def greet():
    print("Welcome to the Super Secret Data Encryption Service!")
    print("Let's encrypt and decrypt your data with style.\n")

# Normalize the keys based on user preference
def normalize_key(*keys):
    concatenated_key = ''.join(keys)
    key_bytes = concatenated_key.encode()
    hashed_key = hashlib.sha256(key_bytes).digest()
    return base64.urlsafe_b64encode(hashed_key[:32])

# Generate a random password
def generate_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Encrypt data using the provided key
def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data.decode()

# Decrypt data using the provided key
def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data.encode()).decode()
    return decrypted_data

# Main program
def main():
    greet()  # Greet the user
    while True:
        print("Select an option:")
        print("1. Encrypt data")
        print("2. Decrypt data")
        print("3. Exit")
        option = input("Enter your choice (1, 2, or 3): ")

        if option == '1':
            data = input("Enter the data to encrypt: ")

            # Ask user for encryption method choice
            print("Choose encryption method:")
            print("a. User-defined passkeys")
            print("b. System-generated password")
            encryption_method = input("Enter your choice (a or b): ")

            if encryption_method == 'a':
                num_keys = int(input("How many passkeys do you want to use? (1, 2, or 3): "))
                if num_keys == 1:
                    key1 = input("Enter passkey 1 for encryption: ")
                    normalized_key = normalize_key(key1)
                elif num_keys == 2:
                    key1 = input("Enter passkey 1 for encryption: ")
                    key2 = input("Enter passkey 2 for encryption: ")
                    normalized_key = normalize_key(key1, key2)
                elif num_keys == 3:
                    key1 = input("Enter passkey 1 for encryption: ")
                    key2 = input("Enter passkey 2 for encryption: ")
                    key3 = input("Enter passkey 3 for encryption: ")
                    normalized_key = normalize_key(key1, key2, key3)
                else:
                    print("Invalid number of passkeys.")
                    continue

            elif encryption_method == 'b':
                password = generate_password()
                print("System-generated password:", password)
                normalized_key = normalize_key(password)  # Use same password for all keys
            else:
                print("Invalid encryption method choice.")
                continue

            try:
                encrypted_data = encrypt_data(data, normalized_key)
                print("Encrypted data:", encrypted_data)
            except ValueError as e:
                print("Encryption error:", e)

        elif option == '2':
            data = input("Enter the data to decrypt: ")

            # Ask user for decryption passkeys
            num_keys = int(input("How many passkeys do you want to use? (1, 2, or 3): "))
            if num_keys == 1:
                key1 = input("Enter passkey 1 for decryption: ")
                normalized_key = normalize_key(key1)
            elif num_keys == 2:
                key1 = input("Enter passkey 1 for decryption: ")
                key2 = input("Enter passkey 2 for decryption: ")
                normalized_key = normalize_key(key1, key2)
            elif num_keys == 3:
                key1 = input("Enter passkey 1 for decryption: ")
                key2 = input("Enter passkey 2 for decryption: ")
                key3 = input("Enter passkey 3 for decryption: ")
                normalized_key = normalize_key(key1, key2, key3)
            else:
                print("Invalid number of passkeys.")
                continue

            try:
                decrypted_data = decrypt_data(data, normalized_key)
                print("Decrypted data:", decrypted_data)
            except ValueError as e:
                print("Decryption error:", e)

        elif option == '3':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
