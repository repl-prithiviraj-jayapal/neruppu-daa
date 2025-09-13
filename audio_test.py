#!/usr/bin/env python3
"""
Simple audio test for debugging NERUPPU DAA sound issues
"""

print("🔍 Testing audio system...")

try:
    import pygame
    print("✅ pygame imported successfully")
except ImportError:
    print("❌ pygame not found")
    exit(1)

try:
    import numpy as np
    print("✅ numpy imported successfully")
except ImportError:
    print("❌ numpy not found")
    exit(1)

print("\n🎵 Initializing audio...")
try:
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.mixer.init()
    print("✅ pygame.mixer initialized")
except Exception as e:
    print(f"❌ Audio initialization failed: {e}")
    exit(1)

print("\n🔊 Creating test sound...")
try:
    # Create a simple beep sound
    duration = 1.0
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a 440Hz tone (A4 note)
    frequency = 440
    wave = np.sin(frequency * 2 * np.pi * t) * 0.3
    
    # Convert to 16-bit integers
    wave = (wave * 32767).astype(np.int16)
    
    # Create stereo sound
    stereo_wave = np.column_stack([wave, wave])
    stereo_wave = np.ascontiguousarray(stereo_wave)
    
    # Create pygame sound
    sound = pygame.sndarray.make_sound(stereo_wave)
    print("✅ Sound created successfully")
    
except Exception as e:
    print(f"❌ Sound creation failed: {e}")
    exit(1)

print("\n🎶 Playing sound for 3 seconds...")
print("   If you don't hear anything, the issue might be:")
print("   1. Audio output device not connected")
print("   2. System audio muted")
print("   3. Terminal blocking audio")
print("   4. macOS audio permissions")

try:
    sound.play()
    pygame.time.wait(3000)  # Wait 3 seconds
    print("✅ Sound playback completed")
    
except Exception as e:
    print(f"❌ Sound playback failed: {e}")

print("\n🔍 Audio system info:")
try:
    print(f"   Mixer frequency: {pygame.mixer.get_init()[0]} Hz")
    print(f"   Mixer format: {pygame.mixer.get_init()[1]}")
    print(f"   Mixer channels: {pygame.mixer.get_init()[2]}")
    print(f"   Number of sound channels: {pygame.mixer.get_num_channels()}")
except:
    print("   Could not get mixer info")

print("\n🎯 Test complete!")
print("   Did you hear a 440Hz beep tone?")
print("   If YES: Audio system works, issue is in game code")
print("   If NO: System audio configuration issue")