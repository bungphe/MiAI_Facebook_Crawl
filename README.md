# 🚀 Multi-Platform Social Media Posting API

API mạnh mẽ để đăng bài tự động lên 6 nền tảng mạng xã hội: **Facebook**, **Instagram**, **TikTok**, **X (Twitter)**, **Threads**, và **YouTube**.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Tính Năng Chính

- ✅ **Đa Nền Tảng**: Đăng bài đồng thời lên 6 mạng xã hội
- 📸 **Hỗ Trợ Media**: Text, hình ảnh, và video
- ⏰ **Hẹn Giờ**: Lên lịch đăng bài tự động
- 🚀 **Hiệu Suất Cao**: Async/await với FastAPI
- 📡 **RESTful API**: Dễ dàng tích hợp
- 📚 **Documentation**: Swagger UI tích hợp sẵn
- 🐳 **Docker Ready**: Deploy dễ dàng

## 🎯 Nền Tảng Hỗ Trợ

| Platform | Text | Image | Video | Scheduling |
|----------|------|-------|-------|------------|
| Facebook | ✅ | ✅ | ✅ | ✅ |
| Instagram | ✅ | ✅ | ✅ | ✅ |
| TikTok | ✅ | ❌ | ✅ | ✅ |
| X (Twitter) | ✅ | ✅ | ✅ | ❌ |
| Threads | ✅ | ✅ | ✅ | ❌ |
| YouTube | ✅ | ❌ | ✅ | ✅ |

## 🚀 Quick Start

### Cài Đặt Nhanh

```bash
# Clone repository
git clone <repository-url>
cd <repository-directory>

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc: venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Cấu hình
cp .env.example .env
# Chỉnh sửa .env với API credentials của bạn

# Khởi động server
python main.py
```

**Hoặc sử dụng script:**

```bash
# Linux/Mac
chmod +x start_api.sh
./start_api.sh

# Windows
start_api.bat
```

**Hoặc với Docker:**

```bash
docker-compose up -d
```

### Sử Dụng API

```bash
curl -X POST "http://localhost:8000/api/post" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello from Multi-Platform API! 🚀",
    "platforms": ["facebook", "instagram", "x"],
    "media_urls": ["https://example.com/image.jpg"]
  }'
```

### Truy Cập Documentation

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📖 Documentation

- [📘 Quick Start Guide](QUICKSTART.md) - Hướng dẫn bắt đầu nhanh
- [📚 API Documentation](API_DOCUMENTATION.md) - Tài liệu API đầy đủ
- [💡 Examples](examples/) - Ví dụ code mẫu
- [🧪 Tests](tests/) - Unit tests

## 🏗️ Cấu Trúc Project

```
.
├── main.py                 # API application chính
├── config.py              # Configuration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose config
├── platforms/            # Platform modules
│   ├── __init__.py
│   ├── base_poster.py    # Base class
│   ├── facebook_api.py   # Facebook poster
│   ├── instagram_api.py  # Instagram poster
│   ├── tiktok_api.py     # TikTok poster
│   ├── x_api.py          # X (Twitter) poster
│   ├── threads_api.py    # Threads poster
│   └── youtube_api.py    # YouTube poster
├── examples/             # Example code
│   ├── post_example.py   # Basic examples
│   ├── async_example.py  # Async examples
│   └── README.md
├── tests/               # Unit tests
│   └── test_api.py
└── docs/               # Documentation
```

## 💻 API Endpoints

### Core Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /api/platforms` - Danh sách platforms

### Posting Endpoints

- `POST /api/post` - Đăng lên nhiều platforms
- `POST /api/post/{platform}` - Đăng lên 1 platform
- `POST /api/upload` - Upload media file

### Auth Endpoints

- `POST /api/auth/{platform}` - Xác thực với platform

## 🔧 Yêu Cầu

- Python 3.8+
- FastAPI
- aiohttp
- API credentials từ các platforms

## 🔑 Lấy API Credentials

### Facebook & Instagram
- [Facebook Developers](https://developers.facebook.com/)
- Tạo app → Get Access Token

### TikTok
- [TikTok Developers](https://developers.tiktok.com/)
- Enable Content Posting API

### X (Twitter)
- [Twitter Developer Portal](https://developer.twitter.com/)
- Generate API Keys và Bearer Token

### Threads
- [Threads API](https://developers.facebook.com/docs/threads)
- Sử dụng Facebook Access Token

### YouTube
- [Google Cloud Console](https://console.cloud.google.com/)
- Enable YouTube Data API v3

Chi tiết xem [API Documentation](API_DOCUMENTATION.md#cách-lấy-api-keys)

## 📝 Ví Dụ Sử Dụng

### Python

```python
import requests

response = requests.post('http://localhost:8000/api/post', json={
    "text": "Hello World! 🌍",
    "platforms": ["facebook", "instagram", "x"],
    "media_urls": ["https://example.com/photo.jpg"]
})

results = response.json()
for result in results:
    print(f"{result['platform']}: {result['message']}")
```

### JavaScript

```javascript
fetch('http://localhost:8000/api/post', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        text: 'Hello from JS! 👋',
        platforms: ['facebook', 'x'],
        media_urls: ['https://example.com/image.jpg']
    })
})
.then(res => res.json())
.then(data => console.log(data));
```

Xem thêm ví dụ trong [examples/](examples/)

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov

# Run specific test
pytest tests/test_api.py::TestRootEndpoints
```

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop
docker-compose down
```

## 🔒 Security

- Không commit file `.env`
- Rotate API tokens định kỳ
- Sử dụng HTTPS trong production
- Implement rate limiting
- Validate user input

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Credits

Original Facebook Crawl project by:
- Fanpage: http://facebook.com/miaiblog
- Group: https://www.facebook.com/groups/miaigroup
- Website: http://miai.vn
- Youtube: http://bit.ly/miaiyoutube

Extended to Multi-Platform Posting API with ❤️

## 📞 Support

- 📖 [Documentation](API_DOCUMENTATION.md)
- 💡 [Examples](examples/)
- 🐛 [Report Issues](https://github.com/yourusername/repo/issues)

---

**Made with ❤️ for the social media automation community**
