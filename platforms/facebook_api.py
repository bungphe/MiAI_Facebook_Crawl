"""
Facebook API Poster
Uses Facebook Graph API to post to Facebook Pages and Profiles
"""

import aiohttp
import os
from typing import Optional, List, Dict
from .base_poster import BasePoster

class FacebookPoster(BasePoster):
    """Facebook posting functionality"""
    
    def __init__(self):
        super().__init__('facebook')
        self.graph_api_url = "https://graph.facebook.com/v18.0"
        self.page_id = os.getenv('FACEBOOK_PAGE_ID')
    
    async def authenticate(
        self,
        access_token: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        additional_params: Optional[Dict] = None
    ) -> Dict:
        """
        Authenticate with Facebook API
        Requires: access_token and page_id
        """
        try:
            # Use provided token or get from environment
            self.access_token = access_token or os.getenv('FACEBOOK_ACCESS_TOKEN')
            
            if additional_params and 'page_id' in additional_params:
                self.page_id = additional_params['page_id']
            else:
                self.page_id = self.page_id or os.getenv('FACEBOOK_PAGE_ID')
            
            if not self.access_token:
                raise Exception("Facebook access token is required")
            
            # Verify token by making a test API call
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.graph_api_url}/me",
                    params={'access_token': self.access_token}
                ) as response:
                    if response.status == 200:
                        user_data = await response.json()
                        self.authenticated = True
                        return {
                            'authenticated': True,
                            'user_id': user_data.get('id'),
                            'user_name': user_data.get('name')
                        }
                    else:
                        error_data = await response.json()
                        raise Exception(f"Authentication failed: {error_data}")
        
        except Exception as e:
            self.authenticated = False
            raise Exception(f"Facebook authentication error: {str(e)}")
    
    async def create_post(
        self,
        text: str,
        media_urls: Optional[List[str]] = None,
        schedule_time: Optional[str] = None
    ) -> Dict:
        """
        Create a post on Facebook
        
        Parameters:
        - text: Post content
        - media_urls: List of image/video URLs
        - schedule_time: Scheduled publish time (Unix timestamp)
        """
        try:
            # Auto-authenticate if not already authenticated
            if not self.authenticated:
                await self.authenticate()
            
            # Determine endpoint (page or user feed)
            endpoint = f"{self.page_id}/feed" if self.page_id else "me/feed"
            
            # Prepare post data
            post_data = {
                'message': text,
                'access_token': self.access_token
            }
            
            # Add media if provided
            if media_urls and len(media_urls) > 0:
                if len(media_urls) == 1:
                    # Single image/video
                    post_data['link'] = media_urls[0]
                else:
                    # Multiple images - use photos endpoint
                    # Note: For multiple images, need to use batch upload
                    post_data['attached_media'] = media_urls
            
            # Add scheduling if provided
            if schedule_time:
                post_data['published'] = False
                post_data['scheduled_publish_time'] = schedule_time
            
            # Make API request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.graph_api_url}/{endpoint}",
                    data=post_data
                ) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        return {
                            'post_id': result.get('id'),
                            'success': True,
                            'platform': 'facebook'
                        }
                    else:
                        error_data = await response.json()
                        raise Exception(f"Post failed: {error_data}")
        
        except Exception as e:
            raise Exception(f"Facebook post error: {str(e)}")
    
    async def upload_photo(self, photo_url: str) -> str:
        """Upload a photo and return photo ID"""
        try:
            endpoint = f"{self.page_id}/photos" if self.page_id else "me/photos"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.graph_api_url}/{endpoint}",
                    data={
                        'url': photo_url,
                        'published': False,
                        'access_token': self.access_token
                    }
                ) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        return result.get('id')
                    else:
                        raise Exception(f"Photo upload failed: {await response.text()}")
        except Exception as e:
            raise Exception(f"Photo upload error: {str(e)}")
