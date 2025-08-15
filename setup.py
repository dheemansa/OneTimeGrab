import os
import asyncio
import sys

try:
    from telethon import TelegramClient
    from telethon.errors import ApiIdInvalidError
except ImportError:
    print("Error: telethon is not installed.", file=sys.stderr)
    print("Please install it by running: pip install telethon", file=sys.stderr)
    sys.exit(1)


async def login_and_create_session(api_id, api_hash):
    """Logs in with the provided credentials and creates a session file."""
    client = TelegramClient('save', int(api_id), api_hash)
    try:
        async with client:
            print("✅ Login successful. Session file created.")
        return True
    except ApiIdInvalidError:
        print("❌ Invalid API_ID or API_HASH. Please double-check them.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ An error occurred during login: {e}", file=sys.stderr)
        return False

async def main():
    """Interactively creates the .env and session files for the first time."""
    print("🚀 Welcome to the OneTimeGrab setup utility!")
    print("This script should only be run for the initial setup.")

    if os.path.exists(".env") or os.path.exists("save.session"):
        print("✅ It looks like you have already completed the setup.")
        print("If you want to start a new session or change the mode, please run 'python3 new_session.py' or use the './run.sh --new' shortcut.")
        return

    while True:
        api_id = input("Enter your Telegram API_ID: ")
        if not api_id.isdigit():
            print("❌ Invalid API_ID. It should only contain numbers.")
            continue

        api_hash = input("Enter your Telegram API_HASH: ")
        if not api_hash.isalnum():
            print("❌ Invalid API_HASH. It should only contain letters and numbers.")
            continue

        print("🔄 Attempting to log in to Telegram to create a session file...")
        print("You will be prompted for your phone number, login code, and 2FA password (if enabled).")
        if await login_and_create_session(api_id, api_hash):
            break
        else:
            print("Please try entering your credentials again.")

    mode = ""
    while True:
        print("Select the mode:")
        print("1. Automatic (saves all incoming media)")
        print("2. Manual (saves media only when you use a handler)")
        choice = input("Enter your choice (1 or 2): ")
        if choice == '1':
            mode = 'automatic'
            break
        elif choice == '2':
            mode = 'manual'
            break
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")

    handler = ""
    if mode == 'manual':
        handler = input("Enter the handler for manual mode (e.g., .saveit): ")

    with open(".env", "w") as f:
        f.write(f"API_ID={api_id}\n")
        f.write(f"API_HASH={api_hash}\n")
        f.write(f"MODE={mode}\n")
        f.write(f"HANDLER={handler}\n")

    print("✅ Your .env file has been created successfully!")
    print("You can now run the application using run.sh or run.bat.")


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
