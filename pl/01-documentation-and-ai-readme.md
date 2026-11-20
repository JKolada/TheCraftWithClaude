# 01 — Dokumentacja i AI_README

> Przykazanie I: *dokumentuj dla agenta, nie dla archiwum.* Cel: następna sesja rozumie katalog bez
> czytania całego jego kodu.

## Trzy warstwy, podzielone wg czytelnika

| Warstwa | Plik | Zawiera |
|---|---|---|
| **Konstytucja** | `CLAUDE.md` (root) | czym jest projekt, dokładne komendy uruchomienia, **polityki nadpisujące domyślne zachowanie**, datowany „Stan bieżący" z liczbami. Ładowany co sesję. |
| **Mapa katalogu** | `AI_README.md` w każdym katalogu z kodem | indeks modułów, kluczowe API (sygnatura + kontrakt), pułapki, liczby, indeks grep. Czytany **zanim** dotkniesz katalogu. |
| **Referencja / plany** | `docs/` | architektura, model danych, runbooki, `plans/`. |

`README.md` to publiczne drzwi wejściowe (czym jest, jak zacząć) — nie warstwa dla agenta. **Gdzie wpisać
fakt? Zapytaj, kto go czyta** — i wpisz raz; pozostałe pliki linkują.

## Reguły

1. **`CLAUDE.md` wskazuje na mapy `AI_README.md`** — bez tego wskaźnika nowa sesja nie wie, że istnieją.
2. **`AI_README.md` aktualizujesz przed commitem**, w tym samym commicie co kod. Indeksu pilnuje test
   (każdy moduł wymieniony, sufit rozmiaru) → [17](17-language-and-guards.md).
3. **Indeks pisz pod `grep`, nie do czytania.** Gęste od słów kluczowych jednolinijkowce: konkretne nazwy,
   synonimy, oba języki w projekcie dwujęzycznym. `grep -i <temat>` ma trafić **jedną linię** wskazującą **jeden plik**.
4. **Jeden plik = jeden temat.** Temat rozsypany po pięciu plikach to pięć trafień i spalony kontekst.
5. **Stan, nie intencja.** Opisuj, co kod robi teraz; kasuj wpisy usuniętego kodu — martwy wpis jest gorszy
   niż żaden. Liczby (rekordy, testy) się starzeją → aktualizuj je.
6. **`docs/` opisuje wyłącznie bieżącą wersję.** Historia żyje w gicie i `CHANGELOG`; aktualizujesz dokument,
   nie trzymasz starej wersji obok.
7. **`docs/plans/` to żywy backlog.** Problem → opcje → wybór → dlaczego. Gdy plan wejdzie, wpisz decyzję do
   dokumentu / `CLAUDE.md`, którym rządzi, i **usuń plan** — git trzyma zapis.
8. **Nowy katalog powstaje razem ze swoim `AI_README.md`** — nigdy „później".
9. **Artefakty generowane (HTML, snapshoty) to pochodne:** commituj, nigdy nie edytuj ręcznie, regeneruj na
   polecenie (skill), nie przy każdym commicie.

Aktualizuj docsy przy: nowym module/funkcji/skrypcie/fladze, zmianie schematu, zmianie zachowania (próg,
fallback), zmianie liczb. Nie przy: czystym bugfixie bez zmiany API, literówkach.

## Antywzorce
- 🚫 „Uzupełnię docsy na końcu" — koniec nie nadchodzi, docsy kłamią.
- 🚫 `AI_README` opisujący życzenia zamiast stanu.
- 🚫 Ten sam stan skopiowany do pięciu plików — jedno źródło prawdy, reszta linkuje.
- 🚫 Ogólnikowe opisy („helpery", „różne reguły") — grep pudłuje, agent czyta wszystko.
