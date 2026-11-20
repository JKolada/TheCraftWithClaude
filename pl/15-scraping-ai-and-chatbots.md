# 15 — Scraping, API AI i konfigurowalne chatboty

> Dane z sieci i AI jako funkcje produktu — skutecznie, tanio i **na kontrakcie**. Warstwa operacyjna
> (timeouty, backoff, kwoty, wznawialność) → [14](14-operational-resilience.md).

## Scraping

1. **Najpierw oficjalne źródło** (API, feed, eksport, sitemap); scraping HTML to ostateczność.
2. **Szanuj źródło:** `robots.txt`/regulamin, rozsądny throttle, prawdziwy User-Agent (→ [09](09-law-and-protecting-the-creator.md)).
3. **Strona odpowiada dwa razy — polityką i maszynerią.** Gdy `robots.txt` pozwala na odczyt, a tarcza
   antybotowa blokuje, przedstaw się i **zapytaj właściciela**; nigdy nie buduj obejścia tarczy. Jeśli prośba
   nie przejdzie, źródło wypada z produktu.
4. **Odróżnij blokadę IP od tarczy, zanim cokolwiek zbudujesz:** 403 tutaj, a 200 z innej sieci = zablokowany
   adres (przenieś pobieranie); 403 z każdej sieci = tarcza jest sednem.
5. **Waliduj kształt wyniku**, nie status — dryf selektora podnosi alarm, nigdy ciche zera.
6. **Normalizuj u wejścia** względem tabel lookup (→ [11](11-data-model-and-normalization.md)); pobieraj
   **deltę**, nie cały katalog; loadery są idempotentne (→ [04](04-scripts-and-databases.md)).

## API AI

7. **LLM tylko tam, gdzie deterministyczny kod nie daje rady** (ekstrakcja z nieustrukturyzowanego tekstu,
   klasyfikacja, streszczenia) — nigdy do tego, co zrobi regex, SQL albo funkcja.
8. **Wymuś kontrakt wyjścia:** JSON schema / tool use, walidacja, ponowienie przy niezgodności. Wyjście LLM to niezaufane wejście.
9. **Cache dla identycznych wejść; kwota na każde płatne wywołanie; wzbogacaj offline w batchu
   z checkpointami**, a nie na żywo w żądaniu usera. Mierz koszt i latencję per zadanie.

## Chatboty

10. **Persona, zakres i reguły to konfiguracja** (wersjonowane dane), nie kod — strojone bez deployu.
11. **Ugruntowane w Twoich danych, ze źródłem**; bezpieczne „nie wiem" zamiast zmyślania.
12. **Treść usera i z sieci to dane, nigdy instrukcje** (prompt injection): żadnej akcji ze skutkami bez
    potwierdzenia, żadnego wycieku system promptu ani sekretów.
13. **Złoty zestaw pytań chodzi jak testy** przy każdej zmianie promptu.
14. **Disclaimer i podstawa prawna dla przechowywanych rozmów** (→ [09](09-law-and-protecting-the-creator.md)).

## Antywzorce
- 🚫 Scraping, gdy istnieje API; pełny re-scrape co noc.
- 🚫 Obchodzenie tarczy antybotowej, którą postawił właściciel.
- 🚫 Parsowanie wolnej prozy i nadzieja na format.
- 🚫 Brak cache'u i kwoty na płatnych wywołaniach.
- 🚫 Persona wbita w kod; nieugruntowany asystent.
- 🚫 Akcja na podstawie wiadomości z czatu bez potwierdzenia.
