#!/usr/bin/env python3
"""Markers: facts written inline where they are true, and everything built from them.

The pattern is `ops-pattern/process/LIVING-DOCS.md`. Three
inline markers and one file field:

  `[open-question owner=<don|cowork|code> raised=YYYY-MM-DD] question` where raised -> STATUS.md
  `[guards F093.4]` on the check that discharges F093 criterion 4                 -> coverage map
  `[guards F093.4 partial: what it leaves unchecked]` on a check that covers part of one
  `[binds tiers=<planning,code|none> surfaces=<a,b>]` ending a DECISIONS.md line  -> constraints/<tier>.md
      one that binds code names its Issue (#N), its scenario (F###), or says `build=none`
  `[platform <need>[=<topic>][ gap]: what and why]` in product/, a scenario, or DECISIONS.md
      `[platform none]` in a scenario that needs nothing native      -> PLATFORM-IOS.md, PLATFORM-ANDROID.md
  `[replaces 2026-09-22: exact old text]`, `[replaces F059: exact old text]`, `[replaces path.md]`
      on a DECISIONS.md line that supersedes something; the old text must be gone and in git
  `[evidence YYYY-MM-DD from=<source>: what was seen]` on a decision a user's action or words changed
  accepted-risks/*.json "owner" and "review_by"                     -> lint fails once review_by passes
  `gates: launch` in a scenario's frontmatter                       -> its Issues, or none

  python3 scripts/markers.py lint [FILE...]           # default: every tracked file, plus the rest
  python3 scripts/markers.py risks [DIR]              # accepted-risk owners and dates only
  python3 scripts/markers.py index [--code DIR]       # open questions, markdown
  python3 scripts/markers.py coverage [--code DIR] [--summary] [F###...]
  python3 scripts/markers.py constraints [--check]    # write, or diff, constraints/*.md
  python3 scripts/markers.py building [--code DIR]    # is `building` backed by code?
  python3 scripts/markers.py gating                   # does every gating scenario have an Issue?
  python3 scripts/markers.py platform [--check]       # write, or diff, PLATFORM-*.md

A marker inside backticks is a mention, not a marker. `--code` defaults to a
socialus-web checkout beside this repo, read at CODE_REF (origin/main).
"""
import datetime, glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TODAY = datetime.date.today()
OWNERS = ("don", "cowork", "code")
TIERS = ("planning", "code")
BINDS_FROM = datetime.date(2026, 9, 21)  # every decision on or after this date must say what it binds
WEB = "https://github.com/donlafranchi/socialus-web"
CODE_REF = os.environ.get("CODE_REF", "origin/main")
PLANNING = os.environ.get("MARKERS_PLANNING", "planning")  # fixtures point this elsewhere

# Built from pieces so this file never contains a marker of its own.
B = r"\["
OQ = "open-" + "question"
ANY = {
    "oq": re.compile(B + r"open[- ]?question", re.I),
    "guards": re.compile(B + r"guards?(?=[\s\]])", re.I),
    "binds": re.compile(B + r"binds?(?=[\s\]])", re.I),
    "rep": re.compile(B + r"(replac\w*|supersed[\w-]*)", re.I),
    "ev": re.compile(B + r"evidence\b", re.I),
    "plat": re.compile(B + r"platforms?\b", re.I),
}
LIST = r"[a-z0-9-]+(?:,[a-z0-9-]+)*"
FULL_OQ = re.compile(B + OQ + r" owner=(\w+) raised=([0-9-]+)\]")
FULL_GUARDS = re.compile(B + r"guards (F\d{3})\.(\d+[a-z]?)(?: partial: ([^\]]+?))?\]")
FULL_BINDS = re.compile(B + r"binds tiers=(" + LIST + r")(?: surfaces=(" + LIST + r"))?(?: (build=none))?\]")
FULL_PLAT = re.compile(B + r"platform (?:(none)|([a-z]+)(?:=([a-z-]+))?( gap)?: ([^\]]+?))\]")
FULL_REP = re.compile(B + r"replaces (?:(none)|(\d{4}-\d{2}-\d{2}|F\d{3}): ([^\]]+?)|([\w./-]+\.md))\]")
FULL_EV = re.compile(B + r"evidence (\d{4}-\d{2}-\d{2}) from=(\S+): ([^\]]+?)\]")
CLAIM = re.compile(r"\b(revers(e|es|ed|ing)|replac(e|es|ed|ing)|supersed(e|es|ed|ing)|overrul\w*)\b", re.I)
PLATFORM_FROM = datetime.date(2026, 9, 29)  # a scenario approved on or after this carries a platform marker
EVIDENCE_VIEW_BUILT = False  # ops-pattern/process/LIVING-DOCS.md: deferred until the first evidence tag lands
# What a screen or capability can need from a native platform. One list; each platform's view maps it.
NEEDS = ("push", "link", "camera", "photos", "location", "background", "auth", "key", "store")
STORE = ("account-deletion", "sign-in", "ugc", "age-rating", "privacy", "payments")
DECISION = re.compile(r"^- \*\*(\d{4}-\d{2}-\d{2}) — (.+?)\*\*")


def blank_code_spans(line):
    return re.sub(r"`[^`]*`", lambda c: " " * len(c.group()), line)


