#!/usr/bin/env python3
"""Renders the profile README's visual assets with headless Chrome: HTML in the Rehearsal Studio
system -> PNG at 2x, light + dark. Sources stay editable in gen/html/."""
import pathlib, subprocess, re, html

S = pathlib.Path(__file__).resolve().parents[1]
OUT = S / "profile" / "assets"
HTML = S / "gen" / "html"; HTML.mkdir(exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ART = pathlib.Path("/Users/RobertoHernandez/Desktop/Understudy/docs/site/assets")
# 1320x2868 simulator captures from the Cue build (Sept 23, 2026), the same set App Store screenshots v6 are made from.
# 06-market-event.png is left out on purpose: it shows a known headline-tint bug.
SHOTS = pathlib.Path.home() / "Desktop/Understudy_AppStore_Screenshots/v6-captures"

FONTS = "https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&family=Fraunces:ital,wght@1,600&display=swap"

def tokens(theme):
    if theme == "light":
        return """--canvas:#F7F5FB;--card:#FFFFFF;--stroke:#E7E2F0;--ink:#17151F;--muted:#6F6A80;--faint:#A29CB0;
--purple:#7C3AED;--purple-soft:#EDE7FD;--highlight:#FDE68A;--hl-ink:#17151F;
--stocks:#DCF3E6;--stocks-ink:#166534;--estate:#EDE7FD;--estate-ink:#5B21B6;--business:#FBEFC7;--business-ink:#92400E;--bonds:#D7F0EE;--bonds-ink:#0F5F5A;
--blob:.55;--shadow-lg:0 50px 60px rgba(23,21,31,.16),0 12px 22px rgba(23,21,31,.08);--shadow-sm:0 30px 40px rgba(23,21,31,.12),0 8px 16px rgba(23,21,31,.06);"""
    return """--canvas:#0D1117;--card:#1B1826;--stroke:#2E2A3C;--ink:#F4F1FA;--muted:#B7B1C6;--faint:#7E778F;
--purple:#A78BFA;--purple-soft:#2A2340;--highlight:#FDE68A;--hl-ink:#17151F;
--stocks:#153524;--stocks-ink:#86EFAC;--estate:#2A2340;--estate-ink:#C4B5FD;--business:#3A2D12;--business-ink:#FCD34D;--bonds:#10302E;--bonds-ink:#5EEAD4;
--blob:.32;--shadow-lg:0 50px 60px rgba(0,0,0,.5),0 12px 22px rgba(0,0,0,.35);--shadow-sm:0 30px 40px rgba(0,0,0,.4),0 8px 16px rgba(0,0,0,.3);"""

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%;background:transparent}
body{font-family:'Nunito',ui-rounded,system-ui,sans-serif;font-weight:700;color:var(--ink);-webkit-font-smoothing:antialiased;overflow:hidden}
h1,h2,h3{font-weight:900;letter-spacing:-.03em;line-height:1.02}
.em{font-family:'Fraunces',Georgia,serif;font-style:italic;font-weight:600;letter-spacing:-.02em}
.hl{background:var(--highlight);color:var(--hl-ink);border-radius:.32em;padding:0 .2em;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.eyebrow{font-size:13px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--purple)}
.stage{position:relative;width:100%;height:100%;background:var(--canvas);overflow:hidden}
.backdrop{position:absolute;inset:0;pointer-events:none}
.backdrop i{position:absolute;border-radius:50%;filter:blur(80px);opacity:var(--blob)}
.pill{display:inline-flex;align-items:center;gap:10px;background:var(--card);border:1px solid var(--stroke);border-radius:999px;padding:11px 18px;color:var(--purple);font-size:15px;font-weight:800;box-shadow:var(--shadow-sm)}
.chip{display:inline-flex;align-items:center;gap:8px;border-radius:999px;padding:8px 14px;font-size:13px;font-weight:800;letter-spacing:.02em}
"""

def page(theme, w, h, body, css=""):
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="{FONTS}">
<style>:root{{{tokens(theme)}}}{BASE_CSS}{css}</style></head>
<body style="width:{w}px;height:{h}px">{body}</body></html>"""

