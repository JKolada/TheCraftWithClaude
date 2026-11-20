# 08 — Stack i technologie

> Złota zasada altytudy w doborze narzędzi: *najprostsze, co spełnia dzisiejsze wymaganie*; złożoność
> dokładasz, gdy wymusi ją metryka (→ [12](12-flexibility-and-scalability.md)).

## Defaulty (odchodzisz świadomie, z ADR)

| Warstwa | Default | Zmień, gdy |
|---|---|---|
| Agent / proces | **Claude Code** + **Git** + **GitHub** (repo, PR-y, Issues) | — |
| Backend, skrypty, dane | **Python** (FastAPI na API, pytest) — najszerszy ekosystem do skryptów, danych i spinania AI | zadanie lepiej robi inny język: **Go** (współbieżne usługi sieciowe, jedna statyczna binarka), **Rust** (gorące ścieżki, bezpieczeństwo pamięci, mały narzut), **Kotlin** (biblioteki JVM, Android), **TypeScript/Node** (warstwa web już jest w JS) |
| Baza | **SQLite** (WAL) | współbieżne zapisy, role, ciężkie relacje → **PostgreSQL** |
| Web / front | HTML renderowany po stronie serwera + trochę czystego JS | naprawdę bogata interakcja → framework (np. Next.js) |
| API | REST/JSON z jawnym kontraktem (OpenAPI) | — |
| Cache / kolejka | brak | zmierzony profil ruchu → Redis |
| Pakowanie | Docker tam, gdzie zależności bolą | skrypt bez zależności → bez kontenera |
| Hosting | **jeden VPS** (np. Hetzner) + nginx + `systemd`/`pm2` — **monolit** | nierówny/globalny ruch, cold start akceptowalny → serverless |
| Ikony | **tylko Lucide** (jedna geometria, jeden sprite) | — |
| LLM | Claude przez oficjalne SDK, streamowany (→ [13](13-performance-frontend-and-sql.md)) | — |

## Reguły

1. **Monolit to domyślna architektura:** jedna aplikacja, jedna baza, jeden serwer — jeden deploy, jeden
   log, jeden backup, jeden rollback. Na usługi dzielisz dopiero, gdy wymaga tego ruch, zespół albo izolacja awarii.
2. **Język wybierasz wg dopasowania, nie z przyzwyczajenia.** Python to default, nie dogmat: zmień go, gdy
   decyduje wydajność, współbieżność, sposób wdrożenia albo biblioteka, która istnieje tylko w innym
   ekosystemie — i zapisz w ADR, co przesądziło (liczba albo brakująca biblioteka). Jeden język na warstwę,
   nie jeden na humor; przepisanie „dla szybkości" wymaga najpierw pomiaru (→ [13](13-performance-frontend-and-sql.md)).
3. **Testowalne od pierwszej linii bije modne.** Technologia, której nie pokryjesz szybkimi,
   deterministycznymi testami, to zły wybór (→ [03](03-testing-and-verification.md)).
4. **Nudne i dojrzałe ponad nowe:** decydują ekosystem, dokumentacja i testowalność, nie hype.
5. **Odtwarzalne środowiska:** przypięte zależności (lock), wirtualne środowisko / obraz.
6. **Sekrety żyją w env albo w sejfie na sekrety — nigdy w repo.**
7. **Każdy niedomyślny wybór dostaje ADR:** dlaczego i odrzucone alternatywy, w `docs/`.

## Antywzorce
- 🚫 Mikroserwisy, Kubernetes albo rozproszona baza na MVP.
- 🚫 Stack wybrany pod CV.
- 🚫 Ciężkie SPA tam, gdzie wystarczy HTML z serwera.
- 🚫 Mieszanie bibliotek ikon.
- 🚫 Nieprzypięte zależności — „wczoraj działało".
- 🚫 Python wciśnięty w zadanie, któremu źle służy (gorąca ścieżka, współbieżna usługa, biblioteka żyjąca na JVM) — albo przepisanie na „szybszy" język bez pomiaru.
