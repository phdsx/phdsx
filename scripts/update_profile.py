"""Build phdsx's profile from public GitHub data. Python 3.10+, no dependencies."""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from html import escape
from html.parser import HTMLParser
import json
from math import log2
from pathlib import Path
import os
import re
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
USER = "phdsx"
OUT = ROOT / "assets" / "generated"
COLORS = {"JavaScript": "#f1d65c", "Python": "#67b8ec", "HTML": "#f29374", "CSS": "#b797ff", "Jupyter Notebook": "#f6b26b", "TypeScript": "#6c9fff", "Shell": "#88d1a7"}
THEMES = {
    "dark": dict(bg="#10192b", panel="#172338", line="#29364b", text="#edf2ff", muted="#9eacc6", accent="#a99bff", cyan="#72daca", cells=["#202b40", "#454577", "#6961a7", "#9785d5", "#c4adff"]),
    "light": dict(bg="#ffffff", panel="#f6f7fc", line="#e2e6ef", text="#202b45", muted="#66738d", accent="#7461c8", cyan="#168a84", cells=["#edf0f7", "#dbd2f3", "#b9a8e3", "#927acd", "#7156ba"]),
}


def get(url):
    headers = {"User-Agent": "phdsx-profile-generator", "Accept": "application/vnd.github+json"}
    if url.startswith("https://api.github.com/") and os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    with urlopen(Request(url, headers=headers), timeout=35) as response:
        body = response.read().decode("utf-8")
    return json.loads(body) if url.startswith("https://api.github.com/") else body


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.tip_id = None
        self.tip_parts = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "td" and a.get("data-date") and a.get("data-level") is not None:
            self.cells[a["id"]] = {"date": a["data-date"], "level": int(a["data-level"])}
        if tag == "tool-tip" and a.get("for") in self.cells:
            self.tip_id, self.tip_parts = a["for"], []

    def handle_data(self, text):
        if self.tip_id:
            self.tip_parts.append(text)

    def handle_endtag(self, tag):
        if tag == "tool-tip" and self.tip_id:
            text = " ".join(self.tip_parts)
            match = re.search(r"([\d,]+) contributions? on", text)
            if match:
                count = int(match.group(1).replace(",", ""))
            elif re.search(r"No contributions on", text):
                count = 0
            else:
                raise ValueError(f"Unrecognized contribution tooltip: {text}")
            self.cells[self.tip_id]["count"] = count
            self.tip_id = None


def fetch_snapshot():
    user = get(f"https://api.github.com/users/{USER}")
    repos, page = [], 1
    while True:
        batch = get(f"https://api.github.com/users/{USER}/repos?per_page=100&sort=updated&page={page}")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    own = [repo for repo in repos if not repo["fork"]]
    def languages(repo):
        return repo["name"], get(repo["languages_url"])
    with ThreadPoolExecutor(max_workers=4) as pool:
        by_repo = dict(pool.map(languages, own))
    html = get(f"https://github.com/users/{USER}/contributions")
    parser = CalendarParser()
    parser.feed(html)
    days = sorted(parser.cells.values(), key=lambda x: x["date"])
    if not days or any("count" not in day for day in days):
        raise ValueError("GitHub contribution calendar could not be parsed completely")
    total_match = re.search(r'id="js-contribution-activity-description"[^>]*>\s*([\d,]+)\s+contributions?', html)
    total = sum(day["count"] for day in days)
    if not total_match or int(total_match.group(1).replace(",", "")) != total:
        raise ValueError("Contribution total does not match GitHub's calendar heading")
    fields = ("name", "description", "html_url", "language", "fork", "archived", "stargazers_count", "forks_count", "pushed_at", "updated_at")
    return {
        "username": USER,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sources": [f"https://api.github.com/users/{USER}", f"https://api.github.com/users/{USER}/repos", f"https://github.com/users/{USER}/contributions", "Each non-fork repository's GitHub languages endpoint"],
        "user": {k: user[k] for k in ("login", "html_url", "created_at", "public_repos", "followers", "following")},
        "repositories": [{k: repo[k] for k in fields} for repo in repos],
        "language_bytes_by_repository": by_repo,
        "contributions": days,
        "contribution_total": total,
    }


