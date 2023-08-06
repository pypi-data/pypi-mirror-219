from pathlib import Path
import sys

__all__ = ["cli"]


def cli() -> None:
    """Entry point for the CLI"""

    if len(sys.argv) != 1:
        raise ValueError("Invalid number of arguments")

    task = sys.argv[0]
    if task == "create":
        create()
    else:
        print(f"Unknown task: {task}. `create` is the only task available")


def create(dst: Path | str = ".") -> None:
    """Create a project using templates"""

    if len(sys.argv) == 2:
        dst = sys.argv[1]

    if isinstance(dst, str):
        dst = Path(dst).resolve()

    dst.resolve().parent.mkdir(parents=True, exist_ok=True)

    src = Path(__file__).parent / "templates"

    all_src_files = src.glob("**/*")
    src_files = [f for f in all_src_files if "__pycache__" not in f.parts]
    for src_file in src_files:
        if src_file.is_file():
            dst_file = dst / src_file.relative_to(src)
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            dst_file.write_text(src_file.read_text())
