# Quick Start Guide

Get started with the Multi-Platform Social Media Posting API in 5 minutes!

## 🚀 Quick Setup

### Option 1: Manual Setup (Recommended for Development)

1. **Clone and Navigate**
   ```bash
   cd /path/to/project
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

5. **Start the Server**
   ```bash
   python main.py
   ```

6. **Access API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Option 2: Using Startup Script

**Linux/Mac:**
```bash
chmod +x start_api.sh
./start_api.sh
```

**Windows:**
```batch
start_api.bat
```

### Option 3: Using Docker

1. **Build and Run**
   ```bash
   docker-compose up -d
   ```

2. **View Logs**
   ```bash
   docker-compose logs -f api
   ```

3. **Stop**
   ```bash
   docker-compose down
   ```

## 🔑 Get API Credentials

### Facebook & Instagram

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add "Facebook Login" and "Instagram Graph API"
4. Generate access token from Graph API Explorer
5. For Instagram: Get your Instagram Business Account ID

### TikTok

1. Visit [TikTok Developers](https://developers.tiktok.com/)
2. Create a new app
3. Enable "Content Posting API"
4. Get Client Key and Client Secret
5. Complete OAuth flow to get Access Token

### X (Twitter)

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a project and app
3. Generate API Keys and Bearer Token
4. Enable OAuth 1.0a or OAuth 2.0

### Threads

1. Threads uses Facebook infrastructure
2. Visit [Threads API Docs](https://developers.facebook.com/docs/threads)
3. Use Facebook Access Token
4. Get your Threads User ID

### YouTube

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials
5. Complete OAuth flow to get Access Token

## 📝 Your First Post

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/post" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello from Multi-Platform API! 🚀",
    "platforms": ["facebook", "instagram", "x"],
    "media_urls": ["https://example.com/image.jpg"]
  }'
```

### Using Python

```python
import requests

response = requests.post('http://localhost:8000/api/post', json={
    "text": "Hello World! 🌍",
    "platforms": ["facebook", "x"],
    "media_urls": ["https://example.com/photo.jpg"]
})

print(response.json())
```

### Using JavaScript

```javascript
fetch('http://localhost:8000/api/post', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        text: 'Hello from JavaScript! 👋',
        platforms: ['facebook', 'instagram'],
        media_urls: ['https://example.com/image.jpg']
    })
})
.then(res => res.json())
.then(data => console.log(data));
```

## 🧪 Test Your Setup

1. **Check API Health**
   ```bash
   curl http://localhost:8000/health
   ```

2. **View Supported Platforms**
   ```bash
   curl http://localhost:8000/api/platforms
   ```

3. **Run Examples**
   ```bash
   python examples/post_example.py
   ```

4. **Run Tests**
   ```bash
   pytest tests/
   ```

## 📊 Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
  - Interactive API testing interface
  - Try out endpoints directly from browser
  
- **ReDoc**: http://localhost:8000/redoc
  - Beautiful API documentation
  - Detailed parameter descriptions

## 🎯 Common Tasks

### Post to Single Platform

```bash
curl -X POST "http://localhost:8000/api/post/facebook" \
  -F "text=Single platform post" \
  -F "media_urls=https://example.com/image.jpg"
```

### Upload a File

```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@/path/to/image.jpg"
```

### Schedule a Post

```python
import time
import requests

# Schedule for 1 hour from now
schedule_time = int(time.time()) + 3600

requests.post('http://localhost:8000/api/post', json={
    "text": "Scheduled post!",
    "platforms": ["facebook"],
    "schedule_time": str(schedule_time)
})
```

## ⚠️ Troubleshooting

### API Won't Start
- Check if port 8000 is already in use
- Verify Python version (3.8+)
- Ensure all dependencies are installed

### Authentication Errors
- Verify API credentials in .env
- Check if tokens are still valid
- Ensure correct permissions/scopes

### Post Failed
- Check platform-specific requirements
- Verify media URLs are accessible
- Review character limits for each platform

## 📚 Next Steps

1. Read the full [API Documentation](API_DOCUMENTATION.md)
2. Explore [Example Code](examples/)
3. Check [Platform-Specific Notes](API_DOCUMENTATION.md#platform-specific-notes)
4. Learn about [Error Handling](API_DOCUMENTATION.md#troubleshooting)

## 💡 Tips

- Start with one platform to test your setup
- Use Swagger UI for easy API exploration
- Check health endpoint before posting
- Review logs for debugging
- Keep your API tokens secure

## 🆘 Get Help

- Check documentation: `API_DOCUMENTATION.md`
- Review examples: `examples/`
- Run tests: `pytest tests/`
- Check logs: `logs/` directory

Happy posting! 🎉