def render(name, theme, w, h, body, css="", transparent=False):
    f = HTML / f"{name}-{theme}.html"
    f.write_text(page(theme, w, h, body, css))
    out = OUT / f"{name}-{theme}.png"
    args = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
            "--force-device-scale-factor=2", f"--window-size={w},{h}", "--virtual-time-budget=10000",
            f"--screenshot={out}", f"file://{f}"]
    if transparent:
        args.insert(1, "--default-background-color=00000000")
    subprocess.run(args, check=True, capture_output=True)
    print("rendered", out.name)

def measure(name, theme, body, css=""):
    """Width of #m after layout, via --dump-dom (fonts loaded thanks to the virtual time budget)."""
    f = HTML / f"{name}-{theme}-measure.html"
    f.write_text(page(theme, 1400, 200, body + "<script>addEventListener('load',()=>document.fonts.ready.then(()=>{const r=document.getElementById('m').getBoundingClientRect();document.body.setAttribute('data-w',Math.ceil(r.width));document.body.setAttribute('data-h',Math.ceil(r.height))}))</script>", css))
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-first-run", "--virtual-time-budget=10000", "--dump-dom", f"file://{f}"], capture_output=True, text=True)
    m = re.search(r'data-w="(\d+)" data-h="(\d+)"', r.stdout)
    return int(m.group(1)), int(m.group(2))

# ---------------------------------------------------------------- hero
def hero(theme):
    body = f"""
<div class="stage">
  <div class="backdrop"><i style="width:620px;height:620px;left:-200px;top:-260px;background:var(--estate)"></i>
  <i style="width:520px;height:520px;right:-120px;top:-180px;background:var(--business)"></i>
  <i style="width:460px;height:460px;right:260px;bottom:-300px;background:var(--stocks)"></i></div>
  <div class="grid">
    <div class="copy">
      <div class="eyebrow">Roberto Hernandez · iOS Engineer · Los Angeles</div>
      <h1>Hey, I'm <span class="em hl">Roberto</span>.</h1>
      <p class="lede">I build native iOS apps end to end: from the first SwiftUI view to the App Store listing, and the unglamorous half in between.</p>
      <span class="pill" style="transform:rotate(-2deg)">✦&nbsp; Now shipping <b>Understudy</b> · Fall 2026</span>
    </div>
    <div class="art">
      <div class="ghost"><div class="mini"><div class="row"><span>PRACTICE VALUE</span><b>$10,412.60</b></div>
        <div class="cells"><div class="cell" style="background:var(--stocks);color:var(--stocks-ink)">RETURN<b>+4.1%</b></div><div class="cell" style="background:var(--estate);color:var(--estate-ink)">HORIZON<b>10 yrs</b></div><div class="cell" style="background:var(--business);color:var(--business-ink)">DECISIONS<b>7</b></div></div></div></div>
      <div class="card"><img src="file://{ART}/ill-avatar-protagonist.png"></div>
    </div>
  </div>
</div>"""
    css = """
.grid{position:relative;display:grid;grid-template-columns:1.15fr .85fr;gap:24px;height:100%;padding:48px 72px;align-items:center}
.copy{display:flex;flex-direction:column;gap:18px;align-items:flex-start}
h1{font-size:76px}
.lede{color:var(--muted);font-size:21px;line-height:1.4;max-width:30ch;font-weight:700}
.art{position:relative;height:100%}
.card{position:absolute;right:40px;top:50%;transform:translateY(-50%) rotate(-6deg);width:320px;height:320px;border-radius:48px;overflow:hidden;background:var(--card);box-shadow:var(--shadow-lg)}
.card img{width:100%;height:100%;object-fit:cover;object-position:center 22%}
.ghost{position:absolute;right:10px;top:40px;width:270px;transform:rotate(-10deg);opacity:.5;filter:blur(5px)}
.mini{background:var(--card);border:1px solid var(--stroke);border-radius:22px;padding:16px}
.row{display:flex;justify-content:space-between;align-items:baseline;font-size:11px;font-weight:800;letter-spacing:.1em;color:var(--muted)}
.row b{color:var(--ink);font-size:20px;letter-spacing:0}
.cells{display:flex;gap:8px;margin-top:10px}
.cell{flex:1;border-radius:14px;padding:10px 12px;font-size:10px;font-weight:800;letter-spacing:.08em}
.cell b{display:block;font-size:16px;letter-spacing:0;margin-top:2px}
"""
    render("hero", theme, 1200, 500, body, css)

