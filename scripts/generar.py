"""Genera los SVG del perfil. Uso: python scripts/generar.py"""
from pathlib import Path
from html import escape as e
import math

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)
W = 860
BG, PANEL, LINE = "#090c10", "#10161d", "#25303c"
CYAN, MAG, YEL, VIO, TXT, DIM = "#3b9dff", "#ff8a1f", "#ffc53d", "#8aa4bf", "#dbe4ee", "#6f7d8c"
GRN, RED = "#39d353", "#ff5a36"
FONT = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
CW = 0.602  # ancho de caracter monoespaciado relativo al tamano

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
    L = [("perfil:", None), ("  nombre", "Oscar Olano Paniora"), ("  rol", "Estudiante de Ing. de Software"),
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

# ---------- whoami ----------
def whoami():
    h = 250
    b = [chrome("oscarjscom · shell · online")]
    x, y, w, hh = 22, 62, 548, 166
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="4" fill="{PANEL}" stroke="{VIO}" stroke-opacity=".7"/>')
    b.append(t(x+18, y+28, "❯", CYAN, 14, 700) + t(x+38, y+28, "whoami", CYAN, 14, 700))
    b.append(t(x+18, y+52, "oscar_olano", TXT, 13) + t(x+120, y+52, "—", DIM, 13) + t(x+142, y+52, "Desarrollador Full Stack en formación", YEL, 13, 700))
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
    ps = [("FixMyCity", "proyecto de fin de carrera", CYAN,
           ["Plataforma de reclamos y", "seguimiento ciudadano para", "municipalidades del Perú,", "asistida por IA."],
           ["App ciudadana", "Panel municipal", "Motor de IA"]),
          ("NextCap", "IoT · conteo de aforo", MAG,
           ["Sistema de conteo de personas", "de doble carril con barreras,", "backend en tiempo real y", "visor 3D interactivo."],
           ["Arduino · ESP32-CAM", "Node.js · WebSocket", "Three.js"]),
          ("ekECO", "hackathon QuipuSoft 2026", GRN,
           ["Clasificador de residuos con", "IA sobre una arquitectura", "serverless en AWS."],
           ["AWS serverless", "IA generativa", "Trabajo en equipo"]),
          ("Microservicios", "arquitectura backend", YEL,
           ["Arquitectura de microservicios", "con descubrimiento, puerta de", "enlace y tolerancia a fallos."],
           ["Spring Boot", "Eureka · API Gateway", "Resilience4j"]),
          ("TravelMate", "chatbot de viajes", VIO,
           ["Chatbot para una plataforma", "de viajes con integración", "de OpenAI."],
           ["Laravel", "OpenAI API", "Chatbot"]),
          ("JARVIS offline", "asistente de voz", RED,
           ["Asistente de voz estilo JARVIS", "que funciona sin conexión,", "directo en el navegador."],
           ["HTML · JavaScript", "Web Speech API", "Sin conexión"])]
    cw = (W-44-28)/3; ch = 222; h = 62 + 2*ch + 14 + 22
    b = [chrome("oscarjscom:~$ ls -la proyectos/")]
    for i, (name, tag, col, desc, pts) in enumerate(ps):
        x = 22 + (i % 3)*(cw+14); y = 62 + (i//3)*(ch+14)
        b.append(f'<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{ch}" rx="4" fill="{PANEL}" stroke="{LINE}"/>')
        b.append(f'<rect x="{x:.1f}" y="{y}" width="4" height="{ch}" fill="{col}"/>')
        b.append(t(f"{x+cw-14:.1f}", y+30, f"0{i+1}", LINE, 22, 700, "end"))
        b.append(t(f"{x+18:.1f}", y+32, name, col, 16.5, 700) + t(f"{x+18:.1f}", y+50, "# "+tag, DIM, 10.5))
        for j, d in enumerate(desc):
            b.append(t(f"{x+18:.1f}", y+76+j*16, d, TXT, 11.2))
        for j, pp in enumerate(pts):
            yy = y+156+j*20
            b.append(t(f"{x+18:.1f}", yy, "▸", col, 11) + t(f"{x+34:.1f}", yy, pp, "#a9b6c4", 11))
    return svg(int(h), "\n".join(b))

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

for name, fn in [("hero", hero), ("lema", lema), ("whoami", whoami), ("estado", estado), ("stack", stack), ("proyectos", proyectos), ("bitacora", bitacora)]:
    (OUT / f"{name}.v2.svg").write_text(fn(), encoding="utf-8")
    print("ok", name)
