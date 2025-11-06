"""
X (Twitter) API Poster
Uses X API v2 for posting tweets
"""

import aiohttp
import os
from typing import Optional, List, Dict
from .base_poster import BasePoster
import base64
import hmac
import hashlib
import time
import secrets

class XPoster(BasePoster):
    """X (Twitter) posting functionality"""
    
    def __init__(self):
        super().__init__('x')
        self.api_url = "https://api.twitter.com/2"
        self.api_key = os.getenv('X_API_KEY')
        self.api_secret = os.getenv('X_API_SECRET')
        self.bearer_token = os.getenv('X_BEARER_TOKEN')
    
    async def authenticate(
        self,
        access_token: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        additional_params: Optional[Dict] = None
    ) -> Dict:
        """
        Authenticate with X API
        Uses OAuth 2.0 Bearer Token or OAuth 1.0a
        """
        try:
            self.access_token = access_token or os.getenv('X_ACCESS_TOKEN')
            self.access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')
            self.api_key = api_key or self.api_key
            self.api_secret = api_secret or self.api_secret
            self.bearer_token = self.bearer_token or os.getenv('X_BEARER_TOKEN')
            
            if not self.bearer_token and not (self.access_token and self.access_token_secret):
                raise Exception("X API requires bearer token or access tokens")
            
            # Verify credentials by getting user info
            async with aiohttp.ClientSession() as session:
                headers = {}
                if self.bearer_token:
                    headers['Authorization'] = f'Bearer {self.bearer_token}'
                
                async with session.get(
                    f"{self.api_url}/users/me",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        user_data = result.get('data', {})
                        self.authenticated = True
                        return {
                            'authenticated': True,
                            'user_id': user_data.get('id'),
                            'username': user_data.get('username'),
                            'name': user_data.get('name')
                        }
                    else:
                        error_data = await response.json()
                        raise Exception(f"Authentication failed: {error_data}")
        
        except Exception as e:
            self.authenticated = False
            raise Exception(f"X authentication error: {str(e)}")
    
    async def create_post(
        self,
        text: str,
        media_urls: Optional[List[str]] = None,
        schedule_time: Optional[str] = None
    ) -> Dict:
        """
        Create a tweet on X (Twitter)
        
        Parameters:
        - text: Tweet text (max 280 characters for standard, 4000 for X Premium)
        - media_urls: List of media URLs (up to 4 images or 1 video)
        - schedule_time: Not directly supported in API v2
        """
        try:
            if not self.authenticated:
                await self.authenticate()
            
            # Prepare tweet data
            tweet_data = {
                'text': text
            }
            
            # Upload media if provided
            if media_urls and len(media_urls) > 0:
                media_ids = []
                for media_url in media_urls[:4]:  # Max 4 media items
                    media_id = await self._upload_media(media_url)
                    media_ids.append(media_id)
                
                if media_ids:
                    tweet_data['media'] = {'media_ids': media_ids}
            
            # Post tweet
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Content-Type': 'application/json'
                }
                
                if self.bearer_token:
                    headers['Authorization'] = f'Bearer {self.bearer_token}'
                elif self.access_token:
                    # Use OAuth 1.0a
                    headers['Authorization'] = self._get_oauth_header('POST', f"{self.api_url}/tweets")
                
                async with session.post(
                    f"{self.api_url}/tweets",
                    headers=headers,
                    json=tweet_data
                ) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        return {
                            'post_id': result.get('data', {}).get('id'),
                            'success': True,
                            'platform': 'x'
                        }
                    else:
                        error_data = await response.json()
                        raise Exception(f"Tweet posting failed: {error_data}")
        
        except Exception as e:
            raise Exception(f"X post error: {str(e)}")
    
    async def _upload_media(self, media_url: str) -> str:
        """Upload media to X and return media_id"""
        try:
            # Download media
            async with aiohttp.ClientSession() as session:
                async with session.get(media_url) as media_response:
                    if media_response.status != 200:
                        raise Exception("Failed to download media")
                    
                    media_data = await media_response.read()
                    
                    # Determine media type
                    content_type = media_response.headers.get('Content-Type', 'image/jpeg')
                    
                    # Upload to X (using v1.1 media upload endpoint)
                    upload_url = "https://upload.twitter.com/1.1/media/upload.json"
                    
                    # INIT
                    init_data = {
                        'command': 'INIT',
                        'total_bytes': len(media_data),
                        'media_type': content_type
                    }
                    
                    headers = {}
                    if self.bearer_token:
                        headers['Authorization'] = f'Bearer {self.bearer_token}'
                    
                    async with session.post(
                        upload_url,
                        headers=headers,
                        data=init_data
                    ) as init_response:
                        if init_response.status in [200, 201, 202]:
                            init_result = await init_response.json()
                            media_id = init_result.get('media_id_string')
                            
                            # APPEND
                            append_data = {
                                'command': 'APPEND',
                                'media_id': media_id,
                                'segment_index': 0,
                                'media': media_data
                            }
                            
                            async with session.post(
                                upload_url,
                                headers=headers,
                                data=append_data
                            ) as append_response:
                                if append_response.status in [200, 201, 204]:
                                    # FINALIZE
                                    finalize_data = {
                                        'command': 'FINALIZE',
                                        'media_id': media_id
                                    }
                                    
                                    async with session.post(
                                        upload_url,
                                        headers=headers,
                                        data=finalize_data
                                    ) as finalize_response:
                                        if finalize_response.status in [200, 201]:
                                            return media_id
                                        else:
                                            raise Exception("Media finalization failed")
                                else:
                                    raise Exception("Media append failed")
                        else:
                            error_data = await init_response.json()
                            raise Exception(f"Media init failed: {error_data}")
        
        except Exception as e:
            raise Exception(f"Media upload error: {str(e)}")
    
    def _get_oauth_header(self, method: str, url: str) -> str:
        """Generate OAuth 1.0a authorization header"""
        # This is a simplified version. For production, use a proper OAuth library
        oauth_params = {
            'oauth_consumer_key': self.api_key,
            'oauth_token': self.access_token,
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': str(int(time.time())),
            'oauth_nonce': secrets.token_hex(16),
            'oauth_version': '1.0'
        }
        
        # Generate signature (simplified)
        # In production, use tweepy or python-twitter library
        
        return f'OAuth {", ".join([f"{k}="{v}"" for k, v in oauth_params.items()])}'
