# 16 — Prowadzenie Claude

> Funkcje agenta dokumentuje sam agent; ten rozdział ustala tylko **politykę projektu** ich użycia — kiedy
> są obowiązkowe i gdzie są granice.

## Reguły

1. **Plan mode jest obowiązkowy**, gdy kształt pracy jest otwarty, promień rażenia szeroki (migracja, rename
   po całym drzewie, URL-e/redirecty) albo zmianę trudno cofnąć. Plan nazywa pliki, kompromis i **jak wynik
   zostanie zweryfikowany**. Przy ograniczonym fixie — odpuść.
2. **Autopilot to default — w granicach mapy uprawnień** (→ [06](06-collaboration-and-memory.md)). Środkowa
   i prawa kolumna wciąż go zatrzymują; to właśnie czyni autopilota bezpiecznym.
3. **Model wg stawki:** tańszy do pracy mechanicznej, najmocniejszy do architektury, trudnych bugów i
   wszystkiego, co może zgubić dane. Nigdy nie oszczędzaj na operacji, która może zgubić dane.
4. **Długa praca w tle; to, co ma przeżyć sesję — odpięte** (→ [14](14-operational-resilience.md)).
5. **Rozpraszaj na subagentów**, gdy realnie pomaga szerokość, równoległe niezależne edycje albo
   adwersarialna weryfikacja — zostaje wniosek, nie zrzuty. Nie do poprawki na jedną linię.
6. **Jedna równoległa sesja = jeden `git worktree`.** Dwie sesje w jednym checkoucie dzielą index:
   stageują sobie pliki i wmiatają pół-gotowe edycje do commitów (→ [05](05-git-and-deployments.md)).
7. **Powtarzalne procedury stają się skillami; „zawsze rób X po Y" staje się hookiem** (→ [02](02-skills-and-refactoring.md)).

## Antywzorce
- 🚫 Szeroka albo nieodwracalna zmiana bez plan mode — recenzujesz diff zamiast decyzji.
- 🚫 Ręczne potwierdzanie każdej bezpiecznej edycji — wolno i uczy przyklepywania.
- 🚫 Tani model na migracji, która może zgubić dane.
- 🚫 Dwie sesje w jednym checkoucie.
- 🚫 Zadanie, które ma przeżyć sesję, zostawione w tle sesji.