# ---------------------------------------------------------------- section headers
SECTIONS = [("01", "now", "Now", "Fall 2026"), ("02", "build", "How I build", "Architecture, concurrency, tests, shipping"),
            ("03", "work", "Where I've worked", "2018 → today"), ("04", "beyond", "Beyond code", "Sports, guitar, coffee"),
            ("05", "connect", "Say hi", "Roles, collaborations, coffee chats")]
def section(theme, n, key, title, sub):
    body = f"""<div class="sec"><div class="num">{n}</div><div class="t"><h2>{title}</h2><div class="sub">{sub}</div></div><div class="rule"></div></div>"""
    css = """
.sec{display:flex;align-items:center;gap:20px;height:100%;padding:0 8px}
.num{width:52px;height:52px;border-radius:16px;background:var(--purple-soft);color:var(--purple);display:grid;place-items:center;font-size:17px;font-weight:900;letter-spacing:.02em;flex:none}
.t{display:flex;flex-direction:column;gap:4px}
h2{font-size:38px}
.sub{color:var(--muted);font-size:14px;font-weight:800;letter-spacing:.06em;text-transform:uppercase}
.rule{flex:1;height:2px;background:var(--stroke);border-radius:2px;margin-left:8px}
"""
    render(f"section-{key}", theme, 1200, 96, body, css, transparent=True)

# ---------------------------------------------------------------- understudy showcase
def showcase(theme):
    shots = ["07-pick-a-path.png", "02-portfolio.png", "05-concept-sheet.png"]
    phones = "".join(f'<div class="ph p{i}"><img src="file://{SHOTS}/{s}"></div>' for i, s in enumerate(shots))
    phones += '<div class="cap">Screens from the app · every price simulated</div>'
    body = f"""
<div class="stage">
  <div class="backdrop"><i style="width:560px;height:560px;left:380px;top:-240px;background:var(--estate)"></i>
  <i style="width:520px;height:520px;right:-140px;bottom:-260px;background:var(--business)"></i>
  <i style="width:420px;height:420px;left:-160px;bottom:-200px;background:var(--stocks)"></i></div>
  <div class="grid">
    <div class="copy">
      <div class="brand"><img src="file://{ART}/icon-cue-512.png"><div><div class="name">Understudy</div><div class="sub">Investing Practice · Berto Labs</div></div></div>
      <h2>Rehearse investing <span class="em hl">before</span> you risk a real dollar.</h2>
      <p class="lede">A practice brokerage for beginners. Real market behaviour, practice money, every concept explained with your own numbers. Nothing here is real, and that's the point.</p>
      <div class="chips">
        <span class="chip" style="background:var(--stocks);color:var(--stocks-ink)">● &nbsp;In App Review · submitted Sept 14</span>
        <span class="chip" style="background:var(--purple-soft);color:var(--purple)">RevenueCat Shipaton 2026</span>
      </div>
      <div class="stats">
        <div><b>8</b><span>Swift packages</span></div><div><b>400</b><span>tests on Xcode Cloud</span></div><div><b>Swift 6</b><span>strict concurrency</span></div><div><b>iOS 26</b><span>on the iOS 27 SDK</span></div>
      </div>
    </div>
    <div class="art">{phones}</div>
  </div>
</div>"""
    css = """
.grid{position:relative;display:grid;grid-template-columns:1fr 1fr;height:100%;padding:52px 0 52px 64px;align-items:center;gap:0}
.copy{display:flex;flex-direction:column;gap:20px;align-items:flex-start;max-width:520px}
.brand{display:flex;align-items:center;gap:14px}
.brand img{width:64px;height:64px;border-radius:18px;box-shadow:var(--shadow-sm)}
.name{font-size:24px;font-weight:900;letter-spacing:-.02em}.sub{color:var(--muted);font-size:13px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;margin-top:2px}
h2{font-size:46px;max-width:12ch}
.lede{color:var(--muted);font-size:17px;line-height:1.45;max-width:44ch}
.chips{display:flex;gap:10px;flex-wrap:wrap}
.stats{display:flex;gap:26px;margin-top:6px}
.stats div{display:flex;flex-direction:column;gap:2px}
.stats b{font-size:26px;font-weight:900;letter-spacing:-.03em}.stats span{font-size:12px;color:var(--muted);font-weight:800;letter-spacing:.04em;text-transform:uppercase}
.art{position:relative;height:100%}
.ph{position:absolute;top:50%;width:206px;aspect-ratio:1320/2868;border-radius:36px;overflow:hidden;background:var(--card);box-shadow:var(--shadow-lg);border:6px solid var(--card)}
.ph img{width:100%;height:100%;display:block;object-fit:cover}
.p0{left:24px;transform:translateY(-47%) rotate(-8deg);z-index:1}
.p1{left:176px;transform:translateY(-50%);z-index:3}
.p2{left:328px;transform:translateY(-47%) rotate(8deg);z-index:2}
.cap{position:absolute;z-index:4;left:24px;width:510px;bottom:4px;text-align:center;font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
"""
    render("understudy", theme, 1200, 640, body, css)

