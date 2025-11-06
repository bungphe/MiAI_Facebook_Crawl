"""
Instagram API Poster
Uses Instagram Graph API to post to Instagram Business/Creator accounts
"""

import aiohttp
import os
from typing import Optional, List, Dict
from .base_poster import BasePoster

class InstagramPoster(BasePoster):
    """Instagram posting functionality"""
    
    def __init__(self):
        super().__init__('instagram')
        self.graph_api_url = "https://graph.facebook.com/v18.0"
        self.instagram_account_id = os.getenv('INSTAGRAM_ACCOUNT_ID')
    
    async def authenticate(
        self,
        access_token: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        additional_params: Optional[Dict] = None
    ) -> Dict:
        """
        Authenticate with Instagram API
        Requires: access_token and instagram_account_id
        """
        try:
            self.access_token = access_token or os.getenv('INSTAGRAM_ACCESS_TOKEN')
            
            if additional_params and 'instagram_account_id' in additional_params:
                self.instagram_account_id = additional_params['instagram_account_id']
            else:
                self.instagram_account_id = self.instagram_account_id or os.getenv('INSTAGRAM_ACCOUNT_ID')
            
            if not self.access_token or not self.instagram_account_id:
                raise Exception("Instagram access token and account ID are required")
            
            # Verify credentials
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.graph_api_url}/{self.instagram_account_id}",
                    params={
                        'fields': 'id,username,account_type',
                        'access_token': self.access_token
                    }
                ) as response:
                    if response.status == 200:
                        account_data = await response.json()
                        self.authenticated = True
                        return {
                            'authenticated': True,
                            'account_id': account_data.get('id'),
                            'username': account_data.get('username'),
                            'account_type': account_data.get('account_type')
                        }
                    else:
                        error_data = await response.json()
                        raise Exception(f"Authentication failed: {error_data}")
        
        except Exception as e:
            self.authenticated = False
            raise Exception(f"Instagram authentication error: {str(e)}")
    
    async def create_post(
        self,
        text: str,
        media_urls: Optional[List[str]] = None,
        schedule_time: Optional[str] = None
    ) -> Dict:
        """
        Create a post on Instagram
        
        Instagram requires a 2-step process:
        1. Create media container
        2. Publish the container
        
        Parameters:
        - text: Post caption
        - media_urls: List of image/video URLs (must be publicly accessible)
        - schedule_time: Not directly supported, but can be implemented with containers
        """
        try:
            if not self.authenticated:
                await self.authenticate()
            
            if not media_urls or len(media_urls) == 0:
                raise Exception("Instagram requires at least one media URL")
            
            # Step 1: Create media container
            container_id = await self._create_media_container(text, media_urls[0])
            
            # Step 2: Publish the container
            post_id = await self._publish_media_container(container_id)
            
            return {
                'post_id': post_id,
                'success': True,
                'platform': 'instagram'
            }
        
        except Exception as e:
            raise Exception(f"Instagram post error: {str(e)}")
    
    async def _create_media_container(self, caption: str, media_url: str) -> str:
        """Create Instagram media container"""
        try:
            # Determine if it's a video or image
            is_video = media_url.lower().endswith(('.mp4', '.mov', '.avi'))
            
            data = {
                'caption': caption,
                'access_token': self.access_token
            }
            
            if is_video:
                data['media_type'] = 'VIDEO'
                data['video_url'] = media_url
            else:
                data['image_url'] = media_url
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.graph_api_url}/{self.instagram_account_id}/media",
                    data=data
                ) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        return result.get('id')
                    else:
                        error_data = await response.json()
                        raise Exception(f"Container creation failed: {error_data}")
        
        except Exception as e:
            raise Exception(f"Container creation error: {str(e)}")
    
    async def _publish_media_container(self, container_id: str) -> str:
        """Publish Instagram media container"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.graph_api_url}/{self.instagram_account_id}/media_publish",
                    data={
                        'creation_id': container_id,
                        'access_token': self.access_token
                    }
                ) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        return result.get('id')
                    else:
                        error_data = await response.json()
                        raise Exception(f"Publishing failed: {error_data}")
        
        except Exception as e:
            raise Exception(f"Publishing error: {str(e)}")
    
    async def create_story(self, media_url: str) -> Dict:
        """Create an Instagram Story"""
        try:
            if not self.authenticated:
                await self.authenticate()
            
            # Create story container
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.graph_api_url}/{self.instagram_account_id}/media",
                    data={
                        'image_url': media_url,
                        'media_type': 'STORIES',
                        'access_token': self.access_token
                    }
                ) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        container_id = result.get('id')
                        
                        # Publish story
                        story_id = await self._publish_media_container(container_id)
                        return {
                            'story_id': story_id,
                            'success': True,
                            'platform': 'instagram'
                        }
                    else:
                        error_data = await response.json()
                        raise Exception(f"Story creation failed: {error_data}")
        
        except Exception as e:
            raise Exception(f"Instagram story error: {str(e)}")
