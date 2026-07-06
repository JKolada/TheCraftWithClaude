# 13 — Wydajność: frontend i SQL

> Przykazanie III w czystej postaci: *weryfikuj, nie deklaruj* — zastosowane do szybkości.
> „Wydaje się szybciej" nie istnieje. Istnieją **liczby przed/po**.

Wydajność to nie przeczucie, to pomiar. Najczęstszy błąd optymalizacji: zgadywanie, co jest
wolne, i „poprawianie" tego bez dowodu, że było problemem. Mierz **najpierw**, popraw to, co
metryka wskazuje, i **udowodnij liczbą**, że poprawiłeś. Wydajność to też SEO (Core Web Vitals
→ [10](10-seo-and-translations.md)) i koszt (szybsze zapytanie = tańszy serwer → [12](12-flexibility-and-scalability.md)).

## Mierz najpierw
- **Lighthouse / Core Web Vitals**: LCP (largest contentful paint), CLS (layout shift),
  INP (interaction), TBT. To są twarde liczby, nie wrażenia.
- **Przed/po, nie „wydaje się szybciej".** Np. optymalizacja home: preload hero,
  GPU-promoted animacje, `content-visibility: auto` poniżej folda; raportujesz LCP przed i po,
  nie „chyba lżej". → [03](03-testing-and-verification.md)
- **SQL: `EXPLAIN QUERY PLAN`** mówi, czy zapytanie używa indeksu, czy skanuje całą tabelę.

## Frontend
- **Code-splitting** + **lazy-load below-fold** — nie ładuj tego, czego user nie widzi.
- **Obrazy**: WebP (np. konwersja wszystkich do WebP q=95), responsive `srcset`,
  **preload hero** (LCP), reszta lazy.
- **Fonty**: self-host (np. Playfair/Outfit, jak na jakub.solutions), `font-display: swap` — tekst
  widoczny zanim font dojdzie.
- **`content-visibility: auto`** na sekcjach poniżej folda — przeglądarka pomija render niewidocznego.
- **GPU-promoted animacje** (`translateZ(0)`/`transform`) zamiast layoutujących właściwości.
- **Cache statyków**: `immutable` + długi `max-age` na prodzie (np. 7 dni immutable prod).
- **Cache-busting per deploy**: skoro CSS/JS są `immutable`, doklej `?v=<git-short-hash>` do
  każdego linku — każdy deploy zmienia URL → świeży pobór. Bez tego user widzi **starą apkę**
  (rozjechany layout) aż do twardego odświeżenia (→ [05](05-git-and-deployments.md)).
- **Streaming / SSE dla czatu** — odpowiedź LLM **token-by-token** (np. przez SSE), user widzi
  pierwsze słowa od razu, a nie pustkę do końca generacji. → [08](08-stack-and-technologies.md)
- **Server-side pagination** — nigdy nie ślij całego katalogu do przeglądarki (np.
  paginacja po stronie serwera dla ~kilku tysięcy pozycji).

## Mobile: viewport to ruchomy cel

Na telefonie viewport **nie jest stałym prostokątem**: pasek URL rośnie i kurczy się przy scrollu, a
klawiatura ekranowa zjada dolną połowę. Potraktuj go jako statyczny, a dostajesz elementy schowane **za**
klawiaturą albo wysoki pusty pas tam, gdzie *był* pasek URL. Mierz **realny** viewport — nie zakładaj go.

- **Używaj jednostki dynamicznej.** `100dvh` (dynamic viewport height) na pełnoekranowy panel — **nie** `100vh`
  (to *największy* viewport i wchodzi pod pasek URL). Zadeklaruj najpierw `height: 100vh` jako fallback, potem
  `height: 100dvh` jako override — **kolejność właściwości ma znaczenie**, stary silnik trzyma ostatnią regułę, którą rozumie.
- **Elementy „przyklejone" nad klawiaturą kotwicz do `visualViewport`, nie do layout viewport.** Input czatu albo
  sticky CTA na `position: fixed; bottom: 0` jest mierzony względem *layout* viewport i wjeżdża pod klawiaturę.
  Jedyną pewną kotwicą jest **API `visualViewport`** (`.height`/`.offsetTop`, odczyt na jego `resize`/`scroll`)
  — zasłania różnice zachowania klawiatury iOS vs Android. Skacz do nowego rozmiaru; **nie animuj** otwarcia
  klawiatury (`transition`/`transform` na evencie klawiatury daje widoczny skok).
