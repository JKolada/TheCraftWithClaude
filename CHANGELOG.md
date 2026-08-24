# Changelog — Rzemiosło (The Craft)

Wszystkie istotne zmiany doktryny **Rzemiosło — The Craft (Kolada Build)**. Wersjonowanie **semantyczne**
(MAJOR.MINOR.PATCH). **Data wpisu = dzień publikacji** — wtedy wersja została zdeployowana na
[thecraft.jakub.solutions](https://thecraft.jakub.solutions) i gotowa do pobrania.

Zasada: jedno źródło prawdy. `version` w [craft.json](craft.json) zawsze odpowiada najwyższemu
wpisowi poniżej. Każde wydanie tagujemy w gicie (`vMAJOR.MINOR.PATCH`) — Przykazanie VIII.

> **MAJOR** — przebudowa/usunięcie reguł lub rozdziału (zmiana niekompatybilna z dotychczasowym
> rozumieniem). **MINOR** — nowy rozdział lub istotna nowa reguła. **PATCH** — doprecyzowanie,
> przykład, literówka, drobna korekta.

## 1.0.2 — 2026-07-10

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
