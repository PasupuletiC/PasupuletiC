# Generates the profile section SVGs in assets/profile/. Run: python scripts/build-profile.py
# All-white design with SMIL animation (plays inside GitHub's <img> rendering, no scripts).
import base64, io, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'profile')
os.makedirs(OUT, exist_ok=True)
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
INK, MUTED, TEAL, BORDER, WHITE = '#12263f', '#475569', '#1f9a73', '#dbe7ef', '#ffffff'
INF = 'repeatCount="indefinite"'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def write(name, s):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(s)


def fade(body, delay=0.0, dy=12):
    """Fade + slide in once. Visible by default, so static renderers still show everything."""
    if delay <= 0:
        delay = 0.01
    T = delay + 0.8
    k = f'0;{delay / T:.3f};1'
    return (f'<g><animate attributeName="opacity" values="0;0;1" keyTimes="{k}" dur="{T:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 {dy};0 {dy};0 0" keyTimes="{k}" dur="{T:.2f}s" fill="freeze"/>'
            f'{body}</g>')


def pop(body, cx, cy, delay=0.0):
    """Scale-in around (cx, cy)."""
    T = delay + 0.6
    k = f'0;{delay / T:.3f};{(delay + .3) / T:.3f};1'
    return (f'<g transform="translate({cx} {cy})"><g><animateTransform attributeName="transform" type="scale" '
            f'values="0;0;1.18;1" keyTimes="{k}" dur="{T:.2f}s" fill="freeze"/>'
            f'<g transform="translate({-cx} {-cy})">{body}</g></g></g>')


def shimmer(w, h, uid, dur=6.0, begin=0.0, rx=16):
    """Soft green light band sweeping across a card."""
    return (f'<defs><clipPath id="c{uid}"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx}"/></clipPath>'
            f'<linearGradient id="s{uid}"><stop offset="0" stop-color="{TEAL}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{TEAL}" stop-opacity=".09"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></linearGradient></defs>'
            f'<g clip-path="url(#c{uid})"><rect x="-120" y="0" width="110" height="{h}" fill="url(#s{uid})" transform="skewX(-18)">'
            f'<animate attributeName="x" values="-160;{w + 60}" dur="{dur}s" begin="{begin}s" {INF}/></rect></g>')


def svg(name, w, h, body, title, bg=WHITE, stroke=BORDER, delay=0.0, sh=True, dur=7.0, begin=1.5):
    uid = name.replace('.svg', '').replace('-', '')
    inner = fade(f'<g font-family="{FONT}">{body}</g>', delay, 10)
    write(name, f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
          f'aria-label="{esc(title)}"><title>{esc(title)}</title>'
          f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="16" fill="{bg}" stroke="{stroke}" stroke-width="1.5"/>'
          f'{shimmer(w, h, uid, dur, begin) if sh else ""}{inner}</svg>')