def parse_line(path, line):
    """Yield (kind, ok, info). info is an error string, or the parsed marker."""
    bare = blank_code_spans(line)
    for m in ANY["oq"].finditer(bare):
        f = FULL_OQ.match(bare, m.start())
        if not f:
            end = bare.find("]", m.start())
            head = bare[m.start(): end + 1 if end != -1 else m.start() + 60]
            missing = [k for k in ("owner=", "raised=") if k not in head]
            yield "oq", False, (f"missing {' and '.join(missing)}" if missing
                                else "not `[" + OQ + " owner=… raised=YYYY-MM-DD]`") + f": {head.strip()}"
            continue
        owner, raised = f.groups()
        if owner not in OWNERS:
            yield "oq", False, f"owner={owner} is not one of {', '.join(OWNERS)}"; continue
        try:
            d = datetime.date.fromisoformat(raised)
        except ValueError:
            yield "oq", False, f"raised={raised} is not a date"; continue
        if d > TODAY:
            yield "oq", False, f"raised={raised} is in the future"; continue
        text = re.sub(r"(\*/|-->)\s*$", "", line[f.end():]).replace("**", "").strip(" *_-—:\t\r\n")
        if not text:
            yield "oq", False, "no question after the marker"; continue
        if os.path.basename(path) == "DECISIONS.md":
            yield "oq", False, "DECISIONS.md holds answers, not questions — mark it where it was raised"; continue
        yield "oq", True, (owner, d, text)
    for m in ANY["guards"].finditer(bare):
        f = FULL_GUARDS.match(bare, m.start())
        if not f:
            yield "guards", False, "not `[guards F###.N]` or `[guards F###.N partial: what it leaves unchecked]` — one criterion per marker"; continue
        yield "guards", True, f.groups()
    for m in ANY["plat"].finditer(bare):
        f = FULL_PLAT.match(bare, m.start())
        if not f:
            yield "plat", False, "not `[platform <need>[=<topic>][ gap]: what and why]` or `[platform none]`"; continue
        none, need, topic, gap, _ = f.groups()
        text = line[f.start(5):f.end(5)] if not none else None  # the detail keeps its code spans
        scen = os.path.basename(path).startswith("scenario-")
        if not (scen or os.path.basename(path) == "DECISIONS.md" or "product/" in path):
            yield "plat", False, "a platform marker lives on a spine entry in product/, a scenario, or a DECISIONS.md line"; continue
        if none:
            yield ("plat", True, None) if scen else ("plat", False, "`[platform none]` is a scenario's assessment — the spine marks only what is needed"); continue
        if need not in NEEDS:
            yield "plat", False, f"need {need} is not one of {', '.join(NEEDS)}"; continue
        if (need == "store") != bool(topic):
            yield "plat", False, f"store names one topic ({', '.join(STORE)}); no other need takes one"; continue
        if topic and topic not in STORE:
            yield "plat", False, f"store topic {topic} is not one of {', '.join(STORE)}"; continue
        yield "plat", True, (need, topic, bool(gap), text.strip())
    for m in ANY["binds"].finditer(bare):
        f = FULL_BINDS.match(bare, m.start())
        if not f:
            yield "binds", False, "not `[binds tiers=<planning,code|none> surfaces=<a,b>]`"; continue
        tiers = f.group(1).split(",")
        surfaces = f.group(2).split(",") if f.group(2) else []
        if os.path.basename(path) != "DECISIONS.md":
            yield "binds", False, "a binds tag lives on a DECISIONS.md line and nowhere else"; continue
        if tiers == ["none"]:
            yield "binds", True, ([], surfaces, False); continue
        bad = [t for t in tiers if t not in TIERS]
        if bad:
            yield "binds", False, f"tier {', '.join(bad)} is not one of {', '.join(TIERS)} (or none)"; continue
        if not surfaces:
            yield "binds", False, "a decision that binds a tier names the surfaces it binds"; continue
        yield "binds", True, (tiers, surfaces, bool(f.group(3)))
    dec = os.path.basename(path) == "DECISIONS.md"
    for m in ANY["rep"].finditer(bare):
        f = FULL_REP.match(bare, m.start())
        if not f:
            yield "rep", False, "not `[replaces YYYY-MM-DD: old text]`, `[replaces F###: old text]`, `[replaces path.md]` or `[replaces none]`"; continue
        if not dec:
            yield "rep", False, "a replaces tag lives on a DECISIONS.md line — a supersession is a ruling"; continue
        yield "rep", True, ("none",) if f.group(1) else ("path", f.group(4)) if f.group(4) else (f.group(2), f.group(3).strip())
    for m in ANY["ev"].finditer(bare):
        f = FULL_EV.match(bare, m.start())
        if not f:
            yield "ev", False, "not `[evidence YYYY-MM-DD from=<source>: what was seen]`"; continue
        try:
            d = datetime.date.fromisoformat(f.group(1))
        except ValueError:
            yield "ev", False, f"{f.group(1)} is not a date"; continue
        if d > TODAY:
            yield "ev", False, f"evidence dated {d} is in the future"; continue
        if not dec:
            yield "ev", False, "an evidence tag lives on the DECISIONS.md line it changed"; continue
        yield "ev", True, f.groups()


