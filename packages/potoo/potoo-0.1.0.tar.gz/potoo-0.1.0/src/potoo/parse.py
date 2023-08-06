from collections.abc import Iterable
from io import StringIO
from typing import (
    Any,
    TextIO,
)

from yaml import safe_load


def parse_document(
    md_content_fp: TextIO, header_split_level: int
) -> tuple[list[str], dict[str, Any]]:
    headers_to_split_at = {"#" * level for level in range(1, header_split_level + 1)}
    all_slides: list[str] = []
    current_slide = StringIO()
    line: str

    inside_frontmatter = False
    frontmatter_content: list[str] = []

    # No support for them yet
    inside_speaker_notes = False
    inside_code_block = False

    def save_slide():
        nonlocal current_slide
        slide_content = current_slide.getvalue()
        if slide_content:
            all_slides.append(slide_content)
        current_slide = StringIO()

    for index, line in enumerate(md_content_fp):
        if line.strip().startswith("<!--"):
            # HTML comment
            continue
        # YAML-Frontmatter handling
        if index == 0 and line.strip() == "---":
            inside_frontmatter = True
            continue
        if inside_frontmatter:
            if line.startswith("#"):
                # YAML comment
                continue
            if line.strip() == "---":
                inside_frontmatter = False
                continue
            frontmatter_content.append(line)
            continue
        # Code blocks, required to prevent slide spitting when using '#' as comment
        # inside of if
        if line.strip().startswith("```"):
            inside_code_block = not inside_code_block
            current_slide.write(line)
            continue
        if inside_code_block:
            current_slide.write(line)
            continue
        # Speaker note handling
        if inside_speaker_notes:
            if line.startswith(":::"):
                inside_speaker_notes = False
            continue
        if line.startswith("::: notes"):
            inside_speaker_notes = True
            continue
        # Start new slide
        if line.startswith("---"):
            save_slide()
            continue
        # Split at specified header level(s)
        if line.split(" ", maxsplit=1)[0] in headers_to_split_at:
            save_slide()
        current_slide.write(line)
    save_slide()
    return all_slides, safe_load("\n".join(frontmatter_content)) or {}


def parse_slide(slide_content: str) -> Iterable[str]:
    inside_code_block = False

    fragment_lines_so_far: list[str] = []
    for line in slide_content.splitlines():
        if line.strip().startswith("```"):
            inside_code_block = not inside_code_block
            fragment_lines_so_far.append(line)
            continue
        if inside_code_block:
            fragment_lines_so_far.append(line)
            continue
        if line.strip() == ". . .":
            yield "\n".join(fragment_lines_so_far)
            fragment_lines_so_far = []
            continue
        fragment_lines_so_far.append(line)
    yield "\n".join(fragment_lines_so_far)

    return 0
