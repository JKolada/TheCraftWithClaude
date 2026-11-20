# 05 — Git i wdrożenia

> Przykazania II, VI, VIII, IX. Git to pamięć projektu i przycisk cofania dla całej reszty; polityka
> deployu to miejsce, gdzie błąd kosztuje najwięcej. Próba na preprodzie → [18](18-release-rehearsal.md);
> swap bazy proda → [19](19-database-swap-runbook.md).

## Nawyki w gicie

1. **Szukaj w historii, zanim zaimplementujesz:**
   ```bash
   git log -S"symbol" --oneline     # gdzie narodził się symbol/flaga/kolumna
   git log -G"regex" --oneline      # commity, których diff pasuje
   git log --grep="słowo" --oneline # opisy commitów
   git blame <plik> -L a,b          # kto/kiedy/dlaczego
   ```
2. **Trzymaj `git status` czysty.** Jeden temat na commit. Śmieci (`.bak`, pliki tymczasowe, przypadkowe
   bazy) wcześnie do `.gitignore` (komentarz `#` w osobnej linii). Plik widoczny jako zmieniony przy pustym
   `git diff HEAD` to szum CRLF, nie praca — nie commituj go.
3. **Sieroty:** niezacommitowana praca, której nie pisałeś (innej sesji), **nigdy nie trafia do Twojego
   commita ani deployu** bez potwierdzenia — zapytaj, czy to skończona praca, czy eksperyment.
4. **Opisy commitów po angielsku**, co + dlaczego, `refs #N` / `fixes #N`.

## Cofanie: najprawdopodobniej tego nie straciłeś

Zacommitowana praca jest do odzyskania; git pamięta każdą pozycję gałęzi (~90 dni). **Commituj wcześnie** —
commit jest darmowy, prywatny do pushu i jest Twoim punktem zapisu.

| Sytuacja | Droga powrotna |
|---|---|
| Rozwalony plik, bez commita | `git restore <plik>` |
| Cofnij ostatni commit, zostaw pracę | `git reset --soft HEAD~1` |
| Commit na złej gałęzi | `git branch <właściwa>` tutaj, potem `git reset --hard HEAD~1` na złej |
| Skasowana gałąź / „zgubione" commity | `git reflog` → znajdź hash → `git branch <nazwa> <hash>` |
| Merge poszedł źle (bez pushu) | `git reset --hard ORIG_HEAD` |
| Potrzebny plik w dawnej wersji | `git show <commit>:<ścieżka>` · `git restore --source=<commit> -- <ścieżka>` |

Tylko trzy komendy niszczą pracę — i tylko **niezacommitowaną**: `git reset --hard`, `git restore .` /
`git checkout .`, `git clean -fd`. Git nie ma dla nich dry-runu: **wcześniejszy commit jest dry-runem** (→ IV).

## Praca równoległa: issues i krótkie gałęzie

„Solo" to i tak wielu piszących: jeden developer rutynowo odpala **kilka sesji Claude** na jednym repo.
„Drugą stroną" jest zwykle inna sesja — czytaj „współpracownik" jako „inna sesja".

1. **Jedno zadanie = jeden issue**: tytuł = rezultat, treść = kontekst + kryteria zaliczenia. Numer issue
   spina gałąź, commity i PR; zamyka go **PR/merge**, nie commit na gałęzi roboczej.
2. **Krótkie gałęzie** (`feat/NN-koszyk`, `fix/NN-logowanie`) żyjące godziny–dni; małe PR-y; merge, kasuj,
   synchronizuj się z `main` często.
3. **Diff przed mergem do gałęzi deployu** — merge wnosi *każdy* commit ze źródła, także pracę innych sesji:
   `git log <deploy>..<źródło> --oneline`. Pilny izolowany fix idzie **cherry-pickiem**.
4. **Po każdym cherry-picku sprawdź wynik:** `git diff <baza-deployu> HEAD --stat` ma pokazać tylko Twoją
   zmianę — fallback 3-way potrafi wciągnąć cudzy hunk (zabłąkany `require` → crash przy starcie → 502).
5. **Jedna równoległa sesja = jeden `git worktree`**, nigdy dwie sesje w jednym checkoucie (→ [16](16-driving-claude.md)).

**Branching rośnie z projektem — każdy szczebel dokładasz, gdy wymusi go metryka:**
1. Solo, brak żywych userów → sam `main`, commitowany z dyscypliną.
2. Pierwsze wdrożenie produkcyjne → każda zmiana na krótkiej gałęzi, przejrzana, zmergowana do zawsze-wdrażalnego `main`, deploy otagowany.
3. Więcej osób / równoległe nurty → `develop` do integracji, wydania `develop → main`, najpierw sprawdzone
   na preprodzie — kopii proda (→ [18](18-release-rehearsal.md)).

Każda zmiana trafia na `main` przejrzana — solo recenzentem jest świadomy drugi przegląd diffu.

## Wdrożenia — polityka nadrzędna

> ⛔ **Nigdy nie deployuj na prod automatycznie.** Pull na serwerze, reload, migracja, swap bazy, flaga
> maintenance — **tylko na wyraźne „wdrażaj" użytkownika.** Możesz zaproponować deploy; czekasz na „tak".
> Commit i push to nie deploy. Ta reguła bije każdy tryb auto.

1. **Serwer wdraża `origin/<gałąź>`, nie Twój laptop.** Przed każdym deployem: `git fetch`, potem
   `git log origin/<g>..<g>` (niewypchnięte commity → najpierw push) i `git log <g>..origin/<g>` (inna sesja
   wypchnęła → najpierw pull).
2. **Boot-check na celu przed reloadem:** po pullu uruchom nowy kod w jednorazowym procesie
   (`node -e "require('./src/app')"`, z `listen` za `require.main === module`); reload **tylko** na jego
   marker OK. Crash zostawia wtedy stary proces w pracy.
3. **Dwa typy deployu.** Sam kod → pull + boot-check + reload bez przestoju. Migracja / zmiana zależności /
   swap bazy → **okno maintenance** (firmowa strona 503), żeby nic nie działało na pół-zmigrowanym schemacie.
4. **Taguj każdy deploy:** `git tag -a deploy-$(date +%F) -m "<co idzie live>"` + `git push --tags`.
   Co jest live: `git describe --tags --abbrev=0 --match 'deploy-*'`. Rollback kodu = checkout tagu + reload;
   rollback schematu = przywrócenie backupu.
5. **Każdy deploy aktualizuje publiczny changelog** prostym językiem — co user zyskuje.
6. **Każdy incydent na prodzie staje się datowaną, numerowaną lekcją w runbooku** (`docs/`), czytaną przed
   kolejnym deployem (→ [14](14-operational-resilience.md)).
7. **Pierwsi realni userzy = nocny backup bazy, tagi deployów i firmowa strona maintenance — wszystko pierwszego dnia ruchu.**

## Antywzorce
- 🚫 Auto-deploy, „gotowe, więc idzie".
- 🚫 Deploy bez uzgodnienia lokalne ⇄ `origin` — niewypchnięte commity po cichu nie jadą.
- 🚫 Merge wspólnej gałęzi do gałęzi deployu bez przeczytania, co wnosi.
- 🚫 Długo żyjąca gałąź „wielki refaktor"; PR „wszystko naraz".
- 🚫 Praca bez issue — po miesiącu nikt nie wie „dlaczego".
- 🚫 Brak tagu deployu — „co jest live?" staje się zgadywanką.
- 🚫 Niezmiennik skryptu deployu bez testu (`$(date)` rozwinięty raz → każdy backup nadpisuje ten sam plik).
