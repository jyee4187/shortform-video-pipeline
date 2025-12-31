#!/usr/bin/env python3
"""Short-Form Video Pipeline

Automated video processing pipeline for creating TikTok/YouTube Shorts.
Uses FFmpeg for GPU-accelerated encoding and Whisper for captions.
"""

import argparse
import json
import subprocess
from pathlib import Path
from typing import Optional


class VideoPipeline:
    """Main video processing pipeline."""
    
    def __init__(self, input_dir: Path, output_dir: Path, preset: str = 'tiktok'):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.preset = preset
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load preset configuration
        self.config = self._load_preset(preset)
    
    def _load_preset(self, preset: str) -> dict:
        """Load video preset configuration."""
        presets = {
            'tiktok': {
                'width': 1080,
                'height': 1920,
                'fps': 30,
                'bitrate': '5M',
                'codec': 'h264_nvenc',  # NVIDIA GPU encoding
            },
            'youtube': {
                'width': 1080,
                'height': 1920,
                'fps': 60,
                'bitrate': '8M',
                'codec': 'h264_nvenc',
            }
        }
        return presets.get(preset, presets['tiktok'])
    
    def process_video(self, input_file: Path) -> Path:
        """Process a single video file."""
        print(f"Processing: {input_file.name}")
        
        output_file = self.output_dir / f"{input_file.stem}_processed.mp4"
        
        # Build FFmpeg command with GPU acceleration
        cmd = [
            'ffmpeg',
            '-hwaccel', 'cuda',  # Enable CUDA acceleration
            '-i', str(input_file),
            '-vf', f"scale={self.config['width']}:{self.config['height']}:force_original_aspect_ratio=decrease,pad={self.config['width']}:{self.config['height']}:(ow-iw)/2:(oh-ih)/2",
            '-c:v', self.config['codec'],
            '-b:v', self.config['bitrate'],
            '-r', str(self.config['fps']),
            '-c:a', 'aac',
            '-b:a', '128k',
            '-y',  # Overwrite output
            str(output_file)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ Completed: {output_file.name}")
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"✗ Error processing {input_file.name}: {e.stderr.decode()}")
            return None
    
    def add_captions(self, video_file: Path) -> Path:
        """Add auto-generated captions using Whisper.
        
        Note: Requires whisper to be installed: pip install openai-whisper
        """
        print(f"Adding captions to: {video_file.name}")
        # TODO: Implement Whisper transcription and subtitle burning
        # For now, return original file
        return video_file
    
    def run(self):
        """Run the pipeline on all videos in input directory."""
        video_extensions = {'.mp4', '.mkv', '.avi', '.mov'}
        
        input_files = [
            f for f in self.input_dir.iterdir()
            if f.suffix.lower() in video_extensions
        ]
        
        if not input_files:
            print(f"No video files found in {self.input_dir}")
            return
        
        print(f"Found {len(input_files)} video(s) to process\n")
        
        for input_file in input_files:
            processed = self.process_video(input_file)
            if processed:
                # TODO: Add caption support
                # self.add_captions(processed)
                pass
        
        print(f"\n✓ Pipeline complete! Output: {self.output_dir}")


def main():
    parser = argparse.ArgumentParser(description='Short-form video pipeline')
    parser.add_argument('--input', '-i', default='input', help='Input directory')
    parser.add_argument('--output', '-o', default='output', help='Output directory')
    parser.add_argument('--preset', '-p', default='tiktok', 
                       choices=['tiktok', 'youtube'], help='Video preset')
    
    args = parser.parse_args()
    
    pipeline = VideoPipeline(
        input_dir=args.input,
        output_dir=args.output,
        preset=args.preset
    )
    
    pipeline.run()


if __name__ == '__main__':
    main()
