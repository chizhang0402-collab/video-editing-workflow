# Jianying/CapCut Draft Notes

These notes summarize local experiments with Jianying Pro draft files.

## What was safe and useful

- `draft_virtual_store.json` is plain JSON in some Jianying projects.
- `draft_virtual_store` item with `type: 0` stores folder/group entries.
- `draft_virtual_store` item with `type: 1` stores child links.
- A child appears inside a folder when its `parent_id` equals the folder `id`.
- Back up `draft_virtual_store.json` before changing it.

Minimal folder pattern:

```json
{
  "type": 0,
  "value": [
    {
      "creation_time": 1778220662,
      "display_name": "Project Folder",
      "filter_type": 0,
      "id": "UUID",
      "import_time": 1778220662,
      "import_time_us": 1778220662000000,
      "sort_sub_type": 0,
      "sort_type": 0
    }
  ]
}
```

Minimal child link:

```json
{
  "child_id": "MATERIAL_OR_FOLDER_ID",
  "parent_id": "FOLDER_UUID"
}
```

## What was not stable

- Creating a `subdraft/<uuid>/draft_content.json` folder can make a folder visible only when indexed, but does not guarantee a usable timeline/subdraft clip.
- Main timeline files such as `draft_info.json` may be base64-like encoded binary with high entropy. Do not rewrite these as JSON.
- Directly injecting a rough-cut timeline into Jianying/CapCut was not proven safe.

## Recommendation

Use draft-file edits only for organizing imported media. For actual rough cuts, generate numbered MP4 clips and SRT subtitles outside Jianying, then import them.
