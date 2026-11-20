# 06 — Współpraca i pamięć

> Przykazania VI i X: jak pracujemy razem i jak nie tracimy kontekstu.

## Styl współpracy (użytkownik + Claude)

- **Plan → iteruj → review.** Najpierw pokaż plan albo **mały szkic** (3 przykłady, nie 100),
  zbierz feedback, dopiero potem skaluj. Karty OG w projekcie referencyjnym: 3 → poprawki → 10 → poprawki
  → 100. Nigdy odwrotnie.
- **Rekomenduj, nie rozkładaj parasola opcji.** Gdy ważysz wybór — daj **rekomendację** z
  uzasadnieniem, nie wyczerpującą listę, której i tak nie zrealizujesz. Pytaj tylko, gdy
  odpowiedź realnie zmienia, co robisz dalej (i gdy nie wynika z kodu/sensownego defaultu).
- **Liczby weryfikuj u źródła** — nie z pamięci, nie z docsów.
- **UX z ciepłem.** Poprawność to minimum; produkt ma być przyjemny. Estetyka i ton się liczą
  (w produktach wrażliwych szczególnie: minimalistycznie, ale ciepło).
- **Mów w języku użytkownika.** Rozmawiaj z użytkownikiem w jego **natywnym** języku — najlepiej, gdy
  briefuje Cię w języku, w którym myśli. **Ustal go na starcie i zapisz, w ilu/jakich językach mówi/czyta
  w `AI_README`/`CLAUDE.md`** — to konfiguracja współpracy, ustawiana raz (→ [07](07-new-project-day-0.md), [01](01-documentation-and-ai-readme.md)).
  Kod i opisy commitów zostają po **angielsku** bez względu na język rozmowy; nazwy, które drukuje
  narzędzie (komendy, flagi, statusy), po angielsku wewnątrz dowolnego języka (→ [17](17-language-and-guards.md)).
- **Rozdzielaj niezwiązane rzeczy** — w commitach i w myśleniu. Jeden temat naraz.

## Potwierdzaj to, co nieodwracalne i „na zewnątrz"

Działania trudne do cofnięcia albo wychodzące poza maszynę **potwierdzaj pierwej**, chyba że
masz trwałą autoryzację albo wyraźne „rób bez pytania":
- deploy na prod, wysyłka maili, publikacja treści, kasowanie/nadpisywanie danych.
- **Zgoda w jednym kontekście nie rozciąga się na następny.** „Wdróż X" ≠ „wdrażaj wszystko zawsze".
- **Zanim skasujesz/nadpiszesz — spójrz na cel.** Jeśli to, co widzisz, przeczy opisowi, albo
  tego nie tworzyłeś — zgłoś, nie kasuj.
- Publikacja do zewnętrznego serwisu = treść może zostać zindeksowana/scache'owana, nawet po usunięciu.

### Mapa uprawnień — jedna tabela, trzy kolumny

Granica całej doktryny w jednym miejscu, żeby żadna ze stron nie musiała jej składać z sześciu rozdziałów.
To jest to, co użytkownik zatwierdza raz, w Dniu 0, i co agent czyta co sesję:

