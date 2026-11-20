# 04 — Skrypty i bazy danych

> Przykazania IV i V: *dry-run jest domyślny; backup to rollback.*

## Skrypty

1. **Domyślnie dry-run.** Skrypt zmieniający dane wypisuje plan (co, ile wierszy, gdzie); świadome
   `--execute` zapisuje.
2. **Idempotentny.** Dwa przebiegi dają ten sam stan (`INSERT OR IGNORE` / `UPSERT`).
3. **Wypisz, czego *nie* zrobiłeś** — ucięcie, próbkowanie, pominięte wiersze. Cisza czyta się jak „pokryłem wszystko".
4. **Operacje mutujące katalog trzymaj poza automatycznymi pipeline'ami** (dedup, merge): dry-run → review → ręczne `--execute`.
5. **Środowisko jest zapisane w `CLAUDE.md`** — interpreter, zmienne, venv. Agent nie zgaduje.
6. **Ścieżki absolutne, gdy wartość przechodzi między narzędziami.** `/tmp` to jedno miejsce dla Git Bash,
   inne dla Pythona na Windows, trzecie dla PowerShell — każde narzędzie czyta wtedy *inny plik*. Przekazuj
   pełne ścieżki; gdy przebieg „nic nie zrobił", wypisz `os.path.abspath(p)` / `pwd -W` i porównaj.

## Bazy i migracje

1. **Migracje forward-only.** Bez down-migracji; cofnięcie schematu = przywrócenie backupu.
2. **Backup przed każdą zmianą schematu/danych na prodzie**, z timestampem i retencją:
   `sqlite3 data/app.db ".backup backups/pre-deploy-$(date +%F_%H%M%S).db"`
3. **Snapshot przez `.backup` / `VACUUM INTO`, nigdy `cp`/`scp` żywej bazy** — WAL robi kopię niespójną.
4. **Additive przed destructive.** `ADD COLUMN` jest bezpieczne; `DROP`/`RENAME` czeka na późniejszy deploy,
   gdy żaden działający kod nie czyta kolumny.
5. **Integralność po każdej operacji na danych:** `integrity_check`, `foreign_key_check`, liczby wierszy.
   Odróżnij szum zastany (jest przed i po) od regresji (nowe naruszenia).
6. **Masową albo nieodwracalną mutację przećwicz na świeżej kopii proda** — dry-run pokazuje plan, nie wynik.
   `.backup` proda → przebieg na kopii → sprawdź liczby, integralność i trudne przypadki → dopiero prod.
   Brat tej reguły na poziomie deployu → [18](18-release-rehearsal.md).

## Antywzorce
- 🚫 Skrypt mutujący bez `--dry-run`.
- 🚫 Migracja wdrożona bez backupu „bo additive".
- 🚫 `DROP` kolumny, którą czyta działający kod.
- 🚫 `cp app.db` przy działającym serwerze.
- 🚫 Krok mutujący katalog wpięty w automatyczny pipeline.
