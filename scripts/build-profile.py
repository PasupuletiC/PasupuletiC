# Generates the profile section SVGs in assets/profile/. Run: python scripts/build-profile.py
import base64, io, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'profile')
os.makedirs(OUT, exist_ok=True)
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
INK, MUTED, TEAL, BORDER, BG = '#12263f', '#475569', '#1f9a73', '#dbe7ef', '#f6fafd'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def write(name, s):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(s)


def svg(name, w, h, body, title, bg=BG, stroke=BORDER):
    write(name, f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
          f'aria-label="{esc(title)}"><title>{esc(title)}</title>'
          f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="16" fill="{bg}" stroke="{stroke}" stroke-width="1.5"/>'
          f'<g font-family="{FONT}">{body}</g></svg>')


def text(x, y, s, size=14, fill=MUTED, weight=400, anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>'


def lines(x, y, rows, size=14, fill=MUTED, gap=20, weight=400):
    return ''.join(text(x, y + i * gap, r, size, fill, weight) for i, r in enumerate(rows))


def ico(path, color=TEAL):
    return f'<g fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</g>'


def heading(x, y, label, icon):
    return f'<g transform="translate({x} {y})">{icon}</g>' + text(x + 30, y + 6, label, 19, INK, 700)


def check(y):
    return (f'<circle cx="32" cy="{y-4}" r="8" fill="{TEAL}"/><path d="M28.5 {y-4}l2.5 2.5 4.5-5" stroke="#fff" '
            f'stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


I_USER = ico('<circle cx="0" cy="-3" r="4.5"/><path d="M-9 9a9 9 0 0 1 18 0"/>')
I_STACK = ico('<path d="M0-9L10-4 0 1-10-4Z"/><path d="M-10 1L0 6 10 1M-10 6L0 11 10 6"/>')
I_BRIEF = ico('<rect x="-9" y="-5" width="18" height="13" rx="2"/><path d="M-4-5v-3h8v3M-9 1h18"/>')
I_CAP = ico('<path d="M-11-3L0-8 11-3 0 2Z"/><path d="M-6 0v6c3 3 9 3 12 0V0"/>')
I_TROPHY = ico('<path d="M-5-9h10v7a5 5 0 0 1-10 0ZM-5-6h-4v2a4 4 0 0 0 4 4M5-6h4v2a4 4 0 0 1-4 4M0 3v5M-4 9h8"/>')
I_PLANE = ico('<path d="M10-9L-10-1l7 3 3 7ZM-3 2l6-6"/>')
I_DOC = ico('<path d="M-6-9h9l5 5v13h-14zM3-9v5h5"/>')

# ---- avatar: square head-and-shoulders on soft green ----
src = None
for p in (os.path.join(ROOT, 'assets', 'avatar-source.png'), r'C:\Users\NGC\Downloads\Smiling Bearded Man in Striped Hoodie.png'):
    if os.path.exists(p):
        src = p
        break
im = Image.open(src).convert('RGBA')
sq = im.crop((0, 0, 742, 742)).resize((300, 300), Image.LANCZOS)
bgc = Image.new('RGBA', sq.size, (226, 244, 236, 255))
bgc.alpha_composite(sq)
buf = io.BytesIO()
bgc.convert('RGB').save(buf, 'JPEG', quality=88)
AV = base64.b64encode(buf.getvalue()).decode()

# ================= HERO =================
hero = f'''
<defs><linearGradient id="hg" x2="1" y2="1"><stop stop-color="#f2fbf7"/><stop offset="1" stop-color="#eef5fe"/></linearGradient>
<clipPath id="av"><circle cx="118" cy="150" r="82"/></clipPath></defs>
<rect x=".75" y=".75" width="858.5" height="298.5" rx="16" fill="url(#hg)" stroke="{BORDER}" stroke-width="1.5"/>
<circle cx="118" cy="150" r="96" fill="none" stroke="{TEAL}" stroke-opacity=".35" stroke-width="2" stroke-dasharray="10 14">
 <animateTransform attributeName="transform" type="rotate" from="0 118 150" to="360 118 150" dur="40s" repeatCount="indefinite"/></circle>
<circle cx="118" cy="150" r="88" fill="#fff" stroke="{TEAL}" stroke-width="4"/>
<image href="data:image/jpeg;base64,{AV}" x="36" y="68" width="164" height="164" clip-path="url(#av)" preserveAspectRatio="xMidYMid slice"/>
{text(238, 70, "Hi, I'm", 21, INK, 500)}
{text(236, 116, "Charan Kumar Pasupuleti", 33, INK, 800)}
<rect x="238" y="130" width="176" height="32" rx="8" fill="{TEAL}"/>
{text(326, 152, "AI/ML Engineer", 16, '#fff', 700, 'middle')}
{text(238, 192, "Generative AI   |   RAG   |   Agentic AI   |   Machine Learning", 15, INK, 600)}
{lines(238, 220, ["I build AI applications that retrieve knowledge, coordinate agents,", "and interpret visual data. My focus is practical, reliable model", "behavior, affordable infrastructure, and clear user experiences."], 14, MUTED, 21)}
<g transform="translate(770 150) scale(.82)">
 <circle r="105" fill="#d9f2e6" opacity=".6"><animate attributeName="r" values="100;110;100" dur="6s" repeatCount="indefinite"/></circle>
 <g><animateTransform attributeName="transform" type="translate" values="0 0;0 -6;0 0" dur="5s" repeatCount="indefinite"/>
  <rect x="-70" y="-56" width="140" height="94" rx="10" fill="#fff" stroke="#c9dbea" stroke-width="3"/>
  <rect x="-61" y="-47" width="122" height="76" rx="5" fill="#f1f7fd"/>
  <text x="0" y="-1" font-size="34" font-weight="800" fill="{TEAL}" text-anchor="middle" font-family="Consolas, monospace">&lt;/&gt;</text>
  <path d="M-84 42H84L73 53H-73Z" fill="#dce8f3" stroke="#c9dbea" stroke-width="2"/>
 </g>
 <g><animateTransform attributeName="transform" type="translate" values="0 0;0 8;0 0" dur="4s" repeatCount="indefinite"/>
  <rect x="-108" y="-92" width="40" height="40" rx="11" fill="#fff" stroke="#bfe5d3"/>
  <path d="M-98-78h20M-98-70h14M-98-62h18" stroke="{TEAL}" stroke-width="3" stroke-linecap="round"/></g>
 <g><animateTransform attributeName="transform" type="translate" values="0 0;0 -8;0 0" dur="4.6s" repeatCount="indefinite"/>
  <rect x="62" y="-100" width="42" height="42" rx="21" fill="#fff" stroke="#bfe5d3"/>
  <circle cx="83" cy="-79" r="8" fill="none" stroke="{TEAL}" stroke-width="3"/><circle cx="83" cy="-79" r="2.5" fill="{TEAL}"/></g>
 <g><animateTransform attributeName="transform" type="translate" values="0 0;0 6;0 0" dur="5.4s" repeatCount="indefinite"/>
  <rect x="74" y="-10" width="40" height="40" rx="11" fill="#fff" stroke="#bfe5d3"/>
  <path d="M84 20v-9M94 20v-16M104 20v-23" stroke="{TEAL}" stroke-width="4" stroke-linecap="round"/></g>
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
    b += f'<g transform="translate({x+24} 48) scale(.9)">{ic}</g>' + text(x + 42, 44, t1, 12, INK, 700) + text(x + 42, 62, t2, 10.5, MUTED)
svg('strip.svg', 860, 96, b, 'Education, role, research, focus and current learning', '#fff')

# ================= ABOUT =================
about_rows = [["AI/ML Engineer with hands-on experience in LLMs, RAG,", "computer vision and agent systems."],
              ["Build end-to-end AI applications (research →", "prototype → deployment)."],
              ["Interested in Generative AI, MLOps and real-world", "AI products."]]
b = heading(26, 38, 'About Me', I_USER)
y = 84
for r in about_rows:
    b += check(y) + lines(50, y, r, 13.5, MUTED, 19)
    y += 56
svg('about.svg', 410, 232, b, 'About me', '#fff')

# ================= TECH STACK =================
rows = [('Languages', ['Python', 'TypeScript', 'JavaScript']), ('AI / ML', ['PyTorch', 'TensorFlow', 'scikit-learn']),
        ('GenAI / LLM', ['LangChain', 'LangGraph', 'Qdrant', 'Gemini']), ('Web / API', ['FastAPI', 'Flask', 'Next.js']),
        ('Data / DB', ['PostgreSQL', 'Elasticsearch']), ('Infra / Tools', ['Docker', 'AWS', 'Google Cloud', 'Git', 'Linux'])]
b = heading(26, 38, 'Tech Stack', I_STACK)
y = 64
for lab, items in rows:
    b += f'<rect x="20" y="{y}" width="370" height="42" rx="10" fill="{BG}" stroke="{BORDER}"/>' + text(34, y + 26, lab, 12.5, INK, 700)
    x = 112
    for it in items:
        w = 12 + len(it) * 6.4
        b += f'<rect x="{x:.0f}" y="{y+8}" width="{w:.0f}" height="26" rx="7" fill="#fff" stroke="{BORDER}"/>' + text(f'{x + w / 2:.0f}', y + 25.5, it, 11.5, INK, 600, 'middle')
        x += w + 4
    y += 50
svg('techstack.svg', 410, y + 16, b, 'Tech stack', '#fff')

# ================= WORK =================
svg('work-head.svg', 440, 60,
    heading(24, 32, 'Selected Work', ico('<path d="M-9-7h18v14h-18zM-9-2h18"/>')) + text(416, 36, 'View All Repositories →', 13, TEAL, 700, 'end'),
    'Selected work', '#fff')
cards = [('work-1.svg', 'AI Operations Center', ['Support email triage and incident analysis.', 'Knowledge retrieval with multi-provider', 'model routing.'], ['LangGraph', 'FastAPI', 'Next.js', 'Qdrant'], '#eaf8f1', '#bfe5d3'),
         ('work-2.svg', 'Ruby: Voice Assistant', ['Voice conversations grounded in your', 'documents. Persistent memory, retrieval,', 'OCR and multilingual voice.'], ['Python', 'Flask', 'Groq', 'FAISS'], '#eaf2fd', '#c3d9f4'),
         ('work-3.svg', 'AI Surveillance', ['Connect visual detections with relevant', 'context. YOLOv8 detection and retrieval-', 'augmented incident reports.'], ['YOLOv8', 'OpenCV', 'RAG'], '#f1edfc', '#d6cbf3'),
         ('work-4.svg', 'AI NewsReel Generator', ['Automated AI-driven news reel generation.', 'From topic extraction to scripted video', 'creation.'], ['Gemini', 'FFmpeg', 'MoviePy'], '#fdf1e6', '#f4d6b6')]
for fn, t, desc, chips, fill, stroke in cards:
    b = (f'<rect x="20" y="22" width="40" height="40" rx="11" fill="#fff" stroke="{stroke}"/>'
         f'<path d="M30 36h20M30 42h14M30 48h18" stroke="{TEAL}" stroke-width="3" stroke-linecap="round"><animate attributeName="stroke-opacity" values="1;.35;1" dur="3.2s" repeatCount="indefinite"/></path>')
    b += text(72, 40, t, 15.5, INK, 700) + lines(72, 62, desc, 12.5, MUTED, 17)
    x = 72
    for c in chips:
        w = 14 + len(c) * 6.6
        b += f'<rect x="{x:.0f}" y="116" width="{w:.0f}" height="24" rx="7" fill="#fff" stroke="{stroke}"/>' + text(f'{x + w / 2:.0f}', 132.5, c, 11.5, INK, 600, 'middle')
        x += w + 6
    b += f'<path d="M398 36h14m0 0l-4-4m4 4l-4 4" stroke="{INK}" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
    svg(fn, 440, 156, b, t, fill, stroke)

# ================= EXPERIENCE =================
b = heading(26, 38, 'Experience & Education', I_CAP)
items = [(I_BRIEF, 'AI Developer Intern', ['Brollysolutions', '2025']),
         (I_CAP, 'B.Tech in Computer Science & Engineering', ['Kalasalingam Academy of Research and Education', '(KARE) · 2026']),
         (I_DOC, 'Research Author', ['IEEE INDICON 2025', 'Energy prediction using Random Forest models.'])]
b += '<path d="M34 80V220" stroke="#bfe5d3" stroke-width="2"/>'
y = 86
for ic, t, sub in items:
    b += f'<circle cx="34" cy="{y-4}" r="5" fill="{TEAL}"/>' + f'<g transform="translate(62 {y-4}) scale(.8)">{ic}</g>'
    b += text(82, y, t, 13.5, INK, 700) + lines(82, y + 19, sub, 12, MUTED, 16)
    y += 70
svg('experience.svg', 410, 300, b, 'Experience and education', '#fff')

# ================= HIGHLIGHTS =================
hl = [["Internship at NITK Surathkal under Prof. Chandrasekaran K", "(RASP - AI, Project-Code 2025-P039)."],
      ["IIT Madras Shaastra Hackathon – Top 50 Team (Jan 2025)."],
      ["Kalasalingam ACM Hackathon – Finalist (Dec 2025)."],
      ["Pathway GenAI Hackathon, IIT Hyderabad – Top 10 Team."],
      ["Geospatial Project: LULC Classification & Change Detection", "(Idukki, 2021–2025) using Sentinel-2 & Random Forest."]]
b = heading(26, 38, 'Key Highlights', I_TROPHY)
y = 80
for r in hl:
    b += check(y) + lines(50, y, r, 12.5, MUTED, 17)
    y += 17 * len(r) + 17
svg('highlights.svg', 410, 300, b, 'Key highlights', '#fff')

# ================= CONNECT =================
b = heading(26, 38, 'Connect', I_PLANE) + lines(26, 70, ["Open to entry-level AI/ML Engineer and AI Developer opportunities,", "and conversations about RAG, agents and computer vision."], 14, MUTED, 21)
svg('connect.svg', 860, 100, b, 'Connect', '#fff')
print('built')
