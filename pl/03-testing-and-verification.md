# 03 — Testowanie i weryfikacja

> Przykazanie III: *weryfikuj, nie deklaruj.* Testy to siatka odpalana w kółko; weryfikacja to
> zaobserwowany dowód, że **ta** zmiana robi, co miała. Oba są obowiązkowe.

## Reguły

1. **Każdy commit zmieniający zachowanie niesie test.** Nowy endpoint → test trasy; nowy próg lub fallback →
   test progu; naprawiony bug → test, który najpierw go odtworzył. Zmiana zachowania bez testu to commit
   **niekompletny**. TDD (czerwony → zielony → refaktor) to tryb domyślny.
2. **Pokaż dowód, nie proś usera o sprawdzenie:** kod HTTP / redirect, potwierdzający fragment HTML, liczby
   z bazy (`integrity_check: ok`), screenshot przy zmianach wizualnych.
3. **Smoke test sprawdza właściwą stronę, nie tylko `200`** — marker dowodzący, że wyrenderowała się
   oczekiwana treść. Auth testuj z obu stron: anonim odbity, zalogowany widzi treść.
4. **Po deployu smoke na żywym serwerze** (przez `localhost` za flagą maintenance).
5. **Raportuj uczciwie:** porażki z outputem; pominięte kroki jako pominięte; porażkę z dryfu danych
   (nieaktualny fixture) nazwij po imieniu, z follow-upem — nie chowaj i nie traktuj jako blokady.
6. **Liczby bierzesz u źródła**, nie z pamięci ani z docsów: `SELECT COUNT(*)` nie kłamie.
7. **Guard dowodzi incydent, nie fixture.** Check napisany po awarii odtwarzasz na **realnych danych** tej
   awarii, zanim mu zaufasz — fixture dzieli martwe pole autora (check świeżości przeszedł kiedyś dziewięć
   zielonych testów i przegapił własną awarię: `>` tam, gdzie trzeba było `>=`). Potem zamroź próg w fixture,
   z testem **na** samym progu.
8. **Testuj kontrakt, nie implementację; suite szybki i deterministyczny** (izolowane I/O, seedy, testy
   dzielące port/bazę szeregowo). **CI bramkuje** merge i deploy.
9. **Projekty webowe niosą domyślnie:** meta SEO per strona, canonical + hreflang, JSON-LD, kontrast kolorów
   i nawigację klawiaturą, **parytet językowy jako test, który pada**, brak martwych linków wewnętrznych.

## Antywzorce
- 🚫 „Powinno działać" jako konkluzja.
- 🚫 Jeden test odpalony, „suite zielony" ogłoszony.
- 🚫 Brak smoke po deployu, „bo testy przeszły".
- 🚫 „Kompiluje się" pomylone z „działa dla usera".
- 🚫 Osłabienie testu albo guarda, żeby zrobił się zielony.