def text(x, y, value, fill, size=14, weight=400, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" {extra}>{escape(str(value))}</text>'


def svg_start(w, h, title, t):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title, quote=True)}"><title>{escape(title)}</title><style>text{{font-family:Arial,"Microsoft YaHei",sans-serif}} .mono{{font-family:Consolas,monospace}}</style><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="{t["bg"]}" stroke="{t["line"]}"/>'


def heading(title, sub, t):
    return text(25, 34, title, t["text"], 18, 700) + text(25, 56, sub, t["muted"], 11)


def save_svg(name, mode, content):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}-{mode}.svg").write_text(content + "</svg>\n", encoding="utf-8")


def metrics(s, mode, t):
    repos = s["repositories"]
    values = [(len(repos), "PUBLIC REPOSITORIES"), (sum(r["stargazers_count"] for r in repos), "REPOSITORY STARS"), (s["contribution_total"], "YEAR CONTRIBUTIONS"), (sum(d["count"] > 0 for d in s["contributions"]), "ACTIVE DAYS THIS YEAR")]
    out = svg_start(900, 176, "phdsx · GitHub overview", t)
    out += heading("A little progress, one commit at a time.", f'Public GitHub snapshot · {s["fetched_at"][:10]} UTC', t)
    for i, (value, label) in enumerate(values):
        x = 25 + i * 224
        if i:
            out += f'<path d="M{x-13} 83v66" stroke="{t["line"]}"/>'
        out += text(x, 119, f"{value:,}", t["accent"], 36, 700) + text(x, 146, label, t["muted"], 10)
    save_svg("overview", mode, out)


def language_card(s, mode, t):
    totals = Counter()
    for langs in s["language_bytes_by_repository"].values():
        totals.update(langs)
    all_rows = totals.most_common()
    rows = all_rows[:6] + ([("Other", sum(value for _, value in all_rows[6:]))] if len(all_rows) > 6 else [])
    total = sum(totals.values())
    out = svg_start(440, 282, "Languages in phdsx's non-fork public repositories", t)
    out += heading("Languages in the repositories", "Source bytes · excludes forks · not coding time", t)
    x = 25
    for name, value in rows:
        width = value / total * 390 if total else 0
        out += f'<rect x="{x:.2f}" y="78" width="{width:.2f}" height="13" fill="{COLORS.get(name, t["accent"])}"/>'
        x += width
    for i, (name, value) in enumerate(rows[:7]):
        y = 119 + i * 21
        out += f'<circle cx="30" cy="{y-4}" r="4" fill="{COLORS.get(name, t["accent"])}"/>'
        out += text(43, y, name, t["text"], 12) + text(414, y, f"{value/total:.1%}", t["muted"], 12, anchor="end")
    if not rows:
        out += text(25, 135, "No language data available", t["muted"])
    save_svg("languages", mode, out)


def streak_card(s, mode, t):
    days = s["contributions"]
    streak = longest = 0
    for day in days:
        streak = streak + 1 if day["count"] else 0
        longest = max(streak, longest)
    # GitHub's current UTC calendar date can still be in progress.
    last = len(days) - 1
    if last >= 0 and days[last]["count"] == 0:
        last -= 1
    current = 0
    while last >= 0 and days[last]["count"]:
        current += 1
        last -= 1
    out = svg_start(440, 282, "phdsx · contribution streak within displayed calendar", t)
    out += heading("Keep the small steps going", "Streaks within the displayed contribution year", t)
    for x, n, label in [(83, current, "Current streak"), (220, longest, "Longest streak"), (357, sum(d["count"] > 0 for d in days), "Active days")]:
        out += f'<circle cx="{x}" cy="140" r="43" fill="{t["panel"]}" stroke="{t["accent"]}" stroke-width="2"/>'
        out += text(x, 151, n, t["text"], 32, 700, "middle") + text(x, 211, label, t["muted"], 12, anchor="middle")
    out += text(220, 254, "A quiet day is part of the journey, too.", t["muted"], 11, anchor="middle")
    save_svg("streak", mode, out)


