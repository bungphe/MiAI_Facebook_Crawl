"""
Threads API Poster
Uses Threads API (built on Instagram infrastructure) for posting
"""

import aiohttp
import os
from typing import Optional, List, Dict
from .base_poster import BasePoster

class ThreadsPoster(BasePoster):
    """Threads posting functionality"""
    
    def __init__(self):
        super().__init__('threads')
        self.graph_api_url = "https://graph.threads.net/v1.0"
        self.threads_user_id = os.getenv('THREADS_USER_ID')
    
    async def authenticate(
        self,
        access_token: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        additional_params: Optional[Dict] = None
    ) -> Dict:
        """
        Authenticate with Threads API
        Requires: access_token and threads_user_id
        """
        try:
            self.access_token = access_token or os.getenv('THREADS_ACCESS_TOKEN')
            
            if additional_params and 'threads_user_id' in additional_params:
                self.threads_user_id = additional_params['threads_user_id']
            else:
                self.threads_user_id = self.threads_user_id or os.getenv('THREADS_USER_ID')
            
            if not self.access_token or not self.threads_user_id:
                raise Exception("Threads access token and user ID are required")
            
            # Verify credentials
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.graph_api_url}/{self.threads_user_id}",
                    params={
                        'fields': 'id,username,threads_profile_picture_url',
                        'access_token': self.access_token
                    }
                ) as response:
                    if response.status == 200:
                        user_data = await response.json()
                        self.authenticated = True
                        return {
                            'authenticated': True,
                            'user_id': user_data.get('id'),
                            'username': user_data.get('username')
                        }
                    else:
                        error_data = await response.json()
                        raise Exception(f"Authentication failed: {error_data}")
        
        except Exception as e:
            self.authenticated = False
            raise Exception(f"Threads authentication error: {str(e)}")
    
    async def create_post(
        self,
        text: str,
        media_urls: Optional[List[str]] = None,
        schedule_time: Optional[str] = None
    ) -> Dict:
        """
        Create a post on Threads
        
        Threads uses a 2-step process:
        1. Create media container
        2. Publish the container
        
        Parameters:
        - text: Post text (up to 500 characters)
        - media_urls: List of image/video URLs (optional)
        - schedule_time: Not currently supported
        """
        try:
            if not self.authenticated:
                await self.authenticate()
            
            # Step 1: Create media container
            container_id = await self._create_media_container(text, media_urls)
            
            # Step 2: Publish the container
            post_id = await self._publish_container(container_id)
            
            return {
                'post_id': post_id,
                'success': True,
                'platform': 'threads'
            }
        
        except Exception as e:
            raise Exception(f"Threads post error: {str(e)}")
    
    async def _create_media_container(
        self,
        text: str,
        media_urls: Optional[List[str]] = None
    ) -> str:
        """Create Threads media container"""
        try:
            data = {
                'media_type': 'TEXT',
                'text': text,
                'access_token': self.access_token
            }
            
            # Add media if provided
            if media_urls and len(media_urls) > 0:
                media_url = media_urls[0]  # Threads supports 1 media item per post
                
                # Determine media type
                is_video = media_url.lower().endswith(('.mp4', '.mov', '.avi'))
                
                if is_video:
                    data['media_type'] = 'VIDEO'
                    data['video_url'] = media_url
                else:
                    data['media_type'] = 'IMAGE'
                    data['image_url'] = media_url
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.graph_api_url}/{self.threads_user_id}/threads",
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
    
    async def _publish_container(self, container_id: str) -> str:
        """Publish Threads container"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.graph_api_url}/{self.threads_user_id}/threads_publish",
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
    
    async def create_reply(self, text: str, reply_to_id: str) -> Dict:
        """Create a reply to a Threads post"""
        try:
            if not self.authenticated:
                await self.authenticate()
            
            # Create reply container
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.graph_api_url}/{self.threads_user_id}/threads",
                    data={
                        'media_type': 'TEXT',
                        'text': text,
                        'reply_to_id': reply_to_id,
                        'access_token': self.access_token
                    }
                ) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        container_id = result.get('id')
                        
                        # Publish reply
                        reply_id = await self._publish_container(container_id)
                        return {
                            'reply_id': reply_id,
                            'success': True,
                            'platform': 'threads'
                        }
                    else:
                        error_data = await response.json()
                        raise Exception(f"Reply creation failed: {error_data}")
        
        except Exception as e:
            raise Exception(f"Threads reply error: {str(e)}")
