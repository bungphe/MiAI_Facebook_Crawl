"""
TikTok API Poster
Uses TikTok Content Posting API for uploading videos
"""

import aiohttp
import os
from typing import Optional, List, Dict
from .base_poster import BasePoster

class TikTokPoster(BasePoster):
    """TikTok posting functionality"""
    
    def __init__(self):
        super().__init__('tiktok')
        self.api_url = "https://open.tiktokapis.com/v2"
        self.client_key = os.getenv('TIKTOK_CLIENT_KEY')
        self.client_secret = os.getenv('TIKTOK_CLIENT_SECRET')
    
    async def authenticate(
        self,
        access_token: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        additional_params: Optional[Dict] = None
    ) -> Dict:
        """
        Authenticate with TikTok API
        Uses OAuth 2.0 flow
        """
        try:
            self.access_token = access_token or os.getenv('TIKTOK_ACCESS_TOKEN')
            self.client_key = api_key or self.client_key
            self.client_secret = api_secret or self.client_secret
            
            if not self.access_token:
                raise Exception("TikTok access token is required")
            
            # Verify token by getting user info
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/user/info/",
                    headers={
                        'Authorization': f'Bearer {self.access_token}',
                        'Content-Type': 'application/json'
                    },
                    params={
                        'fields': 'open_id,union_id,avatar_url,display_name'
                    }
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        user_data = result.get('data', {}).get('user', {})
                        self.authenticated = True
                        return {
                            'authenticated': True,
                            'open_id': user_data.get('open_id'),
                            'display_name': user_data.get('display_name')
                        }
                    else:
                        error_data = await response.json()
                        raise Exception(f"Authentication failed: {error_data}")
        
        except Exception as e:
            self.authenticated = False
            raise Exception(f"TikTok authentication error: {str(e)}")
    
    async def create_post(
        self,
        text: str,
        media_urls: Optional[List[str]] = None,
        schedule_time: Optional[str] = None
    ) -> Dict:
        """
        Create a video post on TikTok
        
        TikTok requires:
        1. Initialize upload
        2. Upload video chunks
        3. Publish video
        
        Parameters:
        - text: Video description/caption
        - media_urls: Video URL (only 1 video at a time)
        - schedule_time: Scheduled publish time (Unix timestamp)
        """
        try:
            if not self.authenticated:
                await self.authenticate()
            
            if not media_urls or len(media_urls) == 0:
                raise Exception("TikTok requires a video URL")
            
            video_url = media_urls[0]
            
            # Step 1: Initialize video upload
            upload_data = await self._initialize_upload()
            
            # Step 2: Upload video
            await self._upload_video(upload_data['upload_url'], video_url)
            
            # Step 3: Publish video
            post_id = await self._publish_video(
                upload_data['publish_id'],
                text,
                schedule_time
            )
            
            return {
                'post_id': post_id,
                'success': True,
                'platform': 'tiktok'
            }
        
        except Exception as e:
            raise Exception(f"TikTok post error: {str(e)}")
    
    async def _initialize_upload(self) -> Dict:
        """Initialize TikTok video upload"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/post/publish/inbox/video/init/",
                    headers={
                        'Authorization': f'Bearer {self.access_token}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'source_info': {
                            'source': 'FILE_UPLOAD',
                            'video_size': 0,  # Will be determined during upload
                            'chunk_size': 10000000,  # 10MB chunks
                            'total_chunk_count': 1
                        }
                    }
                ) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        data = result.get('data', {})
                        return {
                            'upload_url': data.get('upload_url'),
                            'publish_id': data.get('publish_id')
                        }
                    else:
                        error_data = await response.json()
                        raise Exception(f"Upload initialization failed: {error_data}")
        
        except Exception as e:
            raise Exception(f"Upload initialization error: {str(e)}")
    
    async def _upload_video(self, upload_url: str, video_url: str) -> bool:
        """Upload video to TikTok"""
        try:
            # Download video from URL and upload to TikTok
            async with aiohttp.ClientSession() as session:
                # Download video
                async with session.get(video_url) as video_response:
                    if video_response.status == 200:
                        video_data = await video_response.read()
                        
                        # Upload to TikTok
                        async with session.put(
                            upload_url,
                            data=video_data,
                            headers={'Content-Type': 'video/mp4'}
                        ) as upload_response:
                            return upload_response.status in [200, 201, 204]
                    else:
                        raise Exception("Failed to download video")
        
        except Exception as e:
            raise Exception(f"Video upload error: {str(e)}")
    
    async def _publish_video(
        self,
        publish_id: str,
        caption: str,
        schedule_time: Optional[str] = None
    ) -> str:
        """Publish video to TikTok"""
        try:
            post_data = {
                'post_info': {
                    'title': caption,
                    'privacy_level': 'PUBLIC_TO_EVERYONE',
                    'disable_duet': False,
                    'disable_comment': False,
                    'disable_stitch': False,
                    'video_cover_timestamp_ms': 1000
                },
                'source_info': {
                    'source': 'FILE_UPLOAD',
                    'publish_id': publish_id
                }
            }
            
            # Add scheduling if provided
            if schedule_time:
                post_data['post_info']['post_mode'] = 'SCHEDULED'
                post_data['post_info']['schedule_time'] = int(schedule_time)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/post/publish/video/init/",
                    headers={
                        'Authorization': f'Bearer {self.access_token}',
                        'Content-Type': 'application/json'
                    },
                    json=post_data
                ) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        return result.get('data', {}).get('publish_id')
                    else:
                        error_data = await response.json()
                        raise Exception(f"Video publishing failed: {error_data}")
        
        except Exception as e:
            raise Exception(f"Video publishing error: {str(e)}")
