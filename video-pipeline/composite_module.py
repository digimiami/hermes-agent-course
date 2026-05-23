#!/usr/bin/env python3
"""
Composite module video with:
  - Ken Burns background scenes
  - Looping SadTalker face overlay (bottom-right)
  - Voiceover audio
  - ASS captions

Usage: python3 composite_module.py <module_number>
  e.g. python3 composite_module.py 1
"""
import subprocess, sys, os, json
from pathlib import Path

BASE = Path("/root/hermes-course/video-pipeline")
OUT_DIR = Path("/root/hermes-course/course/videos")
SCENES = BASE / "scenes"
AUDIO = BASE / "audio"
FACE = BASE / "face_renders"
CAPTIONS = BASE / "captions"

MODULE_DURATIONS = {1:150, 2:160, 3:155, 4:160, 5:160, 6:150, 7:150, 8:150, 9:160, 10:160}

def to_ass(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def composite(num):
    module_str = f"module{num:02d}"
    total_dur = MODULE_DURATIONS[num]
    fps = 25
    total_frames = int(total_dur * fps)
    
    print(f"\n🎬 Compositing Module {num} ({total_dur}s, {total_frames}frames)")
    
    # Find face animation MP4
    face_dir = FACE / module_str
    face_mp4s = list(face_dir.rglob("*.mp4"))
    if not face_mp4s:
        # Try parent directory
        face_mp4s = list(face_dir.parent.rglob(f"{module_str}*.mp4"))
    face_mp4 = None
    for f in face_mp4s:
        face_mp4 = f
        break
    
    if not face_mp4:
        print(f"❌ No face animation found in {face_dir}")
        # Check if it's in the parent dir
        for p in face_dir.parent.glob("*.mp4"):
            face_mp4 = p
            break
    
    if face_mp4:
        print(f"  Face animation: {face_mp4}")
    else:
        print(f"  ⚠️  No face animation found, proceeding without face overlay")
    
    # Audio
    audio_path = AUDIO / f"{module_str}_voiceover.wav"
    if not audio_path.exists():
        print(f"❌ Voiceover not found: {audio_path}")
        return None
    
    # Scenes
    scene_dir = SCENES / module_str
    concat_file = scene_dir / "concat.txt"
    if not concat_file.exists():
        print(f"❌ Scenes not found: {scene_dir}")
        return None
    
    # Captions
    ass_path = CAPTIONS / f"{module_str}.ass"
    if not ass_path.exists():
        print(f"❌ Captions not found: {ass_path}")
        return None
    
    # --- PASS 1: Ken Burns background ---
    print("  ▶ PASS 1: Background with Ken Burns zoom...")
    bg_video = BASE / f"_bg_{module_str}.mp4"
    
    result = subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-filter_complex",
        f"[0:v]format=pix_fmts=yuv420p,"
        f"zoompan=z='if(eq(on,1),1,min(1+0.0015*(on-1),1.04))':"
        f"d={total_frames}:s=1920x1080:fps={fps}[bg]",
        "-map", "[bg]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-frames:v", str(total_frames),
        str(bg_video)
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"  ❌ Pass 1 failed: {result.stderr[-200:]}")
        return None
    
    bg_size = os.path.getsize(bg_video)
    print(f"  ✓ BG: {bg_size/1024/1024:.1f} MB")
    
    # --- PASS 2: Face overlay + captions + audio ---
    print("  ▶ PASS 2: Face overlay + captions + audio...")
    
    out_path = OUT_DIR / f"{module_str}.mp4"
    
    if face_mp4:
        face_x, face_y = 1920 - 320 - 30, 1080 - 320 - 120
        
        filter_graph = (
            f"[1:v]scale=320:320:force_original_aspect_ratio=decrease,"
            f"setsar=1,format=rgba,"
            f"colorchannelmixer=aa=0.85[face];"
            f"[0:v][face]overlay={face_x}:{face_y}:shortest=1[withface];"
            f"[withface]subtitles={ass_path}[outv]"
        )
        
        result = subprocess.run([
            "ffmpeg", "-y",
            "-i", str(bg_video),
            "-stream_loop", "-1", "-i", str(face_mp4),
            "-i", str(audio_path),
            "-filter_complex", filter_graph,
            "-map", "[outv]",
            "-map", "2:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            str(out_path)
        ], capture_output=True, text=True)
    else:
        # No face - just pass-through
        result = subprocess.run([
            "ffmpeg", "-y",
            "-i", str(bg_video),
            "-i", str(audio_path),
            "-filter_complex",
            f"[0:v]subtitles={ass_path}[outv]",
            "-map", "[outv]",
            "-map", "1:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            str(out_path)
        ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"  ❌ Pass 2 failed: {result.stderr[-200:]}")
        return None
    
    # Verify
    if out_path.exists():
        sz = os.path.getsize(out_path)
        dur = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "csv=p=0", str(out_path)
        ], capture_output=True, text=True).stdout.strip()
        print(f"  ✅ FINAL: {out_path.name} - {sz/1024/1024:.1f} MB, {float(dur):.1f}s")
        return str(out_path)
    else:
        print(f"  ❌ Output not created")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 composite_module.py <module_number>")
        sys.exit(1)
    num = int(sys.argv[1])
    result = composite(num)
    if result:
        # Copy to course videos
        print(f"  📋 Ready: {result}")
    else:
        sys.exit(1)
