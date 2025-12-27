from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017'))
db = client.snipx

print("=" * 60)
print("VIDEO PROCESSING STATUS")
print("=" * 60)

# Find all videos
videos = db.videos.find().sort('created_at', -1).limit(10)

video_count = 0
for video in videos:
    video_count += 1
    print(f"\n📹 Video {video_count}:")
    print(f"   Title: {video.get('title', 'Untitled')}")
    print(f"   Status: {video.get('status', 'unknown')}")
    print(f"   Created: {video.get('created_at', 'unknown')}")
    print(f"   User: {video.get('user_id', 'unknown')}")
    
    # Check for subtitles
    subtitle_langs = video.get('subtitle_languages', [])
    if subtitle_langs:
        print(f"   Subtitles: {', '.join(subtitle_langs)}")
    else:
        print(f"   Subtitles: None")

if video_count == 0:
    print("\n❌ No videos found in database")
else:
    print(f"\n✅ Found {video_count} video(s) (showing last 10)")
    
    # Count by status
    print("\n" + "=" * 60)
    print("STATUS SUMMARY:")
    print("=" * 60)
    
    processing = db.videos.count_documents({'status': 'processing'})
    completed = db.videos.count_documents({'status': 'completed'})
    failed = db.videos.count_documents({'status': 'failed'})
    
    print(f"⏳ Processing: {processing}")
    print(f"✅ Completed: {completed}")
    print(f"❌ Failed: {failed}")

client.close()
