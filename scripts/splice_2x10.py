#!/usr/bin/env python3
"""H3MXA-onlyno999 splice — join two director segments by the settled rule:
segment 1 at its nominal frame count + segment 2 with frame 0 dropped,
segment 2's audio shifted by exactly one frame (1/24s). Hard cut, no fades,
no other audio edits. Output is encoded to the delivery spec
(720x1280, yuv420p, H.264 High@L4.0, bt709 tv, avc1, AAC LC 48kHz,
metadata stripped, faststart).

Usage:
  splice_2x10.py SEG1.mp4 SEG2.mp4 OUT.mp4 [--frames1 240] [--frames2 239]
"""
import argparse, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("seg1"); ap.add_argument("seg2"); ap.add_argument("out")
ap.add_argument("--frames1", type=int, default=240)
ap.add_argument("--frames2", type=int, default=239,
                help="frames taken from seg2 AFTER dropping its frame 0")
a = ap.parse_args()

dur1 = a.frames1 / 24.0
fc = (
    f"[0:v]trim=end_frame={a.frames1},setpts=PTS-STARTPTS[v0];"
    f"[1:v]select='gt(n\\,0)',trim=end_frame={a.frames2},setpts=PTS-STARTPTS[v1];"
    f"[v0][v1]concat=n=2:v=1:a=0,scale=720:1280:flags=lanczos[v];"
    f"[0:a]atrim=0:{dur1:.6f},asetpts=PTS-STARTPTS[a0];"
    f"[1:a]atrim=start={1/24:.6f}:end={dur1:.6f},asetpts=PTS-STARTPTS[a1];"
    f"[a0][a1]concat=n=2:v=0:a=1[a]"
)
cmd = ["ffmpeg", "-v", "error", "-i", a.seg1, "-i", a.seg2,
       "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-profile:v", "high", "-level", "4.0",
       "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
       "-color_trc", "bt709", "-colorspace", "bt709", "-tag:v", "avc1",
       "-c:a", "aac", "-profile:a", "aac_low", "-ar", "48000", "-ac", "2",
       "-map_metadata", "-1", "-movflags", "+faststart", a.out, "-y"]
r = subprocess.run(cmd)
if r.returncode != 0:
    sys.exit(r.returncode)
probe = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-show_entries", "stream=codec_type,nb_frames", "-of", "default=nw=1",
     a.out], capture_output=True, text=True)
print(probe.stdout)
print(f"total frames: {a.frames1 + a.frames2} "
      f"({(a.frames1 + a.frames2) / 24:.3f}s) -> {a.out}")
