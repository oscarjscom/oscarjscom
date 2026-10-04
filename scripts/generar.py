"""Genera los SVG del perfil. Uso: python scripts/generar.py"""
from pathlib import Path
from html import escape as e
import math

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)
W = 860
BG, PANEL, LINE = "#0d1117", "#111820", "#263238"
CYAN, MAG, YEL, VIO, TXT, DIM = "#39d353", "#a3e635", "#d9f99d", "#2dd4bf", "#e6edf3", "#7d8590"
GRN, RED = "#39d353", "#ff5a36"
MINT = "#86efac"
FONT = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
CW = 0.602  # ancho de caracter monoespaciado relativo al tamano

import json as _json
_ORB = _json.loads((Path(__file__).resolve().parent / "orbitron.json").read_text(encoding="utf-8"))
ORB_CSS = f"@font-face{{font-family:'Orb';font-weight:900;src:url(data:font/woff2;base64,{_ORB['woff2_base64']}) format('woff2')}}"
ORB = "'Orb'," + FONT

def ancho_orb(texto, tam, espaciado=0):
    return sum(_ORB["avances"].get(c, 0.8) for c in texto)*tam + espaciado*len(texto)

def svg(h, body, extra_css=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img">
<defs>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{MAG}"/></linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<style>
text{{font-family:{FONT};}}
.in{{opacity:0;animation:in .45s ease-out forwards}}
@keyframes in{{to{{opacity:1}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes pulse{{0%{{opacity:.9;transform:scale(.35)}}100%{{opacity:0;transform:scale(1)}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes dash{{to{{stroke-dashoffset:-24}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.in{{opacity:1}}}}
{extra_css}
</style>
<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="6" fill="{BG}" stroke="{LINE}" stroke-width="1.5"/>
<path d="M1 22V7a6 6 0 0 1 6-6h15M{W-23} 1h15a6 6 0 0 1 6 6v15M{W-1} {h-23}v15a6 6 0 0 1-6 6h-15M22 {h-1}H7a6 6 0 0 1-6-6v-15" fill="none" stroke="{CYAN}" stroke-width="2.5"/>
{body}
</svg>'''

def t(x, y, s, fill=TXT, size=13, weight=400, anchor="start", cls="", style=""):
    c = f' class="{cls}"' if cls else ""
    st = f' style="{style}"' if style else ""
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{c}{st} xml:space="preserve">{e(s)}</text>'

def chrome(title):
    dots = "".join(f'<circle cx="{26+i*18}" cy="24" r="5.5" fill="{c}"/>' for i, c in enumerate([RED, YEL, GRN]))
    return dots + t(W/2, 28, title, DIM, 12, anchor="middle") + f'<line x1="1" y1="46" x2="{W-1}" y2="46" stroke="{LINE}"/>'

# ---------- hero ----------
def hero():
    h = 400
    b = [chrome("vim perfil.yml")]
    # panel izquierdo: mapa de senal
    px, py, pw, ph = 22, 62, 262, 316
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="4" fill="{PANEL}" stroke="{LINE}"/>')
    b.append(t(px+14, py+24, "SIGNAL.MAP", TXT, 11, 700) + t(px+pw-14, py+24, "4 nodos · en línea", DIM, 10, anchor="end"))
    cx, cy = px+pw/2, py+ph/2+8
    for i in range(3):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="112" fill="none" stroke="{CYAN}" stroke-width="1.2" style="transform-origin:{cx}px {cy}px;animation:pulse 3.6s {i*1.2}s linear infinite;opacity:0"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="92" fill="none" stroke="{LINE}" stroke-dasharray="3 5"/>')
    nodes = [("API", -90, CYAN), ("WEB", 0, MAG), ("IoT", 90, YEL), ("APP", 180, VIO)]
    for name, ang, col in nodes:
        a = math.radians(ang); nx, ny = cx+92*math.cos(a), cy+92*math.sin(a)
        b.append(f'<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{col}" stroke-width="1.3" stroke-dasharray="4 4" style="animation:dash 1.2s linear infinite" opacity=".8"/>')
        b.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="21" fill="{BG}" stroke="{col}" stroke-width="1.5" filter="url(#glow)"/>')
        b.append(t(f"{nx:.1f}", f"{ny+4:.1f}", name, col, 11, 700, "middle"))
    # chip central
    b.append(f'<g style="transform-origin:{cx}px {cy}px;animation:spin 18s linear infinite"><rect x="{cx-34}" y="{cy-34}" width="68" height="68" rx="6" fill="none" stroke="{MAG}" stroke-dasharray="2 6" opacity=".7"/></g>')
    b.append(f'<rect x="{cx-26}" y="{cy-26}" width="52" height="52" rx="6" fill="{BG}" stroke="url(#edge)" stroke-width="1.6" filter="url(#glow)"/>')
    b.append(t(cx, cy-1, "</>", CYAN, 15, 700, "middle") + t(cx, cy+14, "oscar", TXT, 9, anchor="middle"))
    b.append(t(px+14, py+ph-12, "LIM · UTC-5", DIM, 9) + t(px+pw-14, py+ph-12, "FULL STACK + IoT", DIM, 9, anchor="end"))
    # panel derecho: yaml
    rx, ry, rw, rh = 298, 62, 540, 316
    b.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="4" fill="{PANEL}" stroke="{LINE}"/>')
    b.append(t(rx+14, ry+24, "perfil.yml", TXT, 11, 700) + t(rx+86, ry+24, "[YAML]", DIM, 10))
    b.append(f'<rect x="{rx+rw-124}" y="{ry+10}" width="110" height="20" rx="10" fill="{BG}" stroke="{LINE}"/>' + t(rx+rw-69, ry+24, "@oscarjscom", CYAN, 10, anchor="middle"))
    L = [("perfil:", None), ("  nombre", "Oscar"), ("  rol", "Estudiante de Ing. de Software"),
         ("  base", "Lima, Perú"), ("  casa", "TECSUP · 5to ciclo"), ("  foco", "Backend · Mobile · IoT"),
         ("  estado", "abierto a prácticas de desarrollo"), ("stack:", None),
         ("  backend", "Spring Boot · Django · Node.js"), ("  frontend", "React · Next.js · Three.js"),
         ("  mobile", "Kotlin/Compose · Swift · Flutter"), ("  datos", "MySQL · Firestore · DynamoDB"),
         ("  iot", "Arduino · ESP32-CAM"), ("contacto:", None), ("  github", "oscarjscom"),
         ("  zona", "UTC-5 · Lima")]
    y0, lh, fs = ry+50, 15.6, 11.5
    for i, (k, v) in enumerate(L):
        y = y0 + i*lh; d = f"animation-delay:{0.25+i*0.13:.2f}s"
        b.append(t(rx+30, f"{y:.1f}", f"{i+1}", DIM, 10, anchor="end", cls="in", style=d))
        if v is None:
            b.append(t(rx+44, f"{y:.1f}", k, TXT, fs, 700, cls="in", style=d))
        else:
            kx = rx+44; vx = kx + (len(k)+2)*fs*CW
            col = YEL if "estado" in k else TXT
            b.append(t(kx, f"{y:.1f}", k+":", MAG, fs, cls="in", style=d) + t(f"{vx:.1f}", f"{y:.1f}", v, col, fs, cls="in", style=d))
    sy = ry+rh-26
    b.append(f'<line x1="{rx}" y1="{sy}" x2="{rx+rw}" y2="{sy}" stroke="{LINE}"/>')
    b.append(f'<rect x="{rx+12}" y="{sy+6}" width="62" height="15" rx="3" fill="{GRN}"/>' + t(rx+43, sy+17, "NORMAL", BG, 9.5, 700, "middle"))
    b.append(t(rx+84, sy+17, "perfil.yml", TXT, 10, 700) + t(rx+rw/2+40, sy+17, "[utf-8]", DIM, 10, anchor="middle") + t(rx+rw-14, sy+17, "16L · 100% · 16:1", DIM, 10, anchor="end"))
    b.append(f'<rect x="{rx+44+ (len("  zona: UTC-5 · Lima"))*fs*CW:.1f}" y="{y0+15*lh-10:.1f}" width="7" height="13" fill="{CYAN}" style="animation:blink 1s steps(1) infinite"/>')
    return svg(h, "\n".join(b))

# ---------- perfil (solo yml, va junto al GIF) ----------
def perfil_anterior():
    global W
    W0, W = W, 580
    try:
        L = [("perfil:", None),
             ("  nombre", "Oscar"),
             ("  rol", "Desarrollador Full Stack Jr."),
             ("  formacion", "Ing. de Software · TECSUP · 5to ciclo"),
             ("  ubicacion", "Lima, Perú · UTC-5"),
             ("busco:", None),
             ("  puesto", "Practicante de desarrollo de software"),
             ("  areas", "Backend · Full Stack · Mobile"),
             ("  disponibilidad", "inmediata"),
             ("stack:", None),
             ("  backend", "Java · Spring Boot · Django · Node.js"),
             ("  frontend", "React · Next.js · JavaScript"),
             ("  mobile", "Kotlin/Compose · Swift · Flutter"),
             ("  datos", "MySQL · Firestore · DynamoDB"),
             ("  devops", "Docker · Git/GitHub · AWS"),
             ("experiencia_en_proyectos:", None),
             ("  -", "FixMyCity · plataforma web con IA"),
             ("  -", "NextCap · IoT en tiempo real"),
             ("  -", "ekECO · hackathon QuipuSoft 2026"),
             ("  -", "Microservicios con Spring Boot"),
             ("idiomas:", None),
             ("  -", "Español · Inglés (en curso)"),
             ("contacto:", None),
             ("  github", "oscarjscom")]
        n = len(L); lh, fs = 15.6, 12
        rx, ry, rw = 20, 62, 540
        rh = 50 + (n-1)*lh + 44
        h = int(ry + rh + 22)
        b = [chrome("vim perfil.yml")]
        b.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh:.0f}" rx="4" fill="{PANEL}" stroke="{LINE}"/>')
        b.append(t(rx+14, ry+24, "perfil.yml", TXT, 11, 700) + t(rx+86, ry+24, "[YAML]", DIM, 10))
        b.append(f'<rect x="{rx+rw-124}" y="{ry+10}" width="110" height="20" rx="10" fill="{BG}" stroke="{LINE}"/>' + t(rx+rw-69, ry+24, "@oscarjscom", CYAN, 10, anchor="middle"))
        y0 = ry+50
        for i, (k, v) in enumerate(L):
            y = y0 + i*lh; d = f"animation-delay:{0.2+i*0.09:.2f}s"
            b.append(t(rx+30, f"{y:.1f}", f"{i+1}", DIM, 10, anchor="end", cls="in", style=d))
            if v is None:
                b.append(f'<text x="{rx+44}" y="{y:.1f}" fill="{TXT}" font-size="{fs}" font-weight="700" class="in" style="{d}" xml:space="preserve">{e(k)}</text>')
            elif k.strip() == "-":
                b.append(f'<text x="{rx+44}" y="{y:.1f}" font-size="{fs}" class="in" style="{d}" xml:space="preserve"><tspan fill="{CYAN}">  -</tspan><tspan fill="{TXT}"> {e(v)}</tspan></text>')
            else:
                col = YEL if k.strip() in ("puesto", "disponibilidad") else TXT
                wt = ' font-weight="700"' if col == YEL else ""
                b.append(f'<text x="{rx+44}" y="{y:.1f}" font-size="{fs}" class="in" style="{d}" xml:space="preserve"><tspan fill="{MAG}">{e(k)}:</tspan><tspan fill="{col}"{wt}> {e(v)}</tspan></text>')
        sy = ry+rh-26
        b.append(f'<line x1="{rx}" y1="{sy:.0f}" x2="{rx+rw}" y2="{sy:.0f}" stroke="{LINE}"/>')
        b.append(f'<rect x="{rx+12}" y="{sy+6:.0f}" width="62" height="15" rx="3" fill="{GRN}"/>' + t(rx+43, f"{sy+17:.0f}", "NORMAL", BG, 9.5, 700, "middle"))
        b.append(t(rx+84, f"{sy+17:.0f}", "perfil.yml", TXT, 10, 700) + t(rx+rw/2+40, f"{sy+17:.0f}", "[utf-8]", DIM, 10, anchor="middle") + t(rx+rw-14, f"{sy+17:.0f}", f"{n}L · 100% · {n}:1", DIM, 10, anchor="end"))
        return svg(h, "\n".join(b))
    finally:
        W = W0

# ---------- perfil compacto (va junto al GIF, misma altura) ----------
def perfil():
    import random
    PW, PH = 580, 393          # proporcion pensada para igualar la altura del GIF cuadrado
    L = [("perfil:", None),
         ("  nombre", "Oscar"),
         ("  rol", "Desarrollador Full Stack Jr."),
         ("  formacion", "Ing. de Software · TECSUP · 5to ciclo"),
         ("  ubicacion", "Lima, Perú · UTC-5"),
         ("busco:", None),
         ("  puesto", "Practicante de desarrollo de software"),
         ("  areas", "Backend · Full Stack · Mobile"),
         ("  disponibilidad", "inmediata"),
         ("contacto:", None),
         ("  github", "oscarjscom")]
    n = len(L); fs = 15.5; lh = 27.5; x0 = 46; y0 = 94; CIC = n*0.9
    o = []
    # cascada tenue a la derecha
    rnd = random.Random(5)
    kana = "アイウエオカキクケコサシスセソ01"
    for c, x in enumerate([PW-44, PW-28, PW-12]):
        fase = rnd.uniform(0, 2); dur = [2.3, 2.9, 2.0][c]
        for f in range(15):
            o.append(f'<text x="{x}" y="{70+f*21}" font-size="13" text-anchor="middle" fill="{CYAN}" opacity=".08" style="animation:cae {dur}s linear {fase+f*dur/15/1.4:.2f}s infinite">{rnd.choice(kana)}</text>')
    # titulo
    tit = "PERFIL.YML"
    o.append(f'<rect x="0" y="14" width="5" height="30" rx="2.5" fill="{CYAN}" filter="url(#g)"/>')
    o.append(f'<text class="orb" x="18" y="40" fill="{TXT}" font-size="26" letter-spacing="2" filter="url(#g)">{tit}</text>')
    o.append(f'<rect x="{18+ancho_orb(tit, 26, 2)+8:.1f}" y="17" width="12" height="25" fill="{CYAN}" style="animation:blink 1s steps(1) infinite"/>')
    o.append(f'<text x="{PW-66}" y="38" fill="{DIM}" font-size="12" text-anchor="end">@oscarjscom</text>')
    o.append(f'<rect x="0" y="56" width="{PW-66}" height="2" fill="url(#fade)"/>')
    # barra de lectura que baja linea por linea
    pasos = ";".join(f"{y0-18+i*lh:.1f}" for i in range(n)) + f";{y0-18:.1f}"
    o.append(f'<rect x="0" y="{y0-18}" width="{PW-66}" height="{lh:.1f}" rx="3" fill="{CYAN}" fill-opacity=".10"><animate attributeName="y" values="{pasos}" dur="{CIC}s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    o.append(f'<rect x="0" y="{y0-18}" width="3" height="{lh:.1f}" fill="{MAG}"><animate attributeName="y" values="{pasos}" dur="{CIC}s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    for i, (k, v) in enumerate(L):
        y = y0 + i*lh
        o.append(f'<text x="30" y="{y:.1f}" fill="{DIM}" font-size="11.5" text-anchor="end">{i+1}</text>')
        if v is None:
            o.append(f'<text x="{x0}" y="{y:.1f}" fill="{TXT}" font-size="{fs}" font-weight="700" xml:space="preserve">{e(k)}</text>')
        else:
            fuerte = k.strip() in ("puesto", "disponibilidad")
            col = YEL if fuerte else TXT
            extra = ' font-weight="700" style="animation:late 2.2s ease-in-out infinite"' if fuerte else ""
            o.append(f'<text x="{x0}" y="{y:.1f}" font-size="{fs}" xml:space="preserve"><tspan fill="{MAG}">{e(k)}:</tspan><tspan fill="{col}"{extra}> {e(v)}</tspan></text>')
    cuerpo = "\n".join(o)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" width="{PW}" height="{PH}" role="img">
<defs><linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<filter id="g" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>{ORB_CSS}
text{{font-family:{FONT}}}
.orb{{font-family:{ORB};font-weight:900}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes late{{0%,100%{{opacity:1}}50%{{opacity:.55}}}}
@keyframes cae{{0%{{opacity:.9;fill:#eaffea}}12%{{opacity:.7;fill:{MAG}}}45%{{opacity:.3;fill:{CYAN}}}80%,100%{{opacity:.06;fill:{CYAN}}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
{cuerpo}
</svg>"""

# ---------- about me (panel en ingles, va junto al GIF) ----------
def about():
    import random
    PW, PH = 600, 360
    parrafo = ["I'm a Software Engineering student at TECSUP (5th term) in Lima,",
               "Peru. I focus on backend and full stack development, and I like",
               "taking a project end to end: from the API to the mobile app."]
    bloques = [("INTERESTED IN", ["Backend development · Mobile apps · IoT"]),
               ("LEARNING", ["iOS development with Swift", "Cloud solutions on AWS", "Advanced web development with Node.js"]),
               ("BUILDING", ["FixMyCity: citizen-report platform for", "municipalities, assisted by AI (capstone)"]),
               ("LOOKING FOR", ["Software development internship", "Backend · Full stack · Mobile · available now"]),
               ("OPEN TO", ["Collaboration and questions about my work"])]
    fs = 13.5; lh = 21; xt = 14; xv = 152; ancho = PW - 52
    o = []
    rnd = random.Random(9)
    kana = "アイウエオカキクケコサシスセソ01"
    for c, x in enumerate([PW-36, PW-22, PW-8]):
        fase = rnd.uniform(0, 2); dur = [2.3, 2.9, 2.0][c]
        for f in range(17):
            o.append(f'<text x="{x}" y="{16+f*21}" font-size="12" text-anchor="middle" fill="{CYAN}" opacity=".08" style="animation:cae {dur}s linear {fase+f*dur/17/1.4:.2f}s infinite">{rnd.choice(kana)}</text>')
    o.append(f'<text x="{xt}" y="20" fill="{DIM}" font-size="12">~/about.md</text>')
    o.append(f'<rect x="{xt+10*12*CW+8:.1f}" y="9" width="7" height="14" fill="{CYAN}" style="animation:blink 1s steps(1) infinite"/>')
    o.append(f'<rect x="0" y="30" width="{ancho}" height="2" fill="url(#fade)"/>')
    y = 56
    for ln in parrafo:
        o.append(f'<text x="{xt}" y="{y}" fill="{TXT}" font-size="{fs}" xml:space="preserve">{e(ln)}</text>')
        y += lh
    y += 12
    tramos = []
    for etq, lineas in bloques:
        alto = len(lineas)*lh + 6
        tramos.append((y-16, alto))
        o.append(f'<text class="orb" x="{xt}" y="{y}" fill="{MAG}" font-size="10.5" letter-spacing="1.2">{etq}</text>')
        for j, ln in enumerate(lineas):
            fuerte = etq == "LOOKING FOR" and j == 0
            extra = f' font-weight="700" fill="{YEL}" style="animation:late 2.2s ease-in-out infinite"' if fuerte else f' fill="{TXT}"'
            o.append(f'<text x="{xv}" y="{y+j*lh}" font-size="{fs}"{extra} xml:space="preserve">{e(ln)}</text>')
        y += len(lineas)*lh + 8
    n = len(tramos); CIC = n*1.6
    ys = ";".join(str(a) for a, _ in tramos) + f";{tramos[0][0]}"
    hs = ";".join(str(b) for _, b in tramos) + f";{tramos[0][1]}"
    barra = (f'<rect x="0" y="{tramos[0][0]}" width="{ancho}" height="{tramos[0][1]}" rx="3" fill="{CYAN}" fill-opacity=".09">'
             f'<animate attributeName="y" values="{ys}" dur="{CIC}s" calcMode="discrete" repeatCount="indefinite"/>'
             f'<animate attributeName="height" values="{hs}" dur="{CIC}s" calcMode="discrete" repeatCount="indefinite"/></rect>'
             f'<rect x="0" y="{tramos[0][0]}" width="3" height="{tramos[0][1]}" fill="{MAG}">'
             f'<animate attributeName="y" values="{ys}" dur="{CIC}s" calcMode="discrete" repeatCount="indefinite"/>'
             f'<animate attributeName="height" values="{hs}" dur="{CIC}s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    cuerpo = barra + "\n" + "\n".join(o)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" width="{PW}" height="{PH}" role="img">
<defs><linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient></defs>
<style>{ORB_CSS}
text{{font-family:{FONT}}}
.orb{{font-family:{ORB};font-weight:900}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes late{{0%,100%{{opacity:1}}50%{{opacity:.55}}}}
@keyframes cae{{0%{{opacity:.9;fill:#eaffea}}12%{{opacity:.7;fill:{MAG}}}45%{{opacity:.3;fill:{CYAN}}}80%,100%{{opacity:.06;fill:{CYAN}}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
{cuerpo}
</svg>"""

# ---------- whoami ----------
def whoami():
    h = 250
    b = [chrome("oscarjscom · shell · online")]
    x, y, w, hh = 22, 62, 548, 166
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="4" fill="{PANEL}" stroke="{VIO}" stroke-opacity=".7"/>')
    b.append(t(x+18, y+28, "❯", CYAN, 14, 700) + t(x+38, y+28, "whoami", CYAN, 14, 700))
    b.append(t(x+18, y+52, "oscar", TXT, 13) + t(x+120, y+52, "—", DIM, 13) + t(x+142, y+52, "Desarrollador Full Stack en formación", YEL, 13, 700))
    b.append(f'<line x1="{x+18}" y1="{y+64}" x2="{x+w-18}" y2="{y+64}" stroke="{LINE}"/>')
    b.append(t(x+18, y+84, "contexto:", DIM, 12) + t(x+104, y+84, "Lima, Perú · TECSUP", VIO, 12))
    b.append(t(x+18, y+103, "misión:", DIM, 12) + t(x+104, y+103, "llevar ideas del sensor a la nube y a la pantalla", GRN, 12))
    b.append(t(x+18, y+128, "❯", CYAN, 13, 700) + t(x+38, y+128, "ls intereses/", CYAN, 13, 700))
    b.append(t(x+18, y+146, "backend/", MAG, 11.5) + t(x+84, y+146, "APIs REST · microservicios", TXT, 11.5) + t(x+290, y+146, "iot/", MAG, 11.5) + t(x+326, y+146, "sensores · tiempo real · 3D", TXT, 11.5))
    # panel derecho: senal neon
    x2, w2 = 584, 254
    b.append(f'<rect x="{x2}" y="{y}" width="{w2}" height="{hh}" rx="4" fill="{PANEL}" stroke="{VIO}" stroke-opacity=".7"/>')
    b.append(t(x2+16, y+26, "carga del sistema", YEL, 12))
    bx, by = x2+28, y+118
    hs = [28, 52, 40, 70, 34, 60, 46, 76, 38, 56, 30, 48]
    css = []
    for i, v in enumerate(hs):
        col = [CYAN, MAG, VIO][i % 3] if i != 7 else YEL
        b.append(f'<rect x="{bx+i*17}" y="{by-v}" width="10" height="{v}" rx="2" fill="{col}" opacity=".9" style="transform-origin:{bx+i*17+5}px {by}px;animation:eq{i%4} {1.4+(i%5)*0.25:.2f}s ease-in-out infinite alternate"/>')
    b.append(f'<line x1="{x2+16}" y1="{by+1}" x2="{x2+w2-16}" y2="{by+1}" stroke="{CYAN}" stroke-width="1.5" filter="url(#glow)"/>')
    b.append(t(x2+16, y+hh-12, "estado: aprendiendo y construyendo", DIM, 10.5))
    extra = "".join(f"@keyframes eq{i}{{to{{transform:scaleY({s})}}}}" for i, s in enumerate([.45, .7, .3, .85]))
    return svg(h, "\n".join(b), extra)

# ---------- stack ----------
def stack():
    cats = [("backend", "⚙", ["Java", "Spring Boot", "Django", "DRF", "Node.js"]),
            ("frontend", "✦", ["React", "Next.js", "Three.js", "JavaScript"]),
            ("mobile", "▣", ["Kotlin", "Jetpack Compose", "Swift", "Flutter"]),
            ("datos", "◉", ["MySQL", "Firestore", "DynamoDB"]),
            ("iot_hardware", "⌁", ["Arduino", "ESP32-CAM", "Sensores"]),
            ("nube_herramientas", "☁", ["Docker", "Git / GitHub", "AWS", "n8n"])]
    colw, rowh, top = (W-44-14)/2, 96, 62
    h = top + 3*rowh + 2*12 + 48
    b = [chrome("oscarjscom:~$ cat tech-stack.yaml")]
    cols = [CYAN, MAG, VIO, YEL, GRN, CYAN]
    for i, (name, ico, items) in enumerate(cats):
        cx = 22 + (i % 2)*(colw+14); cy = top + (i//2)*(rowh+12)
        b.append(f'<rect x="{cx:.1f}" y="{cy}" width="{colw:.1f}" height="{rowh}" rx="4" fill="{PANEL}" stroke="{LINE}"/>')
        pre = "╰─" if i >= 4 else "├─"
        b.append(t(f"{cx+14:.1f}", cy+26, f"{pre} {ico} ", DIM, 12) + t(f"{cx+14+6*12*CW+4:.1f}", cy+26, name+":", cols[i], 12.5, 700))
        x = cx+16; yy = cy+44
        for it in items:
            cw = len(it)*11.5*CW + 20
            b.append(f'<rect x="{x:.1f}" y="{yy}" width="{cw:.1f}" height="26" rx="13" fill="{BG}" stroke="{cols[i]}" stroke-opacity=".75"/>' + t(f"{x+cw/2:.1f}", yy+17.5, it, TXT, 11.5, anchor="middle"))
            x += cw + 8
    fy = h-22
    b.append(t(22, fy, "status:", DIM, 12) + t(80, fy, "ready", GRN, 12, 700) + t(128, fy, "·", DIM, 12) + t(146, fy, "environment:", DIM, 12) + t(240, fy, "en constante aprendizaje", YEL, 12, 700))
    return svg(int(h), "\n".join(b))

# ---------- proyectos ----------
def proyectos():
    ps = [("FixMyCity", "capstone project", CYAN,
           ["Citizen-report and tracking platform for municipalities in Peru,", "assisted by AI."],
           ["Citizen app", "Municipal dashboard", "AI engine"]),
          ("NextCap", "IoT · occupancy counting", MAG,
           ["Dual-lane people-counting system with barriers,", "a real-time backend and an interactive 3D viewer."],
           ["Arduino · ESP32-CAM", "Node.js · WebSocket", "Three.js"]),
          ("ekECO", "QuipuSoft 2026 hackathon", VIO,
           ["AI waste classifier built on a", "serverless AWS architecture."],
           ["AWS serverless", "Generative AI", "Teamwork"]),
          ("Microservices", "backend architecture", YEL,
           ["Microservices architecture with service discovery,", "an API gateway and fault tolerance."],
           ["Spring Boot", "Eureka · API Gateway", "Resilience4j"]),
          ("TravelMate", "travel chatbot", CYAN,
           ["Chatbot for a travel platform", "with OpenAI integration."],
           ["Laravel", "OpenAI API", "Chatbot"]),
          ("JARVIS offline", "voice assistant", MINT,
           ["JARVIS-style voice assistant that works offline,", "right in the browser."],
           ["HTML · JavaScript", "Web Speech API", "Offline"])]
    n = len(ps); T = 4.5; CIC = n*T
    h = 300; p1 = 100/n
    css = ["@keyframes blink{50%{opacity:0}}",
           f"@keyframes pasa{{0%{{opacity:0;transform:translateX(40px)}}{p1*0.08:.2f}%{{opacity:1;transform:translateX(0)}}{p1*0.92:.2f}%{{opacity:1;transform:translateX(0)}}{p1:.2f}%{{opacity:0;transform:translateX(-40px)}}100%{{opacity:0;transform:translateX(-40px)}}}}",
           f"@keyframes num{{0%{{opacity:0;transform:translateY(30px)}}{p1*0.1:.2f}%{{opacity:1;transform:translateY(0)}}{p1*0.92:.2f}%{{opacity:1}}{p1:.2f}%,100%{{opacity:0;transform:translateY(-30px)}}}}",
           f"@keyframes raya{{0%{{transform:scaleX(0)}}{p1*0.25:.2f}%,{p1*0.92:.2f}%{{transform:scaleX(1)}}{p1:.2f}%,100%{{transform:scaleX(0)}}}}",
           "@keyframes late{0%,100%{fill-opacity:.07}50%{fill-opacity:.2}}",
           "@keyframes traza{to{stroke-dashoffset:-510}}",
           "@keyframes fallo{0%,100%{transform:translate(0,0)}86%{transform:translate(-7px,2px)}89%{transform:translate(6px,-3px)}92%{transform:translate(-3px,0)}95%{transform:translate(0,0)}}",
           "@media (prefers-reduced-motion:reduce){*{animation:none!important}.s0{opacity:1!important}}"]
    cmd = "oscar@lima:~$ cat projects/*.md"
    b = [t(2, 24, cmd, DIM, 13.5),
         f'<rect x="{2+len(cmd)*13.5*CW+6:.1f}" y="11" width="8" height="16" fill="{CYAN}" style="animation:blink 1s steps(1) infinite"/>',
         f'<line x1="0" y1="36" x2="{W}" y2="36" stroke="{LINE}"/>']
    segw = (W - (n-1)*8)/n
    for i, (name, tag, col, desc, pts) in enumerate(ps):
        d = f"{i*T:.1f}s"
        # numero gigante de fondo
        nt = f'x="{W-18}" y="206" font-size="160" font-weight="900" text-anchor="end" class="orb"'
        b.append(f'<g class="s{i}" opacity="0" style="animation:num {CIC}s ease-out {d} infinite">'
                 f'<text {nt} fill="{col}" fill-opacity=".12" style="animation:late 2.2s ease-in-out infinite">0{i+1}</text>'
                 f'<text {nt} fill="none" stroke="{col}" stroke-opacity=".28" stroke-width="1.5" style="animation:fallo 3.1s steps(1) infinite">0{i+1}</text>'
                 f'<text {nt} fill="none" stroke="{col}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="90 420" filter="url(#g)" style="animation:traza 3.4s linear infinite">0{i+1}</text>'
                 f'</g>')
        b.append(f'<g class="s{i}" opacity="0" style="animation:pasa {CIC}s ease-out {d} infinite">')
        b.append(f'<rect x="0" y="62" width="5" height="170" rx="2.5" fill="{col}" filter="url(#g)"/>')
        b.append(t(26, 84, f"0{i+1} / 0{n}  ·  {tag}", DIM, 12.5, 700))
        b.append(f'<text x="24" y="132" fill="{col}" font-size="38" font-weight="900" letter-spacing="2" class="orb" filter="url(#g)">{e(name)}</text>')
        b.append(f'<rect x="26" y="146" width="{ancho_orb(name, 38, 2):.0f}" height="3" fill="{col}" style="transform-origin:26px 147px;animation:raya {CIC}s ease-out {d} infinite"/>')
        b.append(t(26, 178, " ".join(desc), TXT, 13.5) if len(" ".join(desc))*13.5*CW < W-40 else
                 t(26, 174, " ".join(desc[:len(desc)//2+len(desc)%2]), TXT, 13.5) + t(26, 194, " ".join(desc[len(desc)//2+len(desc)%2:]), TXT, 13.5))
        x = 26
        for pp in pts:
            wchip = len(pp)*12*CW + 24
            b.append(f'<rect x="{x:.1f}" y="210" width="{wchip:.1f}" height="26" rx="13" fill="{BG}" stroke="{col}" stroke-opacity=".8"/>' + t(f"{x+wchip/2:.1f}", 227.5, pp, TXT, 12, anchor="middle"))
            x += wchip + 10
        b.append('</g>')
        # barra de progreso
        sx = i*(segw+8); ini = i*p1; fin = (i+1)*p1
        css.append(f"@keyframes seg{i}{{0%,{ini:.2f}%{{transform:scaleX(0)}}{fin:.2f}%,99.5%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}")
        b.append(f'<rect x="{sx:.1f}" y="270" width="{segw:.1f}" height="4" rx="2" fill="{LINE}"/>'
                 f'<rect x="{sx:.1f}" y="270" width="{segw:.1f}" height="4" rx="2" fill="{col}" style="transform-origin:{sx:.1f}px 272px;transform:scaleX(0);animation:seg{i} {CIC}s linear infinite"/>')
        b.append(t(f"{sx+segw/2:.1f}", 292, name, DIM, 10.5, anchor="middle"))
    cuerpo = "\n".join(b)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img">
<defs><filter id="g" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>{ORB_CSS}
text{{font-family:{FONT}}}
.orb{{font-family:{ORB};font-weight:900}}
{chr(10).join(css)}</style>
{cuerpo}
</svg>"""

# ---------- estado actual ----------
def estado():
    cols = [("01", "FIN DE CARRERA", CYAN, "FixMyCity", ["App del ciudadano", "Panel de gestión municipal", "Motor de IA para reclamos"]),
            ("02", "5TO CICLO · TECSUP", MAG, "En aula", ["iOS con Swift", "Soluciones en la nube", "Web avanzado con Node.js"]),
            ("03", "OBJETIVO", GRN, "Prácticas", ["Desarrollo de software", "Backend · Full Stack", "Lima, Perú"])]
    cw = (W-44-28)/3; ch = 160; h = 62+ch+48
    b = [chrome("oscarjscom:~$ ./estado --actual")]
    for i, (n, head, col, title, items) in enumerate(cols):
        x = 22 + i*(cw+14); y = 62
        b.append(f'<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{ch}" rx="4" fill="{PANEL}" stroke="{LINE}"/>')
        b.append(t(f"{x+16:.1f}", y+26, f"[{n}]", col, 11.5, 700) + t(f"{x+52:.1f}", y+26, head, DIM, 10.5, 700))
        b.append(f'<circle cx="{x+cw-18:.1f}" cy="{y+22}" r="4" fill="{col}" filter="url(#glow)" style="animation:blink 1.6s {i*0.4}s ease-in-out infinite"/>')
        b.append(t(f"{x+16:.1f}", y+58, title, TXT, 19, 700))
        b.append(f'<line x1="{x+16:.1f}" y1="{y+70}" x2="{x+cw-16:.1f}" y2="{y+70}" stroke="{LINE}"/>')
        for j, it in enumerate(items):
            b.append(t(f"{x+16:.1f}", y+92+j*19, "›", col, 12, 700) + t(f"{x+32:.1f}", y+92+j*19, it, "#a9b6c4", 11.5))
    fy = h-20
    b.append(t(22, fy, "[", DIM, 12) + t(32, fy, "OK", GRN, 12, 700) + t(50, fy, "]", DIM, 12) + t(66, fy, "3 procesos activos · sin errores · café al 100%", DIM, 12))
    return svg(int(h), "\n".join(b))

# ---------- bitacora ----------
def bitacora():
    L = [("feat", "pfc", CYAN, "FixMyCity: plataforma de reclamos ciudadanos con IA", "HEAD -> main"),
         ("feat", "mobile", MAG, "apps iOS con Swift y diseño de interfaces en Flutter", None),
         ("feat", "cloud", YEL, "despliegues y servicios en la nube con AWS", None),
         ("feat", "hackathon", GRN, "ekECO: clasificador de residuos con IA · QuipuSoft 2026", None),
         ("feat", "iot", MAG, "NextCap: conteo de aforo con Arduino, ESP32-CAM y visor 3D", None),
         ("feat", "backend", CYAN, "microservicios con Spring Boot, Eureka y API Gateway", None),
         ("feat", "api", VIO, "APIs REST con Django REST Framework y Node.js", None),
         ("init", "carrera", RED, "primer commit en Ingeniería de Software · TECSUP", None)]
    lh = 27; h = 62 + len(L)*lh + 42
    b = [chrome("oscarjscom:~$ git log --oneline --graph")]
    gx = 40
    b.append(f'<line x1="{gx}" y1="76" x2="{gx}" y2="{76+(len(L)-1)*lh}" stroke="{LINE}" stroke-width="2"/>')
    for i, (typ, scope, col, msg, ref) in enumerate(L):
        y = 80 + i*lh; d = f"animation-delay:{0.2+i*0.15:.2f}s"
        b.append(f'<g class="in" style="{d}"><circle cx="{gx}" cy="{y-4}" r="5" fill="{BG}" stroke="{col}" stroke-width="2"/>')
        ref_t = f'<tspan fill="{YEL}" font-size="11.5" font-weight="700">  ({e(ref)})</tspan>' if ref else ""
        b.append(f'<text x="62" y="{y}" font-size="12.5" fill="{TXT}" xml:space="preserve"><tspan fill="{col}" font-weight="700">{typ}({scope}):</tspan> {e(msg)}{ref_t}</text>')
        b.append('</g>')
    b.append(t(22, h-18, "-- más commits en camino --", DIM, 11.5))
    return svg(int(h), "\n".join(b))

# ---------- lema rotativo ----------
def lema():
    frases = ["Backend con Spring Boot y Django", "Apps móviles nativas", "Del sensor a la nube", "Aprendo construyendo"]
    n = len(frases); dur = n*3
    css = f"@keyframes rot{{0%,{100/n-4:.1f}%{{opacity:1}}{100/n:.1f}%,100%{{opacity:0}}}}"
    b = []
    for i, f in enumerate(frases):
        b.append(f'<text x="{W/2}" y="34" fill="{TXT}" font-size="20" font-weight="700" text-anchor="middle" style="opacity:0;animation:rot {dur}s {i*3}s infinite">'
                 f'<tspan fill="{MAG}">&gt;_ </tspan>{e(f)}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 52" width="{W}" height="52" role="img"><style>text{{font-family:{FONT}}}{css}@media (prefers-reduced-motion:reduce){{text{{animation:none!important}}text:first-of-type{{opacity:1!important}}}}</style>{"".join(b)}</svg>'

# ---------- cabecera (sobria, con animacion suave) ----------
def cabecera():
    h = 224
    fs = 13.5
    chips = ["Backend", "Mobile", "IoT"]
    anchos = [len(c)*fs*CW + 30 for c in chips]
    lugar = "Lima, Peru"
    wl = len(lugar)*fs*CW + 22
    total = sum(anchos) + 10*len(chips) + 18 + wl
    x = (W - total)/2
    fila = []
    for c, wc in zip(chips, anchos):
        fila.append(f'<rect x="{x:.1f}" y="180" width="{wc:.1f}" height="28" rx="14" fill="{CYAN}" fill-opacity=".08" stroke="{CYAN}" stroke-opacity=".7" style="animation:chip 4.5s ease-in-out {len(fila)*1.5:.1f}s infinite"/>'
                    f'<text x="{x+wc/2:.1f}" y="198.5" fill="{TXT}" font-size="{fs}" text-anchor="middle">{c}</text>')
        x += wc + 10
    x += 8
    fila.append(f'<rect x="{x:.1f}" y="184" width="1" height="20" fill="{LINE}"/>')
    x += 18
    fila.append(f'<g style="animation:pin 2.4s ease-in-out infinite"><path transform="translate({x:.1f},185)" d="M7 0a7 7 0 0 1 7 7c0 5-7 12-7 12S0 12 0 7a7 7 0 0 1 7-7zm0 4.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5z" fill="{CYAN}" fill-rule="evenodd"/></g>'
                f'<text x="{x+22:.1f}" y="198.5" fill="{DIM}" font-size="{fs}">{lugar}</text>')
    sg = _json.loads((Path(__file__).resolve().parent / "spacegrotesk.json").read_text(encoding="utf-8"))
    sg_css = f"@font-face{{font-family:'SG';font-weight:700;src:url(data:font/woff2;base64,{sg['woff2_base64']}) format('woff2')}}"
    fsn = 92; lsn = 1
    nombre = "Oscar"
    wn = sum(sg["avances"][c] for c in nombre + ".")*fsn + lsn*len(nombre)
    xn = (W - wn)/2
    wpal = sum(sg["avances"][c] for c in nombre)*fsn + lsn*len(nombre)
    letras = (f'<text class="sg" x="{xn:.1f}" y="112" font-size="{fsn}" letter-spacing="{lsn}" fill="url(#luz)">{nombre}</text>'
              f'<text class="sg" x="{xn+wpal:.1f}" y="112" font-size="{fsn}" fill="{CYAN}">.</text>')
    punto = ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img">
<defs>
<pattern id="pts" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{CYAN}"/></pattern>
<linearGradient id="fi" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="fd" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".5"/></linearGradient>
<mask id="mi"><rect x="0" y="0" width="230" height="{h}" fill="url(#fi)"/></mask>
<mask id="md"><rect x="{W-230}" y="0" width="230" height="{h}" fill="url(#fd)"/></mask>
<linearGradient id="luz" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="260" y2="0"><stop offset="0" stop-color="{TXT}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{TXT}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-320 0;{W+60} 0;{W+60} 0" keyTimes="0;0.55;1" dur="5s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="li" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".8"/></linearGradient>
<linearGradient id="ld" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity=".8"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
</defs>
<style>{sg_css}
text{{font-family:{FONT}}}
.sg{{font-family:'SG',{FONT};font-weight:700}}
@keyframes raya{{0%{{transform:scaleX(0)}}45%,70%{{transform:scaleX(1)}}100%{{transform:scaleX(1);opacity:0}}}}
@keyframes chip{{0%,100%{{fill-opacity:.08;stroke-opacity:.7}}18%{{fill-opacity:.32;stroke-opacity:1}}36%{{fill-opacity:.08;stroke-opacity:.7}}}}
@keyframes pin{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}}
@keyframes linea{{0%,100%{{transform:scaleX(.35)}}50%{{transform:scaleX(1)}}}}
@keyframes deriva{{from{{transform:translateY(0)}}to{{transform:translateY(-18px)}}}}
@keyframes sube{{0%{{opacity:0;transform:translateY(6px)}}100%{{opacity:1;transform:translateY(0)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;opacity:1!important}}}}</style>
<g mask="url(#mi)"><rect x="0" y="0" width="230" height="{h+18}" fill="url(#pts)" style="animation:deriva 3s linear infinite"/></g>
<g mask="url(#md)"><rect x="{W-230}" y="0" width="230" height="{h+18}" fill="url(#pts)" style="animation:deriva 3s linear infinite"/></g>
<rect x="{W/2-190}" y="29" width="120" height="1.5" fill="url(#li)" style="transform-origin:{W/2-70}px 30px;animation:linea 4s ease-in-out infinite"/>
<rect x="{W/2+70}" y="29" width="120" height="1.5" fill="url(#ld)" style="transform-origin:{W/2+70}px 30px;animation:linea 4s ease-in-out infinite"/>
<text x="{W/2}" y="34" fill="{DIM}" font-size="13" letter-spacing="5" text-anchor="middle">HI, I'M</text>
{letras}
{punto}
<text x="{W/2}" y="158" font-size="16.5" letter-spacing="1.5" text-anchor="middle"><tspan fill="{TXT}">Software Engineering Student </tspan><tspan fill="{DIM}">@ </tspan><tspan fill="{CYAN}" font-weight="700">TECSUP</tspan></text>
{"".join(fila)}
</svg>"""

# ---------- botones ----------
def boton(etiqueta, valor):
    fs = 13; ls = 1.5; h = 40
    w1 = len(etiqueta)*(fs*CW+ls) + 30
    w2 = len(valor)*(fs*CW+ls) + 30
    w = w1 + w2
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h}" width="{w:.0f}" height="{h}" role="img">
<style>text{{font-family:{FONT}}}</style>
<rect x="1" y="1" width="{w-2:.0f}" height="{h-2}" rx="4" fill="{PANEL}" stroke="{CYAN}" stroke-width="1.5"/>
<path d="M5 1h{w1-5:.0f}v{h-2}H5a4 4 0 0 1-4-4V5a4 4 0 0 1 4-4z" fill="{CYAN}"/>
<text x="{w1/2:.1f}" y="25" fill="{BG}" font-size="{fs}" font-weight="700" letter-spacing="{ls}" text-anchor="middle">{e(etiqueta)}</text>
<text x="{w1+w2/2:.1f}" y="25" fill="{TXT}" font-size="{fs}" font-weight="700" letter-spacing="{ls}" text-anchor="middle">{e(valor)}</text>
</svg>"""

# ---------- titulos de seccion ----------
def titulo(num, texto):
    h = 54; fs = 22; ls = 3
    tw = len(texto)*(fs*CW+ls)
    x0 = 58
    xc = x0 + tw + 6
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img">
<defs><linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<filter id="g" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>text{{font-family:{FONT}}}@keyframes blink{{50%{{opacity:0}}}}@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<rect x="0" y="11" width="44" height="28" rx="3" fill="{CYAN}"/>
<text x="22" y="31" fill="{BG}" font-size="15" font-weight="700" text-anchor="middle">{num}</text>
<text x="{x0}" y="33" fill="{TXT}" font-size="{fs}" font-weight="700" letter-spacing="{ls}" filter="url(#g)" xml:space="preserve">{e(texto)}</text>
<rect x="{xc:.1f}" y="15" width="11" height="22" fill="{CYAN}" style="animation:blink 1s steps(1) infinite"/>
<rect x="{xc+26:.1f}" y="25" width="{W-xc-26:.1f}" height="2" fill="url(#fade)"/>
<rect x="0" y="45" width="{W}" height="1" fill="{LINE}"/>
</svg>"""

# ---------- subtitulos del stack ----------
def subtitulo(texto):
    h = 30; fs = 14; ls = 2
    tw = len(texto)*(fs*CW+ls)
    x0 = 30; xl = x0 + tw + 10
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img">
<style>text{{font-family:{FONT}}}
@keyframes pulso{{0%,100%{{opacity:1;transform:translateX(0)}}50%{{opacity:.35;transform:translateX(4px)}}}}
@keyframes corre{{to{{stroke-dashoffset:-28}}}}
@keyframes brillo{{0%,100%{{fill:{MAG}}}50%{{fill:{YEL}}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<text x="4" y="21" fill="{CYAN}" font-size="18" font-weight="700" style="animation:pulso 1.4s ease-in-out infinite">&gt;</text>
<text x="{x0}" y="20" font-size="{fs}" font-weight="700" letter-spacing="{ls}" style="animation:brillo 3s ease-in-out infinite" fill="{MAG}" xml:space="preserve">{e(texto)}</text>
<line x1="{xl:.1f}" y1="15" x2="{W-4}" y2="15" stroke="{CYAN}" stroke-opacity=".55" stroke-width="1.5" stroke-dasharray="2 12" style="animation:corre 1.2s linear infinite"/>
</svg>"""

# ---------- frase con cascada japonesa ----------
def frase():
    import random
    h = 230; CIC = 14
    rnd = random.Random(42)
    kana = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    jp = "「俺が必ず、お前を救ってみせる」"
    es = "\"I swear I'll save you.\""
    o = []
    # cascada: columnas de katakana con un destello que baja
    cols = 43; filas = 11; paso_x = W/cols; paso_y = 20
    for c in range(cols):
        x = paso_x*(c+0.5)
        fase = rnd.uniform(0, 2.4)
        dur = rnd.choice([1.9, 2.3, 2.7])
        for f in range(filas):
            o.append(f'<text x="{x:.1f}" y="{16+f*paso_y}" font-size="14" text-anchor="middle" fill="{CYAN}" opacity=".1" '
                     f'style="animation:cae {dur}s linear {fase+f*dur/filas/1.4:.2f}s infinite">{rnd.choice(kana)}</text>')
    lluvia = "\n".join(o)
    # traduccion letra por letra
    fs = 27; ancho = len(es)*fs*CW
    x0 = (W-ancho)/2 + fs*CW/2
    letras = "".join(
        f'<text x="{x0+i*fs*CW:.1f}" y="124" font-size="{fs}" font-weight="700" text-anchor="middle" fill="{TXT}" opacity="0" '
        f'style="animation:es {CIC}s linear {i*0.045:.3f}s infinite">{e(ch)}</text>'
        for i, ch in enumerate(es) if ch != " ")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img">
<defs><filter id="g" x="-10%" y="-60%" width="120%" height="220%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<radialGradient id="velo" cx="50%" cy="50%" r="60%"><stop offset="0" stop-color="{BG}" stop-opacity=".92"/><stop offset=".65" stop-color="{BG}" stop-opacity=".6"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient></defs>
<style>
text{{font-family:{FONT}}}
@keyframes cae{{0%{{opacity:1;fill:#eaffea}}12%{{opacity:.9;fill:{MAG}}}45%{{opacity:.4;fill:{CYAN}}}80%,100%{{opacity:.08;fill:{CYAN}}}}}
@keyframes lluvia{{0%,24%{{opacity:1}}34%,92%{{opacity:.28}}100%{{opacity:1}}}}
@keyframes velo{{0%,22%{{opacity:0}}32%,92%{{opacity:1}}100%{{opacity:0}}}}
@keyframes jp{{0%,24%{{opacity:0;letter-spacing:14px}}32%,50%{{opacity:1;letter-spacing:3px}}57%,100%{{opacity:0;letter-spacing:3px}}}}
@keyframes es{{0%,56%{{opacity:0;fill:{MAG}}}59%{{opacity:1;fill:#eaffea}}64%,91%{{opacity:1;fill:{TXT}}}96%,100%{{opacity:0;fill:{TXT}}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.fin{{opacity:1!important}}}}
</style>
<g style="animation:lluvia {CIC}s linear infinite">
{lluvia}
</g>
<rect x="0" y="0" width="{W}" height="{h}" fill="url(#velo)" opacity="0" style="animation:velo {CIC}s linear infinite"/>
<text x="{W/2}" y="124" font-size="34" font-weight="700" text-anchor="middle" fill="{CYAN}" filter="url(#g)" opacity="0" style="animation:jp {CIC}s ease-out infinite">{jp}</text>
<g filter="url(#g)">{letras}</g>
</svg>"""

# ---------- despedida: cascada -> japones -> traduccion, y "now playing" ----------
def despedida():
    import random
    hl = 0; h = hl + 70
    pares = [("「来てくれてありがとう」", "THANKS FOR STOPPING BY"),
             ("「バグはすべてセーブポイント」", "EVERY BUG IS A SAVE POINT"),
             ("「もう一度、もっと良く」", "START AGAIN, SHIP IT BETTER"),
             ("「次のコミットでまた会おう」", "SEE YOU IN THE NEXT COMMIT")]
    n = len(pares); T = 6.5; CIC = n*T; p1 = 100/n
    rnd = random.Random(77)
    kana = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    o = []
    cols = 43; filas = 10; px = W/cols; py = 20
    for c in range(cols):
        x = px*(c+0.5); fase = rnd.uniform(0, 2.4); dur = rnd.choice([1.9, 2.3, 2.7])
        for f in range(filas):
            o.append(f'<text x="{x:.1f}" y="{16+f*py}" font-size="14" text-anchor="middle" fill="{CYAN}" opacity=".1" '
                     f'style="animation:cae {dur}s linear {fase+f*dur/filas/1.4:.2f}s infinite">{rnd.choice(kana)}</text>')
    lluvia = "\n".join(o)
    textos = []
    fs = 25; ls = 4
    for i, (jp, en) in enumerate(pares):
        textos.append(f'<text x="{W/2}" y="60" font-size="32" font-weight="700" text-anchor="middle" fill="{CYAN}" filter="url(#g)" opacity="0" '
                      f'style="animation:jp {CIC}s ease-out {i*T:.1f}s infinite">{jp}</text>')
        tw = ancho_orb(en, fs, ls); x = (W - tw)/2
        for k, ch in enumerate(en):
            adv = _ORB["avances"].get(ch, 0.8)*fs + ls
            if ch != " ":
                textos.append(f'<text class="orb" x="{x:.1f}" y="60" font-size="{fs}" fill="{TXT}" opacity="0" '
                              f'style="animation:tr {CIC}s linear {i*T+k*0.04:.2f}s infinite">{e(ch)}</text>')
            x += adv
    cancion, artista = "A Little Death", "The Neighbourhood"
    bx = 6; by = hl + 42
    barras = "".join(
        f'<rect x="{bx+i*7:.1f}" y="{by-22}" width="4" height="22" rx="2" fill="{CYAN}" style="transform-origin:{bx+i*7+2:.1f}px {by}px;animation:eq {0.7+i*0.17:.2f}s ease-in-out {i*0.11:.2f}s infinite alternate"/>'
        for i in range(5))
    a1, a2, a3, a4 = p1*0.02, p1*0.10, p1*0.40, p1*0.47
    b1, b2, b3, b4 = p1*0.47, p1*0.51, p1*0.93, p1*0.98
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 370 {h}" width="370" height="{h}" role="img">
<defs>
<filter id="g" x="-10%" y="-60%" width="120%" height="220%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<radialGradient id="velo" cx="50%" cy="50%" r="60%"><stop offset="0" stop-color="{BG}" stop-opacity=".92"/><stop offset=".65" stop-color="{BG}" stop-opacity=".6"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient>
</defs>
<style>{ORB_CSS}
text{{font-family:{FONT}}}
.orb{{font-family:{ORB};font-weight:900}}
@keyframes cae{{0%{{opacity:1;fill:#eaffea}}12%{{opacity:.9;fill:{MAG}}}45%{{opacity:.4;fill:{CYAN}}}80%,100%{{opacity:.08;fill:{CYAN}}}}}
@keyframes lluvia{{0%,22%{{opacity:1}}32%,93%{{opacity:.28}}100%{{opacity:1}}}}
@keyframes velo{{0%,20%{{opacity:0}}30%,93%{{opacity:1}}100%{{opacity:0}}}}
@keyframes jp{{0%,{a1:.2f}%{{opacity:0;letter-spacing:14px}}{a2:.2f}%,{a3:.2f}%{{opacity:1;letter-spacing:3px}}{a4:.2f}%,100%{{opacity:0;letter-spacing:3px}}}}
@keyframes tr{{0%,{b1:.2f}%{{opacity:0;fill:{MAG}}}{b2:.2f}%{{opacity:1;fill:#eaffea}}{p1*0.58:.2f}%,{b3:.2f}%{{opacity:1;fill:{TXT}}}{b4:.2f}%,100%{{opacity:0;fill:{TXT}}}}}
@keyframes eq{{from{{transform:scaleY(.25)}}to{{transform:scaleY(1)}}}}
@keyframes avanza{{from{{width:0}}to{{width:300px}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
{barras}
<text class="orb" x="{bx+48:.1f}" y="{by-11}" font-size="10" letter-spacing="2" fill="{MAG}">NOW PLAYING</text>
<text x="{bx+48:.1f}" y="{by+4}" font-size="13.5" fill="{TXT}">{cancion} <tspan fill="{DIM}">· {artista}</tspan></text>
<rect x="{bx+48:.1f}" y="{by+14}" width="300" height="3" rx="1.5" fill="{LINE}"/>
<rect x="{bx+48:.1f}" y="{by+14}" width="0" height="3" rx="1.5" fill="{CYAN}" style="animation:avanza 210s linear infinite"/>
</svg>"""

# ---------- marco del contador de visitas ----------
def visitas_izq():
    w, h = 250, 44
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">
<style>{ORB_CSS}
.orb{{font-family:{ORB};font-weight:900}}
@keyframes pulso{{0%{{r:4px;opacity:1}}100%{{r:13px;opacity:0}}}}
@keyframes flecha{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(5px)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<path d="M14 4H4v36h10" fill="none" stroke="{CYAN}" stroke-width="3"/>
<circle cx="30" cy="22" r="4" fill="none" stroke="{CYAN}" stroke-width="1.5" style="animation:pulso 1.6s ease-out infinite"/>
<circle cx="30" cy="22" r="4" fill="{CYAN}"/>
<text class="orb" x="46" y="28" font-size="15" letter-spacing="2.5" fill="{TXT}">PROFILE VIEWS</text>
<text x="226" y="29" font-size="18" fill="{MAG}" font-family="{FONT}" style="animation:flecha 1.2s ease-in-out infinite">&gt;</text>
</svg>"""

def visitas_der():
    w, h = 40, 44
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">
<style>@keyframes blink{{50%{{opacity:0}}}}@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<rect x="4" y="11" width="9" height="22" fill="{CYAN}" style="animation:blink 1s steps(1) infinite"/>
<path d="M26 4h10v36H26" fill="none" stroke="{CYAN}" stroke-width="3"/>
</svg>"""

for name, fn in [("about", about), ("proyectos-carrusel3", proyectos)]:
    (OUT / f"{name}.v8.svg").write_text(fn(), encoding="utf-8")
    print("ok", name)

for i, (name, texto) in enumerate([("titulo-about", "ABOUT ME"), ("titulo-stack", "TECH STACK"), ("titulo-stats", "GITHUB STATS"), ("titulo-proyectos", "PROJECTS")], 1):
    (OUT / f"{name}.v8.svg").write_text(titulo(f"{i:02d}", texto), encoding="utf-8")
    print("ok", name)

(OUT / "cabecera-sobria5.v8.svg").write_text(cabecera(), encoding="utf-8"); print("ok cabecera")
for name, et, val in [("boton-github", "GITHUB", "oscarjscom"), ("boton-repos", "REPOS", "view projects")]:
    (OUT / f"{name}.v8.svg").write_text(boton(et, val), encoding="utf-8"); print("ok", name)

for name, texto in [("sub-lenguajes", "languages/"), ("sub-frameworks", "libraries_and_frameworks/"), ("sub-herramientas", "tools_and_platforms/"), ("sub-datos", "databases/")]:
    (OUT / f"{name}.v8.svg").write_text(subtitulo(texto), encoding="utf-8"); print("ok", name)

(OUT / "frase.v8.svg").write_text(frase(), encoding="utf-8"); print("ok frase")

(OUT / "reproductor-lado.v8.svg").write_text(despedida(), encoding="utf-8"); print("ok despedida")

