"""
Test subtitle generation fix
"""
import os
import sys

# Import video_service to trigger FFmpeg configuration
print("Loading video_service to configure FFmpeg...")
from services import video_service

print("=" * 60)
print("TESTING SUBTITLE GENERATION FIX")
print("=" * 60)

# Test 1: Check FFmpeg configuration
print("\n[TEST 1] Checking FFmpeg environment variables...")
ffmpeg_vars = ['PATH', 'IMAGEIO_FFMPEG_EXE', 'AUDIOREAD_FFMPEG']
for var in ffmpeg_vars:
    value = os.environ.get(var, 'NOT SET')
    if var == 'PATH':
        # Check if ffmpeg is in PATH
        has_ffmpeg = any('ffmpeg' in p.lower() for p in value.split(os.pathsep))
        print(f"  {var}: {'✅ Contains ffmpeg' if has_ffmpeg else '❌ No ffmpeg in PATH'}")
    else:
        print(f"  {var}: {'✅ ' + value if value != 'NOT SET' else '❌ NOT SET'}")

# Test 2: Import Whisper and check configuration
print("\n[TEST 2] Checking Whisper configuration...")
try:
    import whisper
    print("✅ Whisper is installed")
    
    # Check if FFmpeg path is set for Whisper
    if hasattr(whisper.audio, 'FFMPEG_PATH'):
        ffmpeg_path = whisper.audio.FFMPEG_PATH
        print(f"✅ Whisper FFmpeg path: {ffmpeg_path}")
        if os.path.exists(str(ffmpeg_path)):
            print(f"   ✅ FFmpeg executable exists")
        else:
            print(f"   ❌ FFmpeg executable NOT found at path")
    else:
        print("⚠️ Whisper FFmpeg path not set")
    
    # Test Whisper's audio loading function
    print("\n[TEST 3] Testing Whisper's audio loading...")
    from whisper.audio import load_audio
    print("✅ Whisper load_audio function available")
    
    # Find a test video
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        video_files = [f for f in os.listdir(uploads_dir) if f.endswith('.mp4')]
        if video_files:
            test_video = os.path.join(uploads_dir, video_files[0])
            print(f"   Found test video: {video_files[0]}")
            
            # Extract audio first with moviepy (like our code does)
            print("   Extracting audio with moviepy...")
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(test_video)
            if clip.audio:
                test_audio = "test_audio.wav"
                clip.audio.write_audiofile(test_audio, verbose=False, logger=None)
                clip.close()
                print(f"   ✅ Audio extracted to {test_audio}")
                
                # Now test Whisper's audio loading
                print("   Testing Whisper's load_audio...")
                try:
                    audio_data = load_audio(test_audio)
                    duration = len(audio_data) / 16000
                    print(f"   ✅ Whisper loaded audio successfully!")
                    print(f"   Duration: {duration:.2f} seconds")
                    print(f"   Samples: {len(audio_data)}")
                    
                    # Test transcription with tiny model
                    print("\n[TEST 4] Testing actual transcription...")
                    model = whisper.load_model("tiny")
                    result = model.transcribe(audio_data, language='en', fp16=False)
                    text = result.get('text', '').strip()
                    
                    if text and len(text) > 0:
                        print(f"   ✅ TRANSCRIPTION SUCCESSFUL!")
                        print(f"   Result: '{text[:150]}...'")
                        print(f"   Segments: {len(result.get('segments', []))}")
                    else:
                        print(f"   ⚠️ Transcription returned empty text")
                    
                    # Cleanup
                    if os.path.exists(test_audio):
                        os.remove(test_audio)
                    
                except Exception as e:
                    print(f"   ❌ Whisper audio loading FAILED: {e}")
                    import traceback
                    traceback.print_exc()
                    if os.path.exists(test_audio):
                        os.remove(test_audio)
            else:
                print("   ⚠️ Video has no audio track")
                clip.close()
        else:
            print("   ⚠️ No video files in uploads directory")
    else:
        print("   ⚠️ Uploads directory not found")
        
except ImportError as e:
    print(f"❌ Whisper NOT installed: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("\nIf all tests passed, subtitle generation should work correctly!")
print("If tests failed, check:")
print("1. FFmpeg is properly installed and in PATH")
print("2. Whisper is installed: pip install openai-whisper")
print("3. Video files have audio tracks")