def text(x, y, s, size=14, fill=MUTED, weight=400, anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>'


def lines(x, y, rows, size=14, fill=MUTED, gap=20, weight=400):
    return ''.join(text(x, y + i * gap, r, size, fill, weight) for i, r in enumerate(rows))


def ico(path, color=TEAL):
    return f'<g fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</g>'


def heading(x, y, label, icon):
    bob = (f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -2.5;0 0" dur="3.4s" {INF}/>')
    return f'<g transform="translate({x} {y})"><g>{bob}{icon}</g></g>' + text(x + 30, y + 6, label, 19, INK, 700)


def check(y, delay=0.0):
    return pop(f'<circle cx="32" cy="{y-4}" r="8" fill="{TEAL}"/><path d="M28.5 {y-4}l2.5 2.5 4.5-5" stroke="#fff" '
               f'stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>', 32, y - 4, delay)


I_USER = ico('<circle cx="0" cy="-3" r="4.5"/><path d="M-9 9a9 9 0 0 1 18 0"/>')
I_STACK = ico('<path d="M0-9L10-4 0 1-10-4Z"/><path d="M-10 1L0 6 10 1M-10 6L0 11 10 6"/>')
I_BRIEF = ico('<rect x="-9" y="-5" width="18" height="13" rx="2"/><path d="M-4-5v-3h8v3M-9 1h18"/>')
I_CAP = ico('<path d="M-11-3L0-8 11-3 0 2Z"/><path d="M-6 0v6c3 3 9 3 12 0V0"/>')
I_TROPHY = ico('<path d="M-5-9h10v7a5 5 0 0 1-10 0ZM-5-6h-4v2a4 4 0 0 0 4 4M5-6h4v2a4 4 0 0 1-4 4M0 3v5M-4 9h8"/>')
I_PLANE = ico('<path d="M10-9L-10-1l7 3 3 7ZM-3 2l6-6"/>')
I_DOC = ico('<path d="M-6-9h9l5 5v13h-14zM3-9v5h5"/>')

# ---- avatar: square head-and-shoulders on white ----
src = None
for p in (os.path.join(ROOT, 'assets', 'avatar-source.png'), r'C:\Users\NGC\Downloads\Smiling Bearded Man in Striped Hoodie.png'):
    if os.path.exists(p):
        src = p
        break
im = Image.open(src).convert('RGBA')
sq = im.crop((0, 0, 742, 742)).resize((300, 300), Image.LANCZOS)
bgc = Image.new('RGBA', sq.size, (255, 255, 255, 255))
bgc.alpha_composite(sq)
buf = io.BytesIO()
bgc.convert('RGB').save(buf, 'JPEG', quality=90)
AV = base64.b64encode(buf.getvalue()).decode()

# ================= HERO =================
sparks = ''.join(
    f'<circle cx="{x}" cy="{y}" r="{r}" fill="{TEAL}"><animate attributeName="opacity" values="0;.9;0" dur="{d}s" begin="{b}s" {INF}/>'
    f'<animate attributeName="r" values="0;{r};0" dur="{d}s" begin="{b}s" {INF}/></circle>'
    for x, y, r, d, b in [(40, 70, 3.5, 3.2, 0), (205, 62, 3, 4, 1), (214, 214, 3.5, 3.6, .5), (30, 224, 2.5, 4.4, 2), (120, 44, 2.5, 3.8, 1.4)])
hero = f'''
<defs><clipPath id="av"><circle cx="118" cy="150" r="82"/></clipPath>
<clipPath id="badge"><rect x="238" y="130" width="176" height="32" rx="8"/></clipPath></defs>
<rect x=".75" y=".75" width="858.5" height="298.5" rx="16" fill="#fff" stroke="{BORDER}" stroke-width="1.5"/>
<circle cx="118" cy="150" r="96" fill="none" stroke="{TEAL}" stroke-opacity=".4" stroke-width="2" stroke-dasharray="10 14">
 <animateTransform attributeName="transform" type="rotate" from="0 118 150" to="360 118 150" dur="30s" {INF}/></circle>
<circle cx="118" cy="150" r="88" fill="#fff" stroke="{TEAL}" stroke-width="4">
 <animate attributeName="stroke-opacity" values="1;.55;1" dur="4s" {INF}/></circle>
<circle cx="118" cy="150" r="88" fill="none" stroke="{TEAL}" stroke-width="2"><animate attributeName="r" values="88;112" dur="3.2s" {INF}/><animate attributeName="stroke-opacity" values=".5;0" dur="3.2s" {INF}/></circle>
<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="5s" {INF}/>
<image href="data:image/jpeg;base64,{AV}" x="36" y="68" width="164" height="164" clip-path="url(#av)" preserveAspectRatio="xMidYMid slice"/></g>
{sparks}
{fade(text(238, 70, "Hi, I'm", 21, INK, 500), 0.2)}
{fade(text(236, 116, "Charan Kumar Pasupuleti", 33, INK, 800), 0.4)}
{fade(f'<rect x="238" y="130" width="176" height="32" rx="8" fill="{TEAL}"/>' + text(326, 152, "AI/ML Engineer", 16, '#fff', 700, 'middle') +
      f'<g clip-path="url(#badge)"><rect x="150" y="125" width="34" height="44" fill="#fff" opacity=".28" transform="skewX(-20)"><animate attributeName="x" values="150;470" dur="3.6s" begin="1.2s" {INF}/></rect></g>', 0.6)}
{fade(text(238, 192, "Generative AI   |   RAG   |   Agentic AI   |   Machine Learning", 15, INK, 600), 0.8)}
{fade(lines(238, 220, ["I build AI applications that retrieve knowledge, coordinate agents,", "and interpret visual data. My focus is practical, reliable model", "behavior, affordable infrastructure, and clear user experiences."], 14, MUTED, 21), 1.0)}
<rect x="640" y="252" width="8" height="15" rx="1" fill="{TEAL}" opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.05;.5;.5001" dur="1.1s" begin="1.8s" {INF}/></rect>
<g transform="translate(770 150) scale(.82)">
 <circle r="105" fill="none" stroke="#cfeadd" stroke-width="2" stroke-dasharray="4 10"><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="26s" {INF}/></circle>
 <circle r="100" fill="#f4fbf8"><animate attributeName="r" values="98;108;98" dur="6s" {INF}/></circle>
 <g><animateTransform attributeName="transform" type="translate" values="0 0;0 -6;0 0" dur="5s" {INF}/>
  <rect x="-70" y="-56" width="140" height="94" rx="10" fill="#fff" stroke="#c9dbea" stroke-width="3"/>
  <rect x="-61" y="-47" width="122" height="76" rx="5" fill="#fff" stroke="#e3edf6"/>
  <text x="0" y="-1" font-size="34" font-weight="800" fill="{TEAL}" text-anchor="middle" font-family="Consolas, monospace">&lt;/&gt;<animate attributeName="opacity" values="1;.55;1" dur="3s" {INF}/></text>
  <path d="M-84 42H84L73 53H-73Z" fill="#fff" stroke="#c9dbea" stroke-width="2"/>
 </g>
 <g><animateTransform attributeName="transform" type="translate" values="0 0;0 8;0 0" dur="4s" {INF}/>
  <rect x="-108" y="-92" width="40" height="40" rx="11" fill="#fff" stroke="#bfe5d3"/>
  <path d="M-98-78h20M-98-70h14M-98-62h18" stroke="{TEAL}" stroke-width="3" stroke-linecap="round"/></g>
 <g><animateTransform attributeName="transform" type="translate" values="0 0;0 -8;0 0" dur="4.6s" {INF}/>
  <rect x="62" y="-100" width="42" height="42" rx="21" fill="#fff" stroke="#bfe5d3"/>
  <circle cx="83" cy="-79" r="8" fill="none" stroke="{TEAL}" stroke-width="3"/><circle cx="83" cy="-79" r="2.5" fill="{TEAL}"><animate attributeName="r" values="2.5;5;2.5" dur="2.4s" {INF}/></circle></g>
 <g><animateTransform attributeName="transform" type="translate" values="0 0;0 6;0 0" dur="5.4s" {INF}/>
  <rect x="74" y="-10" width="40" height="40" rx="11" fill="#fff" stroke="#bfe5d3"/>
  <path d="M84 20v-9M94 20v-16M104 20v-23" stroke="{TEAL}" stroke-width="4" stroke-linecap="round"><animate attributeName="stroke-opacity" values="1;.4;1" dur="2.6s" {INF}/></path></g>
</g>'''
write('hero.svg', f'<svg xmlns="http://www.w3.org/2000/svg" width="860" height="300" viewBox="0 0 860 300" role="img" aria-label="Charan Kumar Pasupuleti, AI/ML Engineer. Generative AI, RAG, agentic AI and machine learning."><title>Charan Kumar Pasupuleti: AI/ML Engineer</title><g font-family="{FONT}">{hero}</g></svg>')

# ================= STRIP =================
cells = [(I_CAP, 'B.Tech (CSE)', 'KARE, Batch 2026'), (I_BRIEF, 'AI Developer Intern', 'Brollysolutions'),
         (I_TROPHY, 'IEEE INDICON 2025', 'Research Author'),
         (ico('<circle r="9"/><circle r="4.5"/>'), 'Focus', 'RAG · Agents · Vision'),
         (ico('<path d="M-8 9V1M0 9V-4M8 9V-9"/>'), 'Currently Learning', 'LLM eval & production')]
b = ''
for i, (ic, t1, t2) in enumerate(cells):
    x = i * 172
    if i:
        b += f'<path d="M{x} 20V76" stroke="{BORDER}"/>'
    bounce = f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="3s" begin="{i*0.5}s" {INF}/>'
    b += fade(f'<g transform="translate({x+24} 48) scale(.9)"><g>{bounce}{ic}</g></g>' + text(x + 42, 44, t1, 12, INK, 700) + text(x + 42, 62, t2, 10.5, MUTED), 0.15 * i)
svg('strip.svg', 860, 96, b, 'Education, role, research, focus and current learning', dur=8, begin=2)

# ================= ABOUT =================
about_rows = [["AI/ML Engineer with hands-on experience in LLMs, RAG,", "computer vision and agent systems."],
              ["Build end-to-end AI applications (research →", "prototype → deployment)."],
              ["Interested in Generative AI, MLOps and real-world", "AI products."]]
b = heading(26, 38, 'About Me', I_USER)
y = 84
for i, r in enumerate(about_rows):
    b += check(y, 0.4 + i * 0.35) + fade(lines(50, y, r, 13.5, MUTED, 19), 0.4 + i * 0.35, 6)
    y += 56
svg('about.svg', 410, 232, b, 'About me', begin=0.5)

# ================= TECH STACK =================
rows = [('Languages', ['Python', 'TypeScript', 'JavaScript']), ('AI / ML', ['PyTorch', 'TensorFlow', 'scikit-learn']),
        ('GenAI / LLM', ['LangChain', 'LangGraph', 'Qdrant', 'Gemini']), ('Web / API', ['FastAPI', 'Flask', 'Next.js']),
        ('Data / DB', ['PostgreSQL', 'Elasticsearch']), ('Infra / Tools', ['Docker', 'AWS', 'Google Cloud', 'Git', 'Linux'])]
b = heading(26, 38, 'Tech Stack', I_STACK)
y = 64
for r_i, (lab, items) in enumerate(rows):
    row = f'<rect x="20" y="{y}" width="370" height="42" rx="10" fill="#fff" stroke="{BORDER}"/>' + text(34, y + 26, lab, 12.5, INK, 700)
    row += (f'<rect x="20" y="{y+10}" width="3" height="22" rx="1.5" fill="{TEAL}"><animate attributeName="opacity" values=".15;1;.15" dur="3.6s" begin="{r_i*0.45}s" {INF}/></rect>')
    x = 112
    for c_i, it in enumerate(items):
        w = 12 + len(it) * 6.4
        row += (f'<rect x="{x:.0f}" y="{y+8}" width="{w:.0f}" height="26" rx="7" fill="#fff" stroke="{BORDER}">'
                f'<animate attributeName="stroke" values="{BORDER};{TEAL};{BORDER}" dur="6s" begin="{r_i*0.6 + c_i*0.25:.2f}s" {INF}/></rect>'
                + text(f'{x + w / 2:.0f}', y + 25.5, it, 11.5, INK, 600, 'middle'))
        x += w + 4
    b += fade(row, 0.3 + r_i * 0.12, 8)
    y += 50
svg('techstack.svg', 410, y + 16, b, 'Tech stack', begin=1)

# ================= WORK =================
arrow_nudge = f'<animateTransform attributeName="transform" type="translate" values="0 0;5 0;0 0" dur="1.8s" {INF}/>'
svg('work-head.svg', 440, 60,
    heading(24, 32, 'Selected Work', ico('<path d="M-9-7h18v14h-18zM-9-2h18"/>')) +
    f'<g>{arrow_nudge}' + text(416, 36, 'View All Repositories →', 13, TEAL, 700, 'end') + '</g>', 'Selected work', sh=False)
cards = [('work-1.svg', 'AI Operations Center', ['Support email triage and incident analysis.', 'Knowledge retrieval with multi-provider', 'model routing.'], ['LangGraph', 'FastAPI', 'Next.js', 'Qdrant'], '#9fd8bd'),
         ('work-2.svg', 'Ruby: Voice Assistant', ['Voice conversations grounded in your', 'documents. Persistent memory, retrieval,', 'OCR and multilingual voice.'], ['Python', 'Flask', 'Groq', 'FAISS'], '#a8c9ee'),
         ('work-3.svg', 'AI Surveillance', ['Connect visual detections with relevant', 'context. YOLOv8 detection and retrieval-', 'augmented incident reports.'], ['YOLOv8', 'OpenCV', 'RAG'], '#c4b5ec'),
         ('work-4.svg', 'AI NewsReel Generator', ['Automated AI-driven news reel generation.', 'From topic extraction to scripted video', 'creation.'], ['Gemini', 'FFmpeg', 'MoviePy'], '#f0c79a')]
for n, (fn, t, desc, chips, stroke) in enumerate(cards):
    bars = ''.join(
        f'<line x1="30" y1="{yy}" x2="{x2}" y2="{yy}" stroke="{TEAL}" stroke-width="3" stroke-linecap="round">'
        f'<animate attributeName="x2" values="{x2};{x2-9};{x2}" dur="{d}s" {INF}/></line>'
        for yy, x2, d in [(36, 50, 2.2), (42, 44, 1.7), (48, 48, 2.6)])
    b = (f'<rect x="20" y="22" width="40" height="40" rx="11" fill="#fff" stroke="{stroke}"/>' + bars)
    b += text(72, 40, t, 15.5, INK, 700) + lines(72, 62, desc, 12.5, MUTED, 17)
    x = 72
    for c in chips:
        w = 14 + len(c) * 6.6
        b += f'<rect x="{x:.0f}" y="116" width="{w:.0f}" height="24" rx="7" fill="#fff" stroke="{stroke}"/>' + text(f'{x + w / 2:.0f}', 132.5, c, 11.5, INK, 600, 'middle')
        x += w + 6
    b += (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;5 0;0 0" dur="1.8s" begin="{n*0.3}s" {INF}/>'
          f'<path d="M398 36h14m0 0l-4-4m4 4l-4 4" stroke="{INK}" stroke-width="1.8" fill="none" stroke-linecap="round"/></g>')
    svg(fn, 440, 156, b, t, stroke=stroke, delay=0.2 + n * 0.25, dur=6 + n * 0.7, begin=1 + n * 0.8)

# ================= EXPERIENCE =================
b = heading(26, 38, 'Experience & Education', I_CAP)
items = [(I_BRIEF, 'AI Developer Intern', ['Brollysolutions', '2025']),
         (I_CAP, 'B.Tech in Computer Science & Engineering', ['Kalasalingam Academy of Research and Education', '(KARE) · 2026']),
         (I_DOC, 'Research Author', ['IEEE INDICON 2025', 'Energy prediction using Random Forest models.'])]
b += (f'<path d="M34 82V220" stroke="#bfe5d3" stroke-width="2" stroke-dasharray="140 140"><animate attributeName="stroke-dashoffset" '
      f'values="140;0" dur="1.8s" fill="freeze"/></path>')
y = 86
for i, (ic, t, sub) in enumerate(items):
    halo = (f'<circle cx="34" cy="{y-4}" r="5" fill="{TEAL}" opacity=".35"><animate attributeName="r" values="5;12" dur="2.6s" begin="{i*0.8}s" {INF}/>'
            f'<animate attributeName="opacity" values=".4;0" dur="2.6s" begin="{i*0.8}s" {INF}/></circle>')
    row = halo + f'<circle cx="34" cy="{y-4}" r="5" fill="{TEAL}"/>' + f'<g transform="translate(62 {y-4}) scale(.8)">{ic}</g>'
    row += text(82, y, t, 13.5, INK, 700) + lines(82, y + 19, sub, 12, MUTED, 16)
    b += fade(row, 0.5 + i * 0.5, 8)
    y += 70
svg('experience.svg', 410, 300, b, 'Experience and education', begin=2)

# ================= HIGHLIGHTS =================
hl = [["Internship at NITK Surathkal under Prof. Chandrasekaran K", "(RASP - AI, Project-Code 2025-P039)."],
      ["IIT Madras Shaastra Hackathon – Top 50 Team (Jan 2025)."],
      ["Kalasalingam ACM Hackathon – Finalist (Dec 2025)."],
      ["Pathway GenAI Hackathon, IIT Hyderabad – Top 10 Team."],
      ["Geospatial Project: LULC Classification & Change Detection", "(Idukki, 2021–2025) using Sentinel-2 & Random Forest."]]
b = heading(26, 38, 'Key Highlights', I_TROPHY)
y = 80
for i, r in enumerate(hl):
    b += check(y, 0.4 + i * 0.3) + fade(lines(50, y, r, 12.5, MUTED, 17), 0.4 + i * 0.3, 6)
    y += 17 * len(r) + 17
svg('highlights.svg', 410, 300, b, 'Key highlights', begin=3)

# ================= CONNECT =================
fly = (f'<g transform="translate(26 38)"><g><animateTransform attributeName="transform" type="translate" values="0 0;10 -4;0 0" dur="2.8s" {INF}/>{I_PLANE}</g></g>')
b = fly + text(56, 44, 'Connect', 19, INK, 700) + lines(26, 70, ["Open to entry-level AI/ML Engineer and AI Developer opportunities,", "and conversations about RAG, agents and computer vision."], 14, MUTED, 21)
b += (f'<circle cx="700" cy="50" r="6" fill="{TEAL}"/><circle cx="700" cy="50" r="6" fill="none" stroke="{TEAL}"><animate attributeName="r" values="6;22" dur="2.4s" {INF}/>'
      f'<animate attributeName="stroke-opacity" values=".7;0" dur="2.4s" {INF}/></circle>' + text(718, 55, 'Open to work', 13, TEAL, 700))
svg('connect.svg', 860, 100, b, 'Connect. Open to work.', begin=1)
print('built')
