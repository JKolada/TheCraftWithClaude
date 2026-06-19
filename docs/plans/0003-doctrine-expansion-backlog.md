# 0003 — Backlog rozszerzeń doktryny

> Status: **otwarty backlog.** Kandydaci na przyszłe rozdziały/sekcje, świadomie odłożeni — w duchu
> „pisz tylko to, co przeżyte" (jak płatności → [0002](0002-monetization-and-payments.md)). Gdy temat
> zostanie przeżyty/zdecydowany, **awansuje do rozdziału/sekcji, a wpis stąd znika** (bez zombie →
> [01](../../01-documentation-and-ai-readme.md)). Źródło: audyt spójności 2026-06-19.

## Kandydaci (priorytet malejąco)

### Auth/authz jako pełniejszy temat
- **Dziś:** rozsiane — bcrypt/OAuth/`helmet` w [08](../../08-stack-and-technologies.md), sesje w
  [05](../../05-git-and-deployments.md)/[14](../../14-operational-resilience.md), „testuj auth z obu
  stron" w [03](../../03-testing-and-verification.md), indeks bezpieczeństwa w [09](../../09-law-and-protecting-the-creator.md).
- **Luka:** brak skupionego traktowania **autoryzacji** — role/uprawnienia, IDOR, „czy *ten* user może
  ruszyć *ten* wiersz", privilege escalation, egzekwowanie server-side. (Authz domknięty na razie jednym
  punktem w indeksie bezpieczeństwa 09.)
- **Kiedy:** projekt z realnymi rolami/tierami da hands-on → sekcja w 14 albo nowy rozdział.

### Secrets / config / env + runbook wycieku
- **Dziś:** jednolinijkowo (sekrety w env, nie w repo — 08/09).
- **Luka:** `.env` + `.env.example`, rozdział dev/staging/prod, rotacja kluczy, **runbook „sekret wyciekł
  do git history"** (purge → rotate → audit), granica config wg 12-factor.
- **Kiedy:** częściowo przeżyte → zasadne jako sekcja w 08 nawet teraz; albo plan→sekcja po pierwszym wycieku.

### CI/CD pipeline
- **Dziś:** „CI bramkuje" wzmiankowane (03), brak rozdziału o samym pipeline (Actions, co na PR vs main,
  artefakty). Repo świadomie proste (`build.py` + `test.py` ręcznie).
- **Ryzyko:** ciężki rozdział CI/CD kłóci się z „nie over-engineeruj" ([12](../../12-flexibility-and-scalability.md)).
- **Kiedy:** dopiero gdy realnie uruchomimy pipeline (inaczej zostaje planem).

### a11y skonsolidowane *(user pominął w rundzie 2026-06-19)*
- **Dziś:** rozsiane — 03 (cel testów: kontrast, klawiatura, alt/aria), 07 (pytanie WCAG), 13 (`prefers-reduced-motion`).
- **Kiedy:** opcjonalnie sekcja w [13](../../13-performance-frontend-and-sql.md); świadomie odłożone.

### FinOps / incydenty / on-call *(na razie skip)*
- Przedwczesne dla solo/monolitu; runbook z ponumerowanymi lekcjami (05/14) już to lekko łapie.

## Reguła backlogu

Wpis tu = **otwarty** kierunek. Zrealizowany → wtop w rozdział / `CLAUDE.md` i **usuń z backlogu** (git
trzyma historię). Nie trzymaj „zrobionych" pozycji — ten plik ma odzwierciedlać tylko to, co jeszcze przed nami.
