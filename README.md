# Video Editing Workflow

A Codex skill for turning local video files into an editable vlog project.

The workflow is designed for creators who want AI help with the planning and rough-cut stages, while keeping final creative control inside Jianying/CapCut. It analyzes source videos, creates markdown timelines, builds a script and editing guide, then generates ordered pre-cut clips and SRT subtitles that can be imported into an editor.

## What It Does

- Inspects local video files with FFmpeg/FFprobe.
- Creates one markdown timeline per source video.
- Builds a vlog script from selected moments.
- Writes an AI editing guide with clip order, pacing, captions, and style notes.
- Generates numbered pre-cut MP4 clips for easy editor import.
- Generates SRT subtitles matching the pre-cut sequence.
- Documents safe Jianying/CapCut draft-file findings without relying on fragile timeline injection.

## Repository Structure

```text
.
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   └── jianying-draft-notes.md
└── scripts/
    └── prepare_clips.py
```

## Installation

Clone or copy this folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/chizhang0402-collab/video-editing-workflow.git ~/.codex/skills/video-editing-workflow
```

If the skill is already installed locally, update it with:

```bash
git -C ~/.codex/skills/video-editing-workflow pull
```

## Requirements

The full workflow expects local video tooling to be available:

- `ffmpeg`
- `ffprobe`
- Optional: Whisper for speech transcription
- Optional: OpenCV or PySceneDetect for shot/scene analysis

On macOS, FFmpeg can be installed with:

```bash
brew install ffmpeg
```

## Usage

In Codex, ask for the skill by name and provide local video paths:

```text
Use video-editing-workflow to analyze these videos, create a project folder, write the timelines and script, then generate ready-to-import clips and subtitles for Jianying.
```

The recommended output project layout is:

```text
<project-name>/
├── <source-video-stem>.md
├── vlog_video_script.md
├── ai_editing_guide.md
├── rough_cut.mp4
└── ready_clips/
    ├── 01_<short-name>.mp4
    ├── 02_<short-name>.mp4
    ├── ready_subtitles.srt
    ├── manifest.json
    └── README.md
```

## Pre-Cut Clip Script

The bundled script can generate ordered MP4 clips and SRT subtitles from a JSON clip plan.

Example `clip_plan.json`:

```json
{
  "project_name": "Cherry Orchard Vlog",
  "output_dir": "/Users/name/Movies/Cherry Orchard Vlog/ready_clips",
  "resolution": "1080x1920",
  "subtitle_name": "ready_subtitles.srt",
  "clips": [
    {
      "name": "depart",
      "source": "/path/to/source.mp4",
      "start": 2.0,
      "end": 5.0,
      "caption": "Heading to the orchard"
    }
  ]
}
```

Run:

```bash
python3 scripts/prepare_clips.py --plan /path/to/clip_plan.json
```

The script writes:

- Numbered MP4 clips
- `ready_subtitles.srt`
- `manifest.json`
- `README.md`

## Jianying/CapCut Notes

This workflow intentionally avoids directly writing Jianying/CapCut timeline files. Local testing found that media folders can sometimes be organized through plain JSON draft indexes, but main timeline data may be encoded or encrypted.

For reliable editing:

1. Import the generated `ready_clips/` folder.
2. Sort clips by filename.
3. Drag the numbered clips to the timeline.
4. Import the generated SRT.
5. Finish transitions, music, color, and subtitle styling manually.

See `references/jianying-draft-notes.md` for the draft-file findings.

## License

No license has been added yet. Add one before distributing or accepting external contributions.
