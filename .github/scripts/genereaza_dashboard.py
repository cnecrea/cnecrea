#!/usr/bin/env python3
"""
Generează dashboard-ul README.md cu statistici agregate din toate repo-urile.
Rulează zilnic prin GitHub Actions, o oră după colectarea individuală.
"""

import json
import os
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# ── Configurare ──────────────────────────────────────────────────────────────

OWNER = "cnecrea"

REPO_URI = [
    ("Curs BNR", "cursbnr", "Cursuri valutare BNR"),
    ("E-bloc România", "e-bloc.ro", "Plăți, întreținere, facturi, anunțuri, notificări, situația fondurilor "),
    ("E.ON România", "eonromania", "Monitorizare consum energie E.ON"),
    ("CNAIR eRovinieta", "erovinieta", "Verificare roviniete"),
    ("Hidroelectrica", "hidroelectrica", "Monitorizare consum Hidroelectrica"),
    ("Manager de flotă", "fleet", "Manager de flotă pentru transportatori"),
    ("MyElectrica", "myelectrica", "Monitorizare consum Electrica"),
    ("MyENGIE", "myengie", "Monitorizare consum MyENGIE"),
    ("Nova Power & Gas", "vreaulanova", "NOVA - furnizor energie electrica si furnizor gaze naturale pentru consumatori casnici si business"),
    ("OPCOM", "opcom", "Prețuri energie OPCOM"),
    ("Pago Plătește", "pagoplateste", "Ai toate facturile tale într-un singur loc"),
    ("SMS.to", "smsto", "Notificări SMS prin SMS.to"),
    ("Vehicule", "vehicule", "Gestionare vehicule și documente"),
    ("Vehicule Card", "vehicule-card", "Custom Lovelace card"),
]

TZ_RO = timezone(timedelta(hours=3))
README_PATH = Path("README.md")
STATS_RAW_URL = "https://raw.githubusercontent.com/{owner}/{repo}/main/.github/analytics/stats.json"
SHIELDS_RAW_URL = "https://raw.githubusercontent.com/{owner}/{repo}/main/statistici/shields/{fisier}.json"

# Markere pentru înlocuire în README.md
MARKER_START = "<!-- DASHBOARD_START -->"
MARKER_END = "<!-- DASHBOARD_END -->"


# ── Funcții auxiliare ────────────────────────────────────────────────────────

def api_get(url: str, token: str | None = None) -> dict | None:
    """GET request cu error handling."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except (URLError, HTTPError, json.JSONDecodeError) as e:
        print(f"  ⚠ Eroare la {url}: {e}")
        return None


def raw_get(url: str) -> dict | None:
    """GET pe raw.githubusercontent.com (fără auth)."""
    try:
        req = Request(url, headers={"Accept": "application/json"})
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except (URLError, HTTPError, json.JSONDecodeError):
        return None


def format_numar(n: int) -> str:
    """Formatează numere: 1234 → 1.2k, 1234567 → 1.2M."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}k"
    return str(n)


def extrage_clone_cumulate(stats: dict | None) -> int:
    """Extrage clone totale cumulate din stats.json (metrica reală de adopție HACS)."""
    if not stats or "zilnic" not in stats:
        return 0
    return sum(
        zi.get("clones_total", 0)
        for zi in stats["zilnic"].values()
    )


def extrage_trafic_14z(stats: dict | None) -> tuple[int, int]:
    """Extrage vizitatori și clone unice din ultimele 14 zile din stats.json."""
    if not stats or "zilnic" not in stats:
        return 0, 0

    azi = datetime.now(timezone.utc).date()
    limita = azi - timedelta(days=14)

    vizitatori = 0
    clone = 0

    for data_str, info in stats["zilnic"].items():
        try:
            data = datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            continue
        if data < limita:
            continue

        vizitatori += info.get("views_unice", 0)
        clone += info.get("clones_unice", 0)

    return vizitatori, clone


# ── Colectare date ───────────────────────────────────────────────────────────

def colecteaza_date_repo(repo: str, token: str | None) -> dict:
    """Colectează toate datele pentru un singur repo."""
    print(f"📦 {repo}...")

    # 1. GitHub API — repo info (stars, forks) + latest release
    info = api_get(f"https://api.github.com/repos/{OWNER}/{repo}", token)
    release = api_get(f"https://api.github.com/repos/{OWNER}/{repo}/releases/latest", token)

    stars = info.get("stargazers_count", 0) if info else 0
    versiune = release.get("tag_name", "—") if release else "—"

    # 2. stats.json — clone cumulate + trafic
    stats_url = STATS_RAW_URL.format(owner=OWNER, repo=repo)
    stats = raw_get(stats_url)

    instalari = extrage_clone_cumulate(stats)
    vizitatori, clone = extrage_trafic_14z(stats)

    # 3. Fallback pe shields endpoint dacă stats.json nu există
    if stats is None:
        print(f"  ℹ stats.json nu există, încerc shields endpoint...")
        shields_stars = raw_get(SHIELDS_RAW_URL.format(owner=OWNER, repo=repo, fisier="stars"))
        shields_desc = raw_get(SHIELDS_RAW_URL.format(owner=OWNER, repo=repo, fisier="descarcari"))
        shields_viz = raw_get(SHIELDS_RAW_URL.format(owner=OWNER, repo=repo, fisier="vizitatori"))
        shields_clone = raw_get(SHIELDS_RAW_URL.format(owner=OWNER, repo=repo, fisier="clone"))

        if shields_stars and "message" in shields_stars:
            try:
                stars = int(shields_stars["message"].replace(".", "").replace("k", "000").replace("M", "000000"))
            except ValueError:
                pass

    return {
        "versiune": versiune,
        "stars": stars,
        "instalari": instalari,
        "vizitatori": vizitatori,
        "clone": clone,
    }


