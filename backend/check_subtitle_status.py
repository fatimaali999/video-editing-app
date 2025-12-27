from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017'))
db = client.snipx

print("=" * 60)
print("CHECKING VIDEOS WITHOUT SUBTITLES")
print("=" * 60)

# Find videos that are uploaded but not processed
uploaded_videos = list(db.videos.find({'status': 'uploaded'}).sort('_id', -1).limit(5))

if uploaded_videos:
    print(f"\n⏳ Found {len(uploaded_videos)} uploaded videos waiting for processing:\n")
    
    for i, video in enumerate(uploaded_videos, 1):
        print(f"Video {i}:")
        print(f"  ID: {video['_id']}")
        print(f"  Filename: {video.get('filename', 'N/A')}")
        print(f"  Status: {video.get('status')}")
        print(f"  Target Language: {video.get('target_language', 'N/A')}")
        print(f"  Video Path: {video.get('video_path', 'N/A')}")
        print()
else:
    print("\n✅ No videos in 'uploaded' status")

# Check recently completed/failed videos
print("\n" + "=" * 60)
print("RECENT COMPLETED VIDEOS:")
print("=" * 60)

completed = list(db.videos.find({'status': 'completed'}).sort('_id', -1).limit(3))
for i, video in enumerate(completed, 1):
    print(f"\n✅ Video {i}:")
    print(f"  ID: {video['_id']}")
    print(f"  Filename: {video.get('filename', 'N/A')}")
    print(f"  Subtitles: {video.get('subtitle_languages', [])}")
    print(f"  SRT Path: {video.get('srt_path', 'N/A')}")

# Check failed videos
print("\n" + "=" * 60)
print("FAILED VIDEOS:")
print("=" * 60)

failed = list(db.videos.find({'status': 'failed'}).sort('_id', -1).limit(3))
if failed:
    for i, video in enumerate(failed, 1):
        print(f"\n❌ Video {i}:")
        print(f"  ID: {video['_id']}")
        print(f"  Filename: {video.get('filename', 'N/A')}")
        print(f"  Error: {video.get('error_message', 'No error message')}")
else:
    print("\nNo failed videos")

client.close()

print("\n" + "=" * 60)
print("SOLUTION:")
print("=" * 60)
print("\n1. Videos in 'uploaded' status need to be processed")
print("2. Check if backend is running: python app.py")
print("3. Videos should auto-process when uploaded")
print("4. If stuck, you may need to trigger processing manually")
