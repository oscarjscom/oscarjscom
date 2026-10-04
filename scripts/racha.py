"""Genera dist/streak.svg con contribuciones y rachas, a partir del calendario de GitHub.
Uso: GITHUB_TOKEN=... USUARIO=oscarjscom python scripts/racha.py"""
import json
import os
import sys
import random
import urllib.request
from datetime import date

W, H = 860, 210
VERDE, LIMA, TXT, DIM, LINEA = "#39d353", "#a3e635", "#e6edf3", "#7d8590", "#263238"
FONT = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
MESES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def calendario(usuario, token):
    q = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
      totalContributions weeks{contributionDays{date contributionCount}}}}}}"""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": q, "variables": {"login": usuario}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "racha"})
    with urllib.request.urlopen(req) as r:
        cal = json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    dias = [(d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]
    return cal["totalContributions"], dias


def rachas(dias):
    """Devuelve (actual, inicio, fin), (mejor, inicio, fin). dias: lista ordenada de (fecha, n)."""
    mejor = (0, None, None)
    n, ini = 0, None
    for f, c in dias:
        if c > 0:
            if n == 0:
                ini = f
            n += 1
            if n > mejor[0]:
                mejor = (n, ini, f)
        else:
            n = 0
    # racha actual: termina hoy, o ayer si hoy aun no hay contribuciones
    cola = dias[:]
    if cola and cola[-1][1] == 0:
        cola = cola[:-1]
    n, ini, fin = 0, None, None
    for f, c in reversed(cola):
        if c == 0:
            break
        n += 1
        ini = f
        fin = fin or f
    return (n, ini, fin), mejor


def corta(f):
    if not f:
        return "—"
    d = date.fromisoformat(f)
    return f"{MESES[d.month-1]} {d.day}"


def rango(a, b):
    return "no streak" if not a else (corta(a) if a == b else f"{corta(a)} - {corta(b)}")


def lluvia(x, semilla):
    """Separador vertical con cascada de caracteres estilo Matrix."""
    rnd = random.Random(semilla)
    letras = "01アイウエオカキクケコサシスセソ7Z"
    n, paso, y0, dur = 13, 12, 34, 2.6
    out = []
    for col, (dx, fase) in enumerate([(-9, 0.0), (0, 0.9), (9, 1.7)]):
        for i in range(n):
            c = rnd.choice(letras)
            out.append(f'<text x="{x+dx:.1f}" y="{y0+i*paso}" font-size="11" text-anchor="middle" '
                       f'style="animation:cae {dur}s linear {fase+i*dur/n/1.6:.2f}s infinite" opacity=".12" fill="{VERDE}">{c}</text>')
    return "\n".join(out)


def svg(total, dias, actual, mejor):
    cx = [W/6, W/2, 5*W/6]
    r = 46
    circ = 2*3.14159*r
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">
<defs><filter id="g" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>
text{{font-family:{FONT}}}
@keyframes gira{{to{{transform:rotate(360deg)}}}}
@keyframes late{{0%,100%{{opacity:1}}50%{{opacity:.55}}}}
@keyframes llama{{0%,100%{{transform:scale(1) translateY(0)}}50%{{transform:scale(1.18) translateY(-2px)}}}}
@keyframes sube{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes cae{{0%{{opacity:1;fill:#eaffea}}12%{{opacity:.95;fill:{LIMA}}}45%{{opacity:.45;fill:{VERDE}}}80%,100%{{opacity:.1;fill:{VERDE}}}}}
@keyframes onda{{0%{{r:{r}px;opacity:.7}}100%{{r:{r+26}px;opacity:0}}}}
.n{{animation:late 2.4s ease-in-out infinite}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
{lluvia(W/3, 1)}
{lluvia(2*W/3, 2)}

<text class="n" x="{cx[0]}" y="98" fill="{LIMA}" font-size="44" font-weight="700" text-anchor="middle" filter="url(#g)">{total}</text>
<text x="{cx[0]}" y="132" fill="{VERDE}" font-size="14" font-weight="700" letter-spacing="1.5" text-anchor="middle">CONTRIBUTIONS</text>
<text x="{cx[0]}" y="156" fill="{DIM}" font-size="12" text-anchor="middle">{corta(dias[0][0])} - {corta(dias[-1][0])}</text>

<circle cx="{cx[1]}" cy="88" fill="none" stroke="{VERDE}" stroke-width="2" style="animation:onda 2.6s ease-out infinite"/>
<circle cx="{cx[1]}" cy="88" r="{r}" fill="none" stroke="{LINEA}" stroke-width="5"/>
<circle cx="{cx[1]}" cy="88" r="{r}" fill="none" stroke="{VERDE}" stroke-width="5" stroke-linecap="round" stroke-dasharray="{circ*0.7:.1f} {circ*0.3:.1f}" filter="url(#g)" style="transform-origin:{cx[1]}px 88px;animation:gira 3.2s linear infinite"/>
<g style="transform-origin:{cx[1]}px 40px;animation:llama 0.9s ease-in-out infinite">
<path transform="translate({cx[1]-9},26)" d="M9 0c1 4 6 6 6 12a6 6 0 0 1-12 0c0-2 1-3 2-4 0 2 1 3 2 3 0-4 1-7 2-11z" fill="{LIMA}" stroke="#0d1117" stroke-width="1.5"/></g>
<text class="n" x="{cx[1]}" y="103" fill="{TXT}" font-size="40" font-weight="700" text-anchor="middle">{actual[0]}</text>
<text x="{cx[1]}" y="168" fill="{VERDE}" font-size="14" font-weight="700" letter-spacing="1.5" text-anchor="middle">CURRENT STREAK</text>
<text x="{cx[1]}" y="190" fill="{DIM}" font-size="12" text-anchor="middle">{rango(actual[1], actual[2])}</text>

<text class="n" x="{cx[2]}" y="98" fill="{LIMA}" font-size="44" font-weight="700" text-anchor="middle" filter="url(#g)" style="animation-delay:1.2s">{mejor[0]}</text>
<text x="{cx[2]}" y="132" fill="{VERDE}" font-size="14" font-weight="700" letter-spacing="1.5" text-anchor="middle">LONGEST STREAK</text>
<text x="{cx[2]}" y="156" fill="{DIM}" font-size="12" text-anchor="middle">{rango(mejor[1], mejor[2])}</text>
</svg>"""


