# 17 — Język kodu i strażnicy, którzy trzymają reguły przy życiu

> Przykazania I i III zastosowane do nazw: reguła, która żyje tylko w czyjejś głowie, nie jest regułą,
> a reguła bez testu to życzenie.

## Dwa języki, podzielone wg czytelnika

| Warstwa | Język |
|---|---|
| **Kod** — identyfikatory (moduły, klasy, funkcje, zmienne, fixture'y, **nazwy testów**), nazwy plików kodu, tabele i kolumny bazy, flagi CLI, klucze configu i API, wartości enumów/stanów, klucze logów, opisy commitów | **angielski, zawsze** |
| **Proza** — docsy, plany, `AI_README`, komentarze, docstringi, tekst dla usera | **język projektu**, zadeklarowany raz w `CLAUDE.md` |

```
# CLAUDE.md
Code: English (identifiers, tests, DB, CLI, keys). Prose: Polish (docs, comments, docstrings, UI).
```

## Reguły

1. **Angielski kod to język ekosystemu** — narzędzia, autouzupełnianie, błędy i następny inżynier mówią nim;
   identyfikator w języku natywnym transliteruje się na trzy różne sposoby.
2. **Testy to kod.** `test_<podmiot>_<warunek>_<oczekiwanie>` po angielsku; *dlaczego* (incydent, data, koszt)
   trafia do docstringa, w języku prozy.
3. **Żadnych mieszanych identyfikatorów** (`test_cost_NIE_ISTNIEJE_in_window`) — nieczytelne i niegrepowalne.
4. **Nazwy, które drukuje narzędzie, zostają po angielsku wewnątrz prozy** — komenda, flaga, status, plik
   albo tag (`commit`, `--dry-run`, `migrate.py`, `deploy-*`): to ich szukasz grepem. Zwykłe słowo na samą
   czynność może być w języku prozy („wdrożenie" na deploy).
5. **Reguła bez strażnika to życzenie.** Jedna sesja wypuściła 95 z 98 commitów bez dotknięcia indeksu,
   który miała aktualizować. Reguły, które mają przeżyć długą sesję, egzekwuje suite testów.

## Dwa strażniki (gotowe w `guards/`)

Skopiuj je do `tests/` projektu jako `test_ai_readme.py` i `test_code_language.py`, dopasuj listy katalogów,
odpal, zacommituj baseline — w **pierwszym commicie** (→ [07](07-new-project-day-0.md)).
To **referencyjne implementacje w pyteście**: projekt w Pythonie je kopiuje; projekt w Go, Rust, Kotlinie albo
TypeScripcie przenosi tę samą specyfikację do własnego test runnera (strażnik indeksu potrzebuje tylko globów
plików; strażnik języka — parsera identyfikatorów albo lintera danego języka). Regułą jest specyfikacja, nie plik w Pythonie.

- **[`guards/ai_readme_guard.py`](../guards/ai_readme_guard.py)** — każdy katalog z kodem ma `AI_README.md`;
  **każdy moduł jest w nim wymieniony**; **sufit 20 kB** (powyżej indeks przestaje być indeksem — dziel
  katalog, nie plik); lista pilnowanych katalogów pilnuje sama siebie. Nie oceni, czy opis jest *aktualny* —
  to zostaje obowiązkiem piszącego.
- **[`guards/code_language_guard.py`](../guards/code_language_guard.py)** — oznacza identyfikatory wyglądające
  na język prozy (stop-lista słów funkcyjnych + kształt liter); **zapadka** z baselinem per plik.

## Zapadka — jak wprowadzić dowolną regułę do starego kodu

1. **Zamroź** dzisiejszą liczbę per plik w zacommitowanym baselinie (w nowym projekcie pusty).
2. **Nowe pliki muszą być czyste** od dnia, w którym reguła powstała.
3. **Liczby mogą tylko spadać;** gdy spadnie, obniż baseline **na polecenie** (`--write-baseline`), nigdy po cichu.
4. **Ręczne podniesienie baseline'u to osłabienie strażnika** — ten sam grzech co pominięcie testu.
5. **Wyjątki są datowane**, ograniczone do dzisiejszego rozmiaru i powiązane z zadaniem w backlogu, które je usuwa.

Wpinasz doktrynę do istniejącego projektu: odpal strażnika języka raz, zacommituj baseline taki, jaki jest,
i wpisz do backlogu „przemianuj obce identyfikatory — zostało N", z liczbą.

## Antywzorce
- 🚫 „Nazwy testów to nie kod."
- 🚫 Identyfikatory mieszające języki.
- 🚫 Tłumaczenie nazwy, którą drukuje narzędzie (`--dry-run` jako „próba").
- 🚫 Reguła w `CLAUDE.md` bez testu za nią.
- 🚫 Podniesienie baseline'u, żeby suite był zielony.
- 🚫 `AI_README` ponad sufitem, „bo tu wszystko jest ważne".
