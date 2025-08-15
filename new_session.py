import os
import sys
import subprocess

def main():
    """Asks for confirmation, deletes old config, and runs setup.py."""
    print("🚀 This script will reset your configuration and start a new session.")
    
    if not os.path.exists(".env") and not os.path.exists("save.session"):
        print("No existing setup found. Running the first-time setup...")
        subprocess.run([sys.executable, "setup.py"])
        return

    confirm = input("This will delete your existing .env and save.session files. Are you sure you want to continue? (y/n): ").lower()
    if confirm != 'y':
        print("Aborting. Your existing configuration has not been changed.")
        return
    
    if os.path.exists(".env"):
        os.remove(".env")
        print("🗑️  Deleted .env file.")
    
    if os.path.exists("save.session"):
        os.remove("save.session")
        print("🗑️  Deleted save.session file.")
    
    print("🔄 Starting the setup process...")
    subprocess.run([sys.executable, "setup.py"])

if __name__ == "__main__":
    main()
