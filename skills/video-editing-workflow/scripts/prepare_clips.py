#!/usr/bin/env python3
"""Generate ordered pre-cut MP4 clips and SRT subtitles from a clip plan."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys
from typing import Any


def slug(text: str) -> str:
    text = re.sub(r"[\\/:*?\"<>|]+", "_", text.strip())
    text = re.sub(r"\s+", "_", text)
    return text[:80] or "clip"


def srt_time(seconds: float) -> str:
    if seconds < 0:
        seconds = 0
    total_ms = int(round(seconds * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_m = total_s // 60
    m = total_m % 60
    h = total_m // 60
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"Missing required tool: {name}")
    return path


def load_plan(path: pathlib.Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "clips" not in data or not isinstance(data["clips"], list) or not data["clips"]:
        raise SystemExit("Plan must contain a non-empty clips array.")
    return data


def parse_resolution(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+)x(\d+)", value)
    if not match:
        raise SystemExit("resolution must look like 1080x1920")
    return int(match.group(1)), int(match.group(2))


def ffmpeg_cut(
    ffmpeg: str,
    source: pathlib.Path,
    dest: pathlib.Path,
    start: float,
    end: float,
    width: int,
    height: int,
    crf: str,
    preset: str,
) -> None:
    if end <= start:
        raise SystemExit(f"Invalid time range for {source}: start={start}, end={end}")
    if not source.exists():
        raise SystemExit(f"Missing source: {source}")
    duration = end - start
    vf = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1"
    cmd = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-ss",
        str(start),
        "-i",
        str(source),
        "-t",
        str(duration),
        "-vf",
        vf,
        "-r",
        "30",
        "-c:v",
        "libx264",
        "-preset",
        preset,
        "-crf",
        crf,
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "160k",
        "-movflags",
        "+faststart",
        str(dest),
    ]
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=pathlib.Path)
    parser.add_argument("--crf", default="20")
    parser.add_argument("--preset", default="veryfast")
    args = parser.parse_args()

    ffmpeg = require_tool("ffmpeg")
    plan = load_plan(args.plan)
    width, height = parse_resolution(plan.get("resolution", "1080x1920"))
    out_dir = pathlib.Path(plan["output_dir"]).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest: list[dict[str, Any]] = []
    srt_entries: list[str] = []
    current = 0.0

    for idx, clip in enumerate(plan["clips"], 1):
        source = pathlib.Path(clip["source"]).expanduser()
        start = float(clip["start"])
        end = float(clip["end"])
        caption = str(clip.get("caption", "")).strip()
        base_name = slug(str(clip.get("name") or source.stem))
        dest = out_dir / f"{idx:02d}_{base_name}.mp4"

        print(f"[{idx:02d}/{len(plan['clips']):02d}] {dest.name}")
        ffmpeg_cut(ffmpeg, source, dest, start, end, width, height, args.crf, args.preset)

        duration = end - start
        item = {
            "index": idx,
            "file": dest.name,
            "source": str(source),
            "source_start": start,
            "source_end": end,
            "duration": duration,
            "caption": caption,
        }
        manifest.append(item)
        if caption:
            srt_entries.append(f"{idx}\n{srt_time(current)} --> {srt_time(current + duration)}\n{caption}\n")
        current += duration

    subtitle_name = plan.get("subtitle_name", "ready_subtitles.srt")
    (out_dir / subtitle_name).write_text("\n".join(srt_entries), encoding="utf-8")
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [f"# {plan.get('project_name', 'Video')} Ready Clips", "", f"Total duration: {current:.2f}s", ""]
    for item in manifest:
        lines.append(f"{item['index']}. `{item['file']}` - {item['duration']:.2f}s - {item['caption']}")
    (out_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"DONE {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
