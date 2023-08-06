import asyncio
from sys import stderr

from potoo.app import Potoo, Slide
from potoo.cli import parse_cli_arguments
from potoo.export import export
from potoo.parse import parse_document, parse_slide


def main() -> int:
    args = parse_cli_arguments()
    all_slides, presentation_meta = parse_document(
        args["markdown_file"], args["header_split_level"]
    )
    title_slide_lines = [f"# {presentation_meta.get('title', 'Your title here')}"]
    if subtitle := presentation_meta.get("subtitle"):
        title_slide_lines[0] += f" - *{subtitle}*"
    slides: list[Slide] = []

    for key in ("author", "date"):
        if value := presentation_meta.get(key):
            title_slide_lines.append(f"- {value}")
    slides.append(("\n".join(title_slide_lines),))

    for slide in all_slides:
        if not slide.strip():
            continue
        fragments = tuple(parse_slide(slide))
        if args["export"] or args["no_fragments"]:
            slides.append(("\n".join(fragments),))
        else:
            slides.append(fragments)
    app = Potoo(slides, presentation_meta, args["static_footer"])
    app.dark = not args["light_mode"]
    if args["export"]:
        return asyncio.run(
            export(
                app,
                args["export_terminal_size"],
                export_dir=args["export_dir"],
                format=args["export"],
            )
        )
    # Set terminal title to presentation title
    stderr.write(f"\x1b]2;{title_slide_lines[0]}\x07")
    stderr.flush()
    app.run()

    return 0
