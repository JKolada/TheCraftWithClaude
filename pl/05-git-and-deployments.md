# 05 — Git i wdrożenia

> Przykazania II, VI, VII, VIII, IX. Najgęstszy rozdział, bo tu błąd jest najdroższy.

## Git — dwa nawyki na większości zadań

### A. Szukaj w historii ZANIM zaimplementujesz
```bash
git log --oneline -- <ścieżka>      # historia pliku/katalogu
git log -S"symbol" --oneline        # pickaxe: gdzie narodził się symbol/flaga/kolumna
git log -G"regex" --oneline         # commity, których DIFF pasuje do regex
git log --grep="słowo" --oneline    # przeszukaj treści commitów (tam opisane są featury)
git blame <plik> -L a,b             # kto/kiedy/dlaczego
git show <commit>                   # pełna zmiana + kontekst
```
Łącz to z grep po drzewie + `AI_README.md` katalogu. Historia + kod + docs = pełny obraz w
minutę. Robi to różnicę przy: nieznanym kodzie, hunchu „czy my już tego nie robiliśmy",
kolumnie/fladze nieznanego pochodzenia, datowaniu regresji, przed każdym refaktorem.

### B. Czysty, spójny `git status`
- **Rozdzielaj niezwiązane zmiany** na osobne commity (jeden temat = jeden commit).
- **Wykrywaj śmieci wcześnie:** `.bak`, pliki tymczasowe, przypadkowe bazy (`web/_Proj…db`),
  plik o nazwie `-w` z błędnego `curl`. Dodaj wzorce do `.gitignore` (uwaga: gitignore
  **nie ma komentarzy w tej samej linii** — `#` w osobnej linii).
- **Odróżniaj realny diff od szumu CRLF:** `git status` pokazuje plik jako zmieniony, a
  `git diff HEAD` jest pusty → to tylko EOL, nie praca. Nie commituj szumu.
