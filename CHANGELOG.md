# Changelog — Rzemiosło (The Craft)

Wszystkie istotne zmiany doktryny **Rzemiosło — The Craft (Kolada Build)**. Wersjonowanie **semantyczne**
(MAJOR.MINOR.PATCH). **Data wpisu = dzień publikacji** — wtedy wersja została zdeployowana na
[thecraft.jakub.solutions](https://thecraft.jakub.solutions) i gotowa do pobrania.

Zasada: jedno źródło prawdy. `version` w [craft.json](craft.json) zawsze odpowiada najwyższemu
wpisowi poniżej. Każde wydanie tagujemy w gicie (`vMAJOR.MINOR.PATCH`) — Przykazanie VIII.

> **MAJOR** — przebudowa/usunięcie reguł lub rozdziału (zmiana niekompatybilna z dotychczasowym
> rozumieniem). **MINOR** — nowy rozdział lub istotna nowa reguła. **PATCH** — doprecyzowanie,
> przykład, literówka, drobna korekta.

## 1.0.1 — 2026-07-06

Lekcje z pracy w projekcie referencyjnym, wpisane do istniejących rozdziałów (bez zmiany listy rozdziałów —
stąd PATCH). Rdzeń: doktryna jest pisana pod **jednego developera z AI**, gdzie „solo" i tak znaczy **kilka
równoległych sesji Claude** na jednym repo — i to one, nie ludzki zespół, wymuszają dyscyplinę koordynacji.

### Dodane
- **[intro] „Dla kogo to jest".** Pojedynczy developer + AI jako para; „solo" to i tak wielu piszących
  (równoległe sesje agenta) → reguły koordynacji istnieją już przy drugiej otwartej sesji.
- **[05] Koordynacja pracy równoległej.** Przeramowanie „pracy zespołowej" na **równoległe sesje Claude**;
  diff-przed-mergem do gałęzi deployu i pułapka **cherry-pick 3-way merge**; **`origin` vs lokalne** (deploy
  wypuszcza `origin`, sprawdź push przed deployem); **boot-check na celu przed reloadem**; pełna sekcja
  **próby generalnej deployu: dev → preprod → prod** (budowa preprodu z proda, anonimizacja PII, `SITE_URL`
  env-overridable, pułapki ACME/SSH/canonical). + nowe antywzorce.
- **[04] Ścieżki absolutne na granicy narzędzi** (`/tmp` znaczy co innego w Git Bash / Pythonie / PowerShell)
  oraz **próba generalna masowej mutacji na kopii proda** (nie tylko dry-run).
- **[13] Mobile: viewport to ruchomy cel.** `100dvh` zamiast `100vh` (kolejność deklaracji), elementy nad
  klawiaturą kotwiczone do **`visualViewport`**, `flex-basis` z wiersza staje się wysokością w kolumnie,
  emulator kłamie → mierz geometrię DOM / testuj na profilu urządzenia. + nowe antywzorce.

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