# ---------------------------------------------------------------- principles grid
PRINCIPLES = [
 ("▦", "Architecture first", "Clean Architecture + MVVM in flat local Swift packages. A Feature target depends on its own Domain and nothing else; navigation is wired once at the root.", "estate"),
 ("⟳", "Concurrency by design", "Default actor isolation, domain actors for engines, structured cancellation. Not <code>Task {}</code> sprinkled over a problem.", "bonds"),
 ("✓", "Tests where it matters", "Simulation math, entitlements and persistence get Swift Testing coverage. Views get previews at Dynamic Type XXL.", "stocks"),
 ("⬆", "Ship the whole product", "Subscriptions that pass review, privacy labels that match the data, a landing page, a demo video, a cadence. The listing is part of the app.", "business"),
]
def principles(theme):
    cards = "".join(f"""<div class="c"><div class="ic" style="background:var(--{t});color:var(--{t}-ink)">{ic}</div><h3>{h}</h3><p>{p}</p></div>""" for ic, h, p, t in PRINCIPLES)
    body = f'<div class="stage" style="background:transparent"><div class="g">{cards}</div></div>'
    css = """
.g{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;height:100%;padding:6px}
.c{background:var(--card);border:1px solid var(--stroke);border-radius:28px;padding:24px;display:flex;flex-direction:column;gap:12px;box-shadow:0 1px 0 rgba(0,0,0,.02)}
.ic{width:44px;height:44px;border-radius:14px;display:grid;place-items:center;font-size:22px;font-weight:900}
h3{font-size:20px;letter-spacing:-.02em;line-height:1.15}
p{color:var(--muted);font-size:14.5px;line-height:1.45;font-weight:700}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px;background:var(--canvas);border:1px solid var(--stroke);border-radius:6px;padding:1px 5px;color:var(--ink)}
"""
    render("principles", theme, 1200, 250, body, css, transparent=True)

# ---------------------------------------------------------------- link pills (auto-width)
LINKS = [("understudy", "Understudy", "ink", "✦"), ("linkedin", "LinkedIn", "ghost", "in"), ("x", "@PreachOnBerto", "ghost", "𝕏"), ("email", "Email me", "ghost", "✉"),
         ("appstore", "Download on the App Store", "ink", "")]
def pills(theme):
    for key, label, kind, ic in LINKS:
        cls = "b-ink" if kind == "ink" else "b-ghost"
        icon = f'<span class="ic">{ic}</span>' if ic else ''
        body = f'<div style="padding:12px 14px"><span id="m" class="btn {cls}">{icon}{label}</span></div>'
        css = """
.btn{display:inline-flex;align-items:center;gap:10px;border-radius:999px;padding:13px 22px;font-weight:800;font-size:16px;border:1.5px solid transparent;white-space:nowrap;letter-spacing:-.01em}
.b-ink{background:var(--ink);color:var(--canvas);box-shadow:var(--shadow-sm)}
.b-ghost{background:var(--card);color:var(--ink);border-color:var(--stroke);box-shadow:var(--shadow-sm)}
.ic{font-size:15px;font-weight:900;opacity:.9}
"""
        w, h = measure(f"link-{key}", theme, body, css)
        render(f"link-{key}", theme, w + 28, h + 24, body, css, transparent=True)