- **`flex-basis` ustawiony dla wiersza staje się WYSOKOŚCIĄ w kolumnie.** `flex: 1 1 220px` to podpowiedź
  *szerokości* w wierszu; ta sama reguła pod breakpointem `flex-direction: column` robi **pusty box wysoki na 220px.**
  Zresetuj basis (`flex: 0 0 auto`) na breakpoincie, gdzie oś główna się obraca.
- **Emulator kłamie; DOM i urządzenie nie.** Device-mode desktopowej przeglądarki renderuje elementy `dvh`/fixed
  inaczej niż realny telefon — nie „naprawiaj" layoutu ze screenshota. Mierz
  `getBoundingClientRect()`/`getComputedStyle()` na realnych elementach i trzymaj **projekt testowy na profilu
  urządzenia** (np. osobny projekt Playwright przypięty do telefonu), który co przebieg sprawdza geometrię: brak
  poziomego overflow, taby w jednej linii, kluczowy element nad foldem. *Weryfikuj, nie deklaruj* (→ [03](03-testing-and-verification.md)).

## SQL
- **Indeksy** na kolumnach z `WHERE` i `JOIN` — gorące zapytanie bez indeksu to skan całej tabeli.
- **Partial indexes** — np. `uniq_prices_active … WHERE expired_at IS NULL` (indeks
  tylko na aktywnych cenach — mniejszy, szybszy, wymusza unikalność, → [11](11-data-model-and-normalization.md)).
- **`EXPLAIN QUERY PLAN`** przed i po dodaniu indeksu — dowód, że plan się zmienił.
- **Unikaj N+1** — nie zapytanie w pętli po każdym wierszu; batch/join za jednym razem.
- **`SELECT` tylko potrzebnych kolumn** — nie `SELECT *`, gdy potrzebujesz trzech pól.
- **Paginacja server-side** + **cache'owane agregaty** (np. `site_stats` zamiast
  `COUNT(*)` po całej bazie na każde wejście na home).
- **WAL** (SQLite) — czytelnicy nie blokują pisarza; domyślny tryb w projekcie referencyjnym.
- **Ostrożnie z `LIKE '%foo'`** — wiodący wildcard zabija indeks (full scan); rozważ FTS, jeśli
  to gorąca ścieżka wyszukiwania.

## Anty-wzorce
- 🚫 **Optymalizacja bez pomiaru** — „poprawiłem", nie wiedząc, czy było wolne (→ [03](03-testing-and-verification.md)).
- 🚫 **Brak indeksu na gorącym zapytaniu** — najczęstsza przyczyna wolnej strony katalogu.
- 🚫 **N+1 w pętli** — 200 zapytań tam, gdzie wystarczył jeden join.
- 🚫 **`SELECT *`** — przesyłasz i deserializujesz kolumny, których nie używasz.
- 🚫 **Client-side pagination ogromnych zbiorów** — ślesz kilka tysięcy rekordów, by pokazać 20.
- 🚫 **Blokowanie UI w oczekiwaniu na pełną odpowiedź LLM** zamiast streamingu (→ [12](12-flexibility-and-scalability.md)).
- 🚫 **Brak cache drogich agregatów** — `COUNT(*)` po całej bazie na każde żądanie.
- 🚫 **`100vh` na pełnoekranowy panel mobilny** — dół chowa się pod paskiem URL/klawiaturą (użyj `dvh` + `visualViewport`).
- 🚫 **`position: fixed; bottom: 0` na input przyklejony nad klawiaturą** — wjeżdża pod klawiaturę (kotwicz do `visualViewport`).
- 🚫 **flex-basis przeniesiony z wiersza w breakpoint kolumny** — wysoki pusty box (zresetuj basis, gdzie oś się obraca).
- 🚫 **„Naprawianie" mobile ze screenshota z desktopowego emulatora** — naprawiasz artefakt; mierz realną geometrię DOM / testuj na profilu urządzenia.

## Dla nowych projektów
Wpisz do Dnia 0 (→ [07](07-new-project-day-0.md)): **baseline Lighthouse** zaraz po
pierwszej działającej stronie (masz punkt odniesienia), indeksy na kolumnach filtrów od
pierwszej migracji, `EXPLAIN QUERY PLAN` jako nawyk przy każdym gorącym zapytaniu. Reguła
nadrzędna: **żadna optymalizacja bez liczby przed i po** — bo bez dowodu „optymalizacja" bywa
regresją w przebraniu (→ [03](03-testing-and-verification.md)). Szybkość to jednocześnie SEO
(→ [10](10-seo-and-translations.md)) i koszt infrastruktury (→ [12](12-flexibility-and-scalability.md))
— jedna inwestycja, trzy zwroty.
