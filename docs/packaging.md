# Pakowanie `docs/rules/` — kontrakt z The Craft Web

> Dokument stanu bieżącego (nie plan). Podział ról: **to repo** trzyma kanoniczną treść w każdym języku
> (EN w rootcie = baza, PL w `pl/`), **Rzemiosło Web** renderuje witrynę, edycje i **składa paczki**.
> Tłumaczeń nie robi się po stronie Web w oderwaniu od źródła — parytet pilnuje `test.py`.

Paczka = przeglądalny pakiet doktryny: agent go grepuje (`AI_README`), człowiek przegląda czytnikiem
(dwuklik `index.html`). Wypada tylko meta utrzymania tego repo.

## Pakuj

- **Treść:** `AI_README.md`, wszystkie numerowane rozdziały `NN-*.md`, `intro.md`, **`guards/`** (szablony
  testów z rozdziału 17 — celowo bez nazw `test_*.py`, żeby pytest gospodarza ich nie zbierał).
- **Języki:** `pl/` (i kolejne `<lang>/`) dla pełnego przełącznika w czytniku; paczka jednojęzyczna je pomija.
- **Stempel:** `craft.json` (`version`, `released`, `languages`, `edition`).
- **Czytnik:** `index.html` + `content.js` (działa po `file://`), `build.py` (odświeżenie snapshotu),
  `public/logo.png`.

## Nie pakuj

`CLAUDE.md` (konstytucja tego repo — gospodarz ma własny), `README.md`, `CHANGELOG.md`, `docs/`, `test.py`,
`add_chapter.py`, `.claude/`, `.git*`.

## Układ

```
docs/rules/
  AI_README.md  intro.md  craft.json  guards/
  00-commandments.md … NN-*.md                        # treść EN
  pl/  AI_README.md  intro.md  00-….md                 # treść PL
  index.html  content.js  build.py  public/logo.png   # czytnik
```

## Zasady

- **Cross-linki `[NN](NN-nazwa.md)` działają bez zmian** — jeden katalog, slugi wspólne dla języków.
- **Paczka EN+PL** = działający przełącznik języka; **jednojęzyczna** = mniejsza, czytnik bez drugiego języka.
- **Edycje** (techniczna / BIZ-TECH / biznesowa): ten sam zestaw plików, inny rejestr → pole `edition`; dziś
  wydawana jest tylko techniczna.
- **Wpięcie u gospodarza** (→ [07](../07-new-project-day-0.md)): submoduł albo kopia + zwykły wskaźnik
  (bez etykiet `SYSTEM`) na górze `CLAUDE.md` i `AGENTS.md` projektu. Rozesłanie nowej wersji = **pełna
  podmiana** `docs/rules/` (w środku nie ma treści własnej gospodarza).
