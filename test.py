#!/usr/bin/env python3
"""Prosty smoke test repo (czysty Python, zero zależności).

Łapie regresje strukturalne, o które prosi sama doktryna: parytet PL↔EN, martwe
linki między rozdziałami, nieaktualny content.js, rozjazd CHAPTERS/tabel/codex.json.
NIE testuje runtime JS (od tego jest podgląd w przeglądarce — Przykazanie III).

Użycie:  python test.py      # exit 0 = zielone, exit 1 = lista problemów
"""
import json
import re
import sys
from pathlib import Path

import build  # współdzielone: build.content_js(), build.collect()

ROOT = Path(__file__).resolve().parent
EN = ROOT / "en"
errors = []

try:  # Windows: konsola bywa cp1252 — wymuś UTF-8, by polskie znaki nie wywaliły printu.
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def err(msg):
    errors.append(msg)


def chapter_files(base):
    return sorted(p.name for p in base.glob("[0-9][0-9]-*.md"))


def cross_links(path):
    # linki w stylu [tekst](NN-nazwa.md) lub (NN-nazwa.md#kotwica)
    return re.findall(r"\]\((\d\d-[a-z0-9-]+\.md)(?:#[^)]*)?\)", path.read_text(encoding="utf-8"))


def main():
    pl = chapter_files(ROOT)
    en = chapter_files(EN) if EN.is_dir() else []

    # 1) Parytet PL↔EN — ten sam zestaw nazw plików (rozdziały + intro).
    if set(pl) != set(en):
        only_pl = sorted(set(pl) - set(en))
        only_en = sorted(set(en) - set(pl))
        if only_pl:
            err(f"Parytet: rozdziały bez odpowiednika EN: {only_pl}")
        if only_en:
            err(f"Parytet: rozdziały EN bez odpowiednika PL: {only_en}")
    for extra in ("intro.md",):
        if (ROOT / extra).exists() and not (EN / extra).exists():
            err(f"Parytet: brak tłumaczenia en/{extra}")

    # 2) Martwe linki między rozdziałami (cel musi istnieć w tym samym katalogu).
    docs = [ROOT / n for n in pl] + [ROOT / "intro.md"]
    docs += [EN / n for n in en] + [EN / "intro.md"]
    for d in docs:
        if not d.exists():
            continue
        for target in cross_links(d):
            if not (d.parent / target).exists():
                err(f"Martwy link: {d.relative_to(ROOT)} → {target} (brak {d.parent.name}/{target})")

    # 3) Świeżość content.js — musi być zgodny z aktualnymi .md.
    expected, _ = build.content_js()
    actual = (ROOT / "content.js").read_text(encoding="utf-8")
    if expected != actual:
        err("content.js jest nieaktualny — uruchom: python build.py")

    # 4) CHAPTERS (index.html) ↔ pliki ↔ codex.json.
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    chapters = re.findall(r'file:"(\d\d-[a-z0-9-]+\.md)"', html)
    for f in chapters:
        if not (ROOT / f).exists():
            err(f"CHAPTERS: wpis bez pliku PL: {f}")
        if EN.is_dir() and not (EN / f).exists():
            err(f"CHAPTERS: wpis bez pliku EN: en/{f}")
    missing_in_chapters = sorted(set(pl) - set(chapters))
    if missing_in_chapters:
        err(f"CHAPTERS: rozdziały na dysku nieobecne w index.html: {missing_in_chapters}")
    codex = json.loads((ROOT / "codex.json").read_text(encoding="utf-8"))
    if codex.get("chapters") != len(chapters):
        err(f"codex.json chapters={codex.get('chapters')} ≠ liczba rozdziałów ({len(chapters)})")

    # 5) Każdy rozdział wymieniony w README i AI_README (reguła „trzy miejsca w zgodzie").
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    ai = (ROOT / "AI_README.md").read_text(encoding="utf-8")
    for f in pl:
        if f not in readme:
            err(f"README.md nie wymienia rozdziału: {f}")
        if f not in ai:
            err(f"AI_README.md nie wymienia rozdziału: {f}")

    if errors:
        print(f"FAIL — {len(errors)} problem(ów):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK — {len(pl)} rozdziałów PL/EN, content.js świeży, linki i metadane spójne.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
