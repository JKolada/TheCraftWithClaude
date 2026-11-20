# 0004 — Prompt dla The Craft Website: aktualizacja do 1.1.2

> **Żywy plan.** Wklej sekcję „Prompt" do sesji Claude otwartej w `ClaudeBuildCodexWeb`. Gdy Web wyda
> stronę zgodną z 1.1.2 — usuń ten plik (git trzyma zapis, → [01](../../01-documentation-and-ai-readme.md)).

---

## Prompt

Aktualizujesz witrynę **The Craft (Rzemiosło Web)** do wersji rdzenia **1.1.2** (repo `ClaudeBuildCodex`,
`craft.json`: `version 1.1.2`, `chapters 20`, `released 2026-11-20`). Rdzeń jest źródłem prawdy dla reguł;
witryna je **prezentuje i rozwija** — nie zmienia ich brzmienia. Najpierw przeczytaj w rdzeniu
`CHANGELOG.md` (wpisy 1.1.1 i 1.1.2), `AI_README.md` i `docs/packaging.md`.

### Co się zmieniło w rdzeniu (i dlaczego to dotyczy witryny)

1. **Przejście tnące — rdzeń to już tylko twarde reguły** (EN ~160 → ~62 tys. znaków). Każdy rozdział ma
   format: wstęp → **Reguły** (numerowane) → **Antywzorce**. **Wszystkie wyjaśnienia, przykłady, definicje i
   historie z incydentów, które wypadły z rdzenia, mają teraz mieszkać na witrynie.** To główne zadanie:
   - pełne poprzednie wersje rozdziałów weźmiesz z historii rdzenia: `git show 9cf2414:<plik>` (stan tuż
     przed cięciem; EN w rootcie, PL w `pl/`);
   - zbuduj z nich strony „rozwinięcie rozdziału NN" (dlaczego, przykład, historia), każda z linkiem do
     zwięzłej reguły w rdzeniu i na odwrót: rdzeń linkuje ogólnie do `https://thecraft.jakub.solutions`.
2. **Nowe rozdziały i podział 05:**
   - **05 Git i wdrożenia** — teraz: historia, cofanie (tabela „najprawdopodobniej tego nie straciłeś"),
     praca równoległa i drabina branchowania, polityka deployu;
   - **17 Język kodu i strażnicy** — nowy (kod po angielsku, także nazwy testów; strażnicy w `guards/`);
   - **18 Próba generalna wydania** (dev → preprod → prod) — wydzielony z 05;
   - **19 Runbook swapu bazy** — wydzielony z 05.
   Zaktualizuj listę/karty rozdziałów (20 pozycji), nawigację, mapę strony, sitemap i `hreflang` dla nowych slugów.
3. **`intro.md` skrócone** do „czym jest / dla kogo / jak zacząć". **Manifest** („dlaczego warto", trzy
   miesiące później, zaczynasz szybko, prywatność od Dnia 0…) przenieś na stronę główną witryny —
   źródło: `git show 9cf2414:intro.md` i `git show 9cf2414:pl/intro.md`.
4. **Instrukcja instalacji (wpięcie w projekt) — zmień tekst na stronie:** wskaźnik zwykłym językiem
   **tylko w `CLAUDE.md` i `AGENTS.md`**, **bez** etykiet `[SYSTEM — READ FIRST]` i **bez** wpisu w
   `README.md` (wyjaśnij na stronie dlaczego: deklaracja autorytetu w pliku wygląda dla modelu jak prompt
   injection). Dokładny tekst wskaźnika: rozdział 07 rdzenia.
5. **Brief:** plik wyjściowy nazywa się teraz **`project-brief.md`** (było `brief-projektu.md`) — popraw
   formularz/generator i teksty na stronie.
6. **Paczka do pobrania (`docs/rules/`):** dołącz katalog **`guards/`** (szablony testów z rozdziału 17);
   **nie** dołączaj `add_chapter.py` (narzędzie autora). Rozdziały `00`–`19`, `pl/` dla wersji EN+PL.
   Szczegóły: `docs/packaging.md`.
7. **Wersja i changelog na witrynie:** stempel **1.1.2** z `craft.json`. Opis wydania dla ludzi (prostym
   językiem): „Rzemiosło jest teraz krótsze i twardsze: same reguły, bez wykładu — wyjaśnienia znajdziesz na
   tej stronie. Nowe: język kodu i strażnicy, próba generalna wydania, runbook podmiany bazy." Dodaj
   adnotację: **„Wersja 1.1.1 przejrzana i odchudzona z Claude Opus 5.5."**
8. **1.1.2 (dodatkowo):** rozdział 08 nie przypina się już do Pythona — język dobiera się do zadania (Go,
   Rust, Kotlin, TypeScript, gdy lepiej pasują; z ADR i pomiarem). Jeśli witryna opisuje stack, popraw to.
   Kontrakt pakowania żyje teraz w `docs/packaging.md` (zastąpił plan 0001).
9. **Wspólna oś wersji:** numery `1.0.1`, `1.0.2` należały do Web, `1.1.0` istniało tylko w kopiach
   u gospodarzy. Jeśli witryna wypuszcza własne wydanie, weź numer, którego rdzeń nie użył — i wpisz je w
   swój changelog.

### Czego nie robić

- Nie przepisuj reguł innymi słowami w miejscu, gdzie występują jako reguły — cytuj rdzeń, rozwijaj obok.
- Nie dokładaj na witrynie reguł, których nie ma w rdzeniu — nowa reguła idzie najpierw do rdzenia.
- Edycje BIZ-TECH / biznesowa zostają planowane; 1.1.1 nie zmienia ich zakresu.

### Gotowe, gdy

- [ ] 20 rozdziałów na liście, nowe slugi `17-language-and-guards`, `18-release-rehearsal`,
      `19-database-swap-runbook` w nawigacji, sitemap i `hreflang` (EN + PL).
- [ ] Każdy rozdział ma stronę rozwinięcia z treścią przeniesioną z `9cf2414`.
- [ ] Manifest na stronie głównej; tekst instalacji bez `SYSTEM` i bez `README.md`.
- [ ] Brief generuje `project-brief.md`.
- [ ] Paczka do pobrania zawiera `guards/`, nie zawiera `add_chapter.py`.
- [ ] Stempel 1.1.2, opis wydań 1.1.1 i 1.1.2, adnotacja o Claude Opus 5.5.
- [ ] Testy witryny zielone (parytet EN/PL, martwe linki).
