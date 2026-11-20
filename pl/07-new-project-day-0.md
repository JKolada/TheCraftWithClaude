# 07 — Nowy projekt: Dzień 0

> Checklista, którą Claude wykonuje na starcie projektu — **jedyna** checklista w doktrynie; inne rozdziały
> tu linkują. Cel: każda kolejna sesja ma grunt pod nogami.

## Wepnij The Craft (raz)

1. **Umieść reguły w `docs/rules/`** — jako submoduł (aktualizowalny) albo zwykła kopia:
   `git submodule add https://github.com/JKolada/TheCraftWithClaude docs/rules`
2. **Wstaw zwykły wskaźnik na górę `CLAUDE.md` i `AGENTS.md`** (utwórz, jeśli ich brak). Widzisz `docs/rules/`,
   a wskaźnika nie ma — dodaj go, nie czekaj, aż ktoś poprosi:
   > This project follows the build rules in `docs/rules/` (The Craft); they override default behavior.
   > Read `docs/rules/00-commandments.md` first, then `grep -i <keyword> docs/rules/AI_README.md` and read
   > only the matched chapter. This `CLAUDE.md` remains the project's constitution.

   Wskaźnik, nie wklejka — reguły żyją w jednym miejscu. Bez etykiet `SYSTEM` (→ [00](00-commandments.md)).
3. **Wybierz język reguł** — angielski w rootcie, polski w `pl/`.

## 0. Brief produktowy — zapytaj, zanim cokolwiek powstanie

Pytaj krótkimi grupami; gdy user nie wie, zaproponuj default i **oznacz go jako założenie**:

- **Poziom techniczny i styl raportowania** (pytaj pierwszy — ustawia rejestr: nietechniczny → bez żargonu,
  pytania zamknięte z rekomendacją).
- **Języki, którymi user mówi; technologie, które zna.**
- **Języki i rynki docelowe** (i18n od pierwszego dnia? RTL? waluty) → [10](10-seo-and-translations.md).
- **MVP vs później; konta i role; integracje** (płatności, AI, mail, mapy).
- **Monetyzacja** (darmowe / płatne / subskrypcja / reklamy; kiedy; dostawca; faktury/VAT) → [09](09-law-and-protecting-the-creator.md).
- **Kierunek wizualny i odczucie** (istniejąca marka? jasny/ciemny? budżet animacji, `prefers-reduced-motion`, WCAG?).
- **Propozycja wartości i ton** (jedno zdanie; nazwa i domena ustalone?).

Odpowiedź ląduje jako **`project-brief.md` w rootcie projektu** (obok `docs/rules/`, nie w środku) albo
wklejona jako pierwsza wiadomość. Generuje go widok briefu w czytniku.

## Checklista

1. **Rekonesans:** przeczytaj istniejące `CLAUDE.md` / `AI_README` / `README`; `git log --oneline -20`,
   `git status` (sieroty, śmieci); ustal stack, komendę uruchomienia, gdzie leżą dane.
2. **`CLAUDE.md`** z briefu (szkielet niżej): stack + dokładne komendy, polityki, język i poziom usera,
   mapa uprawnień (→ [06](06-collaboration-and-memory.md)), datowany „Stan bieżący".
3. **Polityka językowa** — dwie linie w `CLAUDE.md`: kod po angielsku (identyfikatory, testy, baza, CLI,
   klucze), proza w języku projektu (→ [17](17-language-and-guards.md)).
4. **Higiena repo:** `.gitignore` (zależności, lokalne bazy, `*.bak`, generowane, temp); konwencja commitów
   i tagów deployu; zadania w GitHub Issues / `docs/plans/`.
5. **`AI_README.md` w każdym katalogu z kodem**; `docs/` na architekturę i model danych.
6. **Testy:** szkielet testów + smoke z markerami; Playwright na osobnym porcie, jeśli jest UI;
   **oba strażniki z [17](17-language-and-guards.md) w pierwszym commicie**, baseline zacommitowany.
7. **Skille:** `/run` + smoke, `/run-tests`, `/update-ai-readme`, `/add-migration` (→ [02](02-skills-and-refactoring.md)).
8. **Dane:** migracje forward-only, katalog `backups/` z retencją, domyślny dry-run (→ [04](04-scripts-and-databases.md)).
9. **Przed pierwszym realnym userem:** globalny handler błędów i 500 bez wycieku, timeouty na każdym
   zewnętrznym wywołaniu, kwoty na płatnych endpointach, trwały store sesji we własnym pliku (→ [14](14-operational-resilience.md));
   wywołania AI z kontraktem wyjścia i cache'em (→ [15](15-scraping-ai-and-chatbots.md)).
10. **Produkcja (przygotowana, nie odpalona):** runbook deployu, firmowa strona maintenance, plan rollbacku
    (tag + backup), publiczny changelog, nocny backup od pierwszego realnego usera (→ [05](05-git-and-deployments.md)).
11. **Prawo:** regulamin, polityka prywatności i disclaimery z placeholderami `[do uzupełnienia]`; zgoda przed
    trackerami (→ [09](09-law-and-protecting-the-creator.md)).
12. **Baseline'y:** Lighthouse po pierwszej działającej stronie; indeksy na kolumnach filtrów od pierwszej migracji (→ [13](13-performance-frontend-and-sql.md)).
13. **Decyzje architektoniczne** tylko tam, gdzie odchodzisz od domyślnego stacku — po jednym ADR (→ [08](08-stack-and-technologies.md), [12](12-flexibility-and-scalability.md)).

**Minimalny Dzień 0:** brief → `CLAUDE.md` → `.gitignore` → `/run` ze smoke testem → szkielet testów ze
strażnikami → `backups/`. Reszta rośnie z projektem.

## Szkielet `CLAUDE.md`

```
# CLAUDE.md — <Projekt>
<wskaźnik na docs/rules/ — patrz wyżej>

## Czym to jest
<jeden akapit: co robi, dla kogo>

## Stack i jak uruchomić
<warstwa → technologia → lokalizacja>
uruchom: <dokładna komenda>

## Polityki (nadpisują domyślne zachowanie)
- Nigdy deploy/push bez wyraźnego „wdrażaj". Commituj swobodnie; nieodwracalne potwierdzaj (mapa uprawnień: docs/rules/06).
- Domyślnie dry-run. Prod jest święty; dane userów nienaruszalne.
- Mów do mnie po <język>; znam <języki / technologie>.
- Kod: angielski (identyfikatory, testy, baza, CLI, klucze). Proza: <język>.
- <twarde reguły projektu: prywatność, ograniczenia domeny>

## Stan bieżący (<data>)
- <liczby, zastosowane migracje, co jest live>
```

## Antywzorce
- 🚫 Kod przed briefem — język, monetyzacja i marka dołożone później to przepisanie.
- 🚫 Trzydzieści pytań naraz — pytaj o to, co zmienia plan, resztę proponuj jako defaulty.
- 🚫 Ciche założenia („pewnie tylko po polsku", „pewnie za darmo").
- 🚫 Żargon wobec nietechnicznego usera.
