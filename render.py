#!/usr/bin/env python3
"""Render independent scene images into a narrated vertical MP4."""
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = ROOT / "output"
W, H, FPS = 1080, 1920, 30

def run(*cmd):
    subprocess.run([str(x) for x in cmd], check=True)

def duration(audio):
    p = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(audio)],capture_output=True,text=True,check=True)
    return float(p.stdout.strip())

def ease(t):
    return t*t*(3-2*t)

def fit(img, zoom):
    sw, sh = img.size
    scale = max(W/sw,H/sh)*zoom
    return img.resize((max(W,round(sw*scale)),max(H,round(sh*scale))),Image.Resampling.LANCZOS)

def main():
    images = sorted([p for p in ASSETS.iterdir() if re.fullmatch(r"scene_\d+\.(jpg|jpeg|png|webp)",p.name,re.I)], key=lambda p:int(re.search(r"\d+",p.stem).group()))
    audio = ASSETS / "voice.mp3"
    if not images or not audio.exists():
        sys.exit("Missing assets/scene_01.jpg (or PNG) and/or assets/voice.mp3")
    cfg = json.loads((ROOT/"scenes.json").read_text(encoding="utf-8"))
    total = duration(audio)
    if total <= 0: sys.exit("Audio is empty")
    OUT.mkdir(exist_ok=True)
    frames_total = math.ceil(total*FPS)
    # Keep every scene at least one frame. Split duration evenly, last frame matches audio.
    if len(images) > frames_total: sys.exit("More scenes than output frames")
    with tempfile.TemporaryDirectory() as temp:
        temp=Path(temp)
        segments=[]
        base,rem=divmod(frames_total,len(images))
        for i,path in enumerate(images):
            n=base+(i<rem)
            opts={**cfg.get("defaults",{}),**cfg.get("scenes",{}).get(str(int(re.search(r"\d+",path.stem).group())),{})}
            fx=max(0,min(1,float(opts.get("focus_x",0.5))))
            fy=max(0,min(1,float(opts.get("focus_y",0.5))))
            motion=opts.get("motion","push")
            if motion not in ("push","pull","pan_left","pan_right","static"): raise ValueError("Bad motion: "+str(motion))
            img=ImageOps.exif_transpose(Image.open(path)).convert("RGB")
            raw=temp/f"raw_{i:03d}.rgb"
            with raw.open("wb") as out:
                for j in range(n):
                    t=ease(j/max(1,n-1))
                    zoom=1.10
                    if motion=="push": zoom=1.08+0.07*t
                    elif motion=="pull": zoom=1.15-0.07*t
                    fitted=fit(img,zoom)
                    sw,sh=fitted.size
                    x=fx*sw-W/2
                    y=fy*sh-H/2
                    shift=(t-0.5)*0.06*W
                    if motion=="pan_left": x-=shift
                    if motion=="pan_right": x+=shift
                    x=max(0,min(sw-W,round(x)))
                    y=max(0,min(sh-H,round(y)))
                    frame=fitted.crop((x,y,x+W,y+H))
                    out.write(frame.tobytes())
            seg=temp/f"seg_{i:03d}.mp4"
            run("ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",FPS,"-i",raw,"-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p",seg)
            segments.append(seg)
            raw.unlink()
        listing=temp/"concat.txt"
        listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in segments))
        merged=temp/"merged.mp4"
        run("ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",listing,"-c","copy",merged)
        final=OUT/"asya_shorts.mp4"
        run("ffmpeg","-hide_banner","-loglevel","error","-y","-i",merged,"-i",audio,"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",final)
        print("Created:",final)
if __name__=="__main__":main()