- **Sieroty (niezacommitowana praca w tle)** — w projekcie prowadzonym wielosesyjnie
  („użytkownik + Claude") inne sesje zostawiają zmiany w drzewie. Przed deployem: czy to realna,
  kompletna praca (commituj/potwierdź), czy WIP/eksperyment (zostaw)? **Nie wmiataj cudzej
  niezacommitowanej pracy do deployu bez potwierdzenia.**

### Co kończy commit
- Wiadomości po angielsku, opisowe (co + dlaczego), `fixes #N`/`refs #N` do issue.
- Linkuj PR/issue pełnym URL-em, nie „PR #123".

## Koordynacja pracy równoległej: issues i proste gałęzie

> **Ta doktryna jest pisana pod projekt prowadzony przez JEDNEGO developera z AI — nie pod korporacyjny
> zespół.** Ale „solo" nie znaczy już „jeden piszący": pojedynczy developer rutynowo odpala **kilka sesji
> Claude naraz** na tym samym repo (fix w jednej, feature w drugiej, review w trzeciej). To już jest sytuacja
> wielu piszących — a „drugą stroną" jest tu zwykle **inna sesja agenta**, nie ludzki współpracownik. Więc
> w chwili, gdy wychodzisz poza jedną żywą sesję, potrzebujesz tego samego co zespół: **wspólnej listy zadań**
> (issues) i **lekkiego rozgałęziania** — żeby równoległe sesje nie deptały sobie po palcach, nie wmiatały
> sobie nawzajem pół-gotowej pracy i żeby „co kto robi" było widoczne. Czytaj resztę tej sekcji z tą soczewką:
> **„inna sesja" wszędzie tam, gdzie pisze „współpracownik"**, a zagrożenia niżej (niewypchnięte commity, merge
> wmiatający pracę innej sesji, osierocony WIP w drzewie) to rzeczy, które gryzą *solowego* developera w chwili,
> gdy druga sesja Claude jest otwarta na tym samym repo.

### Issues = jednostki pracy (jedno źródło „co i dlaczego")
- **Jedno zadanie = jeden issue.** Tytuł = rezultat („Koszyk gubi pozycje po odświeżeniu"), treść =
  kontekst, kryteria zaliczenia, linki. To tu mieszka **dlaczego** — nie w głowie i nie na czacie.
- **Numer issue spina pracę:** gałąź, commity (`refs #N`), PR i dyskusję. `fixes #N` w PR **zamyka**
  issue po merge'u (→ „Co kończy commit").
- **Issue zanim kod** przy czymkolwiek nietrywialnym lub cudzym zgłoszeniu — żeby zakres i decyzja
  były zapisane, zanim powstanie diff. Małe, konkretne issues > jeden wielki „epik na wszystko".
- **Backlog to lista, nie pamięć.** Etykiety (`bug`/`feat`/`chore`, priorytet), zamykaj nieaktualne.
  Issue martwy tygodniami = decyzja do podjęcia (robimy / odpuszczamy), nie zombie.

### Proste gałęzie (równoległe sesje, trunk-based)
- **`main` jest zawsze wdrażalny.** Przy więcej niż jednej żywej sesji nie commituj wprost na `main` — to
  wspólny stół, na którym stoi to, co idzie na prod.
- **Krótka gałąź na zadanie:** `feat/NN-koszyk`, `fix/NN-logowanie` (NN = numer issue). Żyje
  **godziny–dni, nie tygodnie** — im dłużej żyje, tym boleśniejszy merge.
- **Mały PR > wielki PR.** Jeden temat, do przejrzenia w kwadrans. Wielkiego PR nikt nie czyta
  uważnie — przechodzi „na zaufanie", czyli bez review.
- **Merge i kasuj gałąź.** Po wejściu do `main`: usuń branch, ściągnij `main`, następne zacznij od
  świeżego. Stare gałęzie to dług i ściema o stanie projektu.
- **Wiedz, co niesie merge — zrób diff ZANIM zmergujesz do gałęzi deployu.** Merge wnosi **każdy** commit
  z gałęzi źródłowej, nie tylko Twój — w tym pracę, którą **inne sesje** już tam zmergowały. Więc przed
  wydaniem/mergem do swojej zawsze-wdrażalnej gałęzi: `git log <gałąź-deployu>..<źródło> --oneline` i
  przeczytaj listę. Przy **pilnym, izolowanym fixie** zrób **cherry-pick tego jednego commita** na czystą
  gałąź deployu, zamiast pełnego merge wspólnej gałęzi integracyjnej, której nie zweryfikowałeś — ślepy merge
  potrafi wmieść niedokończony feature na prod, jadący za Twoim fixem. To brat reguły o niezacommitowanych
  **sierotach** wyżej: oba brzmią „nie wypuszczaj tego, czego nie zamierzałeś."
- **Cherry-pick między rozjechanymi gałęziami też nie jest czysty — weryfikuj WYNIK, nie intencję.** Gdy cel
  nie ma kontekstu, który miał rodzic commita, cherry-pick spada do 3-way merge i może wciągnąć **sąsiednie
  huny** z gałęzi źródłowej — np. mount pliku, którego na celu nie ma (`require("./routes/feed")` →
  `MODULE_NOT_FOUND` przy starcie → prod 502). Po KAŻDYM cherry-picku na gałąź deployu:
  `git diff <baza-deployu> HEAD --stat` **i przeczytaj diff wpięć w aplikację** — musi pokazać TYLKO Twoją
  zmianę. „10 plików, +320" z jednym błąkającym się `app.use(require(...))` to sygnał.
- **Synchronizuj się z `main` często** (merge/rebase w swoją gałąź) — konflikty małe i częste zamiast
  jednego gigantycznego na końcu.

### Branching rośnie z projektem — nie zaczynaj od góry
Dopasuj workflow do tego, gdzie projekt naprawdę jest; eskaluj dopiero, gdy realny trigger to wymusi:

1. **Solo, brak żywych userów → sam `main`.** Commituj wprost, z dyscypliną. Bez gałęzi, bez ceremonii —
   najprostsze, co działa (→ [12](12-flexibility-and-scalability.md): nie over-engineeruj).
2. **Pierwsze wdrożenie produkcyjne (nawet solo) → krótkie gałęzie mergowane prosto do `main`.** Teraz `main`
   *to* „co jest live", więc trzymaj go **zawsze wdrażalnym**: każdą zmianę na gałęzi `feat/`/`fix/`,
   przejrzyj diff, merge do `main`, otaguj deploy (→ *Taguj KAŻDY deploy*). Trunk-based, bez długich gałęzi.
3. **Projekt rośnie / więcej osób / równoległe nurty → dołóż `develop` + środowisko `preproduction`.**
   Gałęzie feature mergują do **`develop`** (integracja); wydanie idzie `develop → main`. Wdrażaj na
   **`preproduction`, które jest kopią produkcji** (ten sam schemat, config, realistyczna próbka danych) i
   weryfikuj tam **przed** prodem — ostatnia bramka łapiąca „działa na dev, pada na prodzie".

Każdy szczebel dokładasz, **gdy metryka go wymusi** (żywi userzy → 2; współpracownik lub praca równoległa →
3), nigdy na zapas. Nie odpalaj trzy-środowiskowego GitFlow dla solowego prototypu — ale i nie zostawaj na
gołym `main`, gdy realni userzy już od niego zależą.

> **Review to nie formalność — to druga para oczu przed prodem.** W zespole każdy PR ma recenzenta;
> solo „recenzentem" jest świadomy drugi przegląd diffu (i Claude jako adwokat diabła). Zmiana wchodzi
> na `main` przejrzana, nie „bo działa u mnie".

### Anty-wzorce
- 🚫 Commit wprost na `main`, gdy w projekcie jest ktoś jeszcze → cudza praca ląduje na pół-gotowym stanie.
- 🚫 Długo żyjąca gałąź „mój wielki refaktor" → merge-piekło i tygodnie dryfu od `main`.
- 🚫 Praca bez issue → zakres i „dlaczego" giną; po miesiącu nikt nie wie, czemu to powstało.
- 🚫 `fixes #N` w commicie do gałęzi roboczej → issue zamyka się przedwcześnie (zamyka **PR/merge**, nie każdy commit).
- 🚫 PR „na wszystko naraz" → review fikcyjne, regresje przechodzą niezauważone.
- 🚫 Merge wspólnej/integracyjnej gałęzi do gałęzi deployu **bez uprzedniego diffu** → cudza zmergowana,
  ale niegotowa praca jedzie z Twoim fixem na prod. `git log <deploy>..<źródło>` przed każdym merge-do-deployu;
  pilny izolowany fix cherry-pickuj zamiast wmiatać całą gałąź.

## Wdrożenia — POLITYKA NADRZĘDNA

> ⛔ **Nigdy nie deployuj na prod automatycznie.** `git pull` na serwerze, `pm2 reload`,
> swap bazy, `migrate.py` na prodzie, flaga maintenance — **tylko gdy user powie wprost**
> („wdrażaj", „deploy"). Możesz **proaktywnie zaproponować** deploy, gdy gotowe — ale czekasz
> na jawne „tak". Commit + push na życzenie to **nie** deploy. Ta reguła bije „auto mode".

### Deploy wypuszcza `origin/<gałąź>`, nie Twoją lokalną gałąź — najpierw sprawdź, że jest wypchnięte
Skrypt deployu robi `pull` **`origin/<gałąź>`** na serwerze; nigdy nie widzi kopii roboczej z Twojego
laptopa. Więc praca zacommitowana, ale **niewypchnięta**, nie jedzie — najgroźniej w **wspólnym repo, gdzie
równoległa sesja zacommitowała na gałąź, ale nie wypchnęła**. Deployujesz, serwer ciągnie starszy szczyt
`origin`, a „najnowszych zmian" po cichu nie ma (przemianowana etykieta wciąż pokazuje stary tekst, nowego
featuru nie widać). Przed każdym deployem: `git fetch && git log origin/<gałąź>..<gałąź>` — jeśli **niepusty**,
Twoje (lub czyjeś) lokalne commity nie są jeszcze na `origin`; najpierw `git push` (czysty fast-forward, gdy
gałąź tylko poszła naprzód), potem deploy. Odwrotność, `git log <gałąź>..origin/<gałąź>`, łapie sytuację
przeciwną — `origin` wyszedł przed Ciebie (równoległa sesja wypchnęła), a Ty zaraz wdrożysz *nieaktualne*
drzewo; pull przed działaniem. W jednym zdaniu: **uzgodnij lokalne ⇄ origin przed deployem, bo serwer widzi
wyłącznie `origin`.**

### Boot-check na celu PRZED reloadem
Błąd require-time (brakujący moduł, zły import) ujawnia się dopiero, gdy proces **startuje** — a `pm2 reload`
startuje nowy kod, zabijając stary. Więc crash ląduje na userach jako 502. Zabramkuj reload: po `git pull`
odpal nowy kod w **jednorazowym** procesie —
`node -e "require('./src/app')"` (schowaj `app.listen` za `require.main === module`, żeby to nie zajmowało
portu) — i `pm2 reload` **tylko** gdy wypisze Twój marker OK. Jeśli rzuci błąd, działający proces zostaje
nietknięty (prod stoi na starym kodzie), a Ty naprawiasz forward z zero-downtime. Rób to na **celu** (realne
`node_modules` + env), nie na laptopie — worktree bez `node_modules` daje fałszywe „startuje".

### Dwa typy deployu
- **Code-only (bez migracji/zależności)** → zero-downtime: `git pull` + **boot-check** + `pm2 reload`.
- **Z migracją/zmianą zależności/swapem bazy** → **okno maintenance** (flaga nginx → 503 +
  branded strona), kilka sekund downtime, gwarancja że app nie biegnie na pół-zmigrowanym schemacie.

### Taguj KAŻDY deploy
```bash
git tag -a deploy-$(date +%F) -m "Co idzie na prod: <jedno zdanie>"   # -2/-3 dla kolejnego tego dnia
git push --tags
```
- Co jest live: `git describe --tags --abbrev=0 --match 'deploy-*'`.
- Rollback kodu: `git checkout <deploy-tag> && pm2 reload`.
- Rollback schematu: przywróć backup (forward-only!).

### Changelog przy każdym deployu
Publiczny „Co nowego" — **prostym językiem, bez żargonu** (żadnego scraper/migracja/commit).
Pisz, **co użytkownik zyskuje**. Bump daty `updated:`. To część checklisty deployu, nie opcja.

---

## Próba generalna deployu: dev → preprod → prod

> Migracja albo swap bazy testowany **pierwszy raz** w prodowym oknie maintenance jest testowany **na Twoich
> użytkownikach.** Lekarstwem jest szczebel między laptopem a prodem: **preprod**, który jest wierną kopią proda,
> gdzie odpalasz *dokładnie* ten runbook **raz, zanim zrobisz to naprawdę.**

**Trzy środowiska, trzy zadania:**
- **dev** (Twoja maszyna) — dane jednorazowe/seed, albo **zanonimizowany refresh z backupu proda**, gdy
  potrzebujesz realnych kształtów danych do reprodukcji buga. Szybkie, jednorazowe, bez userów.
- **preprod** — realny **serwerowy klon proda**: ten sam OS, nginx, `pm2`, TLS — ale bez żywych userów,
  za **basic-auth** i **noindex**. Jego jedyne zadanie to **ćwiczenie migracji i samego deployu.**
- **prod** — święty. Dotykany tylko na jawne „deploy" i tylko krokami, które tego samego dnia przećwiczyłeś na preprodzie.

**Buduj preprod z proda za każdym razem tak samo** (oskryptuj → [04](04-scripts-and-databases.md)):
- klonuj repo **kluczem deployowym samego proda** (auth do prywatnego repo bez tworzenia nowych poświadczeń);
- odśwież bazę z **backupu proda** i **anonimizuj PII, zanim opuści proda** (maile, nazwiska → nagrobki) —
  box nieprodukcyjny nigdy nie może trzymać realnych danych userów (→ [09](09-law-and-protecting-the-creator.md));
- wartości specyficzne dla środowiska zrób **env-overridable, nigdy hard-coded:** `SITE_URL`/canonical/OG muszą
  wskazywać na preprod, żeby ani nie przeciekał prodowych URL-i, ani nie zaindeksował staging boxa (→ [10](10-seo-and-translations.md)).

**Potem przećwicz prawdziwy runbook na preprodzie** — nie wersję uproszczoną: odpal `migrate.py`, **zmierz
okno**, zrób smoke test, potwierdź, że migracja jest **forward-only i idempotentna** (→ [04](04-scripts-and-databases.md)).
Migracja, która pada na preprodzie, to wtorek; ta sama awaria na prodzie to incydent z userami na 503.

**Pułapki, które ujawnia tylko *prawdziwy* preprod** (fałszywy nie): wyzwanie ACME/Let's-Encrypt `http-01` musi
**omijać bramkę basic-auth**, inaczej odnowienie certu daje 401; prywatne repo potrzebuje wpiętego zdalnego SSH
przed pierwszym `pull`; canonical/OG/sitemap muszą być za env, inaczej preprod emituje prodowe linki. Chcesz
wpaść na to na boxie, **którego nikt nie używa** — nie odkrywać w trakcie deployu.

> **Preprod to scena prób, nie drugi prod.** Bez żywych userów, nieświeża/zanonimizowana baza jest OK, a **jego
> bazy nigdy nie swapuje się z powrotem na prod.** W chwili, gdy potraktujesz go jako źródło prawdy, tworzysz
> drugie źródło prawdy do utrzymywania w synchronizacji (→ [11](11-data-model-and-normalization.md)).

## Swap bazy z zachowaniem kont — runbook (najtrudniejsza operacja)

Pełna podmianka prod-bazy (np. lokalny katalog z całą pracą) **z zachowaniem żywych kont**.
To tu jest najwięcej pułapek. Lekcje z projektu referencyjnego:

### Zasady, które ratują dane userów (Przykazanie VII)
1. **„Użytkownicy" to wiele tabel, nie jedna `users`.** Wylicz **każdą** tabelę z FK do
   użytkownika: konta, koszyki, recenzje, polubienia, odznaki, gry, czat (sesje +
   wiadomości + limity), feedback, sesje. Tabelę bez `user_id` (np. `chat_messages`) mapuj
   po jej rodzicu (`session_id`). Gateuj każdą na istnienie kolumny/tabeli.
2. **Mapuj po STABILNYM kluczu (slug), nie po ID.** `product_id` dryfuje między
   bazami po merge'ach — recenzja użytkownika musi trafić po `slug → nowe_id`, a brakujący
   slug jest **pomijany i logowany**, nie wpychany na ślepo.
3. **Źródłem prawdy dla kont jest ŻYWY prod**, nie stary snapshot — żeby nie zgubić
   rejestracji z ostatniej godziny. Migrację uruchom **w oknie maintenance, po `pm2 stop`**,
   czytając zatrzymaną, spójną prod-bazę.
4. **Kolejność FK-safe**: WIPE dzieci przed rodzicami, INSERT rodziców przed dziećmi
   (np. `reviews` przed `review_likes`; `chat_sessions` przed `chat_messages`).
5. **Backup żywego proda PRZED swapem** (`.backup replaced-prod-<ts>.db`) — to Twój rollback.
6. **Zweryfikuj scaloną bazę**: liczba kont = prod, 0 wiszących recenzji (slug-remap OK),
   `integrity_check: ok`, naruszenia FK ≤ stan zastany (nie więcej).
7. **Sesje to osobny, ulotny stan — nie mieszaj ich z podmienianą bazą.** Trzymaj store sesji w
   **osobnym pliku** (np. `sessions.db`) niż baza katalogowa, którą czasem podmieniasz w całości —
   inaczej swap wyzeruje zalogowanych. Store w pamięci procesu wylogowuje wszystkich przy **każdym**
   restarcie/deployu i przecieka pamięć (→ [14](14-operational-resilience.md)).

### Sekwencja (faza nieinwazyjna → okno → finalizacja)
**Faza 1 (serwis żyje):**
- push kodu na GitHub;
- **obrazki/assety gitignorowane kopiuj osobno** (rsync albo tar-over-ssh, **nie** przez git),
  PRZED oknem — są nieaktywne, dopóki nie podmienisz bazy. Wysyłaj tylko deltę (policz brakujące).
- pre-upload czystego snapshotu katalogu na serwer (`/tmp`).

**Faza 2 (okno maintenance, kilkanaście sekund), atomowo (`set -e`):**
`flaga ON → git pull → pm2 stop → backup żywego proda → migrate-users (źródło = prod) →
swap pliku (rm wal/shm, mv, PRAGMA journal_mode=WAL) → pm2 start → SMOKE TEST → flaga OFF`.

**Faza 3:** tag `deploy-…-2` + push, FB/SEO re-scrape jeśli dotyczy, sprzątanie `/tmp` i lokalnych temp.

### Smoke test po swapie (zanim zdejmiesz flagę)
Przez `localhost` (omija nginx maintenance): home/katalog/detal → 200, og:image →
właściwy plik, redirecty (np. scalone → 301 do survivora), liczby w bazie (konta/rekordy),
**`pm2 logs` na błędy**. Znaleziony, trywialny i bezpieczny bug — napraw w oknie i dociągnij
(commit → pull → reload), zamiast wypuszczać znane 500.

### Asety gitignorowane a deploy
Obrazki/pliki, które są w `.gitignore`, **nie jadą przez `git pull`**. Albo je zsynchronizuj
(rsync/tar), albo wygeneruj na serwerze (jeśli ma narzędzia). W projekcie referencyjnym decyzja:
**kopiujemy z lokalnej**, bo serwer nie ma Pillow, a swap zmienia katalog.

## Anty-wzorce
- 🚫 Auto-deploy / „skoro gotowe to wrzucam".
- 🚫 Swap „prócz kont" = tylko `users` → utrata recenzji/odznak/czatu.
- 🚫 Mapowanie user-danych po ID zamiast slug → recenzje lądują na złym produkcie.
- 🚫 Migracja na starym snapshocie → utrata świeżych rejestracji.
- 🚫 Brak tagu deployu → „co jest live?" staje się zgadywanką.
- 🚫 Deploy bez uzgodnienia lokalne ⇄ `origin` → serwer ciągnie `origin`, a Twoje (lub równoległej sesji) **niewypchnięte** commity nie jadą; `git log origin/<gałąź>..<gałąź>` przed każdym deployem.
- 🚫 Transfer 1.5 GB assetów **w** oknie maintenance → długi downtime (rób przed oknem).
- 🚫 Sesje w bazie podmienianej swapem (albo w pamięci procesu) → deploy wylogowuje wszystkich.
- 🚫 Niezmiennik skryptu deployu nietknięty testem — np. `$(date)` rozwinięty raz przy tworzeniu
  pliku (każdy backup nadpisuje ten sam plik). Zabetonuj niezmienniki deploy-skryptu testem.
- 🚫 **Pierwszy przebieg** migracji to prodowe okno maintenance → debugujesz na userach; przećwicz na preprodzie.
- 🚫 Preprod trzymający **realne, niezanonimizowane** dane userów → druga kopia Twojej odpowiedzialności za PII na słabiej strzeżonym boxie.
- 🚫 Preprod **zaindeksowany przez wyszukiwarki / emitujący prodowe URL-e** → duplikat treści + wyciek stagingu (env-gate `SITE_URL`, noindex, basic-auth).

> **Runbook to pamięć incydentów, nie głowa.** Każda awaria na prodzie → wpis w runbooku z datą
> i ponumerowaną lekcją (np. „nigdy nie SCP żywej `.db` — użyj `.backup`; WAL trzyma świeże strony").
> Następny swap czyta runbook, nie powtarza błędu (→ [06](06-collaboration-and-memory.md), [14](14-operational-resilience.md)).

## Wspólna infrastruktura
Projekty mogą dzielić jeden **Hetzner VPS**: statyczne (build `dist/`) idą przez
`scp`/`rsync` + nginx vhost; aplikacje Node przez `git pull` + `pm2 reload` za
nginx. Jeden serwer = wspólny katalog `backups/`, te same nawyki (tag deployu, maintenance
flag). Nowy projekt na tym samym boxie: osobny vhost + osobny katalog, te same reguły.

## W praktyce
Ścieżkę krytyczną (np. logowanie) wdrażaj z testem i pełnym smoke (rejestracja, login,
wylogowanie, trwałość sesji). Przy pierwszym realnym ruchu userów ustaw od razu: nightly backup
bazy, tagowanie deployów, branded maintenance page. → [03](03-testing-and-verification.md)