# ── Generare tabel ───────────────────────────────────────────────────────────

def genereaza_tabel(date: list[tuple[str, str, str, dict]]) -> str:
    """Generează tabela markdown cu statistici."""
    acum = datetime.now(TZ_RO).strftime("%d.%m.%Y %H:%M")

    linii = []
    linii.append(f"## 📈 Statistici integrări")
    linii.append("")
    linii.append(f"<sub>Ultima actualizare: {acum} (automat, zilnic)</sub>")
    linii.append("")
    linii.append("| Integrare | Versiune | ⭐ Stars | 📥 Instalări | 👁 Vizitatori (14z) | 🔄 Clone (14z) |")
    linii.append("|:----------|:--------:|:--------:|:------------:|:-------------------:|:--------------:|")

    total_stars = 0
    total_inst = 0
    total_viz = 0
    total_clone = 0

    for nume, repo, descriere, stats in date:
        total_stars += stats["stars"]
        total_inst += stats["instalari"]
        total_viz += stats["vizitatori"]
        total_clone += stats["clone"]

        linii.append(
            f"| [{nume}](https://github.com/{OWNER}/{repo}) "
            f"| `{stats['versiune']}` "
            f"| {stats['stars']} "
            f"| {format_numar(stats['instalari'])} "
            f"| {stats['vizitatori']} "
            f"| {stats['clone']} |"
        )

    linii.append(
        f"| **TOTAL** | | **{total_stars}** "
        f"| **{format_numar(total_inst)}** "
        f"| **{total_viz}** "
        f"| **{total_clone}** |"
    )

    linii.append("")
    linii.append(f'<sub>📈 Datele se actualizează zilnic prin GitHub Actions. '
                 f'Vizitatori/Clone = ultimele 14 zile (limită API GitHub). '
                 f'Toate integrările sunt disponibile prin '
                 f'<a href="https://hacs.xyz/">HACS</a> (Custom repositories).</sub>')

    return "\n".join(linii)


# ── Actualizare README ───────────────────────────────────────────────────────

def actualizeaza_readme(tabel: str):
    """Înlocuiește secțiunea dashboard din README.md."""
    if not README_PATH.exists():
        print("⚠ README.md nu există, îl creez...")
        README_PATH.write_text(
            f"# 👋 Salut!\n\n"
            f"{MARKER_START}\n{tabel}\n{MARKER_END}\n",
            encoding="utf-8"
        )
        return

    continut = README_PATH.read_text(encoding="utf-8")

    if MARKER_START in continut and MARKER_END in continut:
        pattern = re.compile(
            re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
            re.DOTALL
        )
        continut_nou = pattern.sub(
            f"{MARKER_START}\n{tabel}\n{MARKER_END}",
            continut
        )
    else:
        # Adaugă la final dacă markerele nu există
        print("ℹ Markere lipsă, adaug dashboard la finalul README...")
        continut_nou = continut.rstrip() + f"\n\n{MARKER_START}\n{tabel}\n{MARKER_END}\n"

    README_PATH.write_text(continut_nou, encoding="utf-8")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    token = os.environ.get("GH_TOKEN")
    if not token:
        print("⚠ GH_TOKEN nu este setat, unele date pot lipsi.")

    print("🚀 Colectare statistici pentru dashboard...\n")

    date = []
    for nume, repo, descriere in REPO_URI:
        stats = colecteaza_date_repo(repo, token)
        date.append((nume, repo, descriere, stats))
        print(f"  ✓ {nume}: {stats['versiune']} | ⭐{stats['stars']} | "
              f"📥{format_numar(stats['instalari'])} | "
              f"👁{stats['vizitatori']} | 🔄{stats['clone']}")

    print(f"\n📝 Generare tabel dashboard...")
    tabel = genereaza_tabel(date)

    print(f"📄 Actualizare README.md...")
    actualizeaza_readme(tabel)

    print(f"\n✅ Dashboard actualizat cu succes!")


if __name__ == "__main__":
    main()
