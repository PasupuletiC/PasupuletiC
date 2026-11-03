"""Generate self-hosted animated profile cards from the GitHub API.

Writes assets/generated/card-*.svg and assets/generated/stats.svg.
Third-party card services (github-readme-stats etc.) are frequently rate-limited or down,
so the cards are generated here and committed by a scheduled GitHub Action.
"""
import json, os, subprocess, urllib.request
from xml.sax.saxutils import escape

USER = 'PasupuletiC'
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'generated')
os.makedirs(OUT, exist_ok=True)
PROJECTS = [
    ('AI-Operations-Center', 'AI Operations Center', 'Multi-agent support triage and incident analysis with RAG over Qdrant.'),
    ('rag-voice-assistant', 'Ruby: Voice Assistant', 'Voice conversations grounded in your documents, with memory, OCR and multilingual voice.'),
    ('AI_Surveillance_Monitoring_System', 'AI Surveillance', 'YOLOv8 and OpenCV detection with retrieval-augmented incident reports.'),
    ('AI-NewsReel-Generator', 'AI NewsReel Generator', 'Automated AI-driven news reel generation.'),
    ('dataflow-automator', 'DataFlow Automator', 'Automated data cleaning, quality analysis, visualization and executive reporting.'),
    ('ai-candidate-screening-system', 'AI Candidate Screening', 'Role-based candidate screening with RAG, Flask, Next.js and Groq.'),
]
LANG_COLORS = {'Python': '#3572A5', 'JavaScript': '#f1e05a', 'TypeScript': '#3178c6', 'HTML': '#e34c26', 'CSS': '#7c5cbf',
               'PowerShell': '#012456', 'Jupyter Notebook': '#DA5B0B'}
INF = 'repeatCount="indefinite"'
FONT = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"


def token():
    t = os.environ.get('GITHUB_TOKEN')
    if t:
        return t
    try:
        out = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n\n', capture_output=True, text=True).stdout
        return next((l[9:] for l in out.splitlines() if l.startswith('password=')), None)
    except Exception:
        return None


TOK = token()


