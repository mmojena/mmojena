"""Gera os SVGs animados do README (tema claro e escuro).

Uso: python3 scripts/build_assets.py
Fontes: assets/previews/*.jpg (prévias reais dos projetos). Saída: assets/*.svg
As animações ficam em CSS dentro de cada SVG, porque o GitHub exibe SVG via <img>
(sem JS). Todo elemento animado tem como estado base o quadro final, então
prefers-reduced-motion apenas desliga as animações.
"""
import base64
import random
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

THEMES = {
    "dark": dict(bg="#0E1314", panel="#111719", chrome="#161E1F", line="#273130", grid="#1B2324",
                 ink="#F2F4EF", mute="#9DABA5", accent="#B8FF2C", accent_ink="#B8FF2C", cut="#111719",
                 phone="#070A0B", glow=".10"),
    "light": dict(bg="#F4F6F1", panel="#FFFFFF", chrome="#EEF1EA", line="#D5DBD2", grid="#E4E9E0",
                  ink="#111719", mute="#56625D", accent="#B8FF2C", accent_ink="#3F5F00", cut="#F4F6F1",
                  phone="#111719", glow=".35"),
}

SANS = "'Inter','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
BASE_CSS = f"""
text{{font-family:{SANS}}}
.mono{{font-family:{MONO}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""

M_PATH = "M0 0h24l26 28L76 0h24v100H76V38L50 66 24 38v62H0z"
M_CUT = "M0 0h10l90 90v10H90L0 10z"


def jpeg_size(data):
    i = 2
    while i < len(data):
        marker, length = data[i + 1], struct.unpack(">H", data[i + 2:i + 4])[0]
        if 0xC0 <= marker <= 0xC3:
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + length
    raise ValueError("JPEG sem SOF")


def image(name):
    data = (ASSETS / "previews" / f"{name}.jpg").read_bytes()
    w, h = jpeg_size(data)
    return "data:image/jpeg;base64," + base64.b64encode(data).decode(), w, h


def svg(w, h, title, desc, css, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-labelledby="t d">
<title id="t">{title}</title>
<desc id="d">{desc}</desc>
<style>{BASE_CSS}{css}</style>
{body}
</svg>
"""


