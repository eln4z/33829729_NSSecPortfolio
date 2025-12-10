from password_strength import password_strength
from hashing import hash_demo
from brute_force import brute_force_demo
from system import AuthSystem
import hashlib

def main():
    auth = AuthSystem()

    while True:
        print("\n==== NSSec Week 03 Demo (Modular Version) ====")
        print("1) Check password strength")
        print("2) Hashing demo")
        print("3) Brute-force demo")
        print("4) Register user (bcrypt + TOTP)")
        print("5) Login user (password + TOTP)")
        print("0) Exit")
        choice = input("Choice: ")

        if choice == "1":
            pwd = input("Enter password: ")
            score, entropy = password_strength(pwd)
            print(f"Score: {score}/7  |  Entropy: {entropy} bits")

        elif choice == "2":
            pwd = input("Enter password: ")
            md5_hash, sha256_hash, bcrypt_hash = hash_demo(pwd)
            print("MD5     :", md5_hash)
            print("SHA-256 :", sha256_hash)
            print("bcrypt  :", bcrypt_hash)

        elif choice == "3":
            target = hashlib.sha256(b"password").hexdigest()
            found, pwd, tries = brute_force_demo(target)
            if found:
                print(f"Cracked in {tries} tries → {pwd}")
            else:
                print("Not cracked in small list.")

        elif choice == "4":
            user = input("Username: ")
            pwd = input("Password: ")
            ok, msg = auth.register(user, pwd)
            print(msg)

        elif choice == "5":
            user = input("Username: ")
            pwd = input("Password: ")
            token = input("TOTP code: ")
            ok, msg = auth.login(user, pwd, token)
            print(msg)

        elif choice == "0":
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
