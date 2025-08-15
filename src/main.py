import sys

def check_dependencies():
    """Checks if the required dependencies are installed."""
    try:
        import telethon
        import dotenv
    except ImportError:
        print("Error: Required dependencies are not installed.", file=sys.stderr)
        print("Please install them by running: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

check_dependencies()

import asyncio
import os
from telethon import events
from .telegram_client import client
from .config import MODE, HANDLER, DOWNLOAD_PATH
from .media_handler import process_media_message
from . import utils

user_id = None

@client.on(events.NewMessage())
async def handle_automatic_mode(event):
    """Handle automatic mode - save all incoming media"""
    global user_id

    if MODE != 'automatic':
        return

    if event.sender_id == user_id:
        return

    if not utils.is_supported_media(event.media):
        return

    media_type = utils.get_media_type(event.media)
    print(f"🔄 Auto-processing {media_type} from {event.sender_id}")

    await asyncio.sleep(0.1)

    success, message = await process_media_message(event)
    if not success:
        print(f"❌ Auto-save failed: {message}")

@client.on(events.NewMessage(pattern=rf'^{HANDLER}$'))
async def handle_manual_mode(event):
    """Handle manual mode - save media when handler is used"""
    global user_id

    if event.sender_id != user_id:
        return

    await event.delete()

    if not event.reply_to_msg_id:
        print("❌ Manual save: No message to reply to")
        return

    try:
        replied_message = await event.get_reply_message()
        if not utils.is_supported_media(replied_message.media):
            print("❌ Manual save: No supported media in replied message")
            return

        media_type = utils.get_media_type(replied_message.media)
        print(f"🔄 Manual save: Processing {media_type}")

        success, message = await process_media_message(replied_message)
        if not success:
            print(f"❌ Manual save failed: {message}")

    except Exception as e:
        print(f"❌ Manual save error: {e}")

@client.on(events.NewMessage(pattern=r'^status$'))
async def handle_status_command(event):
    """Handle status command"""
    global user_id

    if event.sender_id != user_id:
        return

    await event.delete()

    print("📊 Bot Status:")
    print(f"   Mode: {MODE.title()}")
    print(f"   Handler: '{HANDLER}'")
    print(f"   User ID: {user_id}")
    print(f"   Download Path: {os.path.abspath(DOWNLOAD_PATH)}")

    if MODE == 'automatic':
        print(f"   🟢 Automatic mode: All incoming media saved automatically")
    else:
        print(f"   🟡 Manual mode: Reply to media with '{HANDLER}' to save")

async def main():
    """Main function to start the bot"""
    async with client:
        global user_id
        me = await client.get_me()
        user_id = me.id

        print("🚀 Telegram Media Saver Bot Started")
        print("=" * 50)
        print(f"👤 User: {me.username or 'Unknown'} (ID: {user_id})")
        print(f"📊 Mode: {MODE.title()}")
        print(f"🔧 Handler: '{HANDLER}'")
        print(f"📁 Download Path: {os.path.abspath(DOWNLOAD_PATH)}")

        if MODE == 'automatic':
            print("🟢 Automatic mode active - All incoming media will be saved")
            print(f"💡 Manual saves still available with '{HANDLER}' command")
        else:
            print(f"🟡 Manual mode active - Reply to media with '{HANDLER}' to save")

        print("✨ Send 'status' to check bot status anytime")
        print("=" * 50)

        utils.ensure_download_directory(DOWNLOAD_PATH)
        await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
