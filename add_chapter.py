#!/usr/bin/env python3
"""Dodaje rozdział do paczki i wpina go we WSZYSTKIE miejsca naraz (czysty Python).

Do 2026-09-26 „dodaj rozdział" było procedurą z pułapką opisaną w AI_README („zsynchronizuj
trzy miejsca + build") — a każde miejsce pominięte to martwy wpis. Ten skrypt robi to jednym
poleceniem i sam sprawdza wynik (`test.py`). Domyślnie DRY-RUN: pokazuje plan, nic nie
zapisuje (Przykazanie IV). Zapis dopiero z `--execute`.

Użycie:
  python add_chapter.py 18 my-topic \\
      --title-en "My topic" --title-pl "Mój temat" \\
      --desc-en "One line for the card." --desc-pl "Jedna linia na kartę." \\
      --keywords-en "kw1, kw2" --keywords-pl "słowo1, słowo2" [--group deep] [--execute]

Co robi (w tej kolejności):
  1. `NN-slug.md` (EN, kanon) i `pl/NN-slug.md` (PL) — szkielet, jeśli plików jeszcze nie ma;
     istniejące pliki zostawia (możesz najpierw napisać treść, a potem wpiąć).
  2. `README.md` — wiersz w tabeli rozdziałów.
  3. `AI_README.md` i `pl/AI_README.md` — wiersz w indeksie plików, linia w indeksie tematów,
     liczby (rozdziałów, zakres pogłębienia).
  4. `index.html` — wpis w `CHAPTERS` (PL tytuł/opis) i w `CH_EN` (EN tytuł/opis).
  5. `craft.json` — tylko `chapters` + 1. **Wersji ani CHANGELOG nie rusza:** rdzeń dzieli oś wersji
     z witryną (Rzemiosło Web), więc numer wydania nadaje autor, nie skrypt.
  6. `python build.py` (content.js) i `python test.py` — wynik jest dowodem, nie deklaracją.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PL = ROOT / "pl"

def chapters() -> list[str]:
    return sorted(p.name for p in ROOT.glob("[0-9][0-9]-*.md"))


def skeleton(no: str, title: str, lang: str) -> str:
    if lang == "en":
        return (f"# {no} — {title}\n\n> Commandment ?: *…* (which commandment does this expand? one line)\n\n"
                "## Why\n\n(the problem this chapter prevents — with an example from a project)\n\n"
                "## Rules\n\n- **…** — terse, imperative, with the \"why\".\n\n"
                "## Anti-patterns\n\n- 🚫 …\n")
    return (f"# {no} — {title}\n\n> Przykazanie ?: *…* (które przykazanie rozwija ten rozdział? jedna linia)\n\n"
            "## Dlaczego\n\n(problem, któremu ten rozdział zapobiega — z przykładem z projektu)\n\n"
            "## Reguły\n\n- **…** — zwięźle, w trybie rozkazującym, z „dlaczego\".\n\n"
            "## Antywzorce\n\n- 🚫 …\n")


class Plan:
    """Zbiera zmiany; zapisuje dopiero na `--execute`."""

    def __init__(self) -> None:
        self.writes: dict[Path, str] = {}
        self.notes: list[str] = []

    def text(self, path: Path) -> str:
        return self.writes.get(path, path.read_text(encoding="utf-8"))

    def replace_once(self, path: Path, old: str, new: str, what: str) -> None:
        t = self.text(path)
        if old not in t:
            raise SystemExit(f"⛔ {path.relative_to(ROOT)}: nie znalazłem kotwicy dla „{what}\" — "
                             f"struktura pliku się zmieniła, popraw skrypt, nie plik")
        self.writes[path] = t.replace(old, new, 1)
        self.notes.append(f"{path.relative_to(ROOT)}: {what}")

    def sub(self, path: Path, pattern: str, repl, what: str, count: int = 1) -> None:
        t = self.text(path)
        new, n = re.subn(pattern, repl, t, count=count, flags=re.M)
        if n == 0:
            raise SystemExit(f"⛔ {path.relative_to(ROOT)}: brak dopasowania dla „{what}\" ({pattern})")
        self.writes[path] = new
        self.notes.append(f"{path.relative_to(ROOT)}: {what}")

    def create(self, path: Path, content: str, what: str) -> None:
        if path.exists():
            self.notes.append(f"{path.relative_to(ROOT)}: istnieje — zostawiam treść")
            return
        self.writes[path] = content
        self.notes.append(f"{path.relative_to(ROOT)}: {what}")


def build_plan(a: argparse.Namespace) -> Plan:
    existing = chapters()
    last_no = int(existing[-1][:2])
    no = f"{a.number:02d}"
    if a.number != last_no + 1:
        raise SystemExit(f"⛔ następny wolny numer to {last_no + 1:02d}, nie {no} "
                         f"(numery i slugi są stabilnymi kotwicami — bez luk i bez nadpisywania)")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", a.slug):
        raise SystemExit("⛔ slug: małe litery ASCII, cyfry i myślniki (kotwica `#NN-slug`, wspólna dla języków)")
    fname = f"{no}-{a.slug}.md"
    prev = existing[-1]
    total = a.number + 1
    p = Plan()

    # 1. pliki rozdziału
    p.create(ROOT / fname, skeleton(no, a.title_en, "en"), "szkielet EN (kanon)")
    p.create(PL / fname, skeleton(no, a.title_pl, "pl"), "szkielet PL (tłumaczenie)")

    # 2. README — wiersz po ostatnim rozdziale
    p.sub(ROOT / "README.md", rf"(^\| {prev[:2]} \| \[[^\n]*\n)",
          lambda m: m.group(1) + f"| {no} | [{a.title_en}]({fname}) | {a.desc_en} |\n", "wiersz tabeli rozdziałów")

    # 3. AI_README EN i PL — indeks plików, indeks tematów, liczby
    for path, desc, kws, lang in ((ROOT / "AI_README.md", a.desc_en, a.keywords_en, "en"),
                                  (PL / "AI_README.md", a.desc_pl, a.keywords_pl, "pl")):
        p.sub(path, rf"(^\| `{re.escape(prev)}` \|[^\n]*\n)",
              lambda m, d=desc: m.group(1) + f"| `{fname}` | {d} |\n", "wiersz indeksu plików")
        p.sub(path, rf"(^- \*\*`{re.escape(prev)}`\*\*[^\n]*\n)",
              lambda m, k=kws: m.group(1) + f"- **`{fname}`** — {k}\n", "linia indeksu tematów")
        p.sub(path, rf"`09`–`{prev[:2]}`", f"`09`–`{no}`", "zakres pogłębienia", count=0)
        if lang == "en":
            p.sub(path, rf"- \d+ chapters \(`00`–`{prev[:2]}`\)", f"- {total} chapters (`00`–`{no}`)", "liczba rozdziałów")
            p.sub(path, rf"Deep dive: \d+ \(09–{prev[:2]}\)", f"Deep dive: {total - 9} (09–{no})", "liczba pogłębienia")
        else:
            p.sub(path, rf"- \d+ rozdziałów \(`00`–`{prev[:2]}`\)", f"- {total} rozdziałów (`00`–`{no}`)", "liczba rozdziałów")
            p.sub(path, rf"Pogłębienie: \d+ \(09–{prev[:2]}\)", f"Pogłębienie: {total - 9} (09–{no})", "liczba pogłębienia")

    # 4. index.html — CHAPTERS (PL) i CH_EN (EN); ostatni wpis dostaje przecinek
    html = ROOT / "index.html"
    p.sub(html, rf'(\{{file:"{re.escape(prev)}",[^\n]*\}})\n(\s*\];)',
          lambda m: (m.group(1) + ',\n    {file:"' + fname + '", no:"' + no + '", group:"' + a.group
                     + '", title:"' + a.title_pl + '", desc:"' + a.desc_pl + '"}\n' + m.group(2)), "CHAPTERS")
    p.sub(html, rf'("{prev[:-3]}":\{{t:"[^"]*",d:"[^"]*"\}})\n(\s*\}};)',
          lambda m: (m.group(1) + ',\n    "' + fname[:-3] + '":{t:"' + a.title_en + '",d:"' + a.desc_en
                     + '"}\n' + m.group(2)), "CH_EN")

    # 5. craft.json — tylko liczba rozdziałów; wersję i CHANGELOG nadaje autor (wspólna oś z Web)
    craft = json.loads(p.text(ROOT / "craft.json"))
    craft["chapters"] = total
    p.writes[ROOT / "craft.json"] = json.dumps(craft, ensure_ascii=False, indent=2) + "\n"
    p.notes.append(f"craft.json: chapters={total} (wersja bez zmian — nadaje ją autor)")
    return p


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("number", type=int, help="numer rozdziału — musi być następnym wolnym")
    ap.add_argument("slug", help="slug ASCII, np. language-and-guards")
    for name in ("title-en", "title-pl", "desc-en", "desc-pl", "keywords-en", "keywords-pl"):
        ap.add_argument(f"--{name}", required=True)
    ap.add_argument("--group", choices=("core", "deep"), default="deep")
    ap.add_argument("--execute", action="store_true", help="zapisz i uruchom build.py + test.py")
    a = ap.parse_args()

    plan = build_plan(a)
    print(("ZAPIS" if a.execute else "DRY-RUN — plan (nic nie zapisano)") + f": {len(plan.writes)} plików")
    for n in plan.notes:
        print("  ·", n)
    if not a.execute:
        print("Zapis: dodaj --execute")
        return 0
    for path, content in plan.writes.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    for step in ("build.py", "test.py"):
        r = subprocess.run([sys.executable, str(ROOT / step)], cwd=ROOT)
        if r.returncode != 0:
            print(f"⛔ {step} nie przeszło — popraw i uruchom `python test.py` ponownie")
            return 1
    print(f"✅ rozdział {a.number:02d}-{a.slug} wpięty; uzupełnij treść EN i PL, a przy wydaniu wersję w craft.json i wpis w CHANGELOG.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
