"""
Configuration file for Multi-Platform Social Media Posting API
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    
    # API Settings
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 8000))
    API_DEBUG = os.getenv('API_DEBUG', 'True').lower() == 'true'
    
    # Facebook
    FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
    FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')
    FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
    FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')
    
    # Instagram
    INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    INSTAGRAM_ACCOUNT_ID = os.getenv('INSTAGRAM_ACCOUNT_ID')
    
    # TikTok
    TIKTOK_ACCESS_TOKEN = os.getenv('TIKTOK_ACCESS_TOKEN')
    TIKTOK_CLIENT_KEY = os.getenv('TIKTOK_CLIENT_KEY')
    TIKTOK_CLIENT_SECRET = os.getenv('TIKTOK_CLIENT_SECRET')
    
    # X (Twitter)
    X_API_KEY = os.getenv('X_API_KEY')
    X_API_SECRET = os.getenv('X_API_SECRET')
    X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
    X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')
    X_BEARER_TOKEN = os.getenv('X_BEARER_TOKEN')
    
    # Threads
    THREADS_ACCESS_TOKEN = os.getenv('THREADS_ACCESS_TOKEN')
    THREADS_USER_ID = os.getenv('THREADS_USER_ID')
    
    # YouTube
    YOUTUBE_ACCESS_TOKEN = os.getenv('YOUTUBE_ACCESS_TOKEN')
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
    YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')
    
    @classmethod
    def validate_credentials(cls, platform: str) -> bool:
        """Validate if credentials are available for a platform"""
        validation_map = {
            'facebook': cls.FACEBOOK_ACCESS_TOKEN is not None,
            'instagram': cls.INSTAGRAM_ACCESS_TOKEN is not None and cls.INSTAGRAM_ACCOUNT_ID is not None,
            'tiktok': cls.TIKTOK_ACCESS_TOKEN is not None,
            'x': cls.X_BEARER_TOKEN is not None or (cls.X_ACCESS_TOKEN is not None and cls.X_ACCESS_TOKEN_SECRET is not None),
            'threads': cls.THREADS_ACCESS_TOKEN is not None and cls.THREADS_USER_ID is not None,
            'youtube': cls.YOUTUBE_ACCESS_TOKEN is not None
        }
        return validation_map.get(platform, False)
    
    @classmethod
    def get_available_platforms(cls) -> list:
        """Get list of platforms with valid credentials"""
        platforms = ['facebook', 'instagram', 'tiktok', 'x', 'threads', 'youtube']
        return [p for p in platforms if cls.validate_credentials(p)]

# Create config instance
config = Config()
