"""AI_README index guard (The Craft, chapter 17).

Copy to the project's `tests/test_ai_readme.py` and adjust GUARDED / SKIPPED.
Enforces: every guarded directory has an AI_README.md, every module in it is named in the
index, the index stays under the grep ceiling, and the GUARDED list is complete.
Stdlib + pytest only.
"""
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]          # tests/ -> project root
GUARDED = ("app", "scripts", "tests")                       # directories with code AND an index
SKIPPED = {"__init__.py", "conftest.py"}                    # nothing to describe
CODE_GLOBS = ("*.py",)                                      # add "*.js", "*.ts" … as needed
INDEX_MAX_BYTES = 20_000


def modules(directory: str) -> list[str]:
    found = []
    for pattern in CODE_GLOBS:
        found += [p.name for p in (ROOT / directory).glob(pattern) if p.name not in SKIPPED]
    return sorted(found)


@pytest.mark.parametrize("directory", GUARDED)
def test_directory_has_an_index(directory):
    assert (ROOT / directory / "AI_README.md").is_file(), f"{directory}/ has no AI_README.md"


@pytest.mark.parametrize("directory", GUARDED)
def test_every_module_is_in_the_index(directory):
    text = (ROOT / directory / "AI_README.md").read_text(encoding="utf-8")
    missing = [m for m in modules(directory) if m not in text and pathlib.Path(m).stem not in text]
    assert not missing, f"{directory}/AI_README.md does not mention: {missing}"


@pytest.mark.parametrize("directory", GUARDED)
def test_index_fits_the_grep_ceiling(directory):
    size = (ROOT / directory / "AI_README.md").stat().st_size
    assert size <= INDEX_MAX_BYTES, f"{directory}/AI_README.md is {size} B — split the directory"


def test_guarded_list_is_complete():
    with_index = set()
    for index in ROOT.rglob("AI_README.md"):
        if any(part in {".git", "node_modules", ".venv", "docs"} for part in index.parts):
            continue
        if any(list(index.parent.glob(p)) for p in CODE_GLOBS):
            with_index.add(index.parent.relative_to(ROOT).as_posix())
    assert with_index <= set(GUARDED), f"add to GUARDED: {sorted(with_index - set(GUARDED))}"
