# API Usage Guide - Step by Step

## 🎯 Workflow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                     CLIENT APPLICATION                        │
│         (Web App / Mobile App / Script / CLI)                │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        │ HTTP Request (JSON)
                        ▼
┌──────────────────────────────────────────────────────────────┐
│                   FASTAPI SERVER                             │
│                  (Port 8000)                                 │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │           API Endpoints                            │    │
│  │  • POST /api/post                                  │    │
│  │  • POST /api/post/{platform}                       │    │
│  │  • POST /api/upload                                │    │
│  │  • POST /api/auth/{platform}                       │    │
│  └────────────────────────────────────────────────────┘    │
│                        │                                     │
│                        ▼                                     │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Request Validation & Processing            │    │
│  │              (Pydantic Models)                     │    │
│  └────────────────────────────────────────────────────┘    │
│                        │                                     │
│                        ▼                                     │
│  ┌────────────────────────────────────────────────────┐    │
│  │          Platform Router/Dispatcher                │    │
│  │         (Async Task Management)                    │    │
│  └────────────────────────────────────────────────────┘    │
└───────────────────────┬──────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌─────────────────┐           ┌─────────────────┐
│  Platform APIs  │           │  Platform APIs  │
│  (Parallel)     │           │  (Parallel)     │
└─────────────────┘           └─────────────────┘
        │                               │
    ┌───┴───┬───────┬───────┬───────┬──┴───┐
    │       │       │       │       │      │
    ▼       ▼       ▼       ▼       ▼      ▼
┌────────┐ │   │   │   │   │   ┌─────────┐
│Facebook│ │   │   │   │   │   │ YouTube │
└────────┘ │   │   │   │   │   └─────────┘
    ┌──────▼┐  │   │   │   │
    │Instagram  │   │   │   │
    └──────┘  │   │   │   │
        ┌─────▼┐  │   │   │
        │TikTok│  │   │   │
        └─────┘  │   │   │
            ┌────▼┐  │   │
            │  X  │  │   │
            └────┘  │   │
                ┌───▼──┐│
                │Threads│
                └───────┘
```

## 📋 Complete Usage Flow

### Step 1: Setup & Configuration

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure credentials
cp .env.example .env
nano .env  # Edit with your API keys

# 3. Start server
python main.py
```

### Step 2: Test API Connection

```bash
# Check if API is running
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "timestamp": "2024-01-01T12:00:00",
#   "platforms_available": ["facebook", "instagram", ...]
# }
```

### Step 3: Authenticate Platforms

```bash
# Authenticate with Facebook
curl -X POST http://localhost:8000/api/auth/facebook \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "facebook",
    "access_token": "YOUR_TOKEN",
    "additional_params": {
      "page_id": "YOUR_PAGE_ID"
    }
  }'
```

### Step 4: Post Content

#### Simple Text Post
```bash
curl -X POST http://localhost:8000/api/post \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello World!",
    "platforms": ["facebook", "x"]
  }'
```

#### Post with Image
```bash
curl -X POST http://localhost:8000/api/post \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Check out this image!",
    "platforms": ["facebook", "instagram"],
    "media_urls": ["https://example.com/image.jpg"]
  }'
```

#### Post with Multiple Images
```bash
curl -X POST http://localhost:8000/api/post \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Gallery post",
    "platforms": ["facebook"],
    "media_urls": [
      "https://example.com/image1.jpg",
      "https://example.com/image2.jpg",
      "https://example.com/image3.jpg"
    ]
  }'
```

#### Scheduled Post
```bash
# Schedule for future (Unix timestamp)
SCHEDULE_TIME=$(date -d "tomorrow 10:00" +%s)

curl -X POST http://localhost:8000/api/post \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"Scheduled post!\",
    \"platforms\": [\"facebook\", \"youtube\"],
    \"schedule_time\": \"$SCHEDULE_TIME\"
  }"
```

### Step 5: Upload Local File

```bash
# Upload a local file first
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/path/to/your/image.jpg"

# Response will include file_path
# Use that file_path in your post
```

## 🔄 Complete Workflow Examples

### Example 1: Daily Social Media Update

```python
import requests
import schedule
import time

API_URL = "http://localhost:8000"

def post_daily_update():
    """Post daily update to all platforms"""
    data = {
        "text": "Good morning! Here's today's update 🌅",
        "platforms": ["facebook", "instagram", "x", "threads"],
        "media_urls": ["https://example.com/morning.jpg"]
    }
    
    response = requests.post(f"{API_URL}/api/post", json=data)
    results = response.json()
    
    for result in results:
        status = "✅" if result["success"] else "❌"
        print(f"{status} {result['platform']}: {result['message']}")

# Schedule daily at 9 AM
schedule.every().day.at("09:00").do(post_daily_update)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Example 2: Content Distribution System

```python
import requests
from typing import List, Dict

