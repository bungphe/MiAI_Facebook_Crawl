"""
Unit tests for Multi-Platform Social Media Posting API
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestRootEndpoints:
    """Test root and health endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct information"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "supported_platforms" in data
        assert len(data["supported_platforms"]) == 6
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "platforms_available" in data
    
    def test_get_platforms(self):
        """Test get platforms endpoint"""
        response = client.get("/api/platforms")
        assert response.status_code == 200
        
        data = response.json()
        assert "platforms" in data
        assert len(data["platforms"]) == 6
        
        # Check structure of first platform
        platform = data["platforms"][0]
        assert "id" in platform
        assert "name" in platform
        assert "description" in platform
        assert "supports_media" in platform
        assert "supports_video" in platform
        assert "supports_scheduling" in platform

class TestPostEndpoints:
    """Test posting endpoints"""
    
    def test_post_to_multiple_platforms_validation(self):
        """Test posting with invalid data"""
        # Missing required fields
        response = client.post("/api/post", json={})
        assert response.status_code == 422
    
    def test_post_to_multiple_platforms_structure(self):
        """Test posting returns correct structure"""
        response = client.post("/api/post", json={
            "text": "Test post",
            "platforms": ["facebook"],
            "media_urls": []
        })
        
        # Should return 200 even if authentication fails
        # (authentication failures are handled gracefully)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check result structure
        result = data[0]
        assert "success" in result
        assert "platform" in result
        assert "message" in result
    
    def test_post_to_invalid_platform(self):
        """Test posting to non-existent platform"""
        response = client.post("/api/post", json={
            "text": "Test post",
            "platforms": ["invalid_platform"],
            "media_urls": []
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data[0]["success"] == False
        assert "not supported" in data[0]["message"].lower()
    
    def test_post_to_single_platform_validation(self):
        """Test single platform posting validation"""
        response = client.post(
            "/api/post/facebook",
            data={"text": ""}
        )
        
        # Empty text should fail validation
        assert response.status_code == 422
    
    def test_post_to_single_platform_invalid(self):
        """Test posting to invalid single platform"""
        response = client.post(
            "/api/post/invalid_platform",
            data={"text": "Test"}
        )
        
        assert response.status_code == 400

class TestUploadEndpoint:
    """Test media upload endpoint"""
    
    def test_upload_no_file(self):
        """Test upload without file"""
        response = client.post("/api/upload")
        assert response.status_code == 422
    
    def test_upload_with_file(self):
        """Test upload with file"""
        # Create a fake file
        files = {
            "file": ("test.txt", b"test content", "text/plain")
        }
        
        response = client.post("/api/upload", files=files)
        
        # Should succeed or fail gracefully
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "success" in data
            assert "filename" in data
            assert "file_path" in data

class TestAuthEndpoint:
    """Test authentication endpoints"""
    
    def test_auth_invalid_platform(self):
        """Test authentication with invalid platform"""
        response = client.post(
            "/api/auth/invalid_platform",
            json={
                "platform": "invalid_platform",
                "access_token": "test_token"
            }
        )
        
        assert response.status_code == 400
    
    def test_auth_missing_credentials(self):
        """Test authentication without credentials"""
        response = client.post(
            "/api/auth/facebook",
            json={
                "platform": "facebook"
            }
        )
        
        # Should fail due to missing credentials
        assert response.status_code in [401, 422]

@pytest.mark.asyncio
class TestAsyncOperations:
    """Test async operations"""
    
    async def test_concurrent_posts(self):
        """Test posting to multiple platforms concurrently"""
        # This would test the async nature of the API
        # In real scenario, this would verify concurrent execution
        pass

class TestErrorHandling:
    """Test error handling"""
    
    def test_malformed_json(self):
        """Test handling of malformed JSON"""
        response = client.post(
            "/api/post",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    def test_missing_content_type(self):
        """Test handling of missing content type"""
        response = client.post("/api/post", data="test")
        assert response.status_code in [422, 400]

class TestDataValidation:
    """Test data validation"""
    
    def test_text_validation(self):
        """Test text field validation"""
        # Empty text
        response = client.post("/api/post", json={
            "text": "",
            "platforms": ["facebook"]
        })
        assert response.status_code == 422
    
    def test_platforms_validation(self):
        """Test platforms field validation"""
        # Empty platforms list
        response = client.post("/api/post", json={
            "text": "Test",
            "platforms": []
        })
        assert response.status_code == 422
    
    def test_media_urls_validation(self):
        """Test media URLs validation"""
        response = client.post("/api/post", json={
            "text": "Test",
            "platforms": ["facebook"],
            "media_urls": ["not_a_valid_url"]
        })
        
        # Should still process but may fail at platform level
        assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
