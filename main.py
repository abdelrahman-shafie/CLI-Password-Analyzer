import sys
import os
import keyboard
from colorama import init, Fore, Style
from getpass import getpass
from utils.analyzer import analyze_password
from utils.generator import generate_strong_password
from utils.storage import store_password, retrieve_passwords
from utils.master_password import setup_master_password, verify_master_password
from datetime import datetime, timezone, timedelta

# Initialize colorama for cross-platform support
init(autoreset=True)

# Function to display the menu
def display_menu():
    print("\nWelcome! What would you like to do")
    print("--------------------------------")
    print(f"({Fore.YELLOW}A{Style.RESET_ALL})nalyze a password")
    print(f"({Fore.YELLOW}G{Style.RESET_ALL})enerate a strong password")
    print(f"({Fore.YELLOW}S{Style.RESET_ALL})tore a password")
    print(f"({Fore.YELLOW}R{Style.RESET_ALL})etrieve stored passwords")
    print(f"({Fore.YELLOW}H{Style.RESET_ALL})elp - Learn how to use the tool")
    print(f"({Fore.YELLOW}Q{Style.RESET_ALL})uit")
    print("--------------------------------")

# Help guide
def display_help():
    print(f"\n{Fore.BLUE}Tool Help Guide{Style.RESET_ALL}")
    print("-------------------------------")
    print(f"{Fore.YELLOW}(A){Style.RESET_ALL} Analyze a password:")
    print("   - Provides a strength score for your password.")
    print("   - Suggests improvements to make your password stronger.")
    print()
    print(f"{Fore.YELLOW}(G){Style.RESET_ALL} Generate a strong password:")
    print("   - Generates a secure and strong password for you.")
    print("   - Automatically copies generated password into your clipboard and deletes it after 30 seconds.")
    print()
    print(f"{Fore.YELLOW}(S){Style.RESET_ALL} Store a password:")
    print("   - Securely stores your desired password after verifying your master password.")
    print()
    print(f"{Fore.YELLOW}(R){Style.RESET_ALL} Retrieve stored passwords:")
    print("   - Lists stored passwords along with their age in days.")
    print("   - Warns you if any password is older than 183 days.")
    print()
    print(f"{Fore.YELLOW}(H){Style.RESET_ALL} Help:")
    print("   - Displays this help guide to explain each option.")
    print()
    print(f"{Fore.YELLOW}(Q){Style.RESET_ALL} Quit:")
    print("   - Exits the program.")
    print("-------------------------------")

# Ctrl+H handler function
def ctrl_h_handler():
    print(f"\n{Fore.YELLOW}You triggered help with Ctrl+H!{Style.RESET_ALL}")
    display_help()

# Start listening for Ctrl+H using keyboard
keyboard.add_hotkey("ctrl+h", ctrl_h_handler)

lockout_until = None  # Tracks the lockout time

def main():
    # Check if the master password is already set
    if not os.path.exists("master_password.hash"):
        setup_master_password()
    while True:
        display_menu()
        choice = input("Select an option: ").strip().lower()

        if choice == "a":
            # Analyze a password
            password = input(Fore.CYAN + "Enter the password to analyze: " + Style.RESET_ALL).strip()
            result = analyze_password(password)
            print(Fore.GREEN + "\nStrength Score:", result['score'])
            print(Fore.YELLOW + "Recommendations:")
            for rec in result['recommendations']:
                print(f"- {rec}")

        elif choice == "g":
            # Generate a strong password
            print(Fore.CYAN + "Generating a strong password..." + Style.RESET_ALL)
            password = generate_strong_password()

        elif choice == "s":
            # Store a password
            password = input(Fore.CYAN + "Enter the password to store: " + Style.RESET_ALL).strip()
            
            # Allow 3 attempts to enter the correct master password
            attempts = 3
            while attempts > 0:
                master_password = getpass(Fore.CYAN + "Enter your master password: " + Style.RESET_ALL).strip()
                
                if not verify_master_password(master_password):
                    attempts -= 1
                    print(Fore.RED + f"Incorrect master password. Attempts left: {attempts}")
                else:
                    # Correct master password
                    try:
                        store_password(password, master_password)
                        print(Fore.GREEN + "Password stored successfully.")
                    except Exception as e:
                        print(Fore.RED + f"Error storing password: {e}")
                    break  # Exit the loop after successful storage
            else:
                # If all attempts are exhausted
                print(Fore.YELLOW + "Too many incorrect attempts. Returning to the main menu.")

        elif choice == "r":
            global lockout_until  # To track the lockout across iterations

            # Check if user is locked out
            if lockout_until and datetime.now(timezone.utc) < lockout_until:
                remaining = (lockout_until - datetime.now(timezone.utc)).seconds
                print(Fore.RED + f"Too many failed attempts. Please wait {remaining} seconds before trying again.")
                continue  # Go back to the main menu

            # Initialize password attempts
            master_password = getpass(Fore.CYAN + "Enter your master password: " + Style.RESET_ALL).strip()
            attempts = 3

            while attempts > 0:
                try:
                    # Attempt to retrieve passwords
                    passwords = retrieve_passwords(master_password)
                    if not passwords:
                        print(Fore.YELLOW + "No passwords stored.")
                        break

                    # Display stored passwords
                    print(Fore.BLUE + "\nStored Passwords:")
                    now = datetime.now(timezone.utc)
                    for idx, record in enumerate(passwords, 1):
                        stored_time = datetime.fromisoformat(record["stored_at"])
                        age_days = (now - stored_time).days
                        print(f"{idx}: {record['password']} (Stored {age_days} days ago)")
                        if age_days > 183:
                            print(Fore.YELLOW + f"   -> Consider changing this password; it's over 183 days old.")
                    break  # Exit loop if successful retrieval

                except Exception as e:
                    # Handle incorrect master password
                    attempts -= 1
                    if attempts > 0:
                        print(Fore.RED + f"Incorrect master password, try again. Attempts left: {attempts}")
                        master_password = getpass(Fore.CYAN + "Re-enter your master password: ").strip()
                    else:
                        print(Fore.RED + "Too many failed attempts. You must wait 1 minute before retrying.")
                        lockout_until = datetime.now(timezone.utc) + timedelta(minutes=1)
                        break

        elif choice == "h":
            display_help()

        elif choice == "q":
            # Quit the program
            print(Fore.GREEN + "Exiting the tool. Goodbye!")
            sys.exit(0)

        else:
            print(f"{Fore.RED}Invalid option{Style.RESET_ALL}. Please select a valid option (a/g/s/r/h/q).")

if __name__ == "__main__":
    main()