def read_lines(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read().splitlines()
    except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
        return []


def tracked():
    out = subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.split()
    return [p for p in out if not p.startswith("scripts/fixtures/")]


def find_code(argv):
    if "--code" in argv:
        i = argv.index("--code"); c = argv[i + 1]; del argv[i:i + 2]
        return c
    for c in (os.environ.get("CODE_REPO", ""), os.path.join(ROOT, "..", "socialus-web"),
              os.path.expanduser("~/Projects/socialus-web")):
        if c and os.path.exists(os.path.join(c, ".git")):
            return os.path.abspath(c)
    return ""


def code_lines(code):
    """(path, n, line) for every marker-bearing line in the code repo at CODE_REF."""
    if not code:
        return None
    r = subprocess.run(["git", "-C", code, "grep", "-n", "-I", "-i", "-E",
                        B + r"(open[- ]?question|guards?[[:space:]]|binds?[[:space:]]|guards?]|binds?])", CODE_REF, "--"],
                       capture_output=True, text=True)
    if r.returncode > 1:
        return None
    rows = []
    for row in r.stdout.splitlines():
        _, path, n, line = row.split(":", 3)
        if not path.startswith("scripts/fixtures/"):
            rows.append((path, int(n), line))
    return rows


# ------------------------------------------------------------------ scenarios
def criteria(fid):
    """Criterion ids of a current scenario, None if the file is gone."""
    lines = read_lines(f"{PLANNING}/scenario-{fid}.md")
    if not lines:
        return None
    out, inside = [], False
    for l in lines:
        if l.startswith("## "):
            inside = l.strip() == "## Acceptance"; continue
        m = re.match(r"^(\d+[a-z]?)\.\s", l)
        if inside and m:
            out.append(m.group(1))
    return out


def ever_existed(fid):
    r = subprocess.run(["git", "log", "--all", "--oneline", "-1", "--", f"planning/scenario-{fid}.md"],
                       capture_output=True, text=True)
    return bool(r.stdout.strip())


def status_of(fid):
    for l in read_lines(f"planning/scenario-{fid}.md")[:12]:
        if l.startswith("status:"):
            return l.split(":", 1)[1].strip()
    return None


def guard_referent_error(fid, crit, partial=None):
    have = criteria(fid)
    if have is None:
        return None if ever_existed(fid) else f"{fid} is not a scenario, now or in history"
    return None if crit in have else f"{fid} has no criterion {crit} (it has {', '.join(have) or 'none'})"


# ---------------------------------------------------------------- decisions
def decisions(path="DECISIONS.md"):
    """One dict per DECISIONS.md entry: line, date, headline, binds, replaces, evidence."""
    out = []
    for n, l in enumerate(read_lines(path), 1):
        m = DECISION.match(l)
        if not m:
            continue
        found = [(k, info) for k, ok, info in parse_line(path, l) if ok]
        out.append({"n": n, "date": m.group(1), "headline": m.group(2).strip().rstrip("."),
                    "binds": next((i for k, i in found if k == "binds"), None),
                    "reps": [i for k, i in found if k == "rep"],
                    "evidence": [i for k, i in found if k == "ev"], "line": l})
    return out


def in_history(path, text=None):
    args = ["git", "log", "--all", "--oneline", "-1"] + ([f"-S{text}"] if text else []) + ["--", path]
    return bool(subprocess.run(args, capture_output=True, text=True).stdout.strip())


def replace_errors(path):
    """A decision that replaces something names it, and the thing named is gone from the live file."""
    lines, errs, real = read_lines(path), [], path == "DECISIONS.md"
    live = "\n".join(re.sub(B + r"replaces [^\]]*\]", "", l) for l in lines)
    for e in decisions(path):
        for ref in e["reps"]:
            if ref[0] == "none":
                continue
            where = f"{path}:{e['n']}"
            if ref[0] == "path":
                if os.path.exists(ref[1]):
                    errs.append(f"{where}: replaces {ref[1]}, which still exists — delete it; git holds it")
                elif real and not in_history(ref[1]):
                    errs.append(f"{where}: replaces {ref[1]}, which never existed")
                continue
            target, text = ref
            if target.startswith("F"):
                sp = f"{PLANNING}/scenario-{target}.md"
                if text in "\n".join(read_lines(sp)):
                    errs.append(f"{where}: replaces text still live in {sp} — prune it")
                elif real and not in_history(f"planning/scenario-{target}.md", text):
                    errs.append(f"{where}: replaces text {target} never held — nothing to find in git")
            else:
                if text in live:
                    errs.append(f"{where}: replaces {target}: {text[:40]}…, which is still in {path} — delete it; git holds it")
                elif real and not in_history(path, text):
                    errs.append(f"{where}: replaces {target}: {text[:40]}…, which {path} never held — nothing to find in git")
    return errs


def render_constraints(tier):
    ds = decisions()
    rows = [e for e in ds if e["binds"] and tier in e["binds"][0]]
    untagged = sum(1 for e in ds if e["binds"] is None)
    o = [f"# CONSTRAINTS — {tier} tier", "",
         "> **Generated by `python3 scripts/markers.py constraints` — never edit this file.** A hand edit is",
         "> lost on the next run, and `scripts/lint.sh` fails whenever this file differs from what",
         "> `DECISIONS.md` generates. To change it, change the `[binds …]` tag on the decision.",
         ">",
         f"> Every ratified decision whose tag binds the **{tier}** tier, newest first. `DECISIONS.md` holds",
         "> only live decisions — a superseded one is deleted — so nothing below conflicts with anything",
         "> else here. If two lines ever seem to, the newer wins (`[newer-decision-wins]`).",
         f"> **{untagged} older decisions carry no tag yet and are not listed** — tagging is required from",
         f"> {BINDS_FROM.isoformat()} onward. Absent here is not the same as not binding.", ""]
    o += [f"- **{e['date']}** · {', '.join(e['binds'][1])} — {e['headline']}" for e in rows] or ["None tagged."]
    return "\n".join(o) + "\n"


# ---------------------------------------------------------------- platform
# The one place the two platforms differ. The markers say what a thing needs; this says what that need
# costs on each platform. A third platform is a third column, not a third inventory.
NATIVE = {
    "push": ("APNs, the Push Notifications capability, a runtime permission prompt, and a server that sends.",
             "FCM, the POST_NOTIFICATIONS runtime permission on Android 13 and later, and a server that sends."),
    "link": ("Universal Links: `apple-app-site-association` served at `/.well-known/` on the site, plus the "
             "Associated Domains entitlement.",
             "App Links: `assetlinks.json` served at `/.well-known/` on the site, plus an `autoVerify` intent filter."),
    "camera": ("`NSCameraUsageDescription` in Info.plist.", "The CAMERA permission, or hand off to the camera app with no permission."),
    "photos": ("PHPicker needs no permission. `NSPhotoLibraryUsageDescription` is needed only for full-library access.",
               "The system Photo Picker needs no permission. Legacy media permissions are needed only for full-library access."),
    "location": ("`NSLocationWhenInUseUsageDescription`, and a prompt the member can refuse.",
                 "ACCESS_COARSE_LOCATION (fine only if it is needed), and a prompt the member can refuse."),
    "background": ("BGTaskScheduler. The OS decides when it runs, and it may never run.",
                   "WorkManager. It is deferred under Doze."),
    "auth": ("ASWebAuthenticationSession, returning through a Universal Link or a custom scheme. The PKCE verifier "
             "must live in the Keychain, not a cookie.",
             "Custom Tabs, returning through an App Link or a custom scheme. The PKCE verifier must live in "
             "EncryptedSharedPreferences, not a cookie."),
    "key": ("The same publishable key ships inside the app bundle and is as extractable as it is from the web bundle.",
            "The same publishable key ships inside the APK and is as extractable as it is from the web bundle."),
}
STORE_RULE = {  # (iOS, Android); None means that store does not require it
    "account-deletion": ("App Review 5.1.1(v): an app that lets people create an account must let them delete it from inside the app.",
                         "Play User Data policy: delete the account in the app, and from a web link listed in the Play Console."),
    "sign-in": ("App Review 4.8: an app offering a third-party sign-in such as Google must also offer Sign in with Apple, or an equivalent privacy-preserving option.",
                None),
    "ugc": ("App Review 1.2: an app with member content needs a filter, a way to report content, a way to block abusive members, and published contact details.",
            "Play User-Generated Content policy: in-app reporting, a way to block users, and moderation that acts on reports."),
    "age-rating": ("The App Store Connect age-rating questionnaire. Unrestricted member content and an open web view both raise the rating.",
                   "The IARC content-rating questionnaire in the Play Console."),
    "privacy": ("App Review 5.1.1(i): a privacy-policy URL in the listing and in the app, plus the App Privacy label.",
                "A privacy-policy URL, plus the Data safety form in the Play Console."),
    "payments": ("App Review 3.1.1: digital goods or features unlocked inside the app go through in-app purchase. Physical goods and services between people are exempt (3.1.3(e)).",
                 "Play Payments policy: the same line, with digital goods through Play Billing."),
}
PLATFORMS = {"ios": ("iOS", "App Store", 0), "android": ("Android", "Google Play", 1)}


def platform_sources():
    files = sorted(set(glob.glob("product/**/*.md", recursive=True) + glob.glob("planning/scenario-F*.md") + ["DECISIONS.md"]))
    return [(p, n, i) for p in files for n, i in platform_marks(p)]


def render_platform(key):
    name, store, col = PLATFORMS[key]
    other = [v[0] for k, v in PLATFORMS.items() if k != key][0]
    marks = [(p, n, i) for p, n, i in platform_sources() if i]
    where = lambda p, n: f"[{p}]({p})"  # no line number: an edit above a marker must not stale the view
    def item(p, n, i):
        scen = os.path.basename(p).startswith("scenario-")
        tag = f" · *{os.path.basename(p)[9:13]}, {status_of(os.path.basename(p)[9:13])} — decided, not built*" if scen else ""
        return f"- {'**GAP** · ' if i[2] else ''}{i[3]} — {where(p, n)}{tag}"
    o = [f"# PLATFORM — {name}", "",
         "> **Generated by `python3 scripts/markers.py platform`. Never edit this file.** A hand edit is lost on the",
         "> next run, and `scripts/lint.sh` fails whenever this file differs from what the markers generate. To",
         "> change it, change a `[platform …]` marker where the fact is true: a spine entry in `product/`, a",
         "> scenario, or a `DECISIONS.md` line. Pattern: `ops-pattern/process/LIVING-DOCS.md` § Platform readiness.",
         ">",
         f"> **One set of markers, one view per platform.** This file and `PLATFORM-{other.upper()}.md` are built",
         "> from the same markers and differ only in what each need costs on each platform. That mapping is a",
         "> table in `scripts/markers.py`. Nobody keeps an inventory for either platform.", ""]
    keys = [(p, n, i) for p, n, i in marks if i[0] == "key"]
    o += ["## Rulings a native client inherits unchanged", "",
          f"**A native {name} app ships the publishable key exactly as the web bundle does.** The rulings below were",
          "written assuming a web client that hands the key to anyone, and **they apply to the app without change**.",
          "The only boundary is what `anon` and `authenticated` may select in SQL. No app, like no component, is",
          f"a place to enforce privacy. {NATIVE['key'][col]}", ""]
    o += [item(*m) for m in keys] or ["None marked."]
    gaps = [m for m in marks if m[2][2] and not (m[2][0] == "store" and STORE_RULE[m[2][1]][col] is None)]
    o += ["", f"## Gaps: {len(gaps)}", "",
          "What a native build or a store review needs and the code does not have today. Each is marked `gap`",
          "where it is true; the gap is gone when its marker is.", ""]
    o += [item(*m) for m in gaps] or ["None marked."]
    o += ["", f"## {store} review", ""]
    for topic, rules in STORE_RULE.items():
        rule = rules[col]
        mine = [m for m in marks if m[2][0] == "store" and m[2][1] == topic]
        o.append(f"**{topic}** · " + (rule if rule else f"{store} has no such requirement; the markers below are for {other}."))
        o += [item(*m) for m in mine] or ([f"- **NOT ASSESSED.** No marker says how this is met or that it is not."] if rule else [])
        o.append("")
    o += ["## By need", ""]
    for need in NEEDS:
        if need in ("key", "store"):
            continue
        mine = [m for m in marks if m[2][0] == need]
        o.append(f"**{need}** · {NATIVE[need][col]}")
        o += [item(*m) for m in mine] or ["- Nothing marked as needing it."]
        o.append("")
    scen = [os.path.basename(p)[9:13] for p in sorted(glob.glob("planning/scenario-F*.md")) if status_of(os.path.basename(p)[9:13]) in ("approved", "building")]
    unassessed = [f for f in scen if not platform_marks(f"planning/scenario-{f}.md")]
    o += ["## Scenarios not yet assessed", "",
          f"**{len(unassessed)} of {len(scen)} approved and building scenarios carry no platform marker**, so what they will",
          f"need from a native platform is unknown, not none. Every scenario approved from {PLATFORM_FROM} on must carry one;",
          "the lint fails one that does not. The older ones are the retro-scan deferred in `ops-pattern/process/LIVING-DOCS.md`.", "",
          (", ".join(unassessed) or "None.")]
    return "\n".join(o) + "\n"


# ------------------------------------------------------------------- risks
def risk_errors(directory="accepted-risks"):
    errs = []
    for path in sorted(glob.glob(os.path.join(directory, "*.json"))):
        try:
            e = json.load(open(path))
        except Exception as x:
            errs.append((path, f"not valid JSON — {x}")); continue
        if e.get("owner") not in OWNERS:
            errs.append((path, f"owner={e.get('owner')!r} — must be one of {', '.join(OWNERS)}"))
        try:
            due = datetime.date.fromisoformat(e.get("review_by") or "")
        except ValueError:
            errs.append((path, f"review_by={e.get('review_by')!r} is not a date")); continue
        if due < TODAY:
            errs.append((path, f"review_by {due} has passed — argue it again (a new DECISIONS.md line and a "
                               f"new date) or delete the entry"))
    return errs


def code_ruling_error(line):
    """A ruling that binds code and names no work is a ruling nobody will build (the identity leaks sat
    eight days so). It names its Issue, or its scenario, or says `build=none`."""
    bare = re.sub(B + r"[^\]]*\]", "", line)
    if re.search(r"(?<![\w&])#\d+", bare):
        return None
    fids = re.findall(r"\bF\d{3}\b", bare)
    if any(criteria(f) is not None or ever_existed(f) for f in fids):
        return None
    if fids:
        return f"binds code and names {', '.join(fids)}, which never existed — name its Issue (#N)"
    return ("binds code and names no `socialus-web` Issue (#N) or scenario (F###) — open the Issue, "
            "or add `build=none` to the tag if it governs conduct and there is nothing to build")


def approved_on(path):
    for l in read_lines(path)[:15]:
        m = re.match(r"approved:\s*(\d{4}-\d{2}-\d{2})", l)
        if m:
            return datetime.date.fromisoformat(m.group(1))
    return None


def platform_marks(path):
    return [(n, i) for n, l in enumerate(read_lines(path), 1) for k, ok, i in parse_line(path, l) if k == "plat" and ok]


def platform_scenario_error(path):
    st = next((l.split(":", 1)[1].strip() for l in read_lines(path)[:12] if l.startswith("status:")), None)
    d = approved_on(path)
    if st in ("approved", "building") and d and d >= PLATFORM_FROM and not platform_marks(path):
        return (f"approved {d} with no platform marker — say what it needs from a native platform, "
                "`[platform <need>: …]`, or `[platform none]`")
    return None


# -------------------------------------------------------------------- lint
def lint(files):
    errs = []
    for p in files:
        for n, l in enumerate(read_lines(p), 1):
            found = list(parse_line(p, l))
            for kind, ok, info in found:
                if not ok:
                    errs.append(f"{p}:{n}: {info}")
                elif kind == "guards":
                    e = guard_referent_error(*info)
                    if e:
                        errs.append(f"{p}:{n}: {e}")
            if n < 15 and os.path.basename(p).startswith("scenario-") and l.startswith("gates:") \
                    and l.split(":", 1)[1].strip() != "launch":
                errs.append(f"{p}:{n}: `gates:` names what the scenario gates — the only gate is `launch`")
            if os.path.basename(p) == "DECISIONS.md":
                m = DECISION.match(l)
                if m and datetime.date.fromisoformat(m.group(1)) >= BINDS_FROM:
                    if not any(k == "binds" for k, _, _ in found):
                        errs.append(f"{p}:{n}: a decision from {BINDS_FROM} on must end with a `[binds …]` tag")
                    binds = next((i for k, ok, i in found if k == "binds" and ok), None)
                    if binds and "code" in binds[0] and not binds[2]:
                        err = code_ruling_error(l)
                        if err:
                            errs.append(f"{p}:{n}: {err}")
                    prose = re.sub(B + r"[^\]]*\]", "", blank_code_spans(l))
                    if CLAIM.search(prose) and not any(k == "rep" for k, _, _ in found):
                        errs.append(f"{p}:{n}: says it {CLAIM.search(prose).group(0).lower()} something but names nothing — "
                                    "add `[replaces …]`, or `[replaces none]` if the word is not a supersession")
        if os.path.basename(p).startswith("scenario-"):
            err = platform_scenario_error(p)
            if err:
                errs.append(f"{p}: {err}")
        if os.path.basename(p) == "DECISIONS.md":
            errs += replace_errors(p)
            if not EVIDENCE_VIEW_BUILT and any(e["evidence"] for e in decisions(p)) and p == "DECISIONS.md":
                errs.append(f"{p}: the first `[evidence …]` tag has landed — build the evidence view deferred in "
                            "ops-pattern/process/LIVING-DOCS.md, then set EVIDENCE_VIEW_BUILT")
    return errs


def main():
    argv = sys.argv[1:]
    mode = argv.pop(0) if argv else ""

    if mode == "lint":
        errs = lint(argv or tracked())
        if not argv:
            errs += [f"{p}: {e}" for p, e in risk_errors()]
            # socialus-web's CI checks its markers' grammar but cannot see this private repo, so the
            # claims its checks make about scenarios are checked here, whenever a checkout is at hand.
            for path, n, l in code_lines(find_code([])) or []:
                for kind, ok, info in parse_line(path, l):
                    e = kind == "guards" and ok and guard_referent_error(*info)
                    if e:
                        errs.append(f"socialus-web {path}:{n}: {e}")
            for tier in TIERS:
                path = f"constraints/{tier}.md"
                if not os.path.exists(path) or open(path).read() != render_constraints(tier):
                    errs.append(f"{path}: stale or missing — a decision binds this tier and the file does not "
                                f"say so. Run `python3 scripts/markers.py constraints`")
            for k in PLATFORMS:
                path = f"PLATFORM-{PLATFORMS[k][0].upper()}.md"
                if not os.path.exists(path) or open(path).read() != render_platform(k):
                    errs.append(f"{path}: stale or missing — a platform marker changed. Run `python3 scripts/markers.py platform`")
            for path in ["STATUS.md", "README.md"] + [f"constraints/{t}.md" for t in TIERS] + [f"PLATFORM-{v[0].upper()}.md" for v in PLATFORMS.values()]:
                head = "\n".join(read_lines(path)[:8])
                if head and not (re.search(r"generated", head, re.I)
                                 and re.search(r"never (hand-)?edit|hand-edit is lost", head, re.I)):
                    errs.append(f"{path}: a generated file must say in its own header that it is generated and never edited")
        for e in errs:
            print(f"markers: {e}")
        sys.exit(1 if errs else 0)

    if mode == "platform":
        if "--gaps" in argv:
            for k, (name, _, col) in PLATFORMS.items():
                print(k, sum(1 for p, n, i in platform_sources() if i and i[2]
                             and not (i[0] == "store" and STORE_RULE[i[1]][col] is None)))
            return
        stale = []
        for k, v in PLATFORMS.items():
            path, body = f"PLATFORM-{v[0].upper()}.md", render_platform(k)
            if (open(path).read() if os.path.exists(path) else None) != body:
                stale.append(path)
                if "--check" not in argv:
                    open(path, "w").write(body)
        if "--check" in argv:
            for p in stale:
                print(f"markers: {p} is stale")
            sys.exit(1 if stale else 0)
        print("\n".join(f"wrote {p}" for p in stale) or "platform: unchanged")
        return

    if mode == "risks":
        errs = risk_errors(argv[0] if argv else "accepted-risks")
        for p, e in errs:
            print(f"markers: {p}: {e}")
        sys.exit(1 if errs else 0)

    if mode == "constraints":
        stale = []
        for tier in TIERS:
            path, body = f"constraints/{tier}.md", render_constraints(tier)
            if (open(path).read() if os.path.exists(path) else None) != body:
                stale.append(path)
                if "--check" not in argv:
                    os.makedirs("constraints", exist_ok=True)
                    open(path, "w").write(body)
        if "--check" in argv:
            for p in stale:
                print(f"markers: {p} is stale")
            sys.exit(1 if stale else 0)
        print("\n".join(f"wrote {p}" for p in stale) or "constraints: unchanged")
        return

    code = find_code(argv)
    rows = code_lines(code)
    only = os.environ.get("MARKERS_SOURCES")  # fixtures: scan these files and nothing else
    sources = [((p, "local"), n, l) for p in (only.split() if only else tracked()) for n, l in enumerate(read_lines(p), 1)]
    gaps = []
    if only:
        rows = []
    if rows is None:
        gaps.append(f"the `socialus-web` code at `{CODE_REF}`" + ("" if code else " — no checkout"))
    else:
        sources += [((p, "code"), n, l) for p, n, l in rows]

    def link(where, n):
        path, kind = where
        if kind == "local":
            return f"[{path}:{n}]({path}#L{n})"
        if kind == "code":
            return f"[socialus-web {path}:{n}]({WEB}/blob/main/{path}#L{n})"
        return f"[{path}]({WEB}/issues/{path[1:]})"

    if mode == "index":
        r = subprocess.run(["gh", "issue", "list", "-R", "donlafranchi/socialus-web", "--state", "open",
                            "--limit", "1000", "--json", "number,body"], capture_output=True, text=True)
        if r.returncode == 0:
            for issue in json.loads(r.stdout):
                for n, l in enumerate((issue["body"] or "").splitlines(), 1):
                    sources.append(((f"#{issue['number']}", "issue"), n, l))
        else:
            gaps.append("open `socialus-web` Issues — `gh` could not read them")
        good, bad = [], []
        for where, n, l in sources:
            for kind, ok, info in parse_line(where[0], l):
                if kind == "oq":
                    (good if ok else bad).append((where, n, info))
        good.sort(key=lambda g: (g[2][1], g[2][0]))
        print("## Open questions\n")
        print("Every open-question marker, found by scanning — nobody maintains this list.")
        print("Oldest first. Rule and grammar: `ops-pattern/process/PIPELINE.md` § Open questions.\n")
        if not good:
            print("None marked.")
        labels = {"don": "Waiting on Don", "cowork": "Cowork owes an answer", "code": "Code owes an answer"}
        for owner in OWNERS:
            mine = [g for g in good if g[2][0] == owner]
            if mine:
                print(f"\n**{labels[owner]}** ({len(mine)})\n")
                for where, n, (_, d, text) in mine:
                    short = text if len(text) <= 160 else text[:157].rstrip() + "…"
                    if short.count("`") % 2:
                        short = short.replace("`", "")
                    print(f"- {(TODAY - d).days}d · {short} — {link(where, n)}")
        if bad:
            print("\n**Malformed — the lint gates this repo only, so these slipped through:**\n")
            for where, n, err in bad:
                print(f"- {link(where, n)} — {err}")
        if gaps:
            print("\n**Not scanned this run:** " + "; ".join(gaps) + ".")
        return

    if mode == "coverage":
        summary = "--summary" in argv
        wanted = [a for a in argv if re.fullmatch(r"F\d{3}", a)]
        claims, dangling = {}, []
        for where, n, l in sources:
            for kind, ok, info in parse_line(where[0], l):
                if kind == "guards" and ok:
                    e = guard_referent_error(*info)
                    if e:
                        dangling.append((where, n, e))
                    else:
                        claims.setdefault(info[:2], []).append((where, n, info[2]))

        def state(f, c):
            """covered: a check claims all of it. partial: checks claim only parts, and parts never add up."""
            cs = claims.get((f, c), [])
            return "covered" if any(p is None for *_, p in cs) else "partial" if cs else "unclaimed"

        scen = sorted(os.path.basename(p)[9:13] for p in glob.glob(f"{PLANNING}/scenario-F*.md"))
        scen = [f for f in scen if f in wanted or (not wanted and status_of(f) in ("approved", "building"))]
        unmarked = [f for f in scen if not any(state(f, c) != "unclaimed" for c in criteria(f) or [])]
        if "--count" in argv:
            print(len(unmarked), len(scen)); return
        if summary:
            print("## Guard coverage\n")
            print(f"**{len(unmarked)} of {len(scen)} approved and building scenarios are unverified — no check is marked")
            print("as discharging any criterion of theirs, so a contradiction in them cannot surface here.** Unmarked")
            print("is unverified, not verified: nothing says a check exists, and under `[guard-proves-itself]` that")
            print("counts as absent. A **partial** criterion has checks that cover only part of it, named with what")
            print("they leave out; parts never add up to covered. Full map: `python3 scripts/markers.py coverage`.\n")
            for f in scen:
                if f in unmarked:
                    continue
                cs = criteria(f) or []
                by = {k: [c for c in cs if state(f, c) == k] for k in ("covered", "partial", "unclaimed")}
                print(f"- **{f}** · {len(by['covered'])} of {len(cs)} covered"
                      + (f" · **partial: {', '.join(by['partial'])}**" if by["partial"] else "")
                      + (f" · unclaimed: {', '.join(by['unclaimed'])}" if by["unclaimed"] else ""))
            if unmarked:
                print(f"- **Unverified — no marked check at all** ({len(unmarked)}): {', '.join(unmarked)}")
        else:
            for f in scen:
                print(f"## {f} ({status_of(f)})\n")
                for c in criteria(f) or []:
                    cs, st = claims.get((f, c), []), state(f, c)
                    full = [(w, n) for w, n, p in cs if p is None]
                    part = [(w, n, p) for w, n, p in cs if p is not None]
                    if st == "unclaimed":
                        print(f"- **{c}** — **no marked check**"); continue
                    cells = [link(w, n) for w, n in full] + [f"{link(w, n)} (leaves out: {p})" for w, n, p in part]
                    print(f"- **{c}** — " + ("**partial** — " if st == "partial" else "") + "; ".join(cells))
                print()
        if dangling:
            print("\n**Markers pointing at nothing:**\n")
            for where, n, e in dangling:
                print(f"- {link(where, n)} — {e}")
        if gaps:
            print("\n**Not scanned this run:** " + "; ".join(gaps) + ".")
        return

    if mode == "building":
        print("## Is `building` backed by code?\n")
        print("Each scenario whose frontmatter says `building`, against what names it in `socialus-web`: commits")
        print("and files on main, and branches. Frontmatter is a claim; this is the evidence.\n")
        for p in sorted(glob.glob("planning/scenario-F*.md")):
            f = os.path.basename(p)[9:13]
            if status_of(f) != "building":
                continue
            if not code:
                print(f"- **{f}** · not checked — no `socialus-web` checkout"); continue
            run = lambda *a: subprocess.run(["git", "-C", code, *a], capture_output=True, text=True).stdout.count("\n")
            commits = run("log", CODE_REF, "--oneline", "-i", f"--grep={f}")
            files = run("grep", "-l", f, CODE_REF, "--")
            branches = run("branch", "-r", "--list", f"origin/{f.lower()}-*")
            plural = lambda n, w, s="s": f"{n} {w}{s * (n != 1)}"
            print(f"- **{f}** · " + ("**nothing in the code names it** — no commit, file or branch" if not (commits or files or branches)
                  else f"{plural(commits, 'commit')} on main · {plural(files, 'file')} naming it · {plural(branches, 'branch', 'es')}"))
        return

    if mode == "gating":
        print("## Gating launch — does each have an Issue?\n")
        print("Every scenario whose frontmatter says `gates: launch`, against the `socialus-web` Issues")
        print("naming it. Five approved gating scenarios once had none, and nothing noticed.\n")
        r = subprocess.run(["gh", "issue", "list", "-R", "donlafranchi/socialus-web", "--state", "all",
                            "--limit", "1000", "--json", "number,title,state"], capture_output=True, text=True)
        issues = json.loads(r.stdout) if r.returncode == 0 else None
        for p in sorted(glob.glob("planning/scenario-F*.md")):
            f = os.path.basename(p)[9:13]
            if not any(l.strip() == "gates: launch" for l in read_lines(p)[:15]):
                continue
            if issues is None:
                print(f"- **{f}** · not checked — `gh` could not read Issues"); continue
            mine = [i for i in issues if re.match(rf"{f}\b", i["title"])]
            st = status_of(f)
            print(f"- **{f}** ({st}) · " + (", ".join(f"#{i['number']} {i['state'].lower()}" for i in mine) if mine
                  else "**no Issue**" + (" — approved and gating launch with nothing to build from" if st in ("approved", "building") else "")))
        # A ruling that binds code gates the code as surely as a scenario does. The lint fails one that names
        # no Issue, scenario or `build=none`; this says whether the Issues it names exist.
        code = [e for e in decisions() if e["binds"] and "code" in e["binds"][0]]
        exempt = [e for e in code if e["binds"][2]]
        print(f"\n**Rulings that bind code: {len(code)}.** Each names its Issue or scenario, or says it has nothing to build;")
        print("the lint fails one that does none of the three — the identity leaks sat eight days with no Issue.\n")
        if issues is not None:
            prs = subprocess.run(["gh", "pr", "list", "-R", "donlafranchi/socialus-web", "--state", "all", "--limit", "1000",
                                  "--json", "number"], capture_output=True, text=True)
            known = {i["number"] for i in issues} | {i["number"] for i in (json.loads(prs.stdout) if prs.returncode == 0 else [])}
            for e in code:
                gone = [n for n in map(int, re.findall(r"(?<![\w&])#(\d+)", re.sub(B + r"[^\]]*\]", "", e["line"]))) if n not in known]
                if gone:
                    print(f"- **{e['date']}** {e['headline'][:90]} — names {', '.join(f'#{n}' for n in gone)}, **which is no `socialus-web` Issue or PR**")
        print(f"- **Nothing to build** ({len(exempt)}), by their own tag: " + "; ".join(f"{e['date']} {e['headline'].replace('`', '')[:60]}…" for e in exempt))
        return

    print(__doc__, file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