def hero(t):
    rnd = random.Random(7)  # partículas determinísticas: o SVG não muda a cada build
    dots = "".join(
        f'<circle class="pt" cx="{rnd.uniform(740, 1180):.0f}" cy="600" r="{rnd.choice((1.5, 2, 2.5, 3))}" '
        f'fill="{t["accent"] if i % 3 else t["mute"]}" '
        f'style="animation-duration:{rnd.uniform(7, 13):.1f}s;animation-delay:-{rnd.uniform(0, 13):.1f}s"/>'
        for i in range(22))
    css = """
.up{animation:up 1s cubic-bezier(.2,.7,.2,1) both}
@keyframes up{from{opacity:0;transform:translateY(30px)}}
.show{animation:show .01s linear both}
@keyframes show{from{opacity:0}}
.bar{transform-box:fill-box;transform:scaleX(0);animation:bar 1s cubic-bezier(.7,0,.2,1) both}
@keyframes bar{0%{transform:scaleX(0);transform-origin:left}45%{transform:scaleX(1);transform-origin:left}55%{transform:scaleX(1);transform-origin:right}100%{transform:scaleX(0);transform-origin:right}}
.gridin{animation:gridin 1.6s ease-out both}
@keyframes gridin{from{opacity:0;transform:scale(1.06)}}
.gridrun{animation:gridrun 10s linear infinite}
@keyframes gridrun{to{transform:translate(40px,40px)}}
.draw{stroke-dasharray:1;animation:draw 2s cubic-bezier(.6,0,.2,1) both}
@keyframes draw{from{stroke-dashoffset:1}}
.outline{stroke-dasharray:1;animation:draw 1.8s cubic-bezier(.65,0,.35,1) .1s both,fadeline .8s ease 1.9s both}
@keyframes fadeline{to{stroke-opacity:.0}}
.fill{animation:fill .9s ease 1.4s both}
@keyframes fill{from{opacity:0}}
.slash{stroke-dasharray:1;animation:slash .9s cubic-bezier(.7,0,.2,1) 1.9s both}
@keyframes slash{0%{stroke-dashoffset:1;opacity:1}60%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}
.cut{animation:cut .8s cubic-bezier(.7,0,.2,1) 2.2s both}
@keyframes cut{from{transform:translate(-120px,-120px)}}
.sq{transform-box:fill-box;transform-origin:center;animation:drop .9s cubic-bezier(.3,1.7,.5,1) 2.5s both,beat 3s ease-in-out 3.6s infinite}
@keyframes drop{from{opacity:0;transform:translateY(-60px) rotate(-90deg) scale(.2)}}
@keyframes beat{50%{transform:scale(.8)}}
.wave{transform-box:fill-box;transform-origin:center;opacity:0;animation:wave 3s cubic-bezier(.2,.6,.3,1) 2.9s infinite}
@keyframes wave{0%{opacity:.9;transform:scale(1)}100%{opacity:0;transform:scale(7)}}
.sweep{animation:sweep 5s cubic-bezier(.5,0,.3,1) 3.2s infinite}
@keyframes sweep{0%{transform:translateX(-80px)}40%,100%{transform:translateX(220px)}}
.float{animation:float 8s ease-in-out 3s infinite}
@keyframes float{50%{transform:translateY(-8px)}}
.drift{animation:drift 8s ease-in-out 3s infinite}
@keyframes drift{50%{transform:translate(6px,5px)}}
.spin{transform-origin:960px 300px;animation:spin 18s linear infinite}
.spinr{transform-origin:960px 300px;animation:spin 30s linear infinite reverse}
.spinf{transform-origin:960px 300px;animation:spin 9s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.pt{opacity:.5;animation:rise linear infinite}
@keyframes rise{0%{opacity:0;transform:translateY(0)}15%{opacity:.9}85%{opacity:.6}100%{opacity:0;transform:translateY(-560px)}}
.scan{opacity:0;animation:scan 7s linear 3s infinite}
@keyframes scan{0%{opacity:0;transform:translateY(0)}8%{opacity:1}35%{opacity:1;transform:translateY(620px)}36%,100%{opacity:0;transform:translateY(620px)}}
.glow{animation:glow 5s ease-in-out infinite}
@keyframes glow{50%{opacity:.4}}
.w{opacity:0;animation:word 9s ease both infinite}
.w1{opacity:1}
@keyframes word{0%{opacity:0;transform:translateY(16px)}5%,30%{opacity:1;transform:none}35%,100%{opacity:0;transform:translateY(-16px)}}
.ping{transform-box:fill-box;transform-origin:center;animation:ping 2s ease-out infinite}
@keyframes ping{from{opacity:.9;transform:scale(1)}to{opacity:0;transform:scale(3.2)}}
.nudge{animation:nudge 2.4s ease-in-out 2.5s infinite}
@keyframes nudge{50%{transform:translate(5px,-5px)}}
"""
    words = ["Sites institucionais.", "Landing pages.", "Produtos digitais."]
    cycle = "".join(
        f'<text class="w{" w1" if i == 0 else ""}" style="animation-delay:{2.2 + i * 3}s" x="52" y="436" font-size="24" fill="{t["mute"]}">{w}</text>'
        for i, w in enumerate(words))

    def line(y, delay, content, width):
        return (f'<text class="show" style="animation-delay:{delay + .45}s" x="46" y="{y}" font-size="108" font-weight="700" letter-spacing="-5" fill="{t["ink"]}">{content}</text>'
                f'<rect class="bar" style="animation-delay:{delay}s" x="44" y="{y - 86}" width="{width}" height="100" fill="{t["accent"]}"/>')

    body = f"""<defs>
<pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" stroke="{t['grid']}"/></pattern>
<radialGradient id="fade" cx="960" cy="300" r="440" gradientUnits="userSpaceOnUse"><stop stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="gm"><rect width="1200" height="620" fill="url(#fade)"/></mask>
<radialGradient id="lime" cx="960" cy="300" r="270" gradientUnits="userSpaceOnUse"><stop stop-color="{t['accent']}" stop-opacity="{t['glow']}"/><stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/></radialGradient>
<linearGradient id="sw" x1="0" x2="1"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="sl" x1="720" x2="1200" gradientUnits="userSpaceOnUse"><stop stop-color="{t['accent']}" stop-opacity="0"/><stop offset=".5" stop-color="{t['accent']}"/><stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/></linearGradient>
<clipPath id="card"><rect width="1200" height="620" rx="20"/></clipPath>
<clipPath id="mb"><rect width="100" height="100"/></clipPath>
<clipPath id="ms"><path d="{M_PATH}"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="1200" height="620" fill="{t['bg']}"/>
<g mask="url(#gm)"><g class="gridin"><rect class="gridrun" x="-40" y="-40" width="1280" height="700" fill="url(#g)"/></g></g>
<circle class="glow" cx="960" cy="300" r="270" fill="url(#lime)"/>
<g>{dots}</g>
<rect class="scan" x="720" y="-2" width="480" height="2" fill="url(#sl)"/>
</g>
<rect x=".5" y=".5" width="1199" height="619" rx="19.5" stroke="{t['line']}"/>

<g class="up" style="animation-delay:.1s">
<rect x="52" y="58" width="10" height="10" fill="{t['accent']}"/>
<text class="mono" x="76" y="68" font-size="17" fill="{t['mute']}">mmojena / criador e fundador</text>
</g>
{line(214, .25, "Miguel", 350)}
{line(318, .5, f'Mojena<tspan fill="{t["accent_ink"]}">.</tspan>', 420)}
<text class="up" style="animation-delay:1.1s" x="52" y="386" font-size="34" letter-spacing="-.6" fill="{t['ink']}">Ideias que ganham forma.</text>
{cycle}
<path class="draw" pathLength="1" d="M52 490H660" stroke="{t['line']}" style="animation-delay:1.2s"/>
<g class="up" style="animation-delay:1.5s">
<circle cx="60" cy="535" r="5" fill="{t['accent']}"/><circle class="ping" cx="60" cy="535" r="5" fill="{t['accent']}"/>
<text class="mono" x="78" y="541" font-size="16" fill="{t['mute']}">disponível para novos projetos</text>
<text x="660" y="541" font-size="18" font-weight="600" text-anchor="end" fill="{t['accent_ink']}">Conheça meu trabalho <tspan class="nudge">↗</tspan></text>
</g>

<g class="drift"><g stroke="{t['line']}" stroke-width="1.2">
<path class="draw" pathLength="1" d="M790 0V620M1130 0V620" style="animation-delay:.2s"/>
<path class="draw" pathLength="1" d="M720 130H1200M720 470H1200" style="animation-delay:.35s"/>
<path class="draw" pathLength="1" d="M800 140L1120 460M800 460L1120 140" style="animation-delay:.5s"/>
<circle class="draw" pathLength="1" cx="960" cy="300" r="200" transform="rotate(-90 960 300)" style="animation-delay:.3s"/>
</g>
<g class="spinr"><circle cx="960" cy="300" r="250" stroke="{t['line']}" stroke-dasharray="2 10" opacity=".9"/><circle cx="960" cy="550" r="3.5" fill="{t['mute']}"/><circle cx="710" cy="300" r="2.5" fill="{t['mute']}"/></g>
<g stroke="{t['mute']}" class="up" style="animation-delay:1s"><path d="M946 86H974M960 72V100M946 514H974M960 500V528"/></g>
<circle cx="790" cy="130" r="4" fill="{t['accent']}" class="up" style="animation-delay:1.4s"/>
<circle cx="1130" cy="470" r="4" fill="{t['accent']}" class="up" style="animation-delay:1.5s"/>
</g>
<g class="spin"><circle cx="960" cy="100" r="5" fill="{t['accent']}"/><circle cx="960" cy="100" r="13" stroke="{t['accent']}" opacity=".45"/></g>
<g class="spinf"><path d="M960 125A175 175 0 0 1 1111 213" stroke="{t['accent']}" stroke-width="2" stroke-linecap="round" opacity=".7"/></g>

<g class="float"><g transform="translate(820 160) scale(2.8)">
<path class="outline" pathLength="1" d="{M_PATH}" stroke="{t['accent']}" stroke-width="2" vector-effect="non-scaling-stroke" stroke-linejoin="round"/>
<path class="fill" d="{M_PATH}" fill="{t['ink']}"/>
<g clip-path="url(#mb)"><path class="cut" d="{M_CUT}" fill="{t['cut']}"/></g>
<path class="slash" pathLength="1" d="M0 0L100 100" stroke="{t['accent']}" stroke-width="3" vector-effect="non-scaling-stroke"/>
<g clip-path="url(#ms)"><g transform="skewX(-20)"><rect class="sweep" x="-40" y="-10" width="36" height="120" fill="url(#sw)"/></g></g>
<rect class="wave" x="80" y="80" width="20" height="20" stroke="{t['accent']}" stroke-width="1.5" vector-effect="non-scaling-stroke"/>
<rect class="sq" x="80" y="80" width="20" height="20" fill="{t['accent']}"/>
</g></g>
"""
    return svg(1200, 620, "Miguel Mojena — criador e fundador",
               "Ideias que ganham forma. Sites institucionais, landing pages e produtos digitais. "
               "Monograma M que se desenha em traços e ganha preenchimento, com órbitas e partículas em movimento.", css, body)


