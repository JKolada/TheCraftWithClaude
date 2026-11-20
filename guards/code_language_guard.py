"""Code-language guard — a ratchet (The Craft, chapter 17).

Copy to the project's `tests/test_code_language.py`; adjust SCANNED, STOP and SHAPE to the
project's prose language (defaults: Polish). Heuristic, not a dictionary — a ratchet, not a court.

  pytest tests/test_code_language.py                      # enforce
  python tests/test_code_language.py --write-baseline     # tighten after renames (on command)
"""
import ast
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCANNED = ("app", "scripts", "tests")
BASELINE = ROOT / "tests" / "code_language_baseline.json"   # {"path": count}
STOP = {"nie", "jest", "bez", "gdy", "czy", "dla", "przy", "tylko", "albo", "oraz", "jako"}
SHAPE = re.compile(r"cz|rz|sz|dz|(?:uje|osci|anie|enie|owy|owa|owe|nych|nego)$")
LOOK_ALIKES = {"ego", "media", "wizard", "jazz", "pizza", "schema", "sizes"}


def tokens(name: str) -> list[str]:
    return [t.lower() for t in re.split(r"_+|(?<=[a-z0-9])(?=[A-Z])", name) if t]


def looks_foreign(name: str) -> bool:
    return any(t not in LOOK_ALIKES and (t in STOP or (len(t) >= 4 and SHAPE.search(t)))
               for t in tokens(name))


def names(path: pathlib.Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    defs = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
    return [path.stem] + [n.name for n in ast.walk(tree) if isinstance(n, defs)]


def scan() -> dict[str, int]:
    counts = {}
    for top in SCANNED:
        for path in (ROOT / top).rglob("*.py"):
            hits = [n for n in names(path) if looks_foreign(n)]
            if hits:
                counts[path.relative_to(ROOT).as_posix()] = len(hits)
    return counts


def test_ratchet():
    base = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.exists() else {}
    now = scan()
    new_files = sorted(k for k in now if k not in base)
    grown = sorted(k for k in now if k in base and now[k] > base[k])
    loose = sorted(k for k in base if now.get(k, 0) < base[k])
    assert not new_files, f"new files must be clean: {new_files}"
    assert not grown, f"a file gained foreign names: {grown}"
    assert not loose, f"tighten the baseline (--write-baseline): {loose}"


if __name__ == "__main__" and "--write-baseline" in sys.argv:
    BASELINE.write_text(json.dumps(scan(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"baseline written: {BASELINE}")
