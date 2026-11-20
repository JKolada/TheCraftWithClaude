# 09 — Prawo i ochrona twórcy

> Przykazania VI i VII na zewnątrz: solowy twórca albo jednoosobowa działalność wypuszczająca publiczną
> aplikację **odpowiada osobiście**. Regulamin, polityka prywatności i disclaimery to jego zbroja — pisana
> tak starannie jak migracja na prodzie. ⚠️ Higiena inżynierska, nie porada prawna: przed wiązaniem realnych
> userów na skalę — prawnik.

## Reguły

1. **Nigdy nie wymyślaj danych prawnych ani tożsamości.** Nazwa firmy, NIP, adres = placeholdery
   `[do uzupełnienia]` wypełniane przez właściciela. Widoczny placeholder bije wiarygodnie wyglądający fałsz.
2. **Nigdy nie deklaruj praktyki, której kod nie realizuje.** „Anonimizujemy", „usuwamy po N dniach", „nie
   czytamy rozmów" musi być prawdą w kodzie — najlepiej dowiedzioną testem (→ [11](11-data-model-and-normalization.md)).
3. **Jeden operator, nazwany identycznie wszędzie:** regulamin, polityka, stopka, faktury, UI.
4. **Regulamin zawiera:** operatora; czym usługa **jest, a czym nie** (np. „porównywarka, nie sprzedawca";
   „informacja, nie porada medyczna/prawna/finansowa"); obowiązki usera (legalne użycie, limit wieku);
   ograniczenie odpowiedzialności; moderację i usuwanie kont; IP (user zachowuje treści, udziela licencji);
   **prawo właściwe Twojej jurysdykcji**, reklamacje, sposób ogłaszania zmian, kontakt.
5. **Polityka prywatności zawiera:** administratora; każdą kategorię danych z celem, podstawą prawną
   i retencją; podmioty przetwarzające; prawa usera (dostęp, usunięcie, eksport, sprzeciw); cookies; wiek; kontakt.
6. **Zgoda przed trackerami.** Skrypty analityczne i marketingowe ładują się dopiero po zgodzie.
7. **Disclaimery pasują do domeny:** bramka wieku dla treści z ograniczeniem wiekowym; „to nie porada" dla
   zdrowia/prawa/finansów; zasoby kryzysowe per region dla produktów wrażliwych (→ [10](10-seo-and-translations.md)).
8. **Regulamin ↔ polityka ↔ UI ↔ kod mówią jedno.** Sprzeczność między warstwami jest gorsza niż brak klauzuli.
9. **Dokumenty prawne wchodzą do Dnia 0 jako placeholdery**, nie „później" (→ [07](07-new-project-day-0.md)).

## Checklista bezpieczeństwa (indeks)

Jedne drzwi; każda reguła jest egzekwowana tam, gdzie żyje.

- **Sekrety** w env / sejfie, rotowane po wycieku (→ [08](08-stack-and-technologies.md)).
- **Auth i sesje:** bcrypt albo OAuth, nagłówki bezpieczeństwa, rate-limit; sesje w trwałym store (→ [14](14-operational-resilience.md)).
- **Autoryzacja po stronie serwera:** *ten* user może dotknąć *tego* wiersza/akcji — nie tylko „zalogowany" (IDOR).
- **Wejście jest wrogie:** waliduj kształt, parametryzuj SQL, treść zewnętrzną i usera traktuj jako
  **dane, nie instrukcje** (→ [15](15-scraping-ai-and-chatbots.md)).
- **Błędy nie wyciekają:** żadnych stack trace'ów, sekretów ani PII do userów ani do logów (→ [14](14-operational-resilience.md)).
- **Kwoty** na płatnych/drogich endpointach (→ [14](14-operational-resilience.md)).

## Antywzorce
- 🚫 Wymyślony NIP, adres albo nazwa firmy w produkcie.
- 🚫 Copy obiecujące więcej, niż produkt robi („w pełni anonimowo", „gwarantowane ceny").
- 🚫 Regulamin i polityka z innym operatorem albo inną retencją.
- 🚫 Strona prawna w jednym języku w produkcie wielojęzycznym.
- 🚫 Analityka ładowana przed zgodą.
