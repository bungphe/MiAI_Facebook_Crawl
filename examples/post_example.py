"""
Example: Post to Multiple Social Media Platforms
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def post_to_multiple_platforms():
    """Post to multiple platforms at once"""
    print("📤 Posting to multiple platforms...")
    
    url = f"{BASE_URL}/api/post"
    
    data = {
        "text": "Hello from Multi-Platform API! 🚀\n\nThis is a test post from our new API.",
        "platforms": ["facebook", "instagram", "x", "threads"],
        "media_urls": ["https://picsum.photos/800/600"]
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        results = response.json()
        
        print("\n✅ Results:")
        for result in results:
            if result["success"]:
                print(f"  ✓ {result['platform']}: Posted successfully (ID: {result['post_id']})")
            else:
                print(f"  ✗ {result['platform']}: Failed - {result['error']}")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

def post_to_single_platform():
    """Post to a single platform"""
    print("\n📤 Posting to Facebook only...")
    
    url = f"{BASE_URL}/api/post/facebook"
    
    data = {
        "text": "This is a Facebook-only post!",
        "media_urls": "https://picsum.photos/800/600"
    }
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        result = response.json()
        
        if result["success"]:
            print(f"✅ Posted successfully! Post ID: {result['post_id']}")
        else:
            print(f"❌ Failed: {result['error']}")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

def upload_and_post():
    """Upload media file and then post"""
    print("\n📤 Uploading media file...")
    
    # First, upload a file
    upload_url = f"{BASE_URL}/api/upload"
    
    # Note: You need to have an actual file to upload
    # files = {'file': open('path/to/your/image.jpg', 'rb')}
    # response = requests.post(upload_url, files=files)
    
    # For this example, we'll use a URL instead
    print("  (Using direct URL instead of upload)")
    
    # Then post with the uploaded file
    post_url = f"{BASE_URL}/api/post"
    
    data = {
        "text": "Posted with uploaded media! 📸",
        "platforms": ["facebook", "instagram"],
        "media_urls": ["https://picsum.photos/1080/1080"]
    }
    
    try:
        response = requests.post(post_url, json=data)
        response.raise_for_status()
        results = response.json()
        
        print("✅ Post results:")
        for result in results:
            print(f"  {result['platform']}: {result['message']}")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

def scheduled_post():
    """Create a scheduled post"""
    print("\n📅 Creating scheduled post...")
    
    url = f"{BASE_URL}/api/post"
    
    # Schedule for 1 hour from now (Unix timestamp)
    import time
    schedule_time = int(time.time()) + 3600
    
    data = {
        "text": "This is a scheduled post! ⏰",
        "platforms": ["facebook", "tiktok", "youtube"],
        "media_urls": ["https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4"],
        "schedule_time": str(schedule_time)
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        results = response.json()
        
        print("✅ Scheduled post results:")
        for result in results:
            if result["success"]:
                print(f"  ✓ {result['platform']}: Scheduled successfully")
            else:
                print(f"  ✗ {result['platform']}: {result['error']}")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

def check_api_health():
    """Check API health status"""
    print("\n🏥 Checking API health...")
    
    url = f"{BASE_URL}/health"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        health = response.json()
        
        print(f"✅ API Status: {health['status']}")
        print(f"   Available platforms: {', '.join(health['platforms_available'])}")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

def get_platform_info():
    """Get information about supported platforms"""
    print("\n📱 Getting platform information...")
    
    url = f"{BASE_URL}/api/platforms"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        print("✅ Supported Platforms:")
        for platform in data['platforms']:
            print(f"\n  {platform['name']} ({platform['id']})")
            print(f"    - {platform['description']}")
            print(f"    - Media: {platform['supports_media']}, Video: {platform['supports_video']}")
            print(f"    - Scheduling: {platform['supports_scheduling']}")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Multi-Platform Social Media Posting API - Examples")
    print("=" * 60)
    
    # Check API health first
    check_api_health()
    
    # Get platform information
    get_platform_info()
    
    # Examples (uncomment to run)
    # post_to_multiple_platforms()
    # post_to_single_platform()
    # upload_and_post()
    # scheduled_post()
    
    print("\n" + "=" * 60)
    print("To run specific examples, uncomment the function calls above")
    print("=" * 60)
