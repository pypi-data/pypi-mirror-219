from pathlib import Path
from shutil import which
from subprocess import run
from typing import Literal, get_args

from potoo.app import Potoo

ExportMode = Literal["svg", "pdf"]
EXPORT_MODES = get_args(ExportMode)


async def export(
    app: Potoo,
    dimensions: tuple[int, int],
    export_dir: Path,
    format: Literal["svg", "pdf"],
) -> int:
    export_dir.mkdir(exist_ok=True, parents=True)
    produced_files = []
    async with app.run_test(size=dimensions) as pilot:
        for i in range(1, app.number_of_slides + 1):
            print("Exporting slide", i)
            produced_files.append(
                pilot.app.save_screenshot(f"slide{i:02d}.svg", str(export_dir))
            )
            await pilot.press("right")
    print("Finished exporting SVGs to", export_dir)
    if format == "pdf":
        rsvg_convert = which("rsvg-convert")
        if not rsvg_convert:
            print("Could not detect `rsvg-convert` binary")
            return 1
        slides_pdf = export_dir / "slides.pdf"
        with open(slides_pdf, "wb") as slides_pdf_out:
            run(
                [rsvg_convert, "--format=pdf", *produced_files],
                stdout=slides_pdf_out,
                check=True,
            )
        print("Finished exporting PDF to", slides_pdf)
    return 0
