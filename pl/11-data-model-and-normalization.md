# 11 — Model danych i normalizacja

> Przykazania V i VII u korzenia: schemat to kontrakt całego systemu. Najpierw normalizuj; denormalizuj
> świadomie, z nazwanym źródłem prawdy.

## Reguły

1. **Słowniki kontrolowane żyją w tabelach lookup** (kraje, typy, tagi) plus `CHECK` tam, gdzie wartości
   są stałe — nigdy wolny tekst w kolumnie.
2. **Relacja wiele-do-wielu idzie przez tabelę łączącą**, nigdy kolumny `primary_x` + `secondary_x`.
3. **Stabilnym identyfikatorem jest slug, nie numeryczne id.** Id dryfują po merge'ach; dane userów mapujesz
   `slug → nowe id`, brakujący slug pomijasz i logujesz (→ [19](19-database-swap-runbook.md)).
4. **Aktywny wiersz zamiast nadpisywania tam, gdzie historia ma wartość:** wygaś stary wiersz (`expired_at`),
   wstaw nowy; partial unique index (`WHERE expired_at IS NULL`) pilnuje jednego aktywnego na klucz. Audyt za darmo.
5. **Wartości liczone są liczone, nie zapisywane** (np. nazwa wyświetlana z części) — zapisane dryfują.
6. **Cache albo snapshot nazywa swoje źródło prawdy** i wraca do niego, gdy jest nieaktualny; nigdy dwa źródła jednego faktu.
7. **Migracje są forward-only i addytywne**, skrypty sprawdzają istnienie kolumny/tabeli, a każda operacja
   na danych kończy się `foreign_key_check` (→ [04](04-scripts-and-databases.md)).
8. **Schemat jest udokumentowany:** ERD plus dozwolone wartości każdego pola słownikowego, w `docs/`.
9. **Zadeklarowanej prywatności pilnuje model:** wrażliwe przetwarzanie to osobny, idempotentny pipeline na
   danych **zanonimizowanych**, z testem, że reidentyfikacja jest niemożliwa (→ [09](09-law-and-protecting-the-creator.md)).

## Antywzorce
- 🚫 Wolny tekst tam, gdzie powinien być lookup („USA", „U.S.A.", „United States").
- 🚫 Jeden fakt trzymany w dwóch miejscach bez synchronizacji.
- 🚫 Dane userów mapowane po zmiennym id.
- 🚫 Zapisana wartość liczona, która dryfuje.
- 🚫 Destrukcyjna migracja pod działającym starym kodem.
