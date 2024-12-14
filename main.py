import sys
import os
import argparse
from getpass import getpass
from utils.analyzer import analyze_password
from utils.generator import generate_strong_password
from utils.storage import store_password, retrieve_passwords
from utils.master_password import setup_master_password, verify_master_password
from datetime import datetime, timezone

def display_menu():
    print("\nWelcome! What would you like to do")
    print("=================================")
    print("(A)nalyze a password")
    print("(G)enerate a strong password")
    print("(S)tore a password")
    print("(R)etrieve stored passwords")
    print("(Q)uit")
    print("=================================")

def main():
    # Check if the master password is already set
    if not os.path.exists("master_password.hash"):
        setup_master_password()
    while True:
        display_menu()
        choice = input("Select an option: ").strip().lower()

        if choice == "a":
            # Analyze a password
            password = input("Enter the password to analyze: ").strip()
            result = analyze_password(password)
            print("\nStrength Score:", result['score'])
            print("Recommendations:")
            for rec in result['recommendations']:
                print("- " + rec)

        elif choice == "g":
            # Generate a strong password
            password = generate_strong_password()
            print("Generated password:", password)

        elif choice == "s":
            # Store a password
            password = input("Enter the password to store: ").strip()
            master_password = getpass("Enter your master password: ").strip()

            if not verify_master_password(master_password):
                print("Incorrect master password.")
                continue

            try:
                store_password(password, master_password)
                print("Password stored successfully.")
            except Exception as e:
                print("Error storing password:", e)

        elif choice == "r":
            # Retrieve stored passwords

            master_password = getpass("Enter your master password: ").strip()
            attempts = 3
            while attempts > 0:
                try:
                    passwords = retrieve_passwords(master_password)
                    if not passwords:
                        print("No passwords stored.")
                        break

                    print("\nStored Passwords:")
                    now = datetime.now(timezone.utc)  # Use timezone-aware UTC time
                    for idx, record in enumerate(passwords, 1):
                        stored_time = datetime.fromisoformat(record["stored_at"])
                        age_days = (now - stored_time).days
                        print(f"{idx}: {record['password']} (Stored {age_days} days ago)")
                        if age_days > 1:
                            print(f"   -> Consider changing this password; it's over 1 days old.")
                    break
                except Exception as e:
                    attempts -= 1
                    if attempts > 0:
                        print(f"Incorrect master password, try again. Attempts left: {attempts}")
                        master_password = getpass("Re-enter your master password: ").strip()
                    else:
                        print("Too many failed attempts. Access denied.")
                        break

        elif choice == "q":
            # Quit the program
            print("Exiting the tool. Goodbye!")
            sys.exit(0)

        else:
            print("Invalid option. Please select a valid option (a/g/s/r/q).")

if __name__ == "__main__":
    main()