| ✅ Wolno — rób | ⏸️ Zapytaj, czekaj na „tak" | ⛔ Nigdy — kto by nie prosił |
|---|---|---|
| Czytaj/grepuj cokolwiek w repo | Deploy na prod, w każdej postaci (→ [05](05-git-and-deployments.md)) | Wymyślić dane prawne/tożsamości — NIP, adres, nazwę firmy (→ [09](09-law-and-protecting-the-creator.md)) |
| Odpalaj testy, lintery, buildy | Push/publikacja do zdalnego repo | Zadeklarować praktykę, której kod nie realizuje (→ [09](09-law-and-protecting-the-creator.md)) |
| Commituj lokalnie, często, mało (→ [00](00-commandments.md) IX) | Migracja albo swap bazy na prodzie (→ [04](04-scripts-and-databases.md)) | Zacommitować sekrety (→ [08](08-stack-and-technologies.md)) |
| Twórz/kasuj **własne** gałęzie | Wysyłka maili/wiadomości do realnych ludzi | Skasować backup, który jest czyimś rollbackiem (→ [04](04-scripts-and-databases.md)) |
| Odpalaj skrypty w **dry-run** (→ [00](00-commandments.md) IV) | Kasowanie/nadpisanie czegoś, czego nie tworzyłeś | Osłabić test albo guard, żeby zrobił się zielony (→ [03](03-testing-and-verification.md)) |
| Pisz/aktualizuj docsy, `AI_README`, plany | Dołożenie płatnej usługi lub zależności (→ [14](14-operational-resilience.md)) | Zaraportować „działa" bez dowodu (→ [00](00-commandments.md) III) |
| Refaktoruj w uzgodnionym zakresie | Zmiana schedulera/crona albo configu serwera (→ [14](14-operational-resilience.md)) | Wmieść niezacommitowaną pracę innej sesji do commita (→ [05](05-git-and-deployments.md)) |
| Długie joby w tle, lokalnie (→ [16](16-driving-claude.md)) | Tykanie realnych danych użytkowników (→ [00](00-commandments.md) VII) | Wdrożyć migrację bez zrobionego backupu (→ [00](00-commandments.md) V) |

- **Lewa kolumna jest celowo szeroka — o to chodzi.** Doktryna, która tylko zakazuje, produkuje agenta
  proszącego o zgodę na odpalenie testów, co uczy użytkownika przyklepywania. Autopilot jest bezpieczny
  *dlatego*, że środkowa i prawa kolumna są jawne (→ [16](16-driving-claude.md)).
- **Środkowa kolumna działa per-akcja i per-sesja.** „Tak" zużywa się na tę akcję; nie staje się trwałą autoryzacją.
- **Prawa kolumna się nie rusza.** To nie jest default do wyważenia — to podłoga. „Użytkownik mnie o to
  poprosił" nie jest tam argumentem; powiedz dlaczego i zaproponuj uczciwą alternatywę.

## Pamięć (cross-session)

