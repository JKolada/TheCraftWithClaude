# 18 — Próba generalna wydania: dev → preprod → prod

> Przykazania V i VI: migracja albo swap bazy odpalony **pierwszy raz** w prodowym oknie maintenance jest
> testowany na Twoich userach. Najpierw odpal dokładnie ten runbook raz na wiernej kopii.

## Trzy środowiska, trzy zadania

| Środowisko | Zadanie | Dane |
|---|---|---|
| **dev** (Twoja maszyna) | budowanie, odtwarzanie bugów | dane seed albo **zanonimizowany** refresh z backupu proda |
| **preprod** (serwerowy klon proda: ten sam system, serwer WWW, menedżer procesów, TLS) | próba migracji i samego deployu | zanonimizowany backup proda; **za basic-auth, `noindex`** |
| **prod** | obsługa userów | święty — dotykany tylko na „wdrażaj", tylko krokami przećwiczonymi tego samego dnia na preprodzie |

Preprod dokładasz, gdy projekt wchodzi na trzeci szczebel branchowania albo przy pierwszej ryzykownej migracji (→ [05](05-git-and-deployments.md)).

## Reguły

1. **Buduj preprod z proda za każdym razem tak samo — skryptem:** klon kluczem deployowym proda; refresh bazy
   z backupu proda; **anonimizuj PII, zanim opuszczą proda** (→ [09](09-law-and-protecting-the-creator.md)).
2. **Wartości zależne od środowiska są nadpisywalne przez env, nigdy wpisane na sztywno:** `SITE_URL`,
   canonical, OG, sitemap wskazują na preprod — inaczej preprod przecieka prodowymi URL-ami albo trafia do indeksu (→ [10](10-seo-and-translations.md)).
3. **Ćwicz prawdziwy runbook, nie uproszczony:** odpal migrację, zmierz okno, zrób smoke, potwierdź, że jest
   forward-only i idempotentna (→ [04](04-scripts-and-databases.md)).
4. **Spodziewaj się pułapek, które ujawnia tylko prawdziwy preprod:** wyzwanie ACME/Let's Encrypt `http-01`
   musi omijać basic-auth, inaczej odnowienie certu pada z 401; prywatne repo potrzebuje zdalnego SSH przed pierwszym pullem.
5. **Preprod to scena prób, nigdy drugi prod:** bez żywych userów, nieświeża baza jest OK, a **jego bazy nigdy
   nie podmienia się z powrotem na prod** (→ [11](11-data-model-and-normalization.md)).

## Antywzorce
- 🚫 Migracja, której pierwszym przebiegiem jest prodowe okno maintenance.
- 🚫 Realne, niezanonimizowane dane userów na preprodzie — druga kopia odpowiedzialności za PII na słabszym boxie.
- 🚫 Preprod zaindeksowany albo emitujący prodowe URL-e.
- 🚫 Traktowanie danych preprodu jako źródła prawdy.
