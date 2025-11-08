# Multi-Platform Social Media Posting API

API mạnh mẽ để đăng bài đồng thời lên 6 nền tảng mạng xã hội: Facebook, Instagram, TikTok, X (Twitter), Threads, và YouTube.

## 📋 Mục Lục

- [Tính Năng](#tính-năng)
- [Cài Đặt](#cài-đặt)
- [Cấu Hình](#cấu-hình)
- [Sử Dụng](#sử-dụng)
- [API Endpoints](#api-endpoints)
- [Ví Dụ](#ví-dụ)
- [Platform-Specific Notes](#platform-specific-notes)

## ✨ Tính Năng

- ✅ Đăng bài đồng thời lên nhiều nền tảng
- ✅ Hỗ trợ text, hình ảnh, và video
- ✅ Hẹn giờ đăng bài (cho các nền tảng hỗ trợ)
- ✅ Upload media files
- ✅ RESTful API với FastAPI
- ✅ Async/await cho hiệu suất cao
- ✅ Xử lý lỗi chi tiết
- ✅ Swagger UI tích hợp sẵn

## 🚀 Cài Đặt

### Yêu Cầu

- Python 3.8+
- Pip package manager
- Tài khoản developer trên các nền tảng bạn muốn sử dụng

### Bước 1: Clone Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### Bước 2: Tạo Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

### Bước 3: Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Cấu Hình

### Bước 1: Tạo File .env

```bash
cp .env.example .env
```

### Bước 2: Điền Thông Tin API Keys

Mở file `.env` và điền các API keys của bạn:

```env
# Facebook
FACEBOOK_ACCESS_TOKEN=your_token_here
FACEBOOK_PAGE_ID=your_page_id_here

# Instagram
INSTAGRAM_ACCESS_TOKEN=your_token_here
INSTAGRAM_ACCOUNT_ID=your_account_id_here

# TikTok
TIKTOK_ACCESS_TOKEN=your_token_here
TIKTOK_CLIENT_KEY=your_client_key_here
TIKTOK_CLIENT_SECRET=your_client_secret_here

# X (Twitter)
X_BEARER_TOKEN=your_bearer_token_here
# hoặc
X_ACCESS_TOKEN=your_access_token_here
X_ACCESS_TOKEN_SECRET=your_secret_here

# Threads
THREADS_ACCESS_TOKEN=your_token_here
THREADS_USER_ID=your_user_id_here

# YouTube
YOUTUBE_ACCESS_TOKEN=your_token_here
YOUTUBE_API_KEY=your_api_key_here
```

### Cách Lấy API Keys

#### Facebook
1. Truy cập [Facebook Developers](https://developers.facebook.com/)
2. Tạo app mới
3. Thêm Facebook Login và Facebook Graph API
4. Lấy Access Token từ Graph API Explorer

#### Instagram
1. Phải có Instagram Business/Creator Account
2. Kết nối với Facebook Page
3. Sử dụng Facebook Graph API để lấy Instagram Account ID
4. Access Token giống Facebook

#### TikTok
1. Đăng ký tại [TikTok Developers](https://developers.tiktok.com/)
2. Tạo app mới
3. Enable "Content Posting API"
4. Lấy Client Key và Client Secret

#### X (Twitter)
1. Truy cập [Twitter Developer Portal](https://developer.twitter.com/)
2. Tạo project và app
3. Lấy API Keys và Bearer Token
4. Enable OAuth 1.0a hoặc OAuth 2.0

#### Threads
1. Threads API hiện được tích hợp với Facebook
2. Truy cập [Threads API Documentation](https://developers.facebook.com/docs/threads)
3. Sử dụng Access Token từ Facebook
4. Lấy Threads User ID

#### YouTube
1. Truy cập [Google Cloud Console](https://console.cloud.google.com/)
2. Tạo project mới
3. Enable YouTube Data API v3
4. Tạo OAuth 2.0 credentials
5. Lấy Access Token qua OAuth flow

## 🎯 Sử Dụng

### Khởi Động Server

```bash
python main.py
```

Hoặc với uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server sẽ chạy tại: `http://localhost:8000`

### Truy Cập API Documentation

Mở trình duyệt và truy cập:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📡 API Endpoints

### 1. Root Endpoint

```http
GET /
```

Trả về thông tin API và danh sách endpoints.

### 2. Health Check

```http
GET /health
```

Kiểm tra trạng thái API và các nền tảng có sẵn.

### 3. Get Supported Platforms

```http
GET /api/platforms
```

Lấy danh sách các nền tảng được hỗ trợ và tính năng của chúng.

### 4. Post to Multiple Platforms

```http
POST /api/post
Content-Type: application/json

{
  "text": "Nội dung bài đăng của bạn",
  "platforms": ["facebook", "instagram", "tiktok"],
  "media_urls": ["https://example.com/image.jpg"],
  "schedule_time": "2024-01-01T12:00:00Z"
}
```

**Response:**

```json
[
  {
    "success": true,
    "platform": "facebook",
    "post_id": "123456789",
    "message": "Successfully posted to facebook",
    "error": null
  },
  {
    "success": true,
    "platform": "instagram",
    "post_id": "987654321",
    "message": "Successfully posted to instagram",
    "error": null
  }
]
```

### 5. Post to Single Platform

```http
POST /api/post/{platform}
Content-Type: multipart/form-data

text=Your post content
media_urls=https://example.com/image.jpg
```

Platforms: `facebook`, `instagram`, `tiktok`, `x`, `threads`, `youtube`

### 6. Upload Media

```http
POST /api/upload
Content-Type: multipart/form-data

file=@/path/to/your/image.jpg
```

**Response:**

```json
{
  "success": true,
  "filename": "image.jpg",
  "file_path": "uploads/20240101_120000_image.jpg",
  "file_size": 1024000,
  "message": "File uploaded successfully"
}
```

### 7. Authenticate Platform

```http
POST /api/auth/{platform}
Content-Type: application/json

{
  "platform": "facebook",
  "access_token": "your_access_token",
  "additional_params": {
    "page_id": "your_page_id"
  }
}
```

## 💡 Ví Dụ

### Python Example

```python
import requests

# API endpoint
url = "http://localhost:8000/api/post"

# Post data
data = {
    "text": "Hello from Multi-Platform API! 🚀",
    "platforms": ["facebook", "x", "threads"],
    "media_urls": ["https://example.com/image.jpg"]
}

# Make request
response = requests.post(url, json=data)
results = response.json()

# Check results
for result in results:
    if result["success"]:
        print(f"✅ Posted to {result['platform']}: {result['post_id']}")
    else:
        print(f"❌ Failed to post to {result['platform']}: {result['error']}")
```

### cURL Example

```bash
# Post to multiple platforms
curl -X POST "http://localhost:8000/api/post" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello World!",
    "platforms": ["facebook", "instagram"],
    "media_urls": ["https://example.com/photo.jpg"]
  }'

# Upload a file
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@/path/to/image.jpg"
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

async function postToSocialMedia() {
    const response = await axios.post('http://localhost:8000/api/post', {
        text: 'Posting from JavaScript! 🎉',
        platforms: ['facebook', 'x'],
        media_urls: ['https://example.com/image.jpg']
    });
    
    console.log(response.data);
}

postToSocialMedia();
```

## 📱 Platform-Specific Notes

### Facebook
- Hỗ trợ text, images (đơn/nhiều), videos
- Có thể hẹn giờ đăng bài
- Cần Page Access Token để đăng lên Page
- Character limit: 63,206 characters

### Instagram
- Yêu cầu Business/Creator account
- Media URLs phải publicly accessible
- Hỗ trợ 1 ảnh hoặc 1 video per post
- Caption limit: 2,200 characters
- Có thể tạo Stories và Reels

### TikTok
- Chỉ hỗ trợ video
- Video phải đáp ứng yêu cầu: độ phân giải, thời lượng, format
- Có thể hẹn giờ đăng
- Description limit: 2,200 characters

### X (Twitter)
- Standard: 280 characters
- X Premium: 4,000 characters
- Hỗ trợ tối đa 4 ảnh hoặc 1 video
- Không hỗ trợ scheduled posts qua API v2

### Threads
- Text limit: 500 characters
- Hỗ trợ 1 ảnh hoặc 1 video per post
- Có thể tạo threads (chuỗi bài đăng)
- Scheduled posts chưa được hỗ trợ

### YouTube
- Chỉ hỗ trợ video
- Title limit: 100 characters
- Description limit: 5,000 characters
- Có thể hẹn giờ publish
- Hỗ trợ privacy settings (public, unlisted, private)

## 🔒 Security Best Practices

1. **Không commit file .env** vào git
2. **Sử dụng environment variables** cho production
3. **Rotate access tokens** định kỳ
4. **Implement rate limiting** để tránh spam
5. **Validate và sanitize** user input
6. **Use HTTPS** trong production

## 🐛 Troubleshooting

### Common Issues

1. **"Authentication failed"**
   - Kiểm tra access token có còn hiệu lực
   - Verify API keys đã được cấu hình đúng
   - Check permissions/scopes của token

2. **"Media upload failed"**
   - Verify media URL publicly accessible
   - Check file format và size requirements
   - Ensure media meets platform requirements

3. **"Rate limit exceeded"**
   - Implement exponential backoff
   - Reduce request frequency
   - Consider upgrading API tier

## 📞 Support

Nếu bạn gặp vấn đề, vui lòng:
1. Kiểm tra documentation
2. Review error messages
3. Check platform-specific requirements
4. Open an issue on GitHub

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Credits

Created with ❤️ for the social media automation community.
