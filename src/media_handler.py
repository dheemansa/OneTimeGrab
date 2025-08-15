from .telegram_client import client
from . import utils
from .config import DOWNLOAD_PATH

async def download_media(message):
    """Download media from message and return file path"""
    if not utils.is_supported_media(message.media):
        return None, "Unsupported or missing media type"
    
    utils.ensure_download_directory(DOWNLOAD_PATH)
    
    media_type = utils.get_media_type(message.media)
    file_path = utils.generate_filename(message, media_type, DOWNLOAD_PATH)
    
    try:
        downloaded_path = await client.download_media(message.media, file=file_path)
        if downloaded_path:
            print(f"📥 Downloaded {media_type}: {downloaded_path}")
            return downloaded_path, "Success"
        
        downloaded_path = await client.download_media(message, file=file_path)
        if downloaded_path:
            print(f"📥 Downloaded {media_type} (fallback): {downloaded_path}")
            return downloaded_path, "Success"
        
        return None, "Download failed - media might be expired or protected"
    
    except Exception as e:
        print(f"❌ Download error: {e}")
        return None, f"Download exception: {str(e)}"

async def process_media_message(message):
    """Process a message with media"""
    file_path, download_status = await download_media(message)
    
    if not file_path:
        print(f"❌ Failed to download: {download_status}")
        return False, download_status
    
    try:
        caption = utils.create_caption(message)
        await client.send_file("me", file_path, caption=caption, force_document=True)
        print(f"💾 Saved to Telegram and kept locally: {file_path}")
        return True, "Media saved successfully"
    
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        print(f"💾 File kept locally: {file_path}")
        return False, f"Upload failed: {str(e)}"
