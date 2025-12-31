# Short-Form Video Pipeline

Automated pipeline for creating short-form videos (TikTok, YouTube Shorts, Reels) using your 4080 GPU and local tools.

## Features

- **GPU-accelerated rendering** (RTX 4080 CUDA/OptiX)
- **Batch processing**: screen recordings → edited clips
- **Auto-captions** with burned-in subtitles
- **Template system** for quick edits (hooks, cuts, transitions)
- **Export presets**: 9:16, 1080x1920, 60fps for TikTok/YT Shorts

## Stack

- **Video editing**: FFmpeg (GPU encoding), DaVinci Resolve API (optional)
- **Captioning**: Whisper (local speech-to-text)
- **Scripting**: Python (orchestration)
- **Optional UI**: Simple web dashboard to queue/monitor renders

## Use Case

Turn your quant project demos, music production clips, or code tutorials into polished short-form content for your TikTok/socials.

## Workflow

1. Drop raw .mp4/.mkv files into `input/` folder
2. Run `pipeline.py --preset tiktok`
3. Pipeline auto-detects scenes, adds captions, applies template
4. Outputs to `output/` ready for upload

## Roadmap

- [ ] FFmpeg CUDA encoding setup
- [ ] Whisper local caption generation
- [ ] Template JSON (hook positions, b-roll overlays)
- [ ] Batch queue system
- [ ] Web UI for monitoring

---

**Built to run on your local 4080 rig, no cloud costs.**
