# 13 — Wydajność: frontend i SQL

> Przykazanie III zastosowane do szybkości: „wydaje się szybciej" nie istnieje — istnieją **liczby przed
> i po**. Standardowa higiena jest założona (indeksy na gorących kolumnach `WHERE`/`JOIN`, brak N+1, brak
> `SELECT *`, WebP + `srcset`, lazy loading poniżej folda, fonty self-hosted z `font-display: swap`,
> paginacja po stronie serwera).

## Reguły

1. **Najpierw mierz, potem udowodnij.** Lighthouse / Core Web Vitals (LCP, CLS, INP) dla frontu,
   `EXPLAIN QUERY PLAN` dla SQL — raportowane **przed i po**. Żadnej optymalizacji bez liczby; niezmierzona
   „optymalizacja" bywa regresją w przebraniu.
2. **Baseline Lighthouse zaraz po pierwszej działającej stronie** — inaczej nie ma do czego porównać.
3. **Cache-busting per deploy:** statyki są `immutable` z długim `max-age`, więc każdy URL assetu niesie
   `?v=<git-short-hash>` — inaczej userzy jadą na starej aplikacji aż do twardego odświeżenia (→ [05](05-git-and-deployments.md)).
4. **Streamuj odpowiedzi LLM** token po tokenie (SSE) — nigdy pusty ekran do końca generacji (→ [15](15-scraping-ai-and-chatbots.md)).
5. **Drogie agregaty są cache'owane** (snapshot statystyk z fallbackiem na żywą bazę), nie liczone przy każdym żądaniu.

## Mobile: viewport to ruchomy cel

6. **`100dvh`, nie `100vh`, dla paneli pełnoekranowych** — najpierw `100vh` jako fallback, potem `100dvh`
   (wygrywa ostatnia reguła, którą silnik rozumie).
7. **Elementy przyklejone nad klawiaturą kotwicz do `visualViewport`** (`height`/`offsetTop`, odczyt na jego
   `resize`/`scroll`), nie `position: fixed; bottom: 0`. Skacz do nowego rozmiaru; nie animuj klawiatury.
8. **Resetuj `flex-basis` tam, gdzie obraca się oś główna** — `flex: 1 1 220px` z wiersza staje się w kolumnie
   pustym boxem wysokim na 220px (`flex: 0 0 auto` na tym breakpoincie).
9. **Emulator kłamie:** mierz realną geometrię (`getBoundingClientRect`) i trzymaj test na profilu urządzenia
   (np. projekt Playwright przypięty do telefonu): brak poziomego overflow, kluczowy element nad foldem.

## Antywzorce
- 🚫 Optymalizacja bez pomiaru.
- 🚫 Przeliczanie `COUNT(*)` po całej bazie przy każdym żądaniu.
- 🚫 Blokowanie UI do czasu pełnej odpowiedzi LLM.
- 🚫 Panele na `100vh` i inputy na `fixed; bottom: 0` na mobile.
- 🚫 „Naprawianie" mobile ze screenshota z desktopowego emulatora.
