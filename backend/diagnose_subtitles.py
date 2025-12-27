"""
Test if Whisper is actually working and can transcribe audio
"""
import os
import sys

print("=" * 60)
print("SUBTITLE GENERATION DIAGNOSIS")
print("=" * 60)

# Test 1: Check if Whisper is installed
print("\n[TEST 1] Checking Whisper installation...")
try:
    import whisper
    print("✅ Whisper is installed")
    print(f"   Whisper version: {whisper.__version__ if hasattr(whisper, '__version__') else 'Unknown'}")
except ImportError as e:
    print(f"❌ Whisper NOT installed: {e}")
    print("   Install with: pip install openai-whisper")
    sys.exit(1)

# Test 2: Check FFmpeg availability for Whisper
print("\n[TEST 2] Checking FFmpeg for Whisper...")
try:
    # Check if FFmpeg is configured
    ffmpeg_path = whisper.audio.FFMPEG_PATH if hasattr(whisper.audio, 'FFMPEG_PATH') else None
    if ffmpeg_path:
        print(f"✅ FFmpeg path set: {ffmpeg_path}")
        if os.path.exists(str(ffmpeg_path)):
            print(f"   ✅ FFmpeg exists at specified path")
        else:
            print(f"   ⚠️ Warning: FFmpeg path doesn't exist")
    else:
        print("⚠️ No FFmpeg path set for Whisper")
        
    # Try to import the audio loading function
    from whisper.audio import load_audio
    print("✅ Whisper audio loading functions available")
except Exception as e:
    print(f"⚠️ Issue with Whisper audio: {e}")

# Test 3: Check if librosa is available (alternative audio loader)
print("\n[TEST 3] Checking librosa (alternative audio loader)...")
try:
    import librosa
    print(f"✅ Librosa is installed (version {librosa.__version__})")
except ImportError:
    print("❌ Librosa NOT installed")
    print("   Install with: pip install librosa")

# Test 4: Try to load a small Whisper model
print("\n[TEST 4] Testing Whisper model loading...")
try:
    print("   Loading 'tiny' model (smallest, fastest)...")
    model = whisper.load_model("tiny")
    print("✅ Successfully loaded Whisper 'tiny' model")
    print(f"   Model is multilingual: {model.is_multilingual}")
except Exception as e:
    print(f"❌ Failed to load Whisper model: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Check recent video file for actual transcription
print("\n[TEST 5] Testing transcription on a real video file...")
try:
    # Find a recent video file
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        video_files = [f for f in os.listdir(uploads_dir) if f.endswith('.mp4')]
        if video_files:
            test_video = os.path.join(uploads_dir, video_files[0])
            print(f"   Found test video: {video_files[0]}")
            
            # Try to transcribe just 5 seconds
            print("   Attempting to transcribe first 5 seconds...")
            
            # Load audio with librosa (more reliable than FFmpeg)
            import librosa
            audio_data, sr = librosa.load(test_video, sr=16000, duration=5, mono=True)
            print(f"   ✅ Audio loaded: {len(audio_data)/sr:.2f} seconds")
            
            # Try transcription
            result = model.transcribe(audio_data, language='en', fp16=False)
            text = result.get('text', '').strip()
            
            if text and len(text) > 0:
                print(f"   ✅ TRANSCRIPTION SUCCESSFUL!")
                print(f"   Result: '{text[:100]}...'")
                print(f"   Detected language: {result.get('language', 'unknown')}")
            else:
                print(f"   ⚠️ Transcription returned empty text")
        else:
            print("   ⚠️ No video files found in uploads directory")
    else:
        print("   ⚠️ Uploads directory not found")
        
except Exception as e:
    print(f"   ❌ Transcription test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("DIAGNOSIS COMPLETE")
print("=" * 60)
print("\nNext steps:")
print("1. If Whisper is working: Check hallucination detection in video_service.py")
print("2. If FFmpeg issues: Ensure FFmpeg path is correctly set")
print("3. If transcription fails: Check audio quality and file format")