class ContentDistributor:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
    
    def post_to_all(self, content: str, media: List[str] = None) -> Dict:
        """Post to all platforms"""
        platforms = ["facebook", "instagram", "tiktok", "x", "threads", "youtube"]
        return self.post(content, platforms, media)
    
    def post(self, content: str, platforms: List[str], media: List[str] = None) -> Dict:
        """Post to specific platforms"""
        data = {
            "text": content,
            "platforms": platforms,
            "media_urls": media or []
        }
        
        response = requests.post(f"{self.api_url}/api/post", json=data)
        return response.json()
    
    def post_with_platform_specific_content(self, posts: Dict[str, Dict]) -> List:
        """Post different content to different platforms"""
        results = []
        
        for platform, content in posts.items():
            response = requests.post(
                f"{self.api_url}/api/post/{platform}",
                data=content
            )
            results.append(response.json())
        
        return results

# Usage
distributor = ContentDistributor()

# Same content to all platforms
distributor.post_to_all(
    "Big announcement! 🎉",
    media=["https://example.com/announcement.jpg"]
)

# Different content per platform
distributor.post_with_platform_specific_content({
    "facebook": {
        "text": "Join us on Facebook for exclusive content!",
        "media_urls": "https://example.com/fb.jpg"
    },
    "instagram": {
        "text": "Beautiful shot 📸 #photography #art",
        "media_urls": "https://example.com/insta.jpg"
    },
    "x": {
        "text": "Quick update on X! 🐦",
        "media_urls": "https://example.com/tweet.jpg"
    }
})
```

### Example 3: Automated News Posting

```python
import requests
import feedparser

API_URL = "http://localhost:8000"

def fetch_and_post_news():
    """Fetch RSS feed and post to social media"""
    # Fetch RSS feed
    feed = feedparser.parse("https://example.com/rss")
    
    for entry in feed.entries[:5]:  # Post top 5 articles
        title = entry.title
        link = entry.link
        summary = entry.summary[:200]  # Truncate
        
        # Create post
        text = f"{title}\n\n{summary}...\n\nRead more: {link}"
        
        # Post to platforms
        response = requests.post(f"{API_URL}/api/post", json={
            "text": text,
            "platforms": ["facebook", "x", "threads"]
        })
        
        print(f"Posted: {title}")

fetch_and_post_news()
```

## 🎨 Advanced Features

### Batch Processing

```python
import asyncio
import aiohttp

async def post_batch(posts: List[Dict]):
    """Post multiple contents concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        for post in posts:
            task = session.post(
                "http://localhost:8000/api/post",
                json=post
            )
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        results = [await r.json() for r in responses]
        
        return results

# Usage
posts = [
    {"text": "Post 1", "platforms": ["facebook"]},
    {"text": "Post 2", "platforms": ["instagram"]},
    {"text": "Post 3", "platforms": ["x"]}
]

asyncio.run(post_batch(posts))
```

### Error Handling & Retry

```python
import requests
import time

def post_with_retry(data: Dict, max_retries: int = 3) -> Dict:
    """Post with automatic retry on failure"""
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "http://localhost:8000/api/post",
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise Exception(f"Failed after {max_retries} attempts: {e}")

# Usage
result = post_with_retry({
    "text": "Important post",
    "platforms": ["facebook", "instagram"]
})
```

## 📊 Monitoring & Analytics

```python
import requests
from datetime import datetime
import json

class SocialMediaMonitor:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.log_file = "social_media_log.json"
    
    def log_post(self, content: str, results: List[Dict]):
        """Log post results"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "results": results
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def get_success_rate(self) -> Dict[str, float]:
        """Calculate success rate per platform"""
        stats = {}
        
        with open(self.log_file, "r") as f:
            for line in f:
                entry = json.loads(line)
                
                for result in entry["results"]:
                    platform = result["platform"]
                    
                    if platform not in stats:
                        stats[platform] = {"success": 0, "total": 0}
                    
                    stats[platform]["total"] += 1
                    if result["success"]:
                        stats[platform]["success"] += 1
        
        # Calculate percentages
        success_rates = {
            platform: (data["success"] / data["total"] * 100)
            for platform, data in stats.items()
        }
        
        return success_rates

# Usage
monitor = SocialMediaMonitor("http://localhost:8000")

# Post and log
data = {"text": "Test post", "platforms": ["facebook", "x"]}
response = requests.post(f"{monitor.api_url}/api/post", json=data)
results = response.json()
monitor.log_post(data["text"], results)

# Get statistics
print(monitor.get_success_rate())
```

## 🔍 Debugging Tips

### Enable Verbose Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)

# Your code here
```

### Check Platform Availability

```bash
curl http://localhost:8000/api/platforms | jq
```

### Test Single Platform First

```bash
# Test Facebook only
curl -X POST http://localhost:8000/api/post/facebook \
  -F "text=Test post"
```

### Verify Credentials

```bash
# Test authentication
curl -X POST http://localhost:8000/api/auth/facebook \
  -H "Content-Type: application/json" \
  -d '{"platform": "facebook", "access_token": "YOUR_TOKEN"}'
```

## 📚 Next Steps

1. ✅ Setup complete
2. ✅ Test API endpoints
3. ✅ Configure platforms
4. ✅ Make first post
5. 📈 Monitor and optimize
6. 🚀 Scale and automate

---

**Happy posting! 🎉**
