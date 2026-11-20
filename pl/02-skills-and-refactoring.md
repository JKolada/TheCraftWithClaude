# 02 — Skille i refaktoring

> Przykazania I i X: automatyzuj to, co się powtarza; refaktoruj tak, by kod czytał się jak sąsiedni.

## Skille (slash-komendy)

1. **Zbuduj skill, gdy** procedura się powtarza (≥3 razy), łatwo pomylić kolejność kroków (migracja:
   numer → SQL → zastosuj → `AI_README` → commit) albo niesie pułapkę specyficzną dla projektu
   (`PYTHONIOENCODING=utf-8` na Windows, `--runInBand` przy działającym serwerze).
2. **Skill ma kontrakt wyjścia** (exit 0 = zielono, inaczej: co padło) i **wypisuje wszystko, co niszczy**.
3. **Skill to przepis dla agenta; hook to automat odpalany przez harness.** „Zawsze rób X po Y" = hook
   w configu, nie skill i nie pamięć.
4. Zestaw startowy: `/run` (serwer + smoke), `/run-tests`, `/update-ai-readme`, `/add-migration` (baza relacyjna).

## Refaktoring

1. **Najpierw szukaj prior art** (`git log -S`, `git blame`) — „brzydki" kształt często ma powód.
2. **Refaktor osobno od zmiany zachowania** — jeden commit to albo porządki, albo funkcja.
3. **Reuse przed przepisaniem** — sprawdź, czy helper już istnieje.
4. **Stare punkty wejścia działają** przy przenosinach (re-eksportujące shimy) albo aktualizujesz wszystkich
   wywołujących w tej samej zmianie.
5. **Małe, sprawdzone kroki:** refaktor → testy zielone → commit.
6. **SOLID proporcjonalnie:** jeden powód do zmiany na moduł; rozszerzaj za flagą zamiast edytować gorącą
   ścieżkę (→ [12](12-flexibility-and-scalability.md)); **żadnej abstrakcji przed drugim konkretnym przypadkiem.**
7. **Dwa tryby review, nigdy razem:** upraszczanie (reuse, czytelność) vs poprawność (adwersarialne szukanie bugów).

## Antywzorce
- 🚫 Skill na coś robionego raz.
- 🚫 Skill, który po cichu robi coś destrukcyjnego.
- 🚫 Przepisanie od zera, po którym nikt nie wie, co się zepsuło.
- 🚫 Pięć warstw i fabryka dla CRUD-a na trzy pola.