def datos_repos(usuario, token):
    """Lenguaje principal de cada repo publico y horas (UTC-5) de los commits recientes."""
    from datetime import datetime, timedelta, timezone
    q = """query($login:String!){user(login:$login){repositories(first:100,ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC){
      nodes{primaryLanguage{name} defaultBranchRef{target{... on Commit{history(first:100){nodes{authoredDate}}}}}}}}}"""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": q, "variables": {"login": usuario}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "racha"})
    with urllib.request.urlopen(req) as r:
        nodos = json.load(r)["data"]["user"]["repositories"]["nodes"]
    lima = timezone(timedelta(hours=-5))
    lengs, horas = {}, [0]*24
    for n in nodos:
        if n.get("primaryLanguage"):
            k = n["primaryLanguage"]["name"]
            lengs[k] = lengs.get(k, 0) + 1
        ref = n.get("defaultBranchRef") or {}
        for c in ((ref.get("target") or {}).get("history") or {}).get("nodes", []):
            d = datetime.fromisoformat(c["authoredDate"].replace("Z", "+00:00")).astimezone(lima)
            horas[d.hour] += 1
    return lengs, horas


def panel(lengs, horas, dias):
    PW, PH = 860, 450
    COLS = [VERDE, LIMA, "#2dd4bf", "#d9f99d", "#86efac", DIM]
    o = []
    def titulo(x, y, t):
        o.append(f'<rect x="{x}" y="{y-11}" width="4" height="14" fill="{VERDE}"/>'
                 f'<text x="{x+12}" y="{y}" fill="{TXT}" font-size="13" font-weight="700" letter-spacing="1.5">{t}</text>')
    # --- dona de lenguajes ---
    titulo(10, 22, "LANGUAGES BY REPOSITORY")
    items = sorted(lengs.items(), key=lambda kv: -kv[1])
    if len(items) > 5:
        items = items[:5] + [("Other", sum(v for _, v in items[5:]))]
    tot = sum(v for _, v in items) or 1
    cx, cy, r = 110, 122, 58
    C = 2*3.14159265*r
    acc = 0.0
    for i, (k, v) in enumerate(items):
        L = C*v/tot
        col = COLS[i % len(COLS)]
        hueco = 3 if len(items) > 1 else 0
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="20" '
                 f'transform="rotate({-90+360*acc/C:.2f} {cx} {cy})" stroke-dasharray="0 {C:.1f}">'
                 f'<animate attributeName="stroke-dasharray" values="0 {C:.1f};{max(L-hueco,0.1):.1f} {C:.1f};{max(L-hueco,0.1):.1f} {C:.1f};0 {C:.1f}" '
                 f'keyTimes="0;{0.08+0.04*i:.2f};0.92;1" dur="9s" repeatCount="indefinite"/></circle>')
        acc += L
        y = 62 + i*24
        o.append(f'<rect x="212" y="{y-10}" width="12" height="12" rx="2" fill="{col}"/>'
                 f'<text x="232" y="{y}" fill="{TXT}" font-size="12.5">{k}</text>'
                 f'<text x="400" y="{y}" fill="{DIM}" font-size="12.5" text-anchor="end">{round(100*v/tot)}%</text>')
    o.append(f'<text x="{cx}" y="{cy-2}" fill="{TXT}" font-size="26" font-weight="700" text-anchor="middle" class="n">{tot}</text>'
             f'<text x="{cx}" y="{cy+16}" fill="{DIM}" font-size="10.5" text-anchor="middle" letter-spacing="1">REPOS</text>')
    # --- barras por hora ---
    bx0, by0, bw, bh = 470, 180, 370, 120
    titulo(450, 22, "COMMITS BY HOUR · UTC-5")
    mx = max(horas) or 1
    paso = bw/24
    o.append(f'<line x1="{bx0}" y1="{by0}" x2="{bx0+bw}" y2="{by0}" stroke="{LINEA}" stroke-width="1.5"/>')
    for hh, v in enumerate(horas):
        alto = bh*v/mx
        x = bx0 + hh*paso + 2
        if v:
            o.append(f'<rect x="{x:.1f}" y="{by0}" width="{paso-4:.1f}" height="0" rx="2" fill="{VERDE}">'
                     f'<animate attributeName="height" values="0;{alto:.1f};{alto:.1f};0" keyTimes="0;{0.10+hh*0.012:.3f};0.9;1" dur="9s" repeatCount="indefinite"/>'
                     f'<animate attributeName="y" values="{by0};{by0-alto:.1f};{by0-alto:.1f};{by0}" keyTimes="0;{0.10+hh*0.012:.3f};0.9;1" dur="9s" repeatCount="indefinite"/></rect>')
        if hh % 6 == 0 or hh == 23:
            o.append(f'<text x="{x+(paso-4)/2:.1f}" y="{by0+16}" fill="{DIM}" font-size="10.5" text-anchor="middle">{hh}h</text>')
    o.append(f'<text x="{bx0+bw}" y="{by0-bh-4}" fill="{DIM}" font-size="10.5" text-anchor="end">max {mx}</text>')
    # --- area de contribuciones por semana ---
    titulo(10, 252, "CONTRIBUTIONS PER WEEK · LAST YEAR")
    sem = [sum(c for _, c in dias[i:i+7]) for i in range(0, len(dias), 7)]
    ax0, ay0, aw, ah = 40, 410, 800, 120
    ms = max(sem) or 1
    pts = [(ax0 + aw*i/max(len(sem)-1, 1), ay0 - ah*v/ms) for i, v in enumerate(sem)]
    linea = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    o.append(f'<defs><linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{VERDE}" stop-opacity=".55"/><stop offset="1" stop-color="{VERDE}" stop-opacity="0"/></linearGradient>'
             f'<clipPath id="rev"><rect x="{ax0}" y="{ay0-ah-10}" width="0" height="{ah+20}"><animate attributeName="width" values="0;{aw};{aw};0" keyTimes="0;0.4;0.93;1" dur="9s" repeatCount="indefinite"/></rect></clipPath></defs>')
    for g in range(0, 5):
        yy = ay0 - ah*g/4
        o.append(f'<line x1="{ax0}" y1="{yy:.1f}" x2="{ax0+aw}" y2="{yy:.1f}" stroke="{LINEA}" stroke-width="1" stroke-dasharray="{"0" if g == 0 else "2 6"}"/>'
                 f'<text x="{ax0-8}" y="{yy+4:.1f}" fill="{DIM}" font-size="10.5" text-anchor="end">{round(ms*g/4)}</text>')
    o.append(f'<g clip-path="url(#rev)"><polygon points="{ax0},{ay0} {linea} {ax0+aw},{ay0}" fill="url(#ar)"/>'
             f'<polyline points="{linea}" fill="none" stroke="{VERDE}" stroke-width="2.5" stroke-linejoin="round" filter="url(#g)"/></g>')
    o.append(f'<rect x="{ax0}" y="{ay0-ah-6}" width="2" height="{ah+6}" fill="{LIMA}" opacity=".9"><animate attributeName="x" values="{ax0};{ax0+aw};{ax0+aw};{ax0}" keyTimes="0;0.4;0.93;1" dur="9s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values=".9;.9;0;0" keyTimes="0;0.4;0.45;1" dur="9s" repeatCount="indefinite"/></rect>')
    visto = None
    for i in range(0, len(dias), 7):
        m = dias[i][0][5:7]
        if m != visto and i/7 < len(sem)-1:
            visto = m
            x = ax0 + aw*(i/7)/max(len(sem)-1, 1)
            o.append(f'<text x="{x:.1f}" y="{ay0+18}" fill="{DIM}" font-size="10.5" text-anchor="middle">{MESES[int(m)-1]}</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" width="{PW}" height="{PH}" role="img">
<defs><filter id="g" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>text{{font-family:{FONT}}}@keyframes late{{0%,100%{{opacity:1}}50%{{opacity:.55}}}}.n{{animation:late 2.4s ease-in-out infinite}}@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
{chr(10).join(o)}
</svg>"""


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        from datetime import timedelta
        rnd = random.Random(7)
        dias = [((date(2025, 10, 5) + timedelta(days=i)).isoformat(), rnd.choice([0, 0, 0, 0, 1, 2, 5]) if i > 200 or i % 40 < 6 else 0) for i in range(365)]
        total = sum(c for _, c in dias)
        lengs = {"JavaScript": 3, "Python": 2, "HTML": 2, "Dart": 1, "Swift": 1}
        horas = [0, 2, 14, 1, 0, 0, 0, 0, 0, 5, 3, 10, 13, 1, 2, 2, 0, 0, 0, 0, 1, 2, 6, 6]
    else:
        total, dias = calendario(os.environ["USUARIO"], os.environ["GITHUB_TOKEN"])
        lengs, horas = datos_repos(os.environ["USUARIO"], os.environ["GITHUB_TOKEN"])
    actual, mejor = rachas(dias)
    os.makedirs("dist", exist_ok=True)
    open("dist/streak.svg", "w", encoding="utf-8").write(svg(total, dias, actual, mejor))
    open("dist/panel-en.svg", "w", encoding="utf-8").write(panel(lengs, horas, dias))
    print(f"total={total} actual={actual} mejor={mejor} lengs={lengs} horas={horas}")
