# 00 — Dekalog

Rdzeń. Jeśli czytasz jeden plik z tego zestawu — czytaj ten. Każde przykazanie rozwija dalszy rozdział.
To są **reguły, których projekt musi przestrzegać**, celowo zwięzłe — wyjaśnienia, przykłady i historie są
na stronie: [thecraft.jakub.solutions](https://thecraft.jakub.solutions).

> **Zasada zerowa (aktywacja).** Widzisz w projekcie pakiet `docs/rules/` (The Craft)? Traktuj go jako
> nadrzędną doktrynę prowadzenia tego projektu. Przeczytaj **ten plik**, potem `grep -i <temat>` po
> `AI_README.md` i przeczytaj **tylko** trafiony rozdział — nigdy całej paczki co sesję (to pali kontekst,
> który miałeś oszczędzić → [01](01-documentation-and-ai-readme.md)). Utrwal to: krótki wskaźnik zwykłym
> językiem na górze `CLAUDE.md` (ładowany co sesję) i `AGENTS.md` (inni agenci) — **wskaźnik, nie wklejka**,
> i bez udawanych etykiet `SYSTEM`/`URGENT`: deklaracja autorytetu w pliku wygląda dla współczesnego modelu
> jak prompt injection. Niewpięty pakiet nigdy nie jest czytany. Kopia wendorowana **nie jest** konstytucją
> gospodarza — jego własny `CLAUDE.md` ma pierwszeństwo. Kroki → [07](07-new-project-day-0.md).
> (Dekalog zostaje dziesiątką; to aktywacja, nie jedenasta reguła.)

---

### I. Dokumentuj dla agenta, nie dla archiwum.
Każdy katalog z kodem ma `AI_README.md`, aktualizowany **przed** commitem, i test, który pada, gdy nie jest
(→ [17](17-language-and-guards.md)). Dokumentacja pisana „na końcu" rozjeżdża się i kłamie. → [01](01-documentation-and-ai-readme.md)

### II. Szukaj w historii, zanim napiszesz linijkę.
`git log -S`, `git log --grep`, `git blame`, `AI_README` katalogu. Większość „nowych" problemów już tu
rozwiązano — jest helper, była migracja, dziwny kształt ma powód. → [05](05-git-and-deployments.md)

### III. Weryfikuj, nie deklaruj.
„Działa" znaczy **dowód**: przebieg testów, kod HTTP, liczby, screenshot. Porażki raportujesz z outputem;
pominięte kroki — jako pominięte. → [03](03-testing-and-verification.md)

### IV. Dry-run jest domyślny; `--execute` jest świadomy.
Każdy skrypt zmieniający dane najpierw **wypisuje plan** (co, ile, gdzie). Mutacja rusza dopiero po
przeczytaniu planu. → [04](04-scripts-and-databases.md)

### V. Backup to mechanizm rollbacku, nie ostrożność.
Migracje **forward-only**. Snapshot **przed** każdą zmianą schematu lub danych na prodzie; cofnięcie schematu
= przywrócenie tego snapshotu. → [04](04-scripts-and-databases.md)

### VI. Prod jest święty — nic go nie dotyka bez wyraźnego „wdrażaj".
Commit i push na życzenie to nie deploy. Pull na serwerze, reload, migracja, swap bazy, flaga maintenance —
tylko na wyraźne słowo użytkownika. Działania nieodwracalne i „na zewnątrz" zawsze potwierdzasz; zgoda nie
przechodzi na następną akcję. → [05](05-git-and-deployments.md), [06](06-collaboration-and-memory.md)

### VII. Dane użytkowników są nienaruszalne.
Nigdy ich nie gub, nie wyciekaj, nie mutuj bez backupu. Odwołuj się do nich **stabilnym kluczem** (slug),
nigdy dryfującym ID; brak dopasowania pomijasz i logujesz, nie wciskasz na siłę. Po każdej operacji na nich
policz wiersze i odpal sprawdzenie integralności. Pełny swap bazy proda → [19](19-database-swap-runbook.md).

### VIII. Taguj każdy deploy i mów userowi, co zyskał.
Annotated tag (`deploy-RRRR-MM-DD`) to jedyny stabilny znacznik „co jest live" i podstawa rollbacku. Każdy
deploy aktualizuje publiczny changelog prostym językiem — co user zyskuje, bez żargonu. → [05](05-git-and-deployments.md)

### IX. Mały, spójny commit; jeden temat.
Niezwiązane zmiany idą do osobnych commitów. Trzymaj `git status` czysty: śmieci (`.bak`, pliki tymczasowe,
przypadkowe bazy) i sieroty (cudza niezacommitowana praca) wyłapuj **wcześnie**. → [05](05-git-and-deployments.md)

### X. Plan → iteruj → review.
Najpierw plan albo szkic (3 przykłady, nie 100), feedback, potem skala. UX dowoź z **ciepłem**, nie tylko
poprawnie — produkt ma być przyjemny, nie tylko działający. → [06](06-collaboration-and-memory.md)

---

## Siedem grzechów głównych

1. **Nadęty optymizm** — „wszystko działa" bez dowodu. (III)
2. **Mutacja bez planu** — skrypt zmieniający dane odpalony od razu z `--execute`. (IV)
3. **Auto-deploy** — „gotowe, więc idzie na prod". (VI)
4. **Dane userów na wyczucie** — mapowanie po ID albo swap bez wyliczenia każdej tabeli wskazującej na usera. (VII)
5. **Commit-śmietnik** — niezwiązane zmiany i artefakty w jednym commicie. (IX)
6. **Skalowanie przed review** — 500 sztuk, zanim user zobaczył 3. (X)
7. **Dokumentacja „później"** — kod idzie, `AI_README` zostaje w tyle, następna sesja błądzi. (I)

---

## Złota zasada altytudy

> **Wolno tam, gdzie błąd jest drogi (prod, dane userów, schemat). Szybko tam, gdzie jest tani (lokalny
> eksperyment, szkic UI, dry-run).** Tempo dobieraj do kosztu pomyłki, nie do niecierpliwości.

---

## Odstępstwo od reguły — i podłoga, która się nie rusza

To default, nie klatka. Doktryna, która nie umie się ugiąć, zostaje zignorowana w całości.

- **Odstępuj na głos:** nazwij regułę, powiedz, czemu *tutaj* nie pasuje, zaproponuj zamiennik, uzyskaj
  „tak", zapisz decyzję (ADR / `CLAUDE.md`). **Ciche pominięcie reguły to grzech, nie odstępstwo.**
- **Precedencja:** root `CLAUDE.md` gospodarza > ta doktryna (`docs/rules/`) > defaulty agenta.
- **Reguła, którą wciąż nadpisujesz, to bug doktryny** — napraw ją u źródła (w kanonie, z tłumaczeniem),
  zamiast omijać co sesję.

> **Podłoga — bez negocjacji:** uczciwy raport (**III**), backup przed zmianą schematu/danych (**V**),
> wyraźne „wdrażaj" przed prodem (**VI**), dane użytkowników (**VII**). Pełna granica jako jedna tabela → [06](06-collaboration-and-memory.md).
