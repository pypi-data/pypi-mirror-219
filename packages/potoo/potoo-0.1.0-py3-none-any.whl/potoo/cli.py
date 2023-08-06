from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, FileType
from pathlib import Path
from typing import TextIO, TypedDict, cast

from potoo.export import EXPORT_MODES, ExportMode


class Args(TypedDict):
    markdown_file: TextIO
    header_split_level: int
    static_footer: str | None
    no_fragments: bool
    export_dir: Path
    export: ExportMode | None
    export_terminal_size: tuple[int, int]
    light_mode: bool


def parse_cli_arguments(_argv: list[str] | None = None) -> Args:
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("markdown_file", type=FileType())
    parser.add_argument(
        "-s",
        "--header-split-level",
        type=int,
        default=3,
        help="""Maximum header level ('###') at which to split into individual slides.
        Given the default value every `#`, `##` and `###` would start a new slide, with
        4 it would be `####` in addition.""",
    )
    parser.add_argument(
        "-f",
        "--static-footer",
        help="""Static text to display in the middle of the footer, e.g. your company
        name. Rich styles (https://rich.readthedocs.io/en/latest/style.html#styles)
        are supported, e.g. `[b]My Company[/]`""",
    )
    parser.add_argument(
        "-n",
        "--no-fragments",
        action="store_true",
        help="""Disable fragments (incrementally appearing items whenever `. . .`
        is used without updating the slide counter). Disabled by default for any
        export.""",
    )
    parser.add_argument(
        "-d",
        "--export-dir",
        type=Path,
        help="Directory to use for exports",
        default=Path("export/"),
    )
    parser.add_argument(
        "-e",
        "--export",
        choices=EXPORT_MODES,
        help="""Export slides as SVG files or one concatenated PDF of all SVG files by
        shelling out to `rsvg-convert`.""",
    )
    parser.add_argument(
        "-t",
        "--export-terminal-size",
        type=int,
        nargs=2,
        default=(80, 24),
        help="""Terminal dimensions for export. Increase it if scrollbars appear inside
        your exported files. It is recommended to preserve the height-width ratio.""",
    )
    parser.add_argument(
        "-l",
        "--light-mode",
        action="store_true",
        help="""Launch in light mode. Primarily required for exports where the toggle
        shortcut (`d`) cannot be used.""",
    )

    args = parser.parse_args(_argv)
    return cast(Args, vars(args))