def api(path):
    req = urllib.request.Request('https://api.github.com' + path, headers={'Accept': 'application/vnd.github+json', **({'Authorization': 'Bearer ' + TOK} if TOK else {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def wrap(s, n):
    words, lines, cur = s.split(), [], ''
    for w in words:
        if len(cur) + len(w) + 1 > n:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + ' ' + w).strip()
    if cur:
        lines.append(cur)
    return lines[:3]


def card(idx, repo, title, fallback):
    try:
        d = api(f'/repos/{USER}/{repo}')
    except Exception:
        d = {}
    desc = d.get('description') or fallback
    lang = d.get('language') or ''
    stars, forks = d.get('stargazers_count', 0), d.get('forks_count', 0)
    topics = (d.get('topics') or [])[:3]
    W, H = 420, 168
    lines = ''.join(f'<text x="22" y="{74 + i * 18}" font-size="12.5" fill="#9fb0c3">{escape(l)}</text>' for i, l in enumerate(wrap(desc, 52)))
    chips, x = '', 22
    for tpc in topics:
        w = 14 + len(tpc) * 6.4
        chips += f'<rect x="{x:.0f}" y="118" width="{w:.0f}" height="20" rx="10" fill="#1f9a73" fill-opacity=".14"/><text x="{x + w / 2:.0f}" y="132" font-size="10.5" fill="#5eead4" text-anchor="middle">{escape(tpc)}</text>'
        x += w + 6
    lc = LANG_COLORS.get(lang, '#8b949e')
    foot = (f'<circle cx="26" cy="152" r="5" fill="{lc}"><animate attributeName="r" values="5;6.5;5" dur="2.4s" {INF}/></circle>'
            f'<text x="38" y="156" font-size="11.5" fill="#9fb0c3">{escape(lang) or "Code"}</text>'
            f'<text x="{W - 22}" y="156" font-size="11.5" fill="#9fb0c3" text-anchor="end">★ {stars}   ⑂ {forks}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}: {escape(desc)}">
<title>{escape(title)}</title>
<defs>
<linearGradient id="bg{idx}" x2="1" y2="1"><stop stop-color="#0f1b2d"/><stop offset="1" stop-color="#0b1220"/></linearGradient>
<linearGradient id="bd{idx}" x2="1" y2="1"><stop stop-color="#34d399"/><stop offset=".5" stop-color="#60a5fa"/><stop offset="1" stop-color="#34d399"/></linearGradient>
<linearGradient id="sw{idx}"><stop stop-color="#34d399" stop-opacity="0"/><stop offset=".5" stop-color="#34d399" stop-opacity=".10"/><stop offset="1" stop-color="#34d399" stop-opacity="0"/></linearGradient>
<clipPath id="cp{idx}"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14"/></clipPath>
</defs>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="url(#bg{idx})" stroke="#243247" stroke-width="1.5"/>
<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="13.5" fill="none" stroke="url(#bd{idx})" stroke-width="2" stroke-dasharray="90 {2 * (W + H)}" stroke-linecap="round">
<animate attributeName="stroke-dashoffset" values="0;-{2 * (W + H) + 90}" dur="{7 + idx}s" {INF}/></rect>
<g clip-path="url(#cp{idx})"><rect x="-140" y="0" width="120" height="{H}" fill="url(#sw{idx})" transform="skewX(-16)"><animate attributeName="x" values="-160;{W + 60}" dur="{6 + idx * .7:.1f}s" begin="{idx * .6:.1f}s" {INF}/></rect></g>
<g font-family="{FONT}">
<path d="M22 26h5l2 3h9a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H22a2 2 0 0 1-2-2V28a2 2 0 0 1 2-2z" transform="translate(0 -6)" fill="none" stroke="#34d399" stroke-width="1.6" stroke-linejoin="round"/>
<text x="52" y="31" font-size="16" font-weight="700" fill="#e6f1ff">{escape(title)}</text>
<text x="{W - 22}" y="31" font-size="11" fill="#60a5fa" text-anchor="end">View repo ↗</text>
{lines}{chips}{foot}
</g></svg>'''
    open(os.path.join(OUT, f'card-{idx + 1}.svg'), 'w', encoding='utf-8').write(svg)
    return d


def stats():
    u = api(f'/users/{USER}')
    repos = api(f'/users/{USER}/repos?per_page=100&type=owner')
    own = [r for r in repos if not r['fork']]
    stars = sum(r['stargazers_count'] for r in own)
    forks = sum(r['forks_count'] for r in own)
    langs = {}
    for r in own:
        if r['language']:
            langs[r['language']] = langs.get(r['language'], 0) + 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]
    total = sum(c for _, c in top) or 1
    W, H = 860, 210
    items = [('Public repos', u['public_repos']), ('Stars earned', stars), ('Followers', u['followers']), ('Forks', forks)]
    cells = ''
    for i, (lab, val) in enumerate(items):
        x = 40 + i * 205
        cells += (f'<g><animate attributeName="opacity" values="0;0;1" keyTimes="0;{.1 + i * .08:.2f};1" dur="1.4s" fill="freeze"/>'
                  f'<text x="{x}" y="70" font-size="40" font-weight="800" fill="#e6f1ff">{val}</text>'
                  f'<text x="{x}" y="94" font-size="12" fill="#8aa0b8" letter-spacing="1">{lab.upper()}</text>'
                  f'<rect x="{x}" y="104" width="150" height="2" rx="1" fill="#1d2b40"/>'
                  f'<rect x="{x}" y="104" width="40" height="2" rx="1" fill="#34d399"><animate attributeName="x" values="{x};{x + 110};{x}" dur="{3 + i * .5}s" {INF}/></rect></g>')
    bars, x = '', 40
    legend = ''
    for i, (name, c) in enumerate(top):
        w = (W - 80) * c / total
        col = LANG_COLORS.get(name, '#8b949e')
        bars += f'<rect x="{x:.1f}" y="140" width="{w:.1f}" height="10" fill="{col}"><animate attributeName="width" values="0;{w:.1f}" dur="1.2s" begin="{i * .15:.2f}s" fill="freeze"/></rect>'
        legend += f'<circle cx="{40 + i * 160}" cy="176" r="5" fill="{col}"/><text x="{52 + i * 160}" y="180" font-size="12" fill="#9fb0c3">{escape(name)} ({c})</text>'
        x += w
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GitHub: {u['public_repos']} public repositories, {stars} stars, {u['followers']} followers, {forks} forks">
<title>GitHub stats for {USER}</title>
<defs><linearGradient id="sbg" x2="1" y2="1"><stop stop-color="#0f1b2d"/><stop offset="1" stop-color="#0b1220"/></linearGradient><clipPath id="sc"><rect x="40" y="140" width="{W - 80}" height="10" rx="5"/></clipPath></defs>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="16" fill="url(#sbg)" stroke="#243247" stroke-width="1.5"/>
<g font-family="{FONT}">
<text x="40" y="30" font-size="12" fill="#34d399" letter-spacing="2">GITHUB / LIVE METRICS</text>
<circle cx="{W - 40}" cy="26" r="4" fill="#34d399"><animate attributeName="opacity" values="1;.3;1" dur="2s" {INF}/></circle>
{cells}
<rect x="40" y="140" width="{W - 80}" height="10" rx="5" fill="#1d2b40"/>
<g clip-path="url(#sc)">{bars}</g>
{legend}
</g></svg>'''
    open(os.path.join(OUT, 'stats.svg'), 'w', encoding='utf-8').write(svg)


for i, (repo, title, fb) in enumerate(PROJECTS):
    card(i, repo, title, fb)
stats()
print('generated')
