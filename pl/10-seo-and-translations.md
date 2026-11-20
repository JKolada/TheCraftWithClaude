# 10 — SEO i tłumaczenia

> Przykazanie III zastosowane do widoczności: indeksowalne, kompletne w każdym języku, zmierzone — nie
> „chyba OK". Standardowe SEO strony (unikalny title i description, canonical, sitemap, `robots.txt`, jedno
> `h1`, czyste slugi, karty OG) jest założone; tu są reguły, które łatwo zepsuć.

## Reguły

1. **Wielojęzyczne = wzajemne `hreflang` dla każdej pary języków + `x-default`.** Bez tego wyszukiwarka
   serwuje zły język.
2. **Kompletność języków to test, który pada:** brakujący klucz albo strona w dowolnym języku psuje build (→ [03](03-testing-and-verification.md)).
3. **Strony prawne i UI istnieją w każdym wydanym języku** (→ [09](09-law-and-protecting-the-creator.md)).
4. **Strony programatyczne potrzebują strażników jakości** (minimum pozycji, ocen, źródeł) i ręcznie
   pisanego wstępu — cienka strona generowana masowo to spam.
5. **Tematy YMYL (zdrowie, pieniądze, bezpieczeństwo) wymagają E-E-A-T:** nazwany autor i operator,
   cytowane źródła, żadnej regulowanej porady — zamiast niej disclaimer i ścieżka kryzysowa.
6. **Rejestr jest częścią tłumaczenia:** poprawne, ale zimne copy to bug. Tłumaczenie maszynowe jest OK na
   szkielet; **człowiek przegląda disclaimery, komunikaty kryzysowe i teksty prawne.**
7. **Języki RTL lustrzanie odwracają cały layout**, nie tylko tekst.
8. **Mierz, co konwertuje** (Search Console, zanonimizowana analityka) i niech to wybiera następną stronę do napisania.
9. **Core Web Vitals to sygnał rankingowy** → mierz i poprawiaj (→ [13](13-performance-frontend-and-sql.md)).

## Antywzorce
- 🚫 Upychanie słów kluczowych; cienkie strony programatyczne.
- 🚫 Strona wielojęzyczna bez `hreflang`.
- 🚫 Nieprzejrzane tłumaczenie maszynowe wrażliwego copy.
- 🚫 Strona prawna tylko po angielsku w produkcie wielojęzycznym.
