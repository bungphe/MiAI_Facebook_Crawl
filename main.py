"""
Multi-Platform Social Media Posting API
Supports: Facebook, Instagram, TikTok, X (Twitter), Threads, YouTube
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from datetime import datetime
import os

# Import platform modules
from platforms.facebook_api import FacebookPoster
from platforms.instagram_api import InstagramPoster
from platforms.tiktok_api import TikTokPoster
from platforms.x_api import XPoster
from platforms.threads_api import ThreadsPoster
from platforms.youtube_api import YouTubePoster

app = FastAPI(
    title="Multi-Platform Social Media Posting API",
    description="API để đăng bài lên 6 nền tảng: Facebook, Instagram, TikTok, X, Threads, YouTube",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class PostContent(BaseModel):
    text: str
    platforms: List[str]  # ['facebook', 'instagram', 'tiktok', 'x', 'threads', 'youtube']
    media_urls: Optional[List[str]] = None
    schedule_time: Optional[str] = None

class AuthCredentials(BaseModel):
    platform: str
    access_token: Optional[str] = None
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    additional_params: Optional[dict] = None

class PostResponse(BaseModel):
    success: bool
    platform: str
    post_id: Optional[str] = None
    message: str
    error: Optional[str] = None

# Initialize platform posters
platform_posters = {
    'facebook': FacebookPoster(),
    'instagram': InstagramPoster(),
    'tiktok': TikTokPoster(),
    'x': XPoster(),
    'threads': ThreadsPoster(),
    'youtube': YouTubePoster()
}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Multi-Platform Social Media Posting API",
        "version": "1.0.0",
        "supported_platforms": ["facebook", "instagram", "tiktok", "x", "threads", "youtube"],
        "endpoints": {
            "post": "/api/post",
            "post_single": "/api/post/{platform}",
            "upload": "/api/upload",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "platforms_available": list(platform_posters.keys())
    }

@app.post("/api/post", response_model=List[PostResponse])
async def post_to_platforms(content: PostContent):
    """
    Đăng bài lên nhiều nền tảng cùng lúc
    
    Parameters:
    - text: Nội dung bài đăng
    - platforms: Danh sách các nền tảng cần đăng (facebook, instagram, tiktok, x, threads, youtube)
    - media_urls: Danh sách URL của ảnh/video (optional)
    - schedule_time: Thời gian hẹn đăng (optional, format: ISO 8601)
    """
    results = []
    
    for platform in content.platforms:
        if platform not in platform_posters:
            results.append(PostResponse(
                success=False,
                platform=platform,
                message="Platform not supported",
                error=f"Platform '{platform}' is not supported"
            ))
            continue
        
        try:
            poster = platform_posters[platform]
            post_result = await poster.create_post(
                text=content.text,
                media_urls=content.media_urls,
                schedule_time=content.schedule_time
            )
            
            results.append(PostResponse(
                success=True,
                platform=platform,
                post_id=post_result.get('post_id'),
                message=f"Successfully posted to {platform}",
                error=None
            ))
        except Exception as e:
            results.append(PostResponse(
                success=False,
                platform=platform,
                post_id=None,
                message=f"Failed to post to {platform}",
                error=str(e)
            ))
    
    return results

@app.post("/api/post/{platform}", response_model=PostResponse)
async def post_to_single_platform(
    platform: str,
    text: str = Form(...),
    media_urls: Optional[str] = Form(None),
    schedule_time: Optional[str] = Form(None)
):
    """
    Đăng bài lên một nền tảng cụ thể
    
    Parameters:
    - platform: Tên nền tảng (facebook, instagram, tiktok, x, threads, youtube)
    - text: Nội dung bài đăng
    - media_urls: URL của ảnh/video (comma-separated)
    - schedule_time: Thời gian hẹn đăng (ISO 8601 format)
    """
    if platform not in platform_posters:
        raise HTTPException(status_code=400, detail=f"Platform '{platform}' is not supported")
    
    try:
        media_list = media_urls.split(',') if media_urls else None
        poster = platform_posters[platform]
        post_result = await poster.create_post(
            text=text,
            media_urls=media_list,
            schedule_time=schedule_time
        )
        
        return PostResponse(
            success=True,
            platform=platform,
            post_id=post_result.get('post_id'),
            message=f"Successfully posted to {platform}",
            error=None
        )
    except Exception as e:
        return PostResponse(
            success=False,
            platform=platform,
            post_id=None,
            message=f"Failed to post to {platform}",
            error=str(e)
        )

@app.post("/api/upload")
async def upload_media(file: UploadFile = File(...)):
    """
    Upload media file (ảnh/video) để sử dụng trong bài đăng
    """
    try:
        # Create uploads directory if not exists
        os.makedirs("uploads", exist_ok=True)
        
        # Save file
        file_path = f"uploads/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {
            "success": True,
            "filename": file.filename,
            "file_path": file_path,
            "file_size": len(content),
            "message": "File uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/auth/{platform}")
async def authenticate_platform(platform: str, credentials: AuthCredentials):
    """
    Xác thực với một nền tảng cụ thể
    
    Parameters:
    - platform: Tên nền tảng
    - credentials: Thông tin xác thực (access_token, api_key, api_secret, etc.)
    """
    if platform not in platform_posters:
        raise HTTPException(status_code=400, detail=f"Platform '{platform}' is not supported")
    
    try:
        poster = platform_posters[platform]
        auth_result = await poster.authenticate(
            access_token=credentials.access_token,
            api_key=credentials.api_key,
            api_secret=credentials.api_secret,
            additional_params=credentials.additional_params
        )
        
        return {
            "success": True,
            "platform": platform,
            "message": f"Successfully authenticated with {platform}",
            "details": auth_result
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

@app.get("/api/platforms")
async def get_supported_platforms():
    """
    Lấy danh sách các nền tảng được hỗ trợ
    """
    return {
        "platforms": [
            {
                "id": "facebook",
                "name": "Facebook",
                "description": "Đăng bài lên Facebook Page hoặc Profile",
                "supports_media": True,
                "supports_video": True,
                "supports_scheduling": True
            },
            {
                "id": "instagram",
                "name": "Instagram",
                "description": "Đăng bài lên Instagram Feed, Stories, Reels",
                "supports_media": True,
                "supports_video": True,
                "supports_scheduling": True
            },
            {
                "id": "tiktok",
                "name": "TikTok",
                "description": "Đăng video lên TikTok",
                "supports_media": False,
                "supports_video": True,
                "supports_scheduling": True
            },
            {
                "id": "x",
                "name": "X (Twitter)",
                "description": "Đăng tweet lên X",
                "supports_media": True,
                "supports_video": True,
                "supports_scheduling": False
            },
            {
                "id": "threads",
                "name": "Threads",
                "description": "Đăng bài lên Threads",
                "supports_media": True,
                "supports_video": True,
                "supports_scheduling": False
            },
            {
                "id": "youtube",
                "name": "YouTube",
                "description": "Upload video lên YouTube",
                "supports_media": False,
                "supports_video": True,
                "supports_scheduling": True
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
