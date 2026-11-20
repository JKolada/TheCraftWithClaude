# 19 — Runbook swapu bazy

> Przykazanie VII w najtrudniejszej postaci: wymiana całej bazy proda (np. przebudowanego katalogu) **z
> zachowaniem każdego żywego konta i wszystkiego, co userzy stworzyli.** Rzadkie — i to tu leży najwięcej pułapek.

## Reguły, które ratują dane userów

1. **„Userzy" to wiele tabel.** Wylicz **każdą** tabelę z kluczem obcym do usera (konta, koszyki, recenzje,
   polubienia, odznaki, sesje, sesje czatu + wiadomości + limity, feedback…). Tabelę bez `user_id` mapujesz
   przez jej rodzica. Każdą bramkuj istnieniem tabeli/kolumny.
2. **Mapuj po stabilnym kluczu (slug → nowe id), nigdy po starym id.** Brakujący slug pomijasz i logujesz.
3. **Źródłem prawdy dla kont jest żywy prod**, czytany po `stop` w oknie maintenance — nie starszy snapshot,
   który gubi rejestracje z ostatniej godziny.
4. **Kolejność bezpieczna dla FK:** usuwaj dzieci przed rodzicami, wstawiaj rodziców przed dziećmi.
5. **Backup żywego proda tuż przed swapem** (`.backup replaced-prod-<ts>.db`) — to jest rollback.
6. **Zweryfikuj scaloną bazę:** liczba kont = prod, 0 wiszących odwołań, `integrity_check: ok`, naruszenia FK
   nie wyżej niż stan zastany.
7. **Sesje żyją we własnym store** (np. `sessions.db`), nigdy w podmienianej bazie i nigdy w pamięci procesu —
   inaczej swap albo dowolny restart wylogowuje wszystkich (→ [14](14-operational-resilience.md)).

## Sekwencja

1. **Faza na żywo:** wypchnij kod; skopiuj gitignorowane assety **przed** oknem (rsync / tar po ssh, tylko
   delta) — nie jadą przez `git pull`; wgraj nowy snapshot na serwer.
2. **Okno (sekundy, atomowo, `set -e`):** flaga ON → pull → stop → backup żywego proda → migracja userów
   (źródło = prod) → podmiana pliku (usuń `-wal`/`-shm`, przenieś, włącz z powrotem WAL) → start → **smoke** → flaga OFF.
3. **Smoke przez `localhost`** (omija stronę maintenance): kluczowe strony 200, redirecty, liczby wierszy, czyste
   logi procesu. Trywialny, bezpieczny bug znaleziony w oknie naprawiasz w oknie — nie wypuszczaj znanego 500.
4. **Po:** otaguj deploy, posprzątaj pliki tymczasowe, wpisz lekcje do runbooka (→ [05](05-git-and-deployments.md)).

## Antywzorce
- 🚫 Swap „prócz kont" trzymający tylko tabelę `users` — recenzje, odznaki i czat przepadają.
- 🚫 Mapowanie danych userów po id — recenzje lądują na złym produkcie.
- 🚫 Migracja kont ze starego snapshotu.
- 🚫 Przenoszenie gigabajtów assetów w trakcie okna.
- 🚫 `scp` żywej `.db` — użyj `.backup`; WAL trzyma świeże strony.
