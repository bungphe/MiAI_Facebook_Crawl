"""
Example: Async posting with aiohttp for better performance
"""

import asyncio
import aiohttp
import json
from typing import List, Dict

BASE_URL = "http://localhost:8000"

async def post_to_platform(session: aiohttp.ClientSession, platform: str, text: str, media_url: str = None) -> Dict:
    """Post to a single platform asynchronously"""
    url = f"{BASE_URL}/api/post/{platform}"
    
    data = {
        "text": text
    }
    
    if media_url:
        data["media_urls"] = media_url
    
    try:
        async with session.post(url, data=data) as response:
            result = await response.json()
            return result
    except Exception as e:
        return {
            "success": False,
            "platform": platform,
            "error": str(e)
        }

async def batch_post_multiple_platforms():
    """Post to multiple platforms concurrently"""
    print("🚀 Posting to multiple platforms concurrently...")
    
    platforms = ["facebook", "instagram", "x", "threads"]
    text = "Hello from async Python! 🐍⚡"
    media_url = "https://picsum.photos/800/600"
    
    async with aiohttp.ClientSession() as session:
        # Create tasks for all platforms
        tasks = [
            post_to_platform(session, platform, text, media_url)
            for platform in platforms
        ]
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks)
        
        # Print results
        print("\n✅ Results:")
        for result in results:
            if result["success"]:
                print(f"  ✓ {result['platform']}: Success (ID: {result.get('post_id')})")
            else:
                print(f"  ✗ {result['platform']}: Failed - {result.get('error')}")

async def sequential_posts_with_different_content():
    """Post different content to different platforms"""
    print("\n📝 Posting different content to each platform...")
    
    posts = [
        {
            "platform": "facebook",
            "text": "Check out our Facebook page! 👍",
            "media": "https://picsum.photos/1200/630"
        },
        {
            "platform": "instagram",
            "text": "Beautiful photo for Instagram 📸 #photography #beautiful",
            "media": "https://picsum.photos/1080/1080"
        },
        {
            "platform": "x",
            "text": "Quick update on X! 🐦",
            "media": "https://picsum.photos/1200/675"
        },
        {
            "platform": "threads",
            "text": "Threading together great content! 🧵",
            "media": "https://picsum.photos/800/800"
        }
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            post_to_platform(session, post["platform"], post["text"], post["media"])
            for post in posts
        ]
        
        results = await asyncio.gather(*tasks)
        
        print("\n✅ Results:")
        for i, result in enumerate(results):
            platform = posts[i]["platform"]
            if result["success"]:
                print(f"  ✓ {platform}: Posted successfully")
            else:
                print(f"  ✗ {platform}: {result.get('error')}")

async def bulk_upload_and_post():
    """Upload multiple files and post them"""
    print("\n📤 Bulk upload and post example...")
    
    # Simulate multiple posts
    post_data_list = [
        {
            "text": "Post #1 - Nature 🌿",
            "platforms": ["facebook", "instagram"],
            "media_urls": ["https://picsum.photos/id/1015/800/600"]
        },
        {
            "text": "Post #2 - Technology 💻",
            "platforms": ["x", "threads"],
            "media_urls": ["https://picsum.photos/id/0/800/600"]
        },
        {
            "text": "Post #3 - Architecture 🏛️",
            "platforms": ["facebook", "threads"],
            "media_urls": ["https://picsum.photos/id/1080/800/600"]
        }
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        for post_data in post_data_list:
            url = f"{BASE_URL}/api/post"
            task = session.post(url, json=post_data)
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        print("\n✅ Bulk post results:")
        for i, response in enumerate(responses):
            results = await response.json()
            print(f"\n  Post #{i+1}:")
            for result in results:
                status = "✓" if result["success"] else "✗"
                print(f"    {status} {result['platform']}")

async def monitor_post_status():
    """Monitor API health continuously"""
    print("\n🔍 Monitoring API status...")
    
    async with aiohttp.ClientSession() as session:
        for i in range(5):
            try:
                async with session.get(f"{BASE_URL}/health") as response:
                    health = await response.json()
                    print(f"  Check {i+1}: Status = {health['status']}, Platforms = {len(health['platforms_available'])}")
                
                await asyncio.sleep(2)  # Wait 2 seconds between checks
            
            except Exception as e:
                print(f"  Check {i+1}: Error - {e}")
                await asyncio.sleep(2)

async def rate_limited_posting():
    """Post with rate limiting to avoid API limits"""
    print("\n⏱️ Rate-limited posting example...")
    
    posts = [f"Post #{i}: Testing rate limiting" for i in range(1, 11)]
    
    async with aiohttp.ClientSession() as session:
        for i, text in enumerate(posts, 1):
            url = f"{BASE_URL}/api/post/facebook"
            
            try:
                async with session.post(url, data={"text": text}) as response:
                    result = await response.json()
                    
                    if result["success"]:
                        print(f"  ✓ Posted #{i}")
                    else:
                        print(f"  ✗ Failed #{i}: {result.get('error')}")
                
                # Wait 1 second between posts to respect rate limits
                await asyncio.sleep(1)
            
            except Exception as e:
                print(f"  ✗ Error #{i}: {e}")

async def error_handling_example():
    """Demonstrate error handling"""
    print("\n🛡️ Error handling example...")
    
    # Try posting to an invalid platform
    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}/api/post"
        
        # Invalid platform
        data = {
            "text": "Test post",
            "platforms": ["invalid_platform", "facebook"]
        }
        
        try:
            async with session.post(url, json=data) as response:
                results = await response.json()
                
                print("\n  Results:")
                for result in results:
                    if result["success"]:
                        print(f"    ✓ {result['platform']}: Success")
                    else:
                        print(f"    ✗ {result['platform']}: {result['error']}")
        
        except Exception as e:
            print(f"  Error: {e}")

async def main():
    """Run all examples"""
    print("=" * 60)
    print("Multi-Platform API - Async Examples")
    print("=" * 60)
    
    # Run examples (uncomment to execute)
    # await batch_post_multiple_platforms()
    # await sequential_posts_with_different_content()
    # await bulk_upload_and_post()
    # await monitor_post_status()
    # await rate_limited_posting()
    # await error_handling_example()
    
    print("\n" + "=" * 60)
    print("To run specific examples, uncomment the await calls in main()")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
