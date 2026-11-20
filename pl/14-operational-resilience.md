# 14 — Odporność operacyjna i zewnętrzne zależności

> Przykazania III, V, VI w runtime: prod żyje w zawodnym świecie. Najgorsze bugi nie krzyczą — zawieszają,
> wylogowują wszystkich albo drenują budżet. Prawie każdą regułę tutaj opłacił incydent.

## Reguły

1. **Jeden zły request degraduje ten request, nie usługę:** łapacze na poziomie procesu dla nieobsłużonych
   rejection/wyjątków, trasy async przekazujące błędy dalej, handler 500 bez wycieku stack trace'a. Broń się
   przed realnymi danymi z brzegu (konto OAuth bez hasła, `null` tam, gdzie zakładasz string).
2. **Długie zadania są wznawialne:** checkpoint skończonych jednostek, zapis co N, idempotencja całości —
   crash kosztuje ostatni batch, nie cały przebieg.
3. **Dopasuj runner do czasu życia zadania:** tło agenta przeżywa tury, ale umiera z sesją; wszystko, co
   ma przeżyć rozmowę, chodzi jako **proces odpięty albo zadanie schedulera systemu**.
4. **Zewnętrzne źródła są wrogie:** timeout na każde wywołanie, retry z wykładniczym backoffem i limitem
   prób, i **waliduj odpowiedź, nie status** — „200 + strona błędu" to porażka.
5. **Sieć providera psuje działający kod dopiero na prodzie:** np. wychodzący SMTP 465 zablokowany → 587 +
   STARTTLS z twardymi timeoutami połączenia/powitania. „Wysłane" ≠ dostarczone: zweryfikowana domena nadawcy
   (SPF/DKIM) i realna wysyłka testowa. Sprawdzaj u providera, nie lokalnie.
6. **Każdy płatny zasób stoi za twardą kwotą** — per user i tier, egzekwowaną po stronie serwera, z jasnym
   komunikatem i datą resetu podaną z góry.
7. **Wiedz, że prod żyje:** logi strukturalne z poziomami (bez sekretów, bez pełnych PII), `/healthz`,
   zewnętrzny ping uptime, alerty na to, co boli (skoki 5xx, nieudane płatności/maile, job, który nie
   ruszył), błędy kierowane tam, gdzie je zobaczysz.
8. **Zadania cykliczne: pilnuj wyniku, nie runnera.** Sprawdzaj **wiek najświeższego rekordu per źródło**
   (`MAX(updated_at)` grupowane po źródle), nie kod wyjścia — zielony raport chodził kiedyś trzy dni obok
   44% zamrożonych danych. Raport pokrywa tylko ścieżki, o których wie.
9. **Ustawienia schedulera to produkcja i żyją poza repo** (ponowienie po przegapionym starcie, warunki
   zasilania i sieci, konto, katalog roboczy) — wpisz je do runbooka i sprawdzaj po każdej zmianie systemu,
   sprzętu albo konta.
10. **Każdy incydent staje się datowaną, numerowaną lekcją w runbooku** (→ [05](05-git-and-deployments.md)).

## Antywzorce
- 🚫 Brak globalnego łapacza — jeden zły request restartuje usługę wszystkim.
- 🚫 Długi scraper bez checkpointów, odpalony z tła sesji.
- 🚫 Zewnętrzne wywołanie bez timeoutu i backoffu.
- 🚫 Płatne API bez kwoty.
- 🚫 Sesje w pamięci procesu — każdy deploy wylogowuje wszystkich.
- 🚫 Zadanie cykliczne pilnowane własnym kodem wyjścia.
- 🚫 Sekrety albo PII w logach.