def marquee(t):
    items = ["SITES INSTITUCIONAIS", "LANDING PAGES", "PRODUTOS DIGITAIS", "HTML", "CSS",
             "JAVASCRIPT", "TYPESCRIPT", "PYTHON"]
    fs, ch, gap = 18, 18 * 0.6, 56  # fonte mono: largura de cada caractere é ~0.6em
    parts, x = [], 0.0
    for it in items:
        parts.append(f'<text class="mono" x="{x:.1f}" y="49" font-size="{fs}" letter-spacing="0" fill="{t["ink"]}">{it}</text>')
        x += len(it) * ch + gap / 2
        parts.append(f'<rect x="{x - 5:.1f}" y="38" width="8" height="8" transform="rotate(45 {x - 1:.1f} 42)" fill="{t["accent"]}"/>')
        x += gap / 2
    period = x
    reps = int(1200 // period) + 2
    track = "".join(f'<g transform="translate({period * i:.1f} 0)">{"".join(parts)}</g>' for i in range(reps))
    css = f".track{{animation:run {period / 40:.1f}s linear infinite}}@keyframes run{{to{{transform:translateX(-{period:.1f}px)}}}}"
    body = f"""<defs><clipPath id="c"><rect width="1200" height="84" rx="14"/></clipPath>
<linearGradient id="e" x1="0" x2="1200" gradientUnits="userSpaceOnUse"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".08" stop-color="#fff"/><stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="m"><rect width="1200" height="84" fill="url(#e)"/></mask></defs>
<g clip-path="url(#c)"><rect width="1200" height="84" fill="{t['bg']}"/>
<g mask="url(#m)"><g class="track" transform="translate(24 0)">{track}</g></g></g>
<rect x=".5" y=".5" width="1199" height="83" rx="13.5" stroke="{t['line']}"/>"""
    return svg(1200, 84, "O que eu faço", "Sites institucionais, landing pages e produtos digitais. "
               "HTML, CSS, JavaScript, TypeScript e Python.", css, body)


PROJECTS = [
    dict(slug="locus", title="Locus", kind="PRODUTO DIGITAL · MERCADO IMOBILIÁRIO", domain="locusmt.tech",
         desc="Plataforma para encontrar imóveis em Mato Grosso: compra, aluguel e temporada."),
    dict(slug="silome", title="Silomé", kind="EXPERIÊNCIA DIGITAL · JOIAS", domain="silome.vercel.app",
         desc="O universo de uma marca de joias em sete capítulos, da pedra bruta à peça pronta."),
    dict(slug="antonia-mojena", title="Antônia Mojena", kind="SITE INSTITUCIONAL · NEUROPSICOPEDAGOGIA",
         domain="vortexcorp1.github.io/AntoniaMojena",
         desc="Serviços, orientações sobre os atendimentos e agendamento pelo WhatsApp."),
    dict(slug="ana-stradiotto", title="Ana Stradiotto", kind="SITE INSTITUCIONAL · MARKETING",
         domain="ana-stradiotto.vercel.app",
         desc="Assessoria de marketing e posicionamento, com serviços, projetos e contato."),
]


def card(t, p, n):
    src, iw, ih = image(p["slug"])
    sx, sy, sw, sh = 56, 250, 1088, 380
    h = sw * ih / iw
    pan = max(h - sh, 0)
    mobile = ASSETS / "previews" / f"{p['slug']}-mobile.jpg"
    css = f"""
.in{{animation:in 1s cubic-bezier(.2,.7,.2,1) both}}
@keyframes in{{from{{opacity:0;transform:translateY(28px)}}}}
.pan{{animation:pan 14s ease-in-out 1.5s infinite alternate}}
@keyframes pan{{0%,12%{{transform:none}}88%,100%{{transform:translateY(-{pan:.0f}px)}}}}
.shine{{animation:shine 7s ease-in-out 2s infinite}}
@keyframes shine{{0%{{transform:translateX(-500px)}}30%,100%{{transform:translateX(1500px)}}}}
.float{{animation:float 6s ease-in-out infinite}}
@keyframes float{{50%{{transform:translateY(-10px)}}}}
.ppan{{animation:ppan 11s ease-in-out 2.5s infinite alternate}}
.nudge{{animation:nudge 2.4s ease-in-out 1.5s infinite}}
@keyframes nudge{{50%{{transform:translate(4px,-4px)}}}}
"""
    phone = ""
    if mobile.exists():
        msrc, mw, mh = image(p["slug"] + "-mobile")
        px, py, pw, ph = 926, 206, 190, 390
        scw, sch = pw - 16, ph - 16
        mhh = scw * mh / mw
        mpan = max(mhh - sch, 0)
        css += f"@keyframes ppan{{0%,15%{{transform:none}}85%,100%{{transform:translateY(-{mpan:.0f}px)}}}}"
        fit = 'preserveAspectRatio="xMidYMin meet"' if mpan else 'preserveAspectRatio="xMinYMid slice"'
        himg = mhh if mpan else sch
        phone = f"""<g class="in" style="animation-delay:.5s"><g class="float">
<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="30" fill="{t['phone']}" stroke="{t['line']}" filter="url(#sh)"/>
<g clip-path="url(#ps)"><g class="{'ppan' if mpan else ''}"><image href="{msrc}" x="{px + 8}" y="{py + 8}" width="{scw}" height="{himg:.0f}" {fit}/></g></g>
<rect x="{px + pw / 2 - 30}" y="{py + 16}" width="60" height="16" rx="8" fill="{t['phone']}"/>
</g></g>"""
        clip_phone = f'<clipPath id="ps"><rect x="{px + 8}" y="{py + 8}" width="{scw}" height="{sch}" rx="22"/></clipPath>'
    else:
        clip_phone = ""
    body = f"""<defs>
<clipPath id="sc"><path d="M{sx} {sy}H{sx + sw}V{sy + sh - 14}Q{sx + sw} {sy + sh} {sx + sw - 14} {sy + sh}H{sx + 14}Q{sx} {sy + sh} {sx} {sy + sh - 14}Z"/></clipPath>
{clip_phone}
<linearGradient id="sg" x1="0" x2="1"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".18"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="vg" x1="0" y1="{sy}" x2="0" y2="{sy + sh}" gradientUnits="userSpaceOnUse"><stop offset=".7" stop-color="{t['panel']}" stop-opacity="0"/><stop offset="1" stop-color="{t['panel']}" stop-opacity=".55"/></linearGradient>
<filter id="sh" x="-30%" y="-20%" width="160%" height="140%"><feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#000" flood-opacity=".35"/></filter>
</defs>
<rect x=".5" y=".5" width="1199" height="679" rx="23.5" fill="{t['panel']}" stroke="{t['line']}"/>
<g class="in">
<text class="mono" x="56" y="74" font-size="18" fill="{t['accent_ink']}">{n:02d}<tspan fill="{t['mute']}"> / {len(PROJECTS):02d}   {p['kind']}</tspan></text>
<text x="1144" y="74" font-size="18" font-weight="600" text-anchor="end" fill="{t['accent_ink']}">Ver projeto <tspan class="nudge">↗</tspan></text>
<text x="50" y="174" font-size="84" font-weight="700" letter-spacing="-3.5" fill="{t['ink']}">{p['title']}<tspan fill="{t['accent_ink']}">.</tspan></text>
</g>
<g class="in" style="animation-delay:.2s">
<rect x="{sx}" y="210" width="{sw}" height="{sh + 40}" rx="14" fill="{t['chrome']}" stroke="{t['line']}"/>
<circle cx="80" cy="230" r="5.5" fill="{t['line']}"/><circle cx="99" cy="230" r="5.5" fill="{t['line']}"/><circle cx="118" cy="230" r="5.5" fill="{t['line']}"/>
<rect x="150" y="219" width="420" height="22" rx="11" fill="{t['panel']}"/>
<text class="mono" x="166" y="235" font-size="13" fill="{t['mute']}">{p['domain']}</text>
<g clip-path="url(#sc)">
<g class="{'pan' if pan else ''}"><image href="{src}" x="{sx}" y="{sy}" width="{sw}" height="{h:.0f}" preserveAspectRatio="xMidYMin slice"/></g>
<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="url(#vg)"/>
<g transform="skewX(-12)"><rect class="shine" x="{sx}" y="{sy}" width="260" height="{sh}" fill="url(#sg)"/></g>
</g>
</g>
{phone}"""
    return svg(1200, 680, f"{p['title']} — {p['kind'].capitalize()}",
               f"Prévia real de {p['domain']}. {p['desc']}", css, body)


def cta(t):
    css = """
.in{animation:in 1s cubic-bezier(.2,.7,.2,1) both}
@keyframes in{from{opacity:0;transform:translateY(24px)}}
.grow{transform-box:fill-box;transform-origin:left;animation:grow 1.4s cubic-bezier(.6,0,.2,1) .6s both}
@keyframes grow{from{transform:scaleX(0)}}
.halo{transform-box:fill-box;transform-origin:center;animation:halo 2.8s ease-out 1.5s infinite}
@keyframes halo{from{opacity:.55;transform:scale(1)}to{opacity:0;transform:scale(1.12,1.5)}}
.nudge{animation:nudge 2.4s ease-in-out 1.5s infinite}
@keyframes nudge{50%{transform:translateX(6px)}}
"""
    body = f"""<defs><pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" stroke="{t['grid']}"/></pattern>
<linearGradient id="f" x1="1200" x2="500" gradientUnits="userSpaceOnUse"><stop stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="gm"><rect width="1200" height="340" fill="url(#f)"/></mask></defs>
<rect x=".5" y=".5" width="1199" height="339" rx="19.5" fill="{t['bg']}" stroke="{t['line']}"/>
<rect x="1" y="1" width="1198" height="338" rx="19" fill="url(#g)" mask="url(#gm)"/>
<g class="in">
<rect x="56" y="56" width="10" height="10" fill="{t['accent']}"/>
<text class="mono" x="80" y="66" font-size="17" fill="{t['mute']}">próximo projeto</text>
<text x="50" y="152" font-size="66" font-weight="700" letter-spacing="-3" fill="{t['ink']}">Vamos dar forma</text>
<text x="50" y="228" font-size="66" font-weight="700" letter-spacing="-3" fill="{t['ink']}">à próxima ideia<tspan fill="{t['accent_ink']}">?</tspan></text>
</g>
<path class="grow" d="M56 270H600" stroke="{t['line']}"/>
<text class="in mono" style="animation-delay:.3s" x="56" y="304" font-size="16" fill="{t['mute']}">sites · landing pages · produtos digitais</text>
<g class="in" style="animation-delay:.5s">
<rect class="halo" x="790" y="146" width="340" height="72" rx="36" stroke="{t['accent']}" stroke-width="2"/>
<rect x="790" y="146" width="340" height="72" rx="36" fill="{t['accent']}"/>
<text x="830" y="191" font-size="24" font-weight="700" fill="#111719">Chamar no WhatsApp <tspan class="nudge">→</tspan></text>
</g>"""
    return svg(1200, 340, "Vamos dar forma à próxima ideia?",
               "Convite para conversar pelo WhatsApp sobre sites, landing pages e produtos digitais.", css, body)


def main():
    for name, t in THEMES.items():
        out = {"hero": hero(t), "marquee": marquee(t), "cta": cta(t)}
        for n, p in enumerate(PROJECTS, 1):
            out[f"card-{p['slug']}"] = card(t, p, n)
        for key, content in out.items():
            (ASSETS / f"{key}-{name}.svg").write_text(content, encoding="utf-8")
            print(f"assets/{key}-{name}.svg  {len(content) // 1024}K")


if __name__ == "__main__":
    main()
