# 17 — Język kodu i strażnicy, którzy trzymają reguły przy życiu

> Przykazania I i III zastosowane do *nazw*: reguła, która żyje tylko w czyjejś głowie, nie jest
> regułą, a reguła bez testu jest życzeniem.

## Dwa języki, podzielone po czytelniku — nigdy po nastroju

Każde repozytorium ma dwóch odbiorców i każda warstwa jest pisana dla dokładnie jednego z nich.

| Warstwa | Kto to czyta | Język |
|---------|--------------|-------|
| **Kod** — identyfikatory (nazwy modułów, klas, funkcji, zmiennych, fixture'ów i **testów**), nazwy plików kodu, tabele i kolumny bazy, flagi CLI, klucze konfiguracji i kontraktów API/JSON, wartości enumów i stanów, klucze logów, tematy commitów | maszyna, `grep`, wyjście CI, każdy przyszły inżynier i agent | **Angielski. Zawsze. Bez wyjątków.** |
| **Proza** — dokumentacja, plany, `AI_README`, komentarze i docstringi, teksty dla użytkownika (etykiety UI, wyjście CLI dla człowieka, e-maile, changelog) | właściciel i jego użytkownicy | **język projektu**, zadeklarowany **raz** w `CLAUDE.md` |

Angielski w kodzie to nie preferencja — to język ekosystemu: każdej biblioteki, komunikatu błędu,
odpowiedzi na Stack Overflow i treningu samego agenta. Polski (albo niemiecki, albo hiszpański)
identyfikator to słowo, którego narzędzia nigdy nie widziały, którego autouzupełnianie nie podpowie
i które następny inżynier zapisze na trzy sposoby. Proza jest odwrotnością: czyta ją właściciel,
myśli w niej, a *dlaczego* stojące za decyzją traci w drugim języku precyzję. Dlatego podział idzie
za **czytelnikiem** i jest ustalony na starcie:

```
# CLAUDE.md
Kod: angielski (identyfikatory, testy, baza, CLI, klucze). Proza: polski (docs, komentarze, docstringi, UI).
```

**Nazwy, które drukuje narzędzie, zostają po angielsku wewnątrz prozy** — komenda, flaga, status, plik
albo tag (`commit`, `--dry-run`, `migrate.py`, `deploy-*`): to ich szukasz grepem. Zwykłe słowo na samą
czynność może być w języku prozy („wdrożenie" na deploy) — tak robi polskie tłumaczenie tej doktryny.

### Testy są kodem

Nazwa testu jest identyfikatorem: drukuje ją runner, grepuje CI, raport z porażki o trzeciej w nocy
składa się wyłącznie z niej. `test_<podmiot>_<warunek>_<oczekiwanie>`, po angielsku. *Dlaczego* —
incydent, data, cena błędu — idzie do **docstringa**, w języku prozy, tam gdzie jego miejsce:

```python
# przed — dla oka wygląda jak kod, dla nikogo nie czyta się jak cokolwiek
def test_koszt_wobec_zysku_brutto_NIE_ISTNIEJE_w_stratnym_podoknie(conn): ...

# po
def test_cost_share_is_none_in_a_losing_window(conn):
    """Źródło 30% `NULL` w kolumnie kosztu z pomiaru 2026-09-26: miara to koszt / zysk
    brutto, więc w stratnym podoknie mianownik nie istnieje — silnik oddaje `None` z zamiarem."""
```

**Identyfikatory mieszane to najgorsze z obu światów.** `test_cost_NIE_ISTNIEJE_in_window` nie da się
ani wyszukać, ani przeczytać. Fixture'y, helpery i identyfikatory parametrize podlegają tej samej
regule — fixture o nazwie `szablon_bazy` to dwujęzyczne API.

## Reguła bez strażnika jest życzeniem

„Każdy katalog ma `AI_README`, aktualizowane **przed** commitem" jest Przykazaniem I tej doktryny od
pierwszego dnia. W projekcie referencyjnym jedna sesja i tak wysłała **95 z 98 commitów z kodem bez
dotknięcia indeksu** — nie ze złej woli: agent przeczytał konstytucję (która deleguje do map) i nigdy
nie otworzył przykazania mówiącego *aktualizuj przed commitem*. Reguły dokumentacji i nazewnictwa
konkurują z bieżącym zadaniem i przegrywają za każdym razem, chyba że coś czerwonego zatrzyma commit.
**Jedyne reguły, które przeżywają kontakt z długą sesją, to te egzekwowane przez zestaw testów.**
Dlatego każda reguła z tego rozdziału jedzie ze strażnikiem: czysty pytest na bibliotece
standardowej, do skopiowania, wpinany w Dniu 0 (→ [07](07-new-project-day-0.md)).

### Strażnik 1 — strażnik indeksu `AI_README`

Czego pilnuje:

1. każdy katalog z modułami kodu ma `AI_README.md`;
2. **każdy moduł z tego katalogu jest w nim wymieniony** — indeks istnieje dla `grep`, a moduł
   nieobecny w indeksie jest dla następnej sesji niewidzialny (→ [01](01-documentation-and-ai-readme.md));
3. lista pilnowanych katalogów pilnuje sama siebie: nowy katalog z modułami i indeksem trzeba do niej
   dopisać, inaczej test pada;
4. **sufit rozmiaru — 20 kB.** `AI_README` jest celem dla `grep`, nie powieścią; ponad sufitem
   przestaje być indeksem. Ponad limitem dziel **katalog** (→ [12](12-flexibility-and-scalability.md)),
   nie plik.

Czego **nie umie** sprawdzić: czy opis jest *aktualny*. Nieaktualne zdanie przechodzi. Obowiązek
aktualizacji przed commitem zostaje po stronie piszącego — strażnik zdejmuje tylko najgorszą awarię,
nieobecność.

```python
# tests/test_ai_readme.py — stdlib + pytest; GUARDED i SKIPPED dopasuj do projektu
import pathlib, pytest
ROOT = pathlib.Path(__file__).resolve().parents[1]
GUARDED = ("app", "app/core", "scripts", "tests")          # katalogi z kodem I indeksem
SKIPPED = {"__init__.py", "conftest.py"}                    # nie ma czego opisywać
INDEX_MAX_BYTES = 20_000

def modules(d): return sorted(p.name for p in (ROOT / d).glob("*.py") if p.name not in SKIPPED)
def index(d):   return (ROOT / d / "AI_README.md").read_text(encoding="utf-8")

@pytest.mark.parametrize("d", GUARDED)
def test_every_module_is_in_the_index(d):
    text = index(d)
    missing = [m for m in modules(d) if m not in text and m.removesuffix(".py") not in text]
    assert not missing, f"{d}/AI_README.md does not mention: {missing}"

@pytest.mark.parametrize("d", GUARDED)
def test_index_fits_the_grep_ceiling(d):
    assert (ROOT / d / "AI_README.md").stat().st_size <= INDEX_MAX_BYTES

def test_guarded_list_is_complete():
    with_index = {str(p.parent.relative_to(ROOT)) for p in ROOT.rglob("AI_README.md")
                  if list(p.parent.glob("*.py"))}
    assert with_index <= set(GUARDED), f"add to GUARDED: {with_index - set(GUARDED)}"
```

### Strażnik 2 — strażnik języka kodu (zapadka)

Heurystyka per token, nie słownik: podziel identyfikator po `_` i CamelCase, oznacz token, który jest
na **liście słów funkcyjnych języka prozy** (dla polskiego: `nie`, `jest`, `bez`, `gdy`, `czy`,
`dla`…) albo ma **kształt** tego języka (polski: `cz`/`rz`/`sz`/`dz` w środku, końcówki `-uje`,
`-osci`, `-anie`, `-owy`, `-nych`). Trzymaj jawną listę angielskich sobowtórów (`ego`, `media`,
`wizard`) i pogódź się, że część słów przepuści: to zapadka, nie sąd.

```python
# tests/test_code_language.py — rdzeń; pełną wersję ma projekt referencyjny
import ast, json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
SCANNED = ("app", "scripts", "tests")
BASELINE = ROOT / "tests" / "code_language_baseline.json"       # {"ścieżka": liczba}
STOP = {"nie", "jest", "bez", "gdy", "czy", "dla", "przy", "tylko", "albo", "oraz"}
SHAPE = re.compile(r"cz|rz|sz|dz|(?:uje|osci|anie|enie|owy|owa|owe|nych|nego)$")

def tokens(name): return [t.lower() for t in re.split(r"_+|(?<=[a-z0-9])(?=[A-Z])", name) if t]
def looks_foreign(name): return any(t in STOP or (len(t) >= 4 and SHAPE.search(t)) for t in tokens(name))
def names(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return [path.stem] + [n.name for n in ast.walk(tree)
                          if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
def scan():
    return {p.relative_to(ROOT).as_posix(): [n for n in names(p) if looks_foreign(n)]
            for top in SCANNED for p in (ROOT / top).rglob("*.py") if any(looks_foreign(n) for n in names(p))}

def test_ratchet():
    base = json.loads(BASELINE.read_text()) if BASELINE.exists() else {}
    now = {k: len(v) for k, v in scan().items()}
    assert not {k for k in now if k not in base}, "new files must be clean"
    assert not {k for k in now if now[k] > base.get(k, 0)}, "a file gained foreign names"
    assert not {k for k in base if now.get(k, 0) < base[k]}, "tighten the baseline (--write-baseline)"
```

### Zapadka — jak wprowadzić dowolną regułę do starego kodu

1. **Zamroź** bieżącą liczbę per plik w baselinie i zacommituj (w projekcie od zera jest pusty).
2. **Nowe pliki muszą być czyste.** Reguła jest bezwzględna od dnia, w którym została spisana.
3. **Liczby mogą tylko spadać.** Każde dotknięcie pliku jest okazją do zaciśnięcia; nikt nie musi
   przepisywać dwóch tysięcy nazw naraz i nikt nie ma prawa dopisać dwutysięcznej pierwszej.
4. **Gdy liczba spadła, obniż baseline na komendę** (`--write-baseline`), nigdy po cichu. Baseline
   luźniejszy niż kod pozwala starej liczbie wrócić bez słowa.
5. **Ręczne podniesienie liczby w baselinie to osłabienie strażnika** — ten sam grzech co pominięcie testu.
6. **Wyjątki datowane** (za duży indeks czekający na podział katalogu) niosą datę, sufit równy
   *dzisiejszemu* rozmiarowi i pozycję backlogu, która je zdejmuje.

## Wpięcie w Dniu 0

- Zadeklaruj język prozy w `CLAUDE.md` (dwie linie — wyżej). → [07](07-new-project-day-0.md)
- Skopiuj oba strażniki do `tests/` **w pierwszym commicie**; uruchom; zacommituj baseline.
- Wpinasz tę doktrynę w istniejący projekt: uruchom strażnika 2 raz, zacommituj baseline taki, jaki
  jest, i wpisz do backlogu „przemianować obce identyfikatory na angielskie — zostało N" z liczbą.
  Projekt referencyjny startował z 2 938 identyfikatorów w 129 plikach, prawie wszystko nazwy testów.
- Wpisz nazwy plików strażników do `tests/AI_README.md` — podlegają strażnikowi 1 jak każdy moduł.

## Antywzorce

- 🚫 „Testy to nie prawdziwy kod, więc ich nazwy mogą być w moim języku." — runner jest innego zdania.
- 🚫 Identyfikatory mieszane (`test_cost_NIE_ISTNIEJE_in_window`) — nieczytelne *i* niegrepowalne.
- 🚫 Tłumaczenie nazwy, którą drukuje narzędzie — flagi, statusu, pliku, tagu (`--dry-run` jako „próba",
  tag `deploy-*` jako „wdrozenie-*") — przestaje pasować do tego, czego szukasz grepem.
- 🚫 Reguła zapisana w `CLAUDE.md` bez testu za nią — następna sesja złamie ją w dobrej wierze.
- 🚫 Podnoszenie baseline'u, żeby zestaw był zielony.
- 🚫 `AI_README`, które rośnie ponad sufit, bo „wszystko tu jest ważne" — przestało być indeksem
  w chwili, gdy `grep` zwraca cały plik.
