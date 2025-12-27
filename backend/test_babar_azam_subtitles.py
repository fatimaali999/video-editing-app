"""
Test subtitle generation specifically for the Babar Azam video
"""
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from services.video_service import VideoService
from models.video import Video
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("BABAR AZAM VIDEO - SUBTITLE REGENERATION TEST")
print("=" * 70)

# Connect to MongoDB
try:
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
    db = client.snipx
    print(f"Connected to MongoDB")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    sys.exit(1)

# Initialize video service
video_service = VideoService(db)

# Find the Babar Azam video
uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
video_file = "Babar_Azam_Interview_Grand_Inauguration_of_the_New-Look_National_Bank_Stadium_Karachi_-_Pakistan_Cricket_360p_h264_youtube.mp4"
video_path = os.path.join(uploads_dir, video_file)

if not os.path.exists(video_path):
    print(f"Video file not found: {video_path}")
    sys.exit(1)

size_mb = os.path.getsize(video_path) / (1024 * 1024)

print(f"\nVideo: {video_file}")
print(f"   Path: {video_path}")
print(f"   Size: {size_mb:.2f} MB")

# Create a mock video object
mock_video = Video(
    user_id="test_user_123",
    filename=video_file,
    filepath=video_path,
    size=int(size_mb * 1024 * 1024)
)

# Delete old subtitle files if they exist
old_en_srt = f"{os.path.splitext(video_path)[0]}_en.srt"
old_en_json = f"{os.path.splitext(video_path)[0]}_en.json"

if os.path.exists(old_en_srt):
    os.remove(old_en_srt)
    print(f"Removed old subtitle file: {old_en_srt}")
if os.path.exists(old_en_json):
    os.remove(old_en_json)
    print(f"Removed old subtitle file: {old_en_json}")

print("\n" + "="*70)
print("GENERATING NEW ENGLISH SUBTITLES")
print("="*70)

# Generate English subtitles with improved system (force transcription)
options = {
    'subtitle_language': 'en',
    'subtitle_style': 'clean',
    'generate_subtitles': True,
    'force_transcription': True  # Skip silence check for testing
}

try:
    # Generate subtitles
    video_service._generate_subtitles(mock_video, options)
    
    # Check if subtitle files were created
    srt_path = old_en_srt
    json_path = old_en_json
    
    if os.path.exists(srt_path):
        print(f"\nNEW SRT file created: {srt_path}")
        # Show content
        with open(srt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"\nSubtitle Content (first 50 lines):")
            print("="*70)
            for i, line in enumerate(lines[:50], 1):
                print(f"{line.rstrip()}")
            if len(lines) > 50:
                print(f"\n... and {len(lines) - 50} more lines")
    else:
        print(f"\nSRT file NOT created: {srt_path}")
    
    if os.path.exists(json_path):
        print(f"\nJSON file created: {json_path}")
        import json
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"   Total segments: {len(data.get('segments', []))}")
            if data.get('segments'):
                print(f"\nFirst 3 segments:")
                for seg in data['segments'][:3]:
                    print(f"   [{seg['start']:.2f}s - {seg['end']:.2f}s]: {seg['text']}")
    else:
        print(f"\nJSON file NOT created: {json_path}")
    
    print(f"\nREGENERATION COMPLETE")
    
except Exception as e:
    print(f"\nREGENERATION FAILED: {e}")
    import traceback
    traceback.print_exc()

print(f"\n{'='*70}")
print("TEST COMPLETE")
print(f"{'='*70}")
