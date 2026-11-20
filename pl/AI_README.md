# AI_README — katalog Rzemiosło (The Craft)

> Mapa katalogu dla następnej sesji / innego agenta. Czytaj **przed** dotknięciem plików tutaj.
> Konstytucja repo: [CLAUDE.md](CLAUDE.md). Test jakości tego pliku: czy po przeczytaniu możesz
> bezpiecznie zmienić cokolwiek w tym katalogu, nie skanując wszystkich plików?
>
> **Podział plików meta** (→ [01](01-documentation-and-ai-readme.md)): `README.md` = opis dla GitHuba
> (publiczny, EN). `CLAUDE.md` = konstytucja repo (jeden język, **nie tłumaczona**). **`AI_README` jest
> tłumaczony per język** — ten plik to wersja **PL**; EN/baza w [`../AI_README.md`](../AI_README.md).

## Co to za katalog

Repozytorium **dokumentacji** (nie aplikacja): doktryna „Rzemiosło — The Craft" (Kolada Build).
Treść to ręcznie pisany markdown; `index.html` jest jej przeglądarką (statyczna SPA, bez build-stepu).
Cel: zestaw reguł reużywalny jako `/docs/rules/` w nowych projektach **oraz** materiał publiczny
dla osób zaczynających z Claude. Szczegóły i polityki → [CLAUDE.md](CLAUDE.md).

## Rdzeń (to repo) vs Web (siostrzane repo)

**Podział ról — nie duplikuj między nimi:**