# ---------------------------------------------------------------- footer (a dim room in both themes)
def footer(theme):
    body = f"""
<div class="stage" style="background:#17151F;color:#F4F1FA">
  <div class="glow"></div>
  <div class="row">
    <div><div class="eyebrow" style="color:#FDE68A">Berto Labs · Los Angeles</div><h2>Thanks for <span class="em" style="color:#FDE68A">stopping by</span>. ✌️</h2></div>
    <div class="q">“You don't need to learn everything, you just need to be curious about learning.<br>When the time comes that you need it, you'll be prepared.”</div>
  </div>
</div>"""
    css = """
.glow{position:absolute;left:-120px;top:-160px;width:520px;height:420px;border-radius:50%;background:radial-gradient(closest-side,rgba(253,230,138,.22),rgba(253,230,138,0));filter:blur(30px)}
.row{position:relative;display:flex;justify-content:space-between;align-items:center;gap:40px;height:100%;padding:0 72px}
h2{font-size:44px;margin-top:10px}
.q{color:#B7B1C6;font-size:15px;line-height:1.5;max-width:44ch;text-align:right;font-weight:700}
"""
    render("footer", theme, 1200, 200, body, css)


# ---------------------------------------------------------------- github stats (real numbers, rendered)
def stats(theme):
    import json, datetime, subprocess as sp
    q = '{ user(login:"RobertoEfrainHernandez"){ createdAt repositories(privacy:PUBLIC){totalCount} contributionsCollection{ restrictedContributionsCount contributionCalendar{ totalContributions weeks{ contributionDays{ contributionCount } } } } } }'
    d = json.loads(sp.run(["gh","api","graphql","-f",f"query={q}"], capture_output=True, text=True, check=True).stdout)["data"]["user"]
    cal = d["contributionsCollection"]["contributionCalendar"]
    weeks = [sum(x["contributionCount"] for x in w["contributionDays"]) for w in cal["weeks"]]
    total, private = cal["totalContributions"], d["contributionsCollection"]["restrictedContributionsCount"]
    pct = round(100 * private / max(total, 1))
    mx = max(weeks) or 1
    bars = "".join(f'<i style="height:{max(6, round(100*w/mx))}%;{"background:var(--purple)" if w else ""}"></i>' for w in weeks)
    since = d["createdAt"][:4]; today = datetime.date.today().strftime("%b %Y")
    body = f"""
<div class="stage" style="background:transparent"><div class="card">
  <div class="left">
    <div class="eyebrow">GitHub · past 12 months</div>
    <div class="tiles">
      <div><b>{total}</b><span>contributions</span></div>
      <div><b>{pct}%</b><span>in private product repos</span></div>
      <div><b>{d["repositories"]["totalCount"]}</b><span>public repos</span></div>
      <div><b>{since}</b><span>on GitHub since</span></div>
    </div>
    <p class="note">The graph undercounts the work: Understudy and PointsCompass live in private repos. <span class="em">The apps are the evidence.</span></p>
  </div>
  <div class="right"><div class="spark">{bars}</div><div class="axis"><span>{(datetime.date.today()-datetime.timedelta(weeks=52)).strftime("%b %Y")}</span><span>one bar per week</span><span>{today}</span></div></div>
</div></div>"""
    css = """
.card{display:grid;grid-template-columns:1fr 1.1fr;gap:40px;height:calc(100% - 12px);margin:6px;background:var(--card);border:1px solid var(--stroke);border-radius:28px;padding:24px 36px;align-items:center}
.left{display:flex;flex-direction:column;gap:16px}
.tiles{display:flex;gap:28px}
.tiles div{display:flex;flex-direction:column;gap:2px}
.tiles b{font-size:30px;font-weight:900;letter-spacing:-.03em}.tiles span{font-size:11.5px;color:var(--muted);font-weight:800;letter-spacing:.05em;text-transform:uppercase}
.note{color:var(--muted);font-size:14px;line-height:1.45;max-width:46ch;font-weight:700}
.note .em{color:var(--ink);font-size:15px}
.right{display:flex;flex-direction:column;gap:10px;height:100%;justify-content:center}
.spark{display:flex;align-items:flex-end;gap:4px;height:120px;padding:0 2px}
.spark i{flex:1;border-radius:4px 4px 2px 2px;background:var(--purple-soft);min-width:0}
.axis{display:flex;justify-content:space-between;font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--faint)}
"""
    render("stats", theme, 1200, 240, body, css, transparent=True)


