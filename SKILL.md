---
name: video-editing-workflow
description: Local video-editing project workflow for vlog or short-form videos. Use when Codex needs to analyze local video files, create per-video markdown timelines, build a story/script from selected moments, write an AI editing guide, generate ordered pre-cut clips, produce SRT subtitles, or prepare assets for Jianying/CapCut without directly editing fragile encrypted draft timelines.
---

# Video Editing Workflow

## Overview

Turn local video files into an editable video project folder. Prefer a stable file-based workflow: analyze source videos, write markdown timelines, create a script and editing guide, then generate numbered pre-cut clips plus SRT subtitles for import into Jianying/CapCut.

## Project Layout

Create one folder per editing project under the user's requested parent directory. If no parent is given, default to the user's Movies folder.

Use a specific project name, never a generic name like `video_editing`.

Recommended structure:

```text
<project-name>/
├── <source-video-stem>.md
├── vlog_video_script.md
├── ai_editing_guide.md
├── rough_cut.mp4               # optional preview render
└── ready_clips/
    ├── 01_<short-name>.mp4
    ├── 02_<short-name>.mp4
    ├── cherry_vlog_ready_subtitles.srt
    ├── manifest.json
    └── README.md
```

## Workflow

1. Inspect source files with `ffprobe`.
   Capture duration, resolution, frame rate, audio presence, rotation/orientation, and basic codec info.

2. Analyze content.
   Use FFmpeg frame extraction, OpenCV/PySceneDetect for shot and motion changes, and Whisper only when speech matters. Write one markdown file per source video with concrete time ranges and visual content notes.

3. Build the narrative.
   Convert useful moments into `vlog_video_script.md`: sequence, pacing, captions/voiceover, and the exact source file/time range for every beat.

4. Write `ai_editing_guide.md`.
   Include the desired runtime, aspect ratio, clip order, pacing rules, transitions, subtitle style, music/audio notes, and a machine-readable clip table.

5. Generate pre-cut clips and SRT.
   Create a clip-plan JSON from the guide and run `scripts/prepare_clips.py`. Number output files so Jianying/CapCut imports them in script order.

6. Validate outputs.
   Probe every generated clip. Confirm count, total duration, resolution, and subtitle file. If possible, create a contact sheet or preview render before final handoff.

## Clip Plan Format

Use this JSON shape with `scripts/prepare_clips.py`:

```json
{
  "project_name": "Cherry Orchard Vlog",
  "output_dir": "/Users/name/Movies/Cherry Orchard Vlog/ready_clips",
  "resolution": "1080x1920",
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
python3 <skill>/scripts/prepare_clips.py --plan /path/to/clip_plan.json
```

The script writes numbered MP4 clips, `manifest.json`, `README.md`, and `.srt` subtitles.

## Jianying/CapCut Guidance

Prefer importing `ready_clips/` into Jianying/CapCut and dragging the numbered clips onto the timeline. Import the generated SRT afterward for editable subtitles.

Direct draft-file editing is experimental. Read `references/jianying-draft-notes.md` before touching Jianying/CapCut project files. The safe lesson from testing: plain `draft_virtual_store.json` can organize imported media into folders, but main timeline files may be encoded/encrypted and should not be rewritten unless the format is clearly understood and backed up.

## Safety

Before writing outside the workspace, request approval when the environment requires it. Before modifying app draft files, create a timestamped backup and keep changes minimal. Never delete or overwrite source videos.
