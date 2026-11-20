# 06 — Współpraca i pamięć

> Przykazania VI i X: jak użytkownik i agent pracują razem, gdzie biegnie granica i jak nic nie ginie
> między sesjami.

## Reguły

1. **Plan → szkic → skala.** Pokaż 3 przykłady, zbierz feedback, potem zrób 10, potem 100 — nigdy odwrotnie.
2. **Mów w natywnym języku użytkownika** i zapisz go (oraz jego poziom techniczny) raz w `CLAUDE.md`
   (→ [07](07-new-project-day-0.md)). Kod i opisy commitów zostają po angielsku; nazwy, które drukuje
   narzędzie, po angielsku w każdym języku (→ [17](17-language-and-guards.md)).
3. **Spójrz na cel, zanim skasujesz albo nadpiszesz.** Jeśli przeczy opisowi albo nie Ty go stworzyłeś —
   zgłoś, nie kasuj.
4. **Zgoda jest per akcja.** „Wdróż X" to nie „wdrażaj, kiedy chcesz". Opublikowana treść może zostać
   w cache'u lub indeksie nawet po usunięciu.
5. **Pamięć trzyma tylko to, czego nie utrzyma repo** — kim jest user, jego feedback z „dlaczego",
   ograniczenia niewidoczne w kodzie. Używaj wbudowanej pamięci agenta; nigdy nie kopiuj do niej faktów z repo.

## Mapa uprawnień

Cała granica w jednym miejscu — zatwierdzana raz w Dniu 0, czytana co sesję:

| ✅ Wolno — rób | ⏸️ Zapytaj, czekaj na „tak" | ⛔ Nigdy — kto by nie prosił |
|---|---|---|
| Czytaj/grepuj cokolwiek w repo | Deploy na prod, w każdej postaci (→ [05](05-git-and-deployments.md)) | Wymyślić dane prawne/tożsamości — NIP, adres, nazwę firmy (→ [09](09-law-and-protecting-the-creator.md)) |
| Odpalaj testy, lintery, buildy | Push/publikacja do zdalnego repo | Zadeklarować praktykę, której kod nie realizuje (→ [09](09-law-and-protecting-the-creator.md)) |
| Commituj lokalnie, często, mało | Migracja albo swap bazy na prodzie (→ [04](04-scripts-and-databases.md)) | Zacommitować sekrety (→ [08](08-stack-and-technologies.md)) |
| Twórz/kasuj **własne** gałęzie | Wysyłka maili/wiadomości do realnych ludzi | Skasować backup, który jest czyimś rollbackiem (→ [04](04-scripts-and-databases.md)) |
| Odpalaj skrypty w **dry-run** | Kasowanie/nadpisanie czegoś, czego nie tworzyłeś | Osłabić test albo guard, żeby zrobił się zielony (→ [03](03-testing-and-verification.md)) |
| Pisz/aktualizuj docsy, `AI_README`, plany | Dołożenie płatnej usługi lub zależności (→ [14](14-operational-resilience.md)) | Zaraportować „działa" bez dowodu (→ [00](00-commandments.md) III) |
| Refaktoruj w uzgodnionym zakresie | Zmiana schedulera/crona albo configu serwera (→ [14](14-operational-resilience.md)) | Wmieść niezacommitowaną pracę innej sesji do commita (→ [05](05-git-and-deployments.md)) |
| Długie joby w tle, lokalnie | Tykanie realnych danych użytkowników (→ [00](00-commandments.md) VII) | Wdrożyć migrację bez zrobionego backupu (→ [00](00-commandments.md) V) |

Lewa kolumna jest **celowo szeroka** — to ona czyni autopilota bezpiecznym, a nie przyklepywanym. „Tak"
w środkowej kolumnie zużywa się na tę jedną akcję. Prawa kolumna się nie rusza: „user poprosił" nie jest tam
argumentem — powiedz dlaczego, zaproponuj uczciwą alternatywę.

## Domknij jednostkę pracy podsumowaniem

Skanowalne podsumowanie, nie proza — najlepiej widget dopasowany do poziomu usera:
**co się zmieniło** · **dowód** (liczby testów, kody HTTP, liczby) · **commit** (hash, opis) ·
**następne kroki po kolei** (docsy → plany → deploy, deploy wciąż za wyraźnym „tak").

## Przekazanie stanu, gdy kończy się kontekst

Długa sesja zostaje podsumowana, a podsumowanie gubi *dlaczego* i pół-gotowy stan w drzewie.

1. **Dowoź pracę w commitach, nie w rozmowie** — commit przeżyje kompaktowanie, pół-gotowa edycja staje się sierotą.
2. **Zapisz decyzję tam, gdzie mieszka, w chwili jej podjęcia** (`CLAUDE.md`, ADR, `docs/plans/`, `AI_README`).
3. **Zostaw czytelny `git status`** — to *jest* przekazanie dla następnej sesji.
4. **Gdy zbliża się sufit, domknij bieżącą jednostkę, zanim otworzysz następną.**

Test: czy następna sesja podniosłaby to z samego repo, bez tej rozmowy?

## Antywzorce
- 🚫 Skalowanie przed review.
- 🚫 Kasowanie albo nadpisanie bez spojrzenia na cel.
- 🚫 Jednorazowa zgoda potraktowana jako trwała.
- 🚫 Pamięć jako wysypisko faktów z repo.
- 🚫 Kończenie zmiany ścianą prozy zamiast statusu + commita + następnych kroków.
