# 12 — Elastyczność i skalowalność

> Złota zasada altytudy w architekturze: zmiana bez przepisywania, wzrost bez przebudowy — i skalowanie
> dopiero, gdy wymaga go metryka, nigdy „na wszelki wypadek".

## Reguły

1. **Warstwy rozdziela kontrakt, nie wspólny kod:** dane ↔ ingest ↔ web, spięte schematem
   (→ [11](11-data-model-and-normalization.md)) albo jawnym kontraktem API. Każdą stronę da się wtedy wymienić.
2. **Zmiany są addytywne i wstecznie zgodne:** nowa kolumna, endpoint czy język nie psują tego, co działa.
3. **Feature flagi wchodzą z pierwszą ryzykowną zmianą, która trafia do żywych userów** — wypuść po cichu,
   potem rozkręcaj. Nie w Dniu 0 prototypu; nigdy pomijane, gdy realni userzy są zagrożeni.
4. **Proces bezstanowy tam, gdzie się da**; sesje i stan idą do store'a (→ [14](14-operational-resilience.md)).
5. **Platforma to zapisany kompromis:** zawsze włączony VPS (stały koszt, bez cold startu) vs scale-to-zero
   (płacisz za użycie, cold start) — wybrany wg profilu ruchu i budżetu, zapisany jako ADR.
6. **Każdy cache ma jawną inwalidację** i podany czas życia.
7. **Pipeline'y są komponowalne i idempotentne:** każdy etap działa sam, ponowny przebieg jest bezpieczny (→ [04](04-scripts-and-databases.md)).
8. **Produkt globalny = i18n od pierwszego commita**, nie doklejane (→ [10](10-seo-and-translations.md)).
9. **Skaluj wg liczb:** SQLite → PostgreSQL, monolit → usługi, tylko gdy latencja, koszt albo rozmiar
   mierzalnie tego wymagają — z ADR (→ [13](13-performance-frontend-and-sql.md)).

## Antywzorce
- 🚫 Mikroserwisy, Kafka albo Kubernetes dla stu userów.
- 🚫 Stan w pamięci procesu, który blokuje restarty i skalowanie.
- 🚫 Przepisanie od zera zamiast addytywnych kroków.
- 🚫 Ryzykowna zmiana dla żywych userów bez flagi i bez rozkręcania.
- 🚫 Migracja do PostgreSQL „na wszelki wypadek", gdy SQLite się nawet nie spocił.
