# AI_README — `docs/`

Dokumentacja „cięższa niż mapa katalogu" **o samym repo Rzemiosło** — nie treść doktryny (ta żyje
w numerowanych rozdziałach `NN-*.md` w rootcie i w `pl/`). Konwencja z rozdziału [01](../01-documentation-and-ai-readme.md).

## Zawartość

| Ścieżka | Po co |
|---------|-------|
| `packaging.md` | **Kontrakt z Web:** co trafia do paczki `docs/rules/`, a co nie; układ; zasady rozsyłania do gospodarzy. Dokument stanu bieżącego. |
| `plans/0002-monetization-and-payments.md` | **Otwarty** — płatności. Brak hands-on → świadomie bez rozdziału; plan trzyma kierunek. |
| `plans/0003-doctrine-expansion-backlog.md` | **Otwarty backlog** kandydatów na rozdziały/sekcje (autoryzacja, sekrety + runbook wycieku, CI/CD, a11y, FinOps). |
| `plans/0004-web-sync-1.1.2.md` | **Aktywny** — prompt dla Rzemiosło Web: aktualizacja witryny do 1.1.2. Usuń, gdy Web go wykona. |

## Zasady

- **`docs/` opisuje stan bieżący, nie historię.** Zrealizowany plan: decyzja awansuje do właściwego
  dokumentu / [CLAUDE.md](../CLAUDE.md), a plan jest usuwany — git trzyma historię.
- **Plan = problem → opcje → decyzja → „dlaczego".** `plans/` trzyma tylko otwarte kierunki.
- Numeracja `NNNN` rośnie monotonicznie; numeru usuniętego planu nie reużywaj.