- **To repo (`ClaudeBuildCodex`, marka „Rzemiosło") = rdzeń kanoniczny.** Forma: **techniczna, zwarta, imperatywna;
  bazą jest angielski** (PL tłumaczenie w `pl/`) — źródło prawdy reguł, dołączane do projektów jako `/docs/rules/`. Optymalizowane pod
  **agenta i osobę techniczną**: gęstość ponad przystępność. Tu wersjonujemy doktrynę (craft.json).
- **Siostrzane `ClaudeBuildCodexWeb` (marka „Rzemiosło Web") = projekt prezentacyjny.** Bierze tę samą doktrynę i **rozwija
  poszczególne tematy** w przyjaźniejszej, obszerniejszej formie. **To Web — nie to repo — odpowiada za:**
  publiczną stronę, **edycje** (techniczna / BIZ-TECH / biznesowa), **wersje językowe** i **budowanie paczek
  `docs/rules/` w konkretnym języku**. Konsumuje treść tego repo + `craft.json` przy buildzie.

> **To repo jest TYLKO zestawem reguł.** Nie jest produktem prezentacyjnym. `index.html` tutaj to
> **minimalny czytnik lokalny/dev** (podgląd treści dla autora i agenta), **nie** publiczna witryna —
> dlatego nie umieszczamy tu badge'y edycji, marketingu ani przełącznika języka. Cała prezentacja,
> edycje i pakowanie wielojęzyczne dzieją się w **The Craft Web** (osobny projekt). Jeśli kusi Cię,
> by tu dodać warstwę prezentacji/marketingu/edycji — to materiał dla Web, nie dla rdzenia.

Co trafia do paczki `docs/rules/` (kontrakt z Web) → [docs/packaging.md](../docs/packaging.md).

## Indeks plików

| Plik | Po co to |
|------|----------|
| `index.html` | **Minimalny czytnik lokalny/dev** (podgląd treści dla autora/agenta) — NIE publiczna witryna. Strona główna (dekalog + karty) + widok rozdziału + brief + przełącznik języka EN/PL (domyślnie EN). |
| `intro.md` | **Krótkie wprowadzenie** — czym jest The Craft, dla kogo, jak zacząć (długa forma jest na stronie). Poza numerowaną listą, routowany jako `#intro`; jest też `pl/intro.md`. |
| `00`–`19` (root) | **Treść EN — kanoniczna, baza, źródło prawdy.** Slugi/numery = stabilne kotwice, wspólne dla wszystkich języków. |
| `pl/` | **Treść PL** — te same numerowane rozdziały (te same nazwy plików, treść po polsku). Tłumaczenie EN. |
| `guards/` | **Gotowi strażnicy testowi** z rozdziału 17: `ai_readme_guard.py` (strażnik indeksu) i `code_language_guard.py` (zapadka). Szablony kopiowane do `tests/` projektu — celowo bez nazwy `test_*.py`, żeby pytest gospodarza nie zbierał ich z `docs/rules/`. Jadą w paczce. |
| `add_chapter.py` | **Dodaje rozdział i wpina go wszędzie** (`NN-slug.md` + szkielet `pl/`, `README`, oba `AI_README`, `CHAPTERS`/`CH_EN`, `chapters` w `craft.json`), potem `build.py` + `test.py`. Domyślnie dry-run, `--execute` zapisuje. **Nigdy nie rusza wersji ani CHANGELOG** — numer wydania nadaje autor (wspólna oś z Web). Narzędzie repo, nie jedzie w paczce. |
 Plany i decyzje meta repo (nie treść doktryny): `docs/AI_README.md`, `docs/plans/`. |
| `content.js` | **Generowany** snapshot `.md` osadzony w JS — pozwala renderować treść po `file://`. Nie edytuj ręcznie. |
| `build.py` | Skrypt buildu: łączy pliki `.md` → `content.js`. Uruchom po edycji treści (`python build.py`). |
| `test.py` | **Smoke test** (czysty Python): parytet PL↔EN, martwe linki, świeżość `content.js`, spójność `CHAPTERS`/tabel/`craft.json`, oraz **statyczna nawigacja `index.html`** (linki `href="#…"`, `data-i18n`↔`UI`, `data-bf-label`↔`BRIEF_FIELDS`). `python test.py`. |
| `CLAUDE.md` | Konstytucja repo: czym jest, stack, jak uruchomić, polityki, stan bieżący. |
| `AI_README.md` | Ten plik — mapa katalogu. |
| `README.md` | Wejście dla człowieka: spis rozdziałów + „jak czytać". |
| `craft.json` | **Wersja wydania** (`version` + `released`) + nazwy marki (`name`/`name_short`/`name_en`). Źródło stempla dla witryny Rzemiosło Web. |
| `CHANGELOG.md` | Historia wydań Rzemiosła (semver, data = dzień publikacji). |
| `00-commandments.md` | **Dekalog** — 10 przykazań, 7 grzechów, złota zasada altytudy, jak odstąpić od reguły. Rdzeń. |
| `01-documentation-and-ai-readme.md` | Trzy warstwy (CLAUDE.md / AI_README / docs) wg czytelnika; indeks grep; docs = tylko bieżący stan; żywe plany. |
| `02-skills-and-refactoring.md` | Kiedy zbudować skill (a kiedy hook); dyscyplina refaktoringu; SOLID proporcjonalnie. |
| `03-testing-and-verification.md` | Każda zmiana zachowania niesie test; dowód zamiast deklaracji; smoke z markerami; uczciwy raport; guard dowodzi incydent. |
| `04-scripts-and-databases.md` | Dry-run/`--execute`, idempotencja, migracje forward-only, backupy; ścieżki absolutne między narzędziami; przećwicz masową mutację na kopii proda. |
| `05-git-and-deployments.md` | Szukanie w historii, cofanie/odzyskiwanie pracy, równoległe sesje i drabina branchowania, polityka deployu (origin, boot-check, tagi, changelog). |
| `06-collaboration-and-memory.md` | Plan→szkic→skala, mapa uprawnień (wolno/zapytaj/nigdy), język usera, wbudowana pamięć, podsumowanie zmian, przekazanie stanu przy urwaniu kontekstu. |
| `07-new-project-day-0.md` | Jedyna checklista: wpięcie The Craft (zwykły wskaźnik w CLAUDE.md/AGENTS.md), brief → `project-brief.md`, kroki Dnia 0, szkielet `CLAUDE.md`. |
| `08-stack-and-technologies.md` | Domyślny stack (Python domyślnie — Go, Rust, Kotlin, TypeScript, gdy lepiej pasują do zadania; SQLite, HTML z serwera, monolit na jednym VPS, Lucide) i kiedy od niego odejść — z ADR. |
| `09-law-and-protecting-the-creator.md` | Nigdy nie wymyślaj danych prawnych ani nie deklaruj niezrealizowanych praktyk; zawartość regulaminu/polityki; zgoda przed trackerami; indeks bezpieczeństwa. |
| `10-seo-and-translations.md` | hreflang + x-default, kompletność języków jako test, strażnicy jakości stron programatycznych, YMYL/E-E-A-T, przegląd wrażliwych tłumaczeń, RTL. |
| `11-data-model-and-normalization.md` | Słowniki lookup, slug zamiast ID, active-row, świadoma denormalizacja. |
| `12-flexibility-and-scalability.md` | Rozdziel warstwy, feature flags, scale-to-zero vs always-on, nie over-engineeruj. |
| `13-performance-frontend-and-sql.md` | Mierz najpierw, indeksy + partial index, brak N+1, streaming czatu, CWV, mobilny viewport (dvh/visualViewport). |
| `14-operational-resilience.md` | Runtime odporny na crash, wznawialne joby, czas życia runnera, wrogie źródła zewnętrzne, limity providera (SMTP), kwoty, observability, strażnicy zadań cyklicznych, config schedulera. |
| `15-scraping-ai-and-chatbots.md` | Skuteczny scraping (oficjalne źródło, walidacja kształtu, delta), AI-API do konkretnych zadań (kontrakt/cache/kwoty), konfigurowalne+ugruntowane chatboty. |
| `16-driving-claude.md` | Polityka projektu wobec agenta: kiedy plan mode jest obowiązkowy, autopilot w mapie uprawnień, model wg stawki, tło vs odpięte, subagenci, worktree na sesję. |
| `17-language-and-guards.md` | Kod po angielsku (także nazwy testów), proza w języku projektu; po angielsku w prozie zostają tylko nazwy drukowane przez narzędzie; dwaj strażnicy w `guards/`; zapadka. |
| `18-release-rehearsal.md` | dev → preprod → prod: ćwicz migracje i deploy na wiernej, zanonimizowanej kopii proda. |
| `19-database-swap-runbook.md` | Podmiana bazy proda z zachowaniem żywych kont: każda tabela z FK, slug nie ID, żywy prod jako źródło, okno maintenance, smoke. |

Rozdziały dzielą się na **rdzeń** (`00`–`08`) i **pogłębienie** (`09`–`19`). Każdy = jedno
przykazanie/temat, zwarty, zakończony antywzorcami.

## Indeks tematów → plik (grep-friendly)

> **Szukasz konkretu? Nie czytaj wszystkiego.** `grep -i <temat>` po tym indeksie (polskie keywordy) →
> nazwa pliku w tej samej linii → przeczytaj **tylko ten rozdział**. Tak oszczędzasz kontekst w
> docelowym projekcie (reguła: [01](01-documentation-and-ai-readme.md)).
> **To wersja PL** (tłumaczenie). Baza (EN) i jej keywordy są w rootcie ([`../AI_README.md`](../AI_README.md));
> slug pliku jest wspólny dla wszystkich języków. Inne języki: w analogicznych podfolderach.

- **`00-commandments.md`** — przykazania, dekalog, 10 przykazań, siedem grzechów głównych, złota zasada, altytuda, rdzeń doktryny, zasada zerowa, bootstrap, odstępstwo od reguły, wyjątek, precedencja, konflikt reguł, podłoga, nienegocjowalne.
- **`01-documentation-and-ai-readme.md`** — dokumentacja, AI_README, CLAUDE.md, README, docs, /docs, plany, docs/plans, grep, indeks słów kluczowych, oszczędność kontekstu, jeden plik jeden temat, tylko bieżący stan, artefakt generowany, struktura folderów.
- **`02-skills-and-refactoring.md`** — skill, slash-komenda, /run, /add-migration, automatyzacja, hook, refaktoring, prior-art, reuse, backward-compat, shim, SOLID, single responsibility, open/closed, dependency inversion, /simplify, /code-review.
- **`03-testing-and-verification.md`** — test, testowanie, TDD, test-first, piramida testów, unit, integration, e2e, Playwright, pytest, Jest, smoke test, weryfikuj nie deklaruj, regresja, CI.
- **`04-scripts-and-databases.md`** — skrypt, mutacja, dry-run, --execute, idempotencja, migracja, forward-only, backup, restore, retencja, seed, backfill, baza danych, ścieżka absolutna, przenośność ścieżek, /tmp niezgodność, granica narzędzi, Git Bash vs Python ścieżka, przećwicz mutację na kopii proda, snapshot, integrity_check, foreign_key_check.
- **`05-git-and-deployments.md`** — git, git log -S, pickaxe, blame, historia, .gitignore, CRLF, sieroty, niezacommitowana praca, opis commita, cofanie, odzyskiwanie utraconej pracy, reflog, git restore, reset --soft, ORIG_HEAD, odzyskanie skasowanej gałęzi, przywrócenie pliku ze starego commita, stash, punkt zapisu, straciłem commity, git straszy, issue, issues, GitHub Issues, gałąź, branching, drabina branchowania, trunk-based, feature branch, develop, PR, pull request, review, równoległe sesje, wiele sesji AI, solo developer, cherry-pick, merge wmiata pracę innej sesji, deploy, wdrożenie, polityka deployu, nigdy auto-deploy, origin vs lokalne, niewypchnięte commity, boot-check przed reloadem, okno maintenance, zero-downtime, tag deployu, rollback, changelog, runbook, lekcje z incydentów, nocny backup.
- **`06-collaboration-and-memory.md`** — współpraca, plan iteruj review, pamięć, potwierdzaj nieodwracalne, raportuj uczciwie, feedback, podsumowanie zmian, widget, następne działania, język natywny, mapa uprawnień, tabela uprawnień, co mi wolno, wolno/zapytaj/nigdy, granica, trwała autoryzacja, zgoda per-akcja, przekazanie stanu, urywa się kontekst, kompaktowanie, podsumowana sesja, długa sesja, wznowienie, podjęcie zadania, stan w drzewie.
- **`07-new-project-day-0.md`** — nowy projekt, Dzień 0, checklista, brief, brief produktowy, project-brief.md, monetyzacja, onboarding, setup, wpięcie The Craft, docs/rules, submodule, wskaźnik, AGENTS.md, szkielet CLAUDE.md, poziom techniczny, języki usera, znane technologie, polityka językowa, minimalny Dzień 0.
- **`08-stack-and-technologies.md`** — Go, Golang, Rust, Kotlin, TypeScript, wybór języka wg dopasowania, wybór języka, przepisanie dla szybkości, stack, technologie, Python, Node.js, FastAPI, SQLite, PostgreSQL, Docker, nginx, pm2, Hetzner, VPS, monolit, serverless, scale-to-zero, ADR, Lucide, baseline, Claude Code, GitHub, Git, GitHub Issues, TDD.
- **`09-law-and-protecting-the-creator.md`** — prawo, regulamin, polityka prywatności, RODO, zgody, cookie, trackery, disclaimer, jurysdykcja, prawo właściwe, JDG, placeholder, wymyślony NIP, bramka wieku, 18+, retencja danych, prawa użytkownika, usunięcie konta, ochrona twórcy, checklista bezpieczeństwa, IDOR, autoryzacja.
- **`10-seo-and-translations.md`** — SEO, hreflang, JSON-LD, schema, canonical, sitemap, meta, OG, Open Graph, E-E-A-T, YMYL, programmatic SEO, tłumaczenia, i18n, l10n, parytet językowy, RTL, lokalizacja.
- **`11-data-model-and-normalization.md`** — model danych, normalizacja, denormalizacja, słownik lookup, controlled vocabulary, slug, slug zamiast ID, active-row, expired_at, partial index, junction, M:N, klucz obcy, ERD, schemat.
- **`12-flexibility-and-scalability.md`** — elastyczność, skalowalność, rozdziel warstwy, granice, feature flag, ship dark, ramp, scale-to-zero, always-on, cold start, cache, inwalidacja, over-engineering, ADR.
- **`13-performance-frontend-and-sql.md`** — wydajność, mierz najpierw, Lighthouse, Core Web Vitals, CWV, LCP, CLS, INP, indeks, partial index, EXPLAIN QUERY PLAN, N+1, SELECT *, WAL, WebP, cache busting, lazy load, streaming, SSE, paginacja, mobile, viewport, dvh, 100vh, visualViewport, klawiatura ekranowa, safe-area, flex-basis, responsywność, emulator urządzenia, getBoundingClientRect, test profilu urządzenia.
- **`14-operational-resilience.md`** — odporność, runtime, crash, unhandledRejection, uncaughtException, pętla restartów, retry, backoff, timeout, 429, rate limit, rotacja, User-Agent, wznawialne, checkpoint, scraper, długie joby, SMTP, 587, STARTTLS, deliverability, SPF, DKIM, poczta, kwota, koszt, abuse, sesje, MemoryStore.
- **`15-scraping-ai-and-chatbots.md`** — scraping, scraper, crawler, robots.txt, selektor, parsing, BeautifulSoup, requests, fuzzy match, rapidfuzz, dedup, delta, incremental, AI API, LLM, model, JSON schema, tool use, kontrakt wyjścia, cache, kwota, chatbot, asystent, system prompt, grounding, RAG, prompt injection, halucynacja, eval, golden set, disclaimer.
- **`16-driving-claude.md`** — Claude Code, plan mode, planowanie, autopilot, auto-accept, autonomia, mapa uprawnień, wybór modelu, model wg stawki, tło, odpięty proces, długie joby, subagent, fan-out, równolegle, adwersarialna weryfikacja, git worktree, równoległe sesje, wspólny checkout, skill, hook.
- **`17-language-and-guards.md`** — język, angielski, język kodu, język prozy, nazewnictwo, identyfikatory, nazwy testów, nazewnictwo testów, polskie identyfikatory, dwujęzyczność, język mieszany, język docstringów, język komentarzy, polityka językowa CLAUDE.md, wdrożenie, terminy techniczne w prozie, nazwy drukowane przez narzędzie, strażnik, strażnicy, guards/, egzekwowanie reguł, strażnik AI_README, strażnik indeksu, każdy moduł w indeksie, sufit rozmiaru, 20 kB, strażnik języka kodu, zapadka, ratchet, baseline, --write-baseline, wyjątek datowany, wpięcie w Dniu 0.
- **`18-release-rehearsal.md`** — preprod, staging, dev/preprod/prod, trzy środowiska, próba generalna deployu, przećwicz migrację, zanonimizowany refresh, basic-auth, noindex, ACME bypass, SITE_URL override, env-overridable, klucz deployowy
- **`19-database-swap-runbook.md`** — swap bazy, podmiana bazy proda, zachowanie kont, tabele użytkownika, kolejność FK, remap po slugu, żywy prod jako źródło, okno maintenance, pm2 stop, backup przed swapem, integrity_check, foreign_key_check, sessions.db, gitignorowane assety, rsync, smoke po swapie, runbook, lekcje z incydentów

## Architektura `index.html` (kontrakt)

Jeden plik, bez zależności build. Mechanika:

- **`CHAPTERS`** (tablica w `<script>`) — **jedyne źródło** listy rozdziałów. Z niej generują się:
  karty na stronie głównej, `<select>` w czytniku, nawigacja prev/next. Pola: `file, no, group
  ("core"|"deep"), title, desc`.
- **Routing przez hash:** `#NN-nazwa` → widok rozdziału; pusty/`#` → strona główna. `route()`
  reaguje na `hashchange`.
- **Język (treść + cały chrome):** `LANG` (`en`/`pl`, domyślnie **`en`**, zapis w `localStorage` `rzemioslo-lang`).
  Treść rozdziału z `file` (EN, root) albo `pl/`+`file` (PL). **Chrome jest w pełni dwujęzyczny** —
  słownik `UI` (`data-i18n`/`data-i18n-html`) + `CH_EN` (tytuły/opisy rozdziałów) + `BRIEF_FIELDS`
  (pola briefu); `applyChrome()` przerysowuje wszystko przy starcie i przy `#langToggle`. Dodajesz
  string do chrome → dodaj klucz do `UI` (oba języki), inaczej zostanie po polsku.
- **Render (dwutorowo):** najpierw `fetch(langPath(file))` (świeże `.md`, gdy serwowane); na błędzie
  fetcha (`file://`) — snapshot `window.RZEMIOSLO_DOCS[LANG][slug]` z `content.js`. Wynik →
  `marked.parse()` → `.prose`, cache w pamięci (`cache[LANG+":"+file]`).
- **`rewriteLinks()`** po renderze: linki `*.md` → `#slug` (nawigacja w SPA), `index.html` → `#`,
  zewnętrzne `http(s)` → `target=_blank`; tabele owijane w `.tablewrap` dla scrolla na mobile.
- **Motyw:** `[data-theme]` na `<html>` (`light`/`dark`); brak atrybutu = wg systemu. Przełącznik
  w topbarze zapisuje wybór w `localStorage` (`rzemioslo-theme`); skrypt w `<head>` ustawia go
  przed renderem (bez mignięcia).
- **Notatka-fallback** pokazuje się tylko, gdy zawiodą **oba** źródła (brak `content.js` i `file://`).

## Gotchas

- **`file://` blokuje `fetch`** — dlatego treść działa z dwukliku **tylko** ze snapshotu
  `content.js`. Po edycji `.md` uruchom `python build.py`, inaczej `file://` pokaże stare treści.
  Serwowane (`http(s)://`, GitHub Pages) zawsze bierze świeże `.md`; na GitHubie `.md` renderują się natywnie.
- **`content.js` jest generowany** — nie edytuj ręcznie (build nadpisze). Commituj go, by `file://`
  działało po sklonowaniu repo.
- **`marked` ładowany z CDN** — bez sieci render nie zadziała (jest miękki fallback do `<pre>`).
- **`index.html` NIE zawiera treści rozdziałów** — czyta `.md`/`content.js`. Nie wklejaj treści do HTML.
- **Nowy rozdział → `python add_chapter.py NN slug --title-en … --title-pl … --desc-en … --desc-pl … --keywords-en … --keywords-pl …`**
  (dry-run; `--execute` zapisuje) — wpina wszystkie miejsca naraz i odpala `build.py` + `test.py`. Dokłada tylko
  kolejny numer; wersji nigdy nie zmienia. Ręczna edycja jednego miejsca = martwy wpis; `test.py` go złapie.
- **Format rozdziału:** jednolinijkowy wstęp (które przykazanie), **Reguły** (numerowane, w trybie
  rozkazującym, jedna linia + dlaczego), **Antywzorce**. Bez wykładów i bez zakończeń „W praktyce" —
  wyjaśnienia są na stronie, jedyna checklista to `07`.
- **Parytet EN↔PL:** zmiana reguły w dowolnym rozdziale (EN, kanon) wymaga aktualizacji odpowiednika w `pl/` (ta sama
  lista, te same nazwy plików). PL to **tłumaczenie**, nie osobna doktryna. `content.js` trzyma oba języki.
- **Nazwy plików = stabilne kotwice** (`#NN-nazwa`, cele linków względnych), **wspólne dla EN i PL**.
  Nie lokalizujemy nazw plików — tylko treść w środku. Nie zmieniaj bez powodu.
- **Marka:** zmiany kolorów rób na zmiennych CSS (`--accent`, `--accent-2`, `--grad`), nie na
  wartościach w miejscu użycia. Tryb jasny i ciemny muszą oba wyglądać dobrze.
- **Treść generyczna, nie „pod jeden projekt".** Konkretne projekty służą
  tylko za ilustrację (`np. …`, „projekt referencyjny"), nigdy za temat rozdziału. Nie czyń żadnego projektu bohaterem doktryny.
- **Dwa języki: EN (kanon, root, baza) + PL (`pl/`).** Pisz reguły przekładalnie. Kierunek i konwencja →
  [docs/packaging.md](../docs/packaging.md). Paczki per język montuje Web.

## Liczby

- 20 rozdziałów (`00`–`19`) + `README.md`, w **dwóch językach** (EN root = baza + PL `pl/`).
  Rdzeń: 9 plików (00–08). Pogłębienie: 11 (09–19).
- `index.html`: 1 plik; runtime z CDN (`marked` + Google Fonts). Build: `build.py` → `content.js`
  (EN: 22 dok. ~66 tys. znaków; PL: 21 dok. ~61 tys. znaków — rozdziały + `intro` + README; struktura `{lang:{slug:md}}`).
- **Dokumenty specjalne (poza numerowaną listą):** `intro.md` (krótkie wprowadzenie, route `#intro`) i widok
  briefu (`#brief`) — routowane osobno, nie ma ich w tablicy `CHAPTERS`.
- **Smoke test:** `python test.py` (parytet PL↔EN, martwe linki, świeżość `content.js`, spójność
  `CHAPTERS`/tabel/`craft.json`, statyczna nawigacja `index.html`: linki `href="#…"` + `data-i18n`↔`UI`
  + `data-bf-label`↔`BRIEF_FIELDS`). Plus „test ręczny" = podgląd przez serwer **i** z dwukliku (`file://`)
  + klik po rozdziałach i przełącznik EN/PL (zachowanie runtime JS, którego smoke nie łapie).