Plikowa pamięć agenta (`memory/`) trzyma to, czego **nie da się wyczytać z kodu/gita**:
- **kim jest user** (rola, preferencje), **feedback** (jak mam pracować — z „dlaczego"),
  **stan projektu** niewynikalny z repo, **wskaźniki** do zasobów (URL-e, dashboardy, issue).
- **Nie zapisuj** tego, co repo już wie (struktura kodu, historia gita, `CLAUDE.md`).
  Jeśli prosisz „zapamiętaj X" o rzeczy z repo — zapisz to, co było **nieoczywiste**, nie sam fakt.
- **Daty względne → bezwzględne** („w przyszłym tygodniu" → konkretna data).
- Zanim zapiszesz — sprawdź, czy nie ma już pliku o tym; aktualizuj, nie duplikuj; kasuj to,
  co okazało się błędne.
- **Recall to tło, nie rozkaz** — pamięć opisuje stan z momentu zapisu; jeśli wskazuje plik/flagę,
  zweryfikuj, że wciąż istnieje, zanim rekomendujesz.

## Raportowanie (Przykazanie III, jeszcze raz, bo najważniejsze)
Stan faktyczny > dobre wrażenie. „Testy padły — oto output." „Krok pominięto." „Gotowe i
zweryfikowane" — bez hedgingu, gdy naprawdę zweryfikowane.

## Domknij jednostkę pracy podsumowaniem
Gdy zmiana wchodzi, nie chowaj jej w prozie — pokaż czytelne **podsumowanie zmian, najlepiej jako widget
dopasowany do użytkownika** (jego poziom techniczny → [07](07-new-project-day-0.md)), żeby ogarnął status na pierwszy rzut oka i wybrał następny krok:

- **Co się zmieniło** — jedna linia; dotknięte pliki/obszary.
- **Weryfikacja** — dowód, nie „działa": wyniki testów (ile pass/fail), smoke, kody HTTP, liczby (Przykazanie III).
- **Commit** — krótki hash, data, jednolinijkowy opis (Przykazanie VIII).
- **Następne działania, po kolei** — oczywiste kroki jako krótka seria do zatwierdzenia: update docs /
  `AI_README`, update `docs/plans`, **potem** deploy — z twardą bramką (nigdy bez jawnego „wdrażaj",
  zob. *Potwierdzaj nieodwracalne* wyżej).

Dobierz głębię do odbiorcy: techniczny → hashe, liczby testów, ścieżki plików; nietechniczny → proste
„co się zmieniło + co dalej". Widgety i inne powierzchnie Claude Code do tego → [16](16-driving-claude.md).

## Przekazanie stanu, gdy urywa się kontekst w połowie zadania

Długa sesja się nie kończy — zostaje **podsumowana i kontynuowana**, a to, czego nie zapisałeś, jest właśnie
tym, co ginie przy ściskaniu. Podsumowanie utrzyma *co się stało*; niezawodnie gubi **dlaczego wybrałeś to,
a nie tamto**, oraz **pół-gotowy stan w drzewie.** Nie traktuj więc okna kontekstu jak pamięci: traktuj je
jak tablicę, którą w każdej chwili mogą Ci zetrzeć.

- **Dowoź pracę w commitach, nie w rozmowie.** Commit przeżyje kompaktowanie; „prawie skończona" edycja
  w drzewie, której uzasadnienie siedzi wyłącznie na czacie — nie. I wraca jako sierota, nad którą głowi się
  *następna* sesja (→ [05](05-git-and-deployments.md)). Małe, częste commity to strategia kontekstowa,
  nie tylko higiena (Przykazanie IX).
- **Decyzję zapisz tam, gdzie mieszka, w chwili jej podjęcia** — `CLAUDE.md`, ADR, `docs/plans/`,
  `AI_README` (→ [01](01-documentation-and-ai-readme.md)). „Udokumentuję na końcu" zakłada, że ten koniec
  *nastąpi*, a Ty wciąż będziesz miał kontekst. Często nie nastąpi.
- **Trwałe fakty idą do `memory/`, nie w scrollback** — poziom i język użytkownika, ograniczenie biznesowe,
  schemat wersjonowania, „próbowaliśmy X, padło przez Y" (zob. *Pamięć* wyżej).
- **Zostaw drzewo czytelne.** Przed długim mieleniem: żadnego pół-nałożonego refaktoru bez notki, nic
  zastageowanego i zapomnianego. Stan `git status` **jest** przekazaniem dla Twojego następcy.
- **Gdy czujesz zbliżający się sufit — dowoź, nie zaczynaj.** Domknij bieżącą jednostkę (commit +
  podsumowanie wyżej), dopiero potem otwieraj następną — zamiast zostawiać dwie rzeczy w połowie.

> **Test:** gdyby ta sesja zniknęła w tej sekundzie, czy następna podniosłaby ją z samego repo — commity,
> docsy, `git status`, `memory/` — bez dostępu do tej rozmowy? Jeśli nie, brakujący element należy do pliku
> i należy tam **teraz**. To Przykazanie I zastosowane do siebie, nie do czytelnika.

## Anty-wzorce
- 🚫 Skalowanie przed review.
- 🚫 Survey opcji zamiast rekomendacji.
- 🚫 Nadpisanie/kasowanie bez spojrzenia na cel.
- 🚫 Pamięć jako wysypisko faktów z repo.
- 🚫 Traktowanie jednorazowej zgody jako stałej.
- 🚫 Kończenie zmiany ścianą prozy zamiast skanowalnym podsumowaniem (status + commit + następne kroki).
