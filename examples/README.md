# Examples

This directory contains example code for using the Multi-Platform Social Media Posting API.

## Files

### 1. `post_example.py`
Basic examples showing how to use the API with synchronous requests.

**Features:**
- Post to multiple platforms
- Post to single platform
- Upload and post media
- Create scheduled posts
- Check API health
- Get platform information

**Usage:**
```bash
python examples/post_example.py
```

### 2. `async_example.py`
Advanced examples using async/await for better performance.

**Features:**
- Concurrent posting to multiple platforms
- Different content for each platform
- Bulk upload and post
- API monitoring
- Rate-limited posting
- Error handling

**Usage:**
```bash
python examples/async_example.py
```

## Quick Start

1. Make sure the API server is running:
```bash
python main.py
```

2. Run an example:
```bash
python examples/post_example.py
```

3. Uncomment specific example functions to test different features.

## Common Use Cases

### Post to Multiple Platforms
```python
import requests

response = requests.post('http://localhost:8000/api/post', json={
    "text": "Hello World!",
    "platforms": ["facebook", "instagram", "x"],
    "media_urls": ["https://example.com/image.jpg"]
})
```

### Upload a File
```python
import requests

with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/upload',
        files={'file': f}
    )
```

### Check Available Platforms
```python
import requests

response = requests.get('http://localhost:8000/api/platforms')
platforms = response.json()['platforms']
```

## Notes

- All examples assume the API is running on `http://localhost:8000`
- You need to configure your API credentials in `.env` file
- Some examples use placeholder image URLs from picsum.photos
- For production use, replace placeholder URLs with your actual media URLs
