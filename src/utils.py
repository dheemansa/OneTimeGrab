import os
import time
from datetime import datetime as dt

def ensure_download_directory(path):
    """Create downloads directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"📁 Created downloads directory: {path}")

def generate_filename(media_message, media_type, download_path):
    """Generate unique filename based on media type and sender"""
    timestamp = int(time.time() * 1000)
    sender_id = getattr(media_message, 'sender_id', 'unknown')
    
    if media_type == 'photo':
        return f"{download_path}photo_{sender_id}_{timestamp}.jpg"
    elif media_type == 'document':
        ext = _get_document_extension(media_message.media.document)
        return f"{download_path}doc_{sender_id}_{timestamp}{ext}"
    else:
        return f"{download_path}media_{sender_id}_{timestamp}"

def _get_document_extension(document):
    """Extract file extension from document"""
    if not document:
        return ""
    
    if hasattr(document, 'mime_type') and document.mime_type:
        mime_extensions = {
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'video/mp4': '.mp4',
            'video/avi': '.avi',
            'audio/mpeg': '.mp3',
            'audio/mp4': '.m4a',
            'application/pdf': '.pdf',
            'application/zip': '.zip'
        }
        if document.mime_type in mime_extensions:
            return mime_extensions[document.mime_type]
    
    if hasattr(document, 'attributes'):
        for attr in document.attributes:
            if hasattr(attr, 'file_name') and attr.file_name and '.' in attr.file_name:
                return '.' + attr.file_name.split('.')[-1]
    
    return ""

def get_media_type(media):
    """Determine media type from message"""
    if hasattr(media, 'photo'):
        return 'photo'
    elif hasattr(media, 'document'):
        return 'document'
    else:
        return 'unknown'

def is_supported_media(media):
    """Check if media type is supported for download"""
    if not media:
        return False
    
    unsupported_types = ['webpage', 'geo', 'contact', 'poll', 'dice']
    for unsupported in unsupported_types:
        if hasattr(media, unsupported):
            return False
    
    return hasattr(media, 'photo') or hasattr(media, 'document')

def create_caption(message):
    """Create caption for saved media"""
    try:
        chat_name = "Unknown"
        if message.chat:
            chat_name = (
                       getattr(message.chat, 'title', None) or 
                       getattr(message.chat, 'username', None) or 
                       "Private Chat")
        
        sender_info = f"Sender ID: {message.sender_id}"
        if hasattr(message, 'sender') and message.sender:
            sender_name = (
                           getattr(message.sender, 'username', None) or 
                           getattr(message.sender, 'first_name', 'Unknown'))
            sender_info = f"Sender: {sender_name} ({message.sender_id})"
        
        timestamp = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"📁 Auto-saved from: {chat_name}\n{sender_info}\n📅 {timestamp}"
    
    except Exception:
        return f"📁 Saved media - {dt.now().strftime('%Y-%m-%d %H:%M:%S')}"
