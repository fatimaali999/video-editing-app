from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017'))
db = client.snipx

print("=" * 60)
print("CHECKING VIDEO PROCESSING STATUS")
print("=" * 60)

# Check if any videos are currently processing
processing = list(db.videos.find({'status': 'processing'}))
print(f"\n⏳ Videos currently processing: {len(processing)}")
for v in processing:
    print(f"  - {v.get('filename')}")
    print(f"    Started: {v.get('process_start_time')}")
    print(f"    Options: {v.get('processing_options')}")
    print()

# Check uploaded videos (waiting to be processed)
uploaded = list(db.videos.find({'status': 'uploaded'}).limit(5))
print(f"\n📤 Videos uploaded but not processed: {len(uploaded)}")
for v in uploaded:
    print(f"  - {v.get('filename')}")
    print(f"    Uploaded: {v.get('upload_time')}")
    print()

# Check completed videos with subtitles
completed_with_subs = list(db.videos.find({
    'status': 'completed',
    'outputs.subtitles': {'$exists': True}
}).sort('_id', -1).limit(3))

print(f"\n✅ Recently completed videos WITH subtitles: {len(completed_with_subs)}")
for v in completed_with_subs:
    subs = v.get('outputs', {}).get('subtitles', {})
    print(f"  - {v.get('filename')}")
    print(f"    Language: {subs.get('language', 'N/A')}")
    print(f"    SRT: {subs.get('srt', 'N/A')}")
    print()

# Check completed videos without subtitles
completed_no_subs = list(db.videos.find({
    'status': 'completed',
    'outputs.subtitles': {'$exists': False}
}).sort('_id', -1).limit(3))

print(f"\n⚠️ Recently completed videos WITHOUT subtitles: {len(completed_no_subs)}")
for v in completed_no_subs:
    print(f"  - {v.get('filename')}")
    print(f"    Processing options: {v.get('processing_options')}")
    print()

print("=" * 60)
print("SUMMARY:")
print("=" * 60)

total_videos = db.videos.count_documents({})
total_with_subs = db.videos.count_documents({'outputs.subtitles': {'$exists': True}})
total_completed = db.videos.count_documents({'status': 'completed'})
total_failed = db.videos.count_documents({'status': 'failed'})

print(f"Total videos: {total_videos}")
print(f"Completed: {total_completed}")
print(f"Failed: {total_failed}")
print(f"With subtitles: {total_with_subs}")
print(f"Completion rate: {(total_completed/total_videos*100) if total_videos > 0 else 0:.1f}%")
print(f"Subtitle rate: {(total_with_subs/total_videos*100) if total_videos > 0 else 0:.1f}%")
