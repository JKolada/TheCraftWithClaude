# Changelog — Rzemiosło (The Craft)

Wszystkie istotne zmiany doktryny **Rzemiosło — The Craft (Kolada Build)**. Wersjonowanie **semantyczne**
(MAJOR.MINOR.PATCH). **Data wpisu = dzień publikacji** — wtedy wersja została zdeployowana na
[thecraft.jakub.solutions](https://thecraft.jakub.solutions) i gotowa do pobrania.

Zasada: jedno źródło prawdy. `version` w [craft.json](craft.json) zawsze odpowiada najwyższemu
wpisowi poniżej. Każde wydanie tagujemy w gicie (`vMAJOR.MINOR.PATCH`) — Przykazanie VIII.

> **Wspólna oś wersji z witryną Rzemiosło Web.** Rdzeń reguł i witryna dzielą numerację, więc numer
> **pominięty tutaj oznacza wydanie po stronie witryny** — `1.0.1` i `1.0.2` należały do Web, dlatego
> rdzeń idzie `1.0.0 → 1.0.3`. `1.1.0` istniało tylko w kopiach u gospodarzy (powstało tam, zanim trafiło
> do kanonu), więc kanon wydaje tę treść jako `1.1.1`. Luki są zamierzone, nie brakiem.

> **MAJOR** — przebudowa/usunięcie reguł lub rozdziału (zmiana niekompatybilna z dotychczasowym
> rozumieniem). **MINOR** — nowy rozdział lub istotna nowa reguła. **PATCH** — doprecyzowanie,
> przykład, literówka, drobna korekta.

## 1.1.1 — 2026-11-20

**Przegląd całej doktryny i przejście tnące, wykonane z Claude Opus 5.5.** The Craft to twarde reguły dla
projektów prowadzonych z AI — więc rdzeń zawiera tylko reguły; wiedzę, którą współczesny model ma i tak,
oraz wyjaśnienia przeniesiono na stronę. Treść EN: ~160 → ~62 tys. znaków, **żadna twarda reguła nie
wypadła**. Do tego nowy rozdział 17 z projektu-gospodarza (tam jako `1.1.0`) oraz podział 05 na 05/18/19.
Wszystko w obu językach.

### Przebudowane
- **Jeden format rozdziału:** jednolinijkowy wstęp → **Reguły** (numerowane, jedna linia + dlaczego) →
  **Antywzorce**. Usunięte wykłady, definicje (np. litery SOLID, podstawy SEO/SQL, piramida testów) i
  zakończenia „W praktyce" — jedyną checklistą jest [07].
- **[05] podzielony** (23 kB łamało regułę „jeden plik = jeden temat" z [01]): 05 = git + cofanie + praca
  równoległa + polityka deployu; nowe **[18] Próba generalna wydania** (dev → preprod → prod) i
  **[19] Runbook swapu bazy**.
- **[intro]** skrócone do „czym jest / dla kogo / jak zacząć" — manifest idzie na stronę.

### Dodane
- **[17] Kod zawsze po angielsku** — identyfikatory, **także nazwy testów**, baza, CLI, klucze, opisy commitów;
  proza w języku projektu, zadeklarowanym raz w `CLAUDE.md`.
- **[17] „Reguła bez strażnika to życzenie"** — strażnik indeksu `AI_README` i strażnik języka kodu jako
  **zapadka**; gotowe pliki w **`guards/`** (celowo bez nazwy `test_*.py`, żeby pytest gospodarza nie zbierał
  ich z `docs/rules/`).
- **`add_chapter.py`** — wpina nowy rozdział wszędzie naraz (dry-run domyślnie); **nie rusza wersji ani
  CHANGELOG** (wspólna oś wersji z Web).

### Zmienione
- **[00, 07] Reguła zerowa:** wskaźnik zwykłym językiem tylko w `CLAUDE.md` i `AGENTS.md` — **bez etykiet
  `SYSTEM`/`URGENT`** (dla współczesnego modelu to kształt prompt injection) i bez wpisu w publicznym `README.md`.
- **[00] Przykazanie VII uogólnione** — z przepisu na swap bazy na regułę: nie gub, nie wyciekaj, nie mutuj
  bez backupu, mapuj po stabilnym kluczu; szczegóły w [19].
- **[06] Pamięć:** jedna reguła zamiast własnego systemu — korzystaj z wbudowanej pamięci agenta, nie kopiuj
  do niej faktów z repo. Usunięte zachowania, które są już defaultem modelu.
- **[16]** tylko polityka projektu (kiedy plan mode jest obowiązkowy, autopilot w mapie uprawnień, model wg
  stawki, worktree na sesję) — bez opisu funkcji harnessu, które starzeją się z wydaniami.
- **[17, 06] Złagodzona reguła terminów:** po angielsku zostają **nazwy, które drukuje narzędzie**; zwykłe
  słowo na czynność może być w języku prozy („wdrożenie"). [06] nie wymaga już „docsów technicznych po angielsku".
- **[07]** brief zapisuje się jako `project-brief.md` (było: `brief-projektu.md` — sprzeczne z [17]);
  usunięta wzmianka o edycjach (to sprawa Web).
- **[08]** rozstrzygnięty konflikt Python vs Node: Python domyślnie, Node gdy warstwa web już jest w JS.
- **[09]** prawo właściwe = Twoja jurysdykcja (było: na sztywno Polska).
- **[12]** feature flagi z pierwszą ryzykowną zmianą dla żywych userów (było: w Dniu 0); ADR tylko przy
  odejściu od domyślnego stacku.
- **`CLAUDE.md` repo** zaktualizowany (zakres rozdziałów, EN jako baza, narzędzia, stan bieżący).

### Dodane
- **[17] Kod zawsze po angielsku** — identyfikatory, **także nazwy testów**, baza, CLI, klucze, opisy commitów;
  proza (docsy, komentarze, docstringi, UI) w języku projektu, zadeklarowanym raz w `CLAUDE.md`.
- **[17] „Reguła bez strażnika to życzenie"** — strażnik indeksu `AI_README` (każdy moduł wymieniony, sufit
  20 kB, lista katalogów pilnująca siebie) i strażnik języka kodu jako **zapadka** z baselinem per plik;
  wzorzec zapadki do wprowadzania dowolnej reguły w stary kod.
- **[01]** wskaźnik: indeksu pilnuje test. **[07]** dwa punkty checklisty Dnia 0 (polityka językowa, strażnicy).

### Zmienione
- **[17, 06] Złagodzona reguła terminów:** po angielsku zostają **nazwy, które drukuje narzędzie** (komenda,
  flaga, status, plik, tag) — zwykłe słowo na czynność może być w języku prozy („wdrożenie"). Usuwa sprzeczność
  z polskim tłumaczeniem doktryny.
- **[06]** „docsy techniczne po angielsku" usunięte — spójnie z [17] (proza w języku projektu); po angielsku
  zostają kod i opisy commitów.

## 1.0.3 — 2026-08-24

Lekcje z pracy w projekcie referencyjnym, wpisane do istniejących rozdziałów (bez zmiany listy rozdziałów —
stąd PATCH), w obu językach (EN kanon + PL). Rdzeń: doktryna jest pisana pod **jednego developera z AI**,
gdzie „solo" i tak znaczy **kilka równoległych sesji Claude** na jednym repo — i to one, nie ludzki zespół,
wymuszają dyscyplinę koordynacji.

### Dodane
- **[intro] „Dla kogo to jest".** Pojedynczy developer + AI jako para; „solo" to i tak wielu piszących
  (równoległe sesje agenta) → reguły koordynacji istnieją już przy drugiej otwartej sesji.
- **[05] Koordynacja pracy równoległej.** Przeramowanie „pracy zespołowej" na **równoległe sesje Claude**;
  diff-przed-mergem do gałęzi deployu i pułapka **cherry-pick 3-way merge**; **`origin` vs lokalne** (deploy
  wypuszcza `origin`, sprawdź push przed deployem); **boot-check na celu przed reloadem**; pełna sekcja
  **próby generalnej deployu: dev → preprod → prod** (budowa preprodu z proda, anonimizacja PII, `SITE_URL`
  env-overridable, pułapki ACME/SSH/canonical). + nowe antywzorce.
- **[14 § 7] Zadania cykliczne: patrz na skutek, nie na runnera.** Czujka mierzy **wiek najświeższego
  rekordu per źródło**, nie kod wyjścia zadania; zielony raport pokrywa tylko to, o czym wie (druga
  ścieżka danych milczy); **konfiguracja harmonogramu to produkcja i żyje poza repo** (nadrabianie
  pominiętego uruchomienia, warunek bateryjny) → do runbooka. + 2 antywzorce.
- **[16] Tryb planowania** jako osobna sekcja (kiedy sięgać, kiedy odpuścić, plan = artefakt przeglądu)
  oraz **izolowany `git worktree` na równoległą sesję** (wspólny checkout = wspólny index). + 3 antywzorce.
- **[15] Serwis odpowiada dwa razy i te odpowiedzi mogą sobie przeczyć.** `robots.txt` to POLITYKA
  właściciela, tarcza antybotowa to MASZYNA, która nie czyta intencji — przedstawiasz się prawdziwie i
  pytasz właściciela, nie szukasz obejścia; 403 z serwera + 200 z innej sieci = blokada ADRESU, 403 z KAŻDEJ
  sieci = tarcza.
- **[03] Guard sprawdza się na incydencie, nie na fiksturze.** Kontrolę pisaną po awarii odtwórz na
  prawdziwych danych tej awarii, zanim jej zaufasz — fiksturę pisze ta sama głowa, która napisała błąd.
- **[04] Ścieżki absolutne na granicy narzędzi** (`/tmp` znaczy co innego w Git Bash / Pythonie / PowerShell)
  oraz **próba generalna masowej mutacji na kopii proda** (nie tylko dry-run).
- **[13] Mobile: viewport to ruchomy cel.** `100dvh` zamiast `100vh` (kolejność deklaracji), elementy nad
  klawiaturą kotwiczone do **`visualViewport`**, `flex-basis` z wiersza staje się wysokością w kolumnie,
  emulator kłamie → mierz geometrię DOM / testuj na profilu urządzenia. + nowe antywzorce.
- **[05] Cofanie: najprawdopodobniej tego nie straciłeś.** Sekcja ratunkowa dla osób niebiegłych w gicie —
  sześć typowych panik i droga powrotna dla każdej (`restore`, `reset --soft`, `reflog`, `ORIG_HEAD`,
  przywrócenie pliku ze starego commita), `reflog` jako przycisk cofania repo oraz **trzy jedyne komendy,
  które realnie niszczą pracę** — i to wyłącznie niezacommitowaną. Reguła spinająca: commituj wcześnie,
  bo destrukcyjne komendy gita nie mają dry-run.
- **[06] Mapa uprawnień — jedna tabela, trzy kolumny** (wolno / zapytaj / nigdy). Granica całej doktryny
  w jednym miejscu, zamiast rozsypki po `00`, `05`, `06` i `16`; lewa kolumna celowo szeroka (to ona czyni
  autopilota bezpiecznym), środkowa per-akcja, prawa nienegocjowalna.
- **[06] Przekazanie stanu, gdy urywa się kontekst.** Długa sesja nie kończy się — zostaje podsumowana,
  a podsumowanie gubi **dlaczego** i **pół-gotowy stan w drzewie**. Dowoź w commitach, nie w rozmowie;
  decyzję zapisz w chwili podjęcia; trwałe fakty do `memory/`; `git status` **jest** przekazaniem dla
  następcy; przy zbliżającym się suficie dowoź, nie zaczynaj. Test: czy następna sesja podniosłaby to
  z samego repo, bez tej rozmowy?
- **[00] Odstępstwo od reguły — i podłoga, która się nie rusza.** Doktryna to default, nie klatka:
  odstępuj **na głos** (nazwij regułę, uzasadnij, zaproponuj zamiennik), ciche pominięcie to grzech;
  precedencja `CLAUDE.md` gospodarza > `docs/rules` > defaulty agenta; reguła wciąż nadpisywana to bug
  doktryny do naprawienia w kanonie. Podłoga: **III, V, VI, VII**.

### Zmienione
- **[00] Reguła zerowa** — „przeczytaj każdy plik" → „przeczytaj Dekalog, resztę grepuj po indeksie
  tematów" (spójność z ekonomią kontekstu z [01]); jawnie: **wskaźnik, nie wklejka**, a kopia
  wendorowana **nie jest** konstytucją projektu-gospodarza.
- **[14 § 2] Runner dobierany do czasu życia zadania** — tło sesji jest trwałe *w* sesji (i należy z niego
  korzystać), ginie *z* sesją; co ma przeżyć sesję → proces odpięty albo harmonogram systemu. Poprzednie
  brzmienie („nie uruchamiaj z tła sesji") przeczyło rozdziałowi [16].
- **[07] Notka `[SYSTEM — READ FIRST]`** doprecyzowana (Dekalog → indeks tematów; **wskaźnik, nie wklejka**).
- **[AI_README, CLAUDE.md]** baner „kopia wendorowana ≠ konstytucja gospodarza", indeks tematów i liczby
  zsynchronizowane ze stanem bieżącym.

---

## 1.0.0 — 2026-06-19

Pierwsze publiczne wydanie — **kompletna doktryna The Craft**, gotowa do wpięcia jako `docs/rules/`
w nowym projekcie. Od pierwszego commita po prod: jak budować z Claude tak, żeby projekt został
zrozumiały, bezpieczny w zmianie i godny zaufania.

### Dodane
- **17 rozdziałów w dwóch językach** (EN kanon + PL — te same rozdziały, te same kotwice):
  **Dekalog** (00) + rdzeń (01–08) + pogłębienie (09–16) — od dokumentacji, testów, gita i wdrożeń,
  przez prawo, SEO i model danych, po wydajność, odporność operacyjną, scraping/AI i prowadzenie Claude.
- **Czytnik HTML** paczki — render `.md` z dwukliku (`file://`), tryb jasny/ciemny, przełącznik EN/PL.
- **Witryna** [thecraft.jakub.solutions](https://thecraft.jakub.solutions) — przyjazne opakowanie z pobieraniem.

---

<!--
Szablon kolejnego wpisu:

## 1.1.0 — RRRR-MM-DD
### Dodane
- …
### Zmienione
- …
### Usunięte
- …
-->
