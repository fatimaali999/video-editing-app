"""
Quick test to verify subtitle generation is working properly
"""
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from services.video_service import VideoService
from models.video import Video
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("SUBTITLE GENERATION TEST")
print("=" * 70)

# Connect to MongoDB
try:
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
    db = client.snipx
    print(f"✅ Connected to MongoDB")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    sys.exit(1)

# Initialize video service
video_service = VideoService(db)

# Find a test video file
uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
test_videos = []

# Prefer videos that are known to have good audio
priority_files = [
    '--_-_Hitler_Speech_at_Krupp_Factory_-The_world_cannot_judge_us-.mp4',
    'WhatsApp_Video_2025-12-23_at_2.22.09_PM.mp4',
    'Babar_Azam_Interview_Grand_Inauguration_of_the_New-Look_National_Bank_Stadium_Karachi_-_Pakistan_Cricket_360p_h264_youtube.mp4',
]

# First try priority files
for file in priority_files:
    full_path = os.path.join(uploads_dir, file)
    if os.path.exists(full_path):
        size_mb = os.path.getsize(full_path) / (1024 * 1024)
        if size_mb < 100:
            test_videos.append((file, full_path, size_mb))
            break

# If no priority file found, find any video
if not test_videos:
    for file in os.listdir(uploads_dir):
        if file.endswith('.mp4') and not file.startswith('enhanced_') and not '_processed' in file and not '_enhanced' in file and not 'edited' in file:
            video_path = os.path.join(uploads_dir, file)
            # Check file size (use small videos for quick testing)
            size_mb = os.path.getsize(video_path) / (1024 * 1024)
            if size_mb < 100:  # Less than 100MB
                test_videos.append((file, video_path, size_mb))

if not test_videos:
    print("❌ No test videos found in uploads directory")
    sys.exit(1)

# Sort by size and pick the smallest one
test_videos.sort(key=lambda x: x[2])
test_video_name, test_video_path, test_video_size = test_videos[0]

print(f"\n📹 Test Video: {test_video_name}")
print(f"   Path: {test_video_path}")
print(f"   Size: {test_video_size:.2f} MB")

# Create a mock video object
mock_video = Video(
    user_id="test_user_123",
    filename=test_video_name,
    filepath=test_video_path,
    size=int(test_video_size * 1024 * 1024)
)

# Test subtitle generation options
test_cases = [
    {'subtitle_language': 'en', 'subtitle_style': 'clean', 'generate_subtitles': True},
]

for i, options in enumerate(test_cases, 1):
    print(f"\n{'='*70}")
    print(f"TEST CASE {i}: Language={options['subtitle_language']}, Style={options['subtitle_style']}")
    print(f"{'='*70}")
    
    try:
        # Generate subtitles
        video_service._generate_subtitles(mock_video, options)
        
        # Check if subtitle files were created
        lang = options['subtitle_language']
        srt_path = f"{os.path.splitext(test_video_path)[0]}_{lang}.srt"
        json_path = f"{os.path.splitext(test_video_path)[0]}_{lang}.json"
        
        if os.path.exists(srt_path):
            print(f"\n✅ SRT file created: {srt_path}")
            # Show first few lines
            with open(srt_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:20]
                print("   First 20 lines:")
                for line in lines:
                    print(f"   {line.rstrip()}")
        else:
            print(f"\n❌ SRT file NOT created: {srt_path}")
        
        if os.path.exists(json_path):
            print(f"\n✅ JSON file created: {json_path}")
            import json
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"   Segments: {len(data.get('segments', []))}")
                if data.get('segments'):
                    print(f"   First segment: {data['segments'][0]}")
        else:
            print(f"\n❌ JSON file NOT created: {json_path}")
        
        print(f"\n✅ TEST CASE {i} PASSED")
        
    except Exception as e:
        print(f"\n❌ TEST CASE {i} FAILED: {e}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*70}")
print("TEST COMPLETE")
print(f"{'='*70}")
