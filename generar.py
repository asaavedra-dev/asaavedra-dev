"""Genera perfil.svg (estilo neofetch) con datos de GitHub actualizados."""
import json, os, urllib.request
from xml.sax.saxutils import escape

USUARIO = "asaavedra-dev"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

# ---------- Datos de GitHub ----------
def api(url, data=None):
    h = {"User-Agent": USUARIO, "Accept": "application/vnd.github+json"}
    if TOKEN:
        h["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def stats():
    s = {"repos": "N/A", "stars": "N/A", "followers": "N/A", "contrib": "N/A"}
    try:
        u = api(f"https://api.github.com/users/{USUARIO}")
        s["repos"], s["followers"] = u["public_repos"], u["followers"]
        repos = api(f"https://api.github.com/users/{USUARIO}/repos?per_page=100")
        s["stars"] = sum(r["stargazers_count"] for r in repos)
        if TOKEN:
            q = {"query": f'{{user(login:"{USUARIO}"){{contributionsCollection{{contributionCalendar{{totalContributions}}}}}}}}'}
            g = api("https://api.github.com/graphql", json.dumps(q).encode())
            s["contrib"] = g["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    except Exception as e:
        print("No se pudieron leer las estadísticas:", e)
    return s

# ---------- Arte ASCII ----------
# El dibujo está en arte.txt: puedes reemplazarlo por cualquier otro ASCII.
def arte():
    with open("arte.txt", encoding="utf-8") as f:
        return f.read().rstrip("\n").split("\n")

# ---------- SVG ----------
VERDE, GRIS, CLARO, TENUE = "#3fb950", "#8b949e", "#c9d1d9", "#484f58"

def svg(s):
    info = [
        ("titulo", f"{USUARIO}@github"),
        ("linea", ""),
        ("OS", "Arch Linux + Hyprland"),
        ("Host", "Instituto Tecnológico de Cuautla  TecNM"),
        ("Rol", "Estudiante de Ing. en Sistemas Computacionales"),
        ("Enfoque", "desarrollo web & ciberseguridad"),
        ("", ""),
        ("Lenguajes", "C++, Python, Java , JavaScript"),
        ("Stack.Web", "HTML, CSS, JavaScript"),
        ("Stack.Móvil", "Android Studio, Kotlin"),
        ("Stack.3D", "Blender, Godot 4"),
        ("Hardware", "ESP32, M5Stack Cardputer, Arduino"),
        ("Intereses", "ciberseguridad, OSINT, gamedev"),
        ("", ""),
        ("seccion", "GitHub Stats"),
        ("Repos", f"{s['repos']}   Stars: {s['stars']}"),
        ("Followers", f"{s['followers']}   Contribuciones: {s['contrib']}"),
    ]
    W, H, LH = 960, 470, 20
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Consolas, \'DejaVu Sans Mono\', \'Courier New\', monospace" font-size="14">',
           f'<rect width="{W}" height="{H}" rx="12" fill="#0d1117" stroke="#30363d"/>']
    # arte
    for i, f in enumerate(arte()):
        out.append(f'<text x="24" y="{40 + i*12}" fill="{VERDE}" xml:space="preserve" font-size="10">{escape(f)}</text>')
    # info
    x, y = 400, 48
    for k, v in info:
        if k == "titulo":
            out.append(f'<text x="{x}" y="{y}" fill="{VERDE}" font-weight="bold" font-size="16">{escape(v)}</text>')
        elif k == "linea":
            out.append(f'<line x1="{x}" y1="{y-8}" x2="{x+300}" y2="{y-8}" stroke="{VERDE}"/>')
        elif k == "seccion":
            out.append(f'<text x="{x}" y="{y}" fill="{GRIS}">— {escape(v)} ———————————————</text>')
        elif k:
            out.append(f'<text x="{x}" y="{y}"><tspan fill="{VERDE}" font-weight="bold">{escape(k)}:</tspan> <tspan fill="{CLARO}">{escape(str(v))}</tspan></text>')
        y += LH
    
    # prompt
    py = H - 40
    out.append(f'<text x="30" y="{py}" fill="{VERDE}" xml:space="preserve">┌──({escape(USUARIO)}@github)-[~]</text>')
    out.append(f'<text x="30" y="{py+20}" fill="{VERDE}" xml:space="preserve">└─$ <tspan fill="{CLARO}">whoami</tspan><tspan fill="{GRIS}">  # sistemas · web · ciberseguridad</tspan></text>')
    out.append('</svg>')
    return "\n".join(out)

if __name__ == "__main__":
    with open("perfil.svg", "w", encoding="utf-8") as f:
        f.write(svg(stats()))
    print("perfil.svg generado")