def activity(s, mode, t):
    days = s["contributions"][-90:]
    out = svg_start(900, 260, "phdsx · contributions over the last 90 calendar days", t)
    out += heading("The recent contribution rhythm", f'{days[0]["date"]} — {days[-1]["date"]} · daily GitHub contributions', t)
    maximum = max(1, max(d["count"] for d in days))
    points = [(42 + i * 816 / max(1, len(days)-1), 204 - 119 * d["count"] / maximum) for i, d in enumerate(days)]
    for n in range(4):
        y = 204 - n * 119 / 3
        out += f'<path d="M42 {y:.1f}H858" stroke="{t["line"]}" stroke-dasharray="3 5"/>' + text(30, y+4, f"{maximum*n/3:.0f}", t["muted"], 9, anchor="end")
    p = " ".join(f"{x:.1f},{y:.1f}" for x,y in points)
    out += f'<polygon points="42,204 {p} 858,204" fill="{t["accent"]}" opacity=".13"/><polyline points="{p}" fill="none" stroke="{t["accent"]}" stroke-width="2.5" stroke-linejoin="round"/>'
    for i in [0, len(days)//3, 2*len(days)//3, len(days)-1]:
        out += text(points[i][0], 235, days[i]["date"][5:], t["muted"], 11, anchor="middle")
    save_svg("activity", mode, out)


def calendar(s, mode, t):
    days = s["contributions"]
    first = date.fromisoformat(days[0]["date"])
    start = first - timedelta(days=(first.weekday()+1)%7)
    out = svg_start(900, 210, "phdsx · animated contribution snake", t)
    out += heading("A snake through the contribution garden", f'{days[0]["date"]} — {days[-1]["date"]} · {s["contribution_total"]} contributions', t)
    positions = {}
    for day in days:
        offset = (date.fromisoformat(day["date"]) - start).days
        col, row = divmod(offset, 7)
        x, y = 44 + col*15, 78 + row*15
        positions[col, row] = (x+5, y+5)
        out += f'<rect x="{x}" y="{y}" width="10" height="10" rx="2" fill="{t["cells"][day["level"]]}"><title>{day["date"]}: {day["count"]} contributions</title></rect>'
    route = []
    for col in range(max(c for c,r in positions)+1):
        for row in (range(7) if col%2 == 0 else range(6,-1,-1)):
            if (col,row) in positions:
                route.append(positions[col,row])
    path = "M" + " L".join(f"{x},{y}" for x,y in route)
    # Every cell represents actual GitHub data. The moving snake is decorative.
    for i in range(5,-1,-1):
        out += f'<g><rect x="-5" y="-5" width="10" height="10" rx="3" fill="{t["cyan"]}" opacity="{1-i*.11:.2f}"/>'
        if i == 0:
            out += f'<circle cx="1.5" cy="-2" r="1" fill="{t["bg"]}"/><circle cx="1.5" cy="2" r="1" fill="{t["bg"]}"/>'
        out += f'<animateMotion path="{path}" dur="42s" begin="{-i*.13}s" repeatCount="indefinite" rotate="auto"/></g>'
    out += text(44, 200, "Less", t["muted"], 10)
    for i, color in enumerate(t["cells"]):
        out += f'<rect x="{78+i*14}" y="190" width="10" height="10" rx="2" fill="{color}"/>'
    out += text(153, 200, "More", t["muted"], 10)
    save_svg("snake", mode, out)


def contribution_3d(s, mode, t):
    days = s["contributions"]
    first = date.fromisoformat(days[0]["date"])
    start = first - timedelta(days=(first.weekday()+1)%7)
    out = svg_start(900, 370, "phdsx · isometric GitHub contribution landscape", t)
    out += heading("A year, seen from another angle", f'Actual contribution counts · height = log₂(count + 1) · {days[-1]["date"]}', t)
    for day in days:
        col,row = divmod((date.fromisoformat(day["date"])-start).days, 7)
        x, y = 120 + col*12.3 - row*11.2, 143 + col*1.7 + row*8.2
        h = 2 + log2(day["count"]+1)*10
        color = t["cells"][day["level"]]
        out += f'<g><title>{day["date"]}: {day["count"]} contributions</title><path d="M{x:.1f},{y:.1f}l10,1.4v{-h:.1f}l-10,-1.4z" fill="{color}" opacity=".72"/><path d="M{x+10:.1f},{y+1.4:.1f}l-8,5.8v{-h:.1f}l8,-5.8z" fill="{color}" opacity=".48"/><path d="M{x:.1f},{y-h:.1f}l10,1.4l-8,5.8l-10,-1.4z" fill="{color}"/></g>'
    out += text(450, 333, "Small blocks. A longer story.", t["muted"], 12, anchor="middle")
    save_svg("contributions-3d", mode, out)


def community(s, mode, t):
    u = s["user"]
    out = svg_start(900, 160, "phdsx · public GitHub community snapshot", t)
    labels = [("GITHUB SINCE", u["created_at"][:4]), ("FOLLOWERS", u["followers"]), ("FOLLOWING", u["following"]), ("PUBLIC REPO FORKS", sum(r["forks_count"] for r in s["repositories"]))]
    for i,(label,value) in enumerate(labels):
        x = 112+i*225
        out += text(x, 62, value, t["accent"], 29, 700, "middle") + text(x, 92, label, t["muted"], 10, anchor="middle")
    out += text(450, 133, "Connections, projects and small discoveries on GitHub.", t["muted"], 11, anchor="middle")
    save_svg("community", mode, out)


def picture(name, alt, width="100%"):
    return f'''<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/generated/{name}-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/generated/{name}-light.svg" />
  <img src="./assets/generated/{name}-light.svg" alt="{alt}" width="{width}" />
</picture>'''


def update_readme(s):
    template = (ROOT / "README.template.md").read_text(encoding="utf-8")
    # Repository ownership does not establish original authorship. Use neutral labels.
    repos = [r for r in s["repositories"] if r["name"] != USER]
    featured = ["Autojs-practice", "Python-public", "Pytorch-NLP", "phdsx.github.io", "tool.github.io", "pic_cut.github.io", "dinnerninja.github.io", "TrendRadar"]
    ordered = sorted(repos, key=lambda r: (featured.index(r["name"]) if r["name"] in featured else len(featured), r["name"]))
    cards = []
    for r in ordered:
        desc = escape(r["description"] or "查看仓库中的代码与说明。")
        lang = escape(r["language"] or "—")
        cards.append(f'<td width="50%" valign="top"><h3><a href="{r["html_url"]}">{escape(r["name"])}</a></h3><p>{desc}</p><p><code>{lang}</code> · ⭐ {r["stargazers_count"]}</p></td>')
    project_table = '<table>\n' + '\n'.join('<tr>' + ''.join(cards[i:i+2]) + '</tr>' for i in range(0,len(cards),2)) + '\n</table>'
    updates = '<ul>\n' + '\n'.join(f'<li><strong>{r["pushed_at"][:10]}</strong> · <a href="{r["html_url"]}">{escape(r["name"])}</a></li>' for r in sorted(repos,key=lambda r:r["pushed_at"],reverse=True)[:5]) + '\n</ul>'
    replacements = {"PROJECTS": project_table, "UPDATES": updates, "UPDATED": s["fetched_at"][:10] + " UTC", "RANGE": s["contributions"][0]["date"] + " — " + s["contributions"][-1]["date"]}
    for name in ["overview", "languages", "streak", "activity", "snake", "contributions-3d", "community"]:
        replacements[name.upper()] = picture(name, f"phdsx · {name}")
    for key, value in replacements.items():
        template = template.replace("{{"+key+"}}", value)
    if re.search(r"\{\{[A-Z0-9_-]+\}\}", template):
        raise ValueError("Unresolved README template field")
    (ROOT / "README.md").write_text(template, encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--offline", action="store_true", help="Regenerate from the checked-in public snapshot")
    args = p.parse_args()
    path = ROOT / "data" / "github-public.json"
    snapshot = json.loads(path.read_text(encoding="utf-8")) if args.offline else fetch_snapshot()
    if snapshot["username"] != USER:
        raise ValueError("Unexpected snapshot owner")
    for mode, theme in THEMES.items():
        for render in [metrics, language_card, streak_card, activity, calendar, contribution_3d, community]:
            render(snapshot, mode, theme)
    update_readme(snapshot)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated profile for {USER}: {len(snapshot['repositories'])} repositories, {snapshot['contribution_total']} contributions. Snapshot: {snapshot['fetched_at']}")


if __name__ == "__main__":
    main()