# ---------------------------------------------------------------- work + beyond, card grids
CARD_CSS = """
.g{display:grid;gap:16px;height:100%;padding:6px}
.c{background:var(--card);border:1px solid var(--stroke);border-radius:28px;padding:24px;display:flex;flex-direction:column;gap:10px}
.ic{width:44px;height:44px;border-radius:14px;display:grid;place-items:center;font-size:22px;font-weight:900}
h3{font-size:21px;letter-spacing:-.02em;line-height:1.15}
.role{font-size:13px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:var(--purple)}
.role span{color:var(--faint)}
p{color:var(--muted);font-size:14.5px;line-height:1.45;font-weight:700}
"""
WORK = [
 ("🧪", "Berto Labs", "Founder, iOS", "Aug 2026 – present", "Understudy (iOS, 2026) and PointsCompass (in development). Design, build, backend, store listing, marketing, the lot.", "estate"),
 ("🏢", "Tapcart", "Software Engineer II, iOS", "2021 – 2025", "E-commerce features for 1,500+ Shopify merchants: checkout and payment flows, custom UI, end-to-end ownership with product and design. Helped with the React Native transition.", "stocks"),
 ("🏀", "HoopStop", "iOS Engineer", "2018 – 2021", "Early-stage sports social network. Real-time updates, media uploads, location features. UIKit to SwiftUI migration. Swift, Core Data, Firebase.", "business"),
]
def work(theme):
    cards = "".join(f"""<div class="c"><div class="ic" style="background:var(--{t});color:var(--{t}-ink)">{ic}</div><h3>{co}</h3><div class="role">{role} <span>· {yrs}</span></div><p>{desc}</p></div>""" for ic, co, role, yrs, desc, t in WORK)
    body = f'<div class="stage" style="background:transparent"><div class="g" style="grid-template-columns:repeat(3,1fr)">{cards}</div></div>'
    render("work", theme, 1200, 262, body, CARD_CSS, transparent=True)

BEYOND = [
 ("⚾️", "Sports", "Falcons, USMNT, Knicks, Mets, Giants. Following the games keeps me sharp and competitive.", "stocks"),
 ("🎸", "Guitar", "A Martin acoustic and a slow, happy climb up the fretboard. Where the creative thinking happens.", "business"),
 ("☕️", "Coffee", "Quality coffee, quality code. It's science.", "estate"),
 ("📚", "Curious", "iOS, system design, whatever's next. Always exploring something new.", "bonds"),
]
def beyond(theme):
    cards = "".join(f"""<div class="c"><div class="ic" style="background:var(--{t});color:var(--{t}-ink)">{ic}</div><h3>{h}</h3><p>{d}</p></div>""" for ic, h, d, t in BEYOND)
    body = f'<div class="stage" style="background:transparent"><div class="g" style="grid-template-columns:repeat(4,1fr)">{cards}</div></div>'
    render("beyond", theme, 1200, 236, body, CARD_CSS, transparent=True)

if __name__ == "__main__":
    import sys
    which = sys.argv[1:] or ["hero", "sections", "showcase", "principles", "pills", "footer", "stats", "work", "beyond"]
    for theme in ("light", "dark"):
        if "hero" in which: hero(theme)
        if "sections" in which:
            for n, k, t, s in SECTIONS: section(theme, n, k, t, s)
        if "showcase" in which: showcase(theme)
        if "principles" in which: principles(theme)
        if "pills" in which: pills(theme)
        if "footer" in which: footer(theme)
        if "stats" in which: stats(theme)
        if "work" in which: work(theme)
        if "beyond" in which: beyond(theme)
    # The three opaque, photo-heavy cards ship as JPEG (sips quality 88 reproduces the committed files byte for byte).
    # The footer is a dim room in both themes, so one file serves both.
    def jpeg(src, dst):
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "88", str(OUT / src), "--out", str(OUT / dst)], check=True, capture_output=True)
        print("jpeg", dst)
    for key in ("hero", "showcase", "footer"):
        if key not in which: continue
        name = "understudy" if key == "showcase" else key
        pngs = [f"{name}-{t}.png" for t in ("light", "dark")]
        if key == "footer": jpeg(pngs[1], "footer.jpg")
        else:
            for p in pngs: jpeg(p, p.replace(".png", ".jpg"))
        for p in pngs: (OUT / p).unlink()
