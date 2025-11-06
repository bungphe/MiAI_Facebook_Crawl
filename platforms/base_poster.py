"""
Base class for all platform posters
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class BasePoster(ABC):
    """Base class for platform-specific posters"""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.access_token = None
        self.api_key = None
        self.api_secret = None
        self.authenticated = False
    
    @abstractmethod
    async def authenticate(
        self,
        access_token: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        additional_params: Optional[Dict] = None
    ) -> Dict:
        """
        Authenticate with the platform
        Returns: Dict with authentication status and details
        """
        pass
    
    @abstractmethod
    async def create_post(
        self,
        text: str,
        media_urls: Optional[List[str]] = None,
        schedule_time: Optional[str] = None
    ) -> Dict:
        """
        Create a post on the platform
        Returns: Dict with post_id and status
        """
        pass
    
    def get_credentials_from_env(self) -> Dict:
        """Get credentials from environment variables"""
        return {
            'access_token': os.getenv(f'{self.platform_name.upper()}_ACCESS_TOKEN'),
            'api_key': os.getenv(f'{self.platform_name.upper()}_API_KEY'),
            'api_secret': os.getenv(f'{self.platform_name.upper()}_API_SECRET'),
            'client_id': os.getenv(f'{self.platform_name.upper()}_CLIENT_ID'),
            'client_secret': os.getenv(f'{self.platform_name.upper()}_CLIENT_SECRET'),
        }
    
    def validate_media_url(self, url: str) -> bool:
        """Validate media URL"""
        if not url:
            return False
        return url.startswith(('http://', 'https://'))
    
    def format_response(self, success: bool, post_id: Optional[str] = None, message: str = "", error: Optional[str] = None) -> Dict:
        """Format response dictionary"""
        return {
            'success': success,
            'platform': self.platform_name,
            'post_id': post_id,
            'message': message,
            'error': error
        }
