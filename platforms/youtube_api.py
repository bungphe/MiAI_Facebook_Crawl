"""
YouTube API Poster
Uses YouTube Data API v3 for uploading videos
"""

import aiohttp
import os
from typing import Optional, List, Dict
from .base_poster import BasePoster
import json

class YouTubePoster(BasePoster):
    """YouTube posting functionality"""
    
    def __init__(self):
        super().__init__('youtube')
        self.api_url = "https://www.googleapis.com/youtube/v3"
        self.upload_url = "https://www.googleapis.com/upload/youtube/v3"
        self.api_key = os.getenv('YOUTUBE_API_KEY')
    
    async def authenticate(
        self,
        access_token: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        additional_params: Optional[Dict] = None
    ) -> Dict:
        """
        Authenticate with YouTube API
        Uses OAuth 2.0 access token
        """
        try:
            self.access_token = access_token or os.getenv('YOUTUBE_ACCESS_TOKEN')
            self.api_key = api_key or self.api_key
            
            if not self.access_token:
                raise Exception("YouTube access token is required")
            
            # Verify token by getting channel info
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/channels",
                    params={
                        'part': 'snippet,contentDetails,statistics',
                        'mine': 'true'
                    },
                    headers={
                        'Authorization': f'Bearer {self.access_token}'
                    }
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('items'):
                            channel = result['items'][0]
                            self.channel_id = channel.get('id')
                            self.authenticated = True
                            return {
                                'authenticated': True,
                                'channel_id': channel.get('id'),
                                'channel_title': channel.get('snippet', {}).get('title'),
                                'subscriber_count': channel.get('statistics', {}).get('subscriberCount')
                            }
                        else:
                            raise Exception("No YouTube channel found")
                    else:
                        error_data = await response.json()
                        raise Exception(f"Authentication failed: {error_data}")
        
        except Exception as e:
            self.authenticated = False
            raise Exception(f"YouTube authentication error: {str(e)}")
    
    async def create_post(
        self,
        text: str,
        media_urls: Optional[List[str]] = None,
        schedule_time: Optional[str] = None
    ) -> Dict:
        """
        Upload a video to YouTube
        
        Parameters:
        - text: Video description
        - media_urls: Video URL (only 1 video)
        - schedule_time: Scheduled publish time (ISO 8601 format)
        """
        try:
            if not self.authenticated:
                await self.authenticate()
            
            if not media_urls or len(media_urls) == 0:
                raise Exception("YouTube requires a video URL")
            
            video_url = media_urls[0]
            
            # Extract title from text (first line) and description (rest)
            lines = text.split('\n', 1)
            title = lines[0][:100]  # YouTube title max 100 chars
            description = lines[1] if len(lines) > 1 else text
            
            # Upload video
            video_id = await self._upload_video(
                title=title,
                description=description,
                video_url=video_url,
                schedule_time=schedule_time
            )
            
            return {
                'post_id': video_id,
                'success': True,
                'platform': 'youtube',
                'video_url': f'https://www.youtube.com/watch?v={video_id}'
            }
        
        except Exception as e:
            raise Exception(f"YouTube post error: {str(e)}")
    
    async def _upload_video(
        self,
        title: str,
        description: str,
        video_url: str,
        schedule_time: Optional[str] = None,
        category_id: str = "22",  # People & Blogs
        privacy_status: str = "public"
    ) -> str:
        """Upload video to YouTube"""
        try:
            # Download video
            async with aiohttp.ClientSession() as session:
                async with session.get(video_url) as video_response:
                    if video_response.status != 200:
                        raise Exception("Failed to download video")
                    
                    video_data = await video_response.read()
                    
                    # Prepare metadata
                    metadata = {
                        'snippet': {
                            'title': title,
                            'description': description,
                            'categoryId': category_id,
                            'tags': []
                        },
                        'status': {
                            'privacyStatus': privacy_status,
                            'selfDeclaredMadeForKids': False
                        }
                    }
                    
                    # Add scheduling if provided
                    if schedule_time:
                        metadata['status']['privacyStatus'] = 'private'
                        metadata['status']['publishAt'] = schedule_time
                    
                    # Upload video using resumable upload
                    upload_url = await self._initiate_upload(metadata)
                    video_id = await self._complete_upload(upload_url, video_data)
                    
                    return video_id
        
        except Exception as e:
            raise Exception(f"Video upload error: {str(e)}")
    
    async def _initiate_upload(self, metadata: Dict) -> str:
        """Initiate resumable upload"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.upload_url}/videos",
                    params={
                        'uploadType': 'resumable',
                        'part': 'snippet,status'
                    },
                    headers={
                        'Authorization': f'Bearer {self.access_token}',
                        'Content-Type': 'application/json',
                        'X-Upload-Content-Type': 'video/*'
                    },
                    json=metadata
                ) as response:
                    if response.status in [200, 201]:
                        # Get upload URL from Location header
                        upload_url = response.headers.get('Location')
                        return upload_url
                    else:
                        error_data = await response.json()
                        raise Exception(f"Upload initiation failed: {error_data}")
        
        except Exception as e:
            raise Exception(f"Upload initiation error: {str(e)}")
    
    async def _complete_upload(self, upload_url: str, video_data: bytes) -> str:
        """Complete resumable upload"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(
                    upload_url,
                    data=video_data,
                    headers={
                        'Content-Type': 'video/*'
                    }
                ) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        return result.get('id')
                    else:
                        error_data = await response.json()
                        raise Exception(f"Upload completion failed: {error_data}")
        
        except Exception as e:
            raise Exception(f"Upload completion error: {str(e)}")
    
    async def update_video(
        self,
        video_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict:
        """Update video metadata"""
        try:
            if not self.authenticated:
                await self.authenticate()
            
            # Get current video details
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/videos",
                    params={
                        'part': 'snippet',
                        'id': video_id
                    },
                    headers={
                        'Authorization': f'Bearer {self.access_token}'
                    }
                ) as get_response:
                    if get_response.status == 200:
                        result = await get_response.json()
                        if not result.get('items'):
                            raise Exception("Video not found")
                        
                        video = result['items'][0]
                        snippet = video.get('snippet', {})
                        
                        # Update fields
                        if title:
                            snippet['title'] = title
                        if description:
                            snippet['description'] = description
                        if tags:
                            snippet['tags'] = tags
                        
                        # Update video
                        async with session.put(
                            f"{self.api_url}/videos",
                            params={'part': 'snippet'},
                            headers={
                                'Authorization': f'Bearer {self.access_token}',
                                'Content-Type': 'application/json'
                            },
                            json={
                                'id': video_id,
                                'snippet': snippet
                            }
                        ) as update_response:
                            if update_response.status == 200:
                                return {
                                    'success': True,
                                    'video_id': video_id,
                                    'message': 'Video updated successfully'
                                }
                            else:
                                error_data = await update_response.json()
                                raise Exception(f"Video update failed: {error_data}")
                    else:
                        error_data = await get_response.json()
                        raise Exception(f"Failed to get video: {error_data}")
        
        except Exception as e:
            raise Exception(f"Video update error: {str(e)}")
