# Seed: devpost-submission-writer skill

Paste this entire file into Claude Code from inside the (empty) repo where you want the
skill to live. It will create an agent skill — a `SKILL.md` plus supporting script,
reference, and template — and wire everything up. The file contents below are exact;
reproduce them verbatim at the given paths.

---

## Task

1. Create the following files at exactly these paths, with exactly the content shown.
2. `chmod +x scripts/analyze_repo.py`.
3. Smoke-test: run `python scripts/analyze_repo.py .` from the repo root and confirm it
   prints a "REPO BRIEF" without error (it will analyze this repo itself).
4. `git init`, add everything, and commit with the message `Add devpost-submission-writer skill`.
5. Do **not** create a remote or push automatically — stop after the commit and tell me the
   publish commands so I can run them when I'm ready.

---

## File: `README.md`

````markdown
# devpost-submission-writer

A Claude **agent skill** that turns a hackathon project repo into a complete,
paste-ready Devpost submission — drafting every field (Inspiration, What it does,
How we built it, Challenges, Accomplishments, What we learned, What's next, Built With,
tagline) to the standard that actually places.

## Why
Writing the Devpost submission is the tax at the end of every hackathon: you're out of
time and you'd rather be polishing the demo. The two ways auto-written submissions fail
are (1) inventing a tech stack or features the repo doesn't have — which judges catch the
moment they open the repo — and (2) generic AI slop that gets mentally discounted. This
skill avoids both by reading the **actual repo** for the true stack and build story, then
writing specific, honest copy in the team's voice.

## How it works
1. `scripts/analyze_repo.py` reads the repo's dependency manifests, git history, and README
   to produce a *verified* "Built With" list, a real build time, the commit-history story
   (great raw material for the Challenges section), and any demo links.
2. The skill drafts each Devpost field to the quality bar in `references/winning-submissions.md`
   (field-by-field guide + a banned-phrases list so it doesn't read like a language model).
3. It outputs the `assets/devpost-template.md` skeleton, filled, plus a pre-submit checklist
   (demo video, public repo, accurate tags, sponsor-prize requirements, teammates added).

## Files
- `SKILL.md` — the skill definition and workflow.
- `scripts/analyze_repo.py` — verified stack + build-story extractor (stdlib only, no install).
- `references/winning-submissions.md` — the quality bar: field guide, banned phrases, honesty rules.
- `assets/devpost-template.md` — paste-ready output skeleton + pre-submit checklist.

## Quickstart
```bash
python scripts/analyze_repo.py /path/to/your/hackathon/repo
```
Then, with Claude using this skill: "Write my Devpost submission for the repo at <path>."

## A note on honesty
The skill articulates real work; it does not fabricate it. If the repo doesn't do what a
claim would say, it writes the honest version — a writeup that overpromises against a repo
judges can read hurts more than it helps.
````

---

## File: `SKILL.md`

````markdown
---
name: devpost-submission-writer
description: Write a complete, paste-ready Devpost project submission from a code repo plus a few notes — drafting every standard field (Inspiration, What it does, How we built it, Challenges, Accomplishments, What we learned, What's next, Built With, tagline) to the quality bar that actually places at hackathons. Use this whenever someone needs to write, draft, or polish a hackathon submission, Devpost writeup, project description, or "submission story" — or says things like "I need to submit my project", "help me write the Devpost", "we have 30 minutes before the deadline", or "turn my repo into a submission." Also use to map a project to judging criteria or sponsor-prize requirements. Pulls the real tech stack and build story straight from the repo so the writeup is accurate, specific, and not AI slop.
---

# Devpost submission writer

Writing the Devpost submission is the tax at the end of every hackathon: you're exhausted,
the deadline is close, and the writeup eats time you'd rather spend polishing the demo. This
skill does the heavy lifting — it reads the project's repo for the true stack and build
story, then drafts every field to the standard that actually places, so the hacker mostly
just edits and pastes.

The two failure modes to avoid above all: (1) **inventing things** — a stack, a feature, a
metric the repo doesn't support, which judges catch the second they open the repo; and (2)
**AI slop** — generic, hype-filled prose that reads as machine-written and gets discounted.
Stay specific, stay honest, keep the team's voice.

## Workflow

### 1. Gather inputs (ask for what's missing, but ask little)

The goal is to extract maximum signal with minimum typing from the user. Ideal inputs:

- **The repo** — a local path or a GitHub URL. This is the richest source; get it if at all
  possible. It yields the verified stack, build time, and real challenges.
- **A few notes** — one or two lines on what the project does and who it's for. If the README
  already covers this, you may not need to ask.
- **(Optional but high-value) the judging rubric and/or sponsor prize list** — so the draft
  can be tailored to what's actually being scored.

If you only have a repo and no notes, draft from the repo and the README, then ask the user
to correct the *What it does* section — don't invent a purpose. If you have neither repo nor
notes, ask for at least a two-sentence description of what the project does and the stack
before drafting.

### 2. Analyze the repo

Run the analyzer to get verified signal (stack, languages, build stats, commit subjects,
demo links). It's stdlib-only Python:

```bash
python scripts/analyze_repo.py /path/to/repo        # local clone (fullest output)
python scripts/analyze_repo.py https://github.com/owner/name   # public repo via API
```

Use the **`built_with_tags`** verbatim for the Built With field — these are read from actual
dependency manifests, so they're true. Mine the **commit subjects** for the *Challenges* and
*What we learned* sections (a "fix CORS" or "cache audio to save budget" commit is a real
story, already written). Use **build stats** ("built in ~17 hours") as honest, credible
detail. Capture any **demo links** for the Try-it-out field and the checklist.

If the repo can't be analyzed (private, no access, API rate-limited), ask the user to paste
their `package.json` / `requirements.txt` (or just list the stack), and proceed.

### 3. Draft every field to the quality bar

Read `references/winning-submissions.md` before drafting — it has the field-by-field guide,
the banned-phrases list, and before/after examples. The essentials:

- **Specific beats grand; honest beats impressive; human beats hollow.**
- Lead with user-facing outcomes, not tech.
- Use only verified tech. Describe only features that exist.
- No banned phrases (no "seamlessly", "revolutionize", "in today's fast-paced world", etc.).
- Keep it skimmable and in the team's voice.

Fill the structure in `assets/devpost-template.md`, keeping the field headers exactly so they
map onto Devpost's form.

### 4. Tailor to judging criteria and sponsor prizes (if provided)

Tailor without lying. Give each judging axis (Technical Difficulty, Originality, Polish,
Impact, Demo) at least one concrete hook in the writeup. For each sponsor prize the project
could enter, make sure the relevant API/tool usage is stated plainly in *What it does* and
*How we built it* (that's where prize matchers look) — and tell the user honestly which
prizes are a real fit versus a stretch. Never inflate trivial usage into a prize claim.

### 5. Self-check, then deliver

Before handing it over, reread the draft and check:

- Would every claim survive a judge opening the repo? Cut anything that wouldn't.
- Any banned phrase or generic sentence that could belong to any other project? Rewrite it.
- Is every Built With tag actually used?
- Does it sound like a person on this team wrote it?

Deliver the filled template as one paste-ready block, then run the **pre-submit checklist**
from `assets/devpost-template.md` and flag anything missing — especially a **demo video**,
which is the highest-leverage asset and a common gap. If there's no video yet, offer the
30-second shot list.

## Files in this skill

- `scripts/analyze_repo.py` — extracts verified stack, build stats, commit-history story, and
  demo links from a local repo path or GitHub URL. Stdlib only.
- `references/winning-submissions.md` — field-by-field quality guide, banned phrases, honesty
  and prize-alignment rules, before/after examples. Read before drafting.
- `assets/devpost-template.md` — the exact paste-ready field skeleton plus a pre-submit
  checklist (demo video, public repo, accurate tags, sponsor requirements, teammates added).

## A note on scope and honesty

This skill writes submissions for projects the user actually built; it shapes and articulates
real work, it does not fabricate it. If the repo is empty or the project doesn't do what the
user wants to claim, say so and help them write an honest version rather than an impressive
fictional one — a writeup that overpromises against a repo judges can read hurts more than it
helps.
````

---

## File: `scripts/analyze_repo.py`

````python
#!/usr/bin/env python3
"""
analyze_repo.py — Extract submission-relevant signal from a hackathon project repo.

The point of this script is to do the boring, deterministic part of a Devpost
submission so the writer (you) doesn't have to: figure out the real tech stack from
dependency manifests, summarize the README, and pull build stats from git history.
LLMs hallucinate tech stacks ("Built with TensorFlow!" when there's no TF anywhere);
this reads the actual manifests so the "Built With" tags are TRUE. Judges click the
repo — accuracy here is what keeps a submission from getting dinged.

Usage:
    python analyze_repo.py /path/to/local/repo
    python analyze_repo.py https://github.com/owner/name        # uses public GitHub API
    python analyze_repo.py /path/to/repo --json                 # raw JSON only

Output: a human-readable "repo brief" plus a JSON block. Feed the JSON back into the
SKILL.md workflow. Stdlib only — no install needed (works at 4am on conference wifi).
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from collections import Counter
from datetime import datetime

# ----------------------------------------------------------------------------
# Dependency name -> human-facing "Built With" tag. Devpost tags are the things
# judges scan for sponsor-prize eligibility, so map to the recognizable product
# name, not the package slug. Extend freely; unknown deps fall through as-is.
# ----------------------------------------------------------------------------
DEP_TO_TAG = {
    # JS / TS frontend
    "react": "React", "react-dom": "React", "next": "Next.js", "vue": "Vue.js",
    "svelte": "Svelte", "@angular/core": "Angular", "solid-js": "SolidJS",
    "tailwindcss": "Tailwind CSS", "three": "Three.js", "d3": "D3.js",
    "framer-motion": "Framer Motion", "@react-three/fiber": "React Three Fiber",
    "vite": "Vite", "expo": "Expo", "react-native": "React Native",
    # JS / TS backend
    "express": "Express", "fastify": "Fastify", "next-auth": "NextAuth",
    "socket.io": "Socket.IO", "prisma": "Prisma", "drizzle-orm": "Drizzle",
    "@trpc/server": "tRPC", "nestjs": "NestJS", "@nestjs/core": "NestJS",
    # Python
    "flask": "Flask", "django": "Django", "fastapi": "FastAPI",
    "streamlit": "Streamlit", "gradio": "Gradio", "pandas": "pandas",
    "numpy": "NumPy", "scikit-learn": "scikit-learn", "torch": "PyTorch",
    "tensorflow": "TensorFlow", "transformers": "Hugging Face Transformers",
    "langchain": "LangChain", "llama-index": "LlamaIndex", "opencv-python": "OpenCV",
    "selenium": "Selenium", "beautifulsoup4": "BeautifulSoup", "celery": "Celery",
    # AI / model providers (high-value for sponsor prizes)
    "openai": "OpenAI API", "anthropic": "Anthropic API", "cohere": "Cohere",
    "google-generativeai": "Google Gemini", "@google/generative-ai": "Google Gemini",
    "replicate": "Replicate", "elevenlabs": "ElevenLabs", "@huggingface/inference": "Hugging Face",
    "groq": "Groq", "mistralai": "Mistral",
    # Data / infra / BaaS (often sponsor-prize relevant)
    "@supabase/supabase-js": "Supabase", "supabase": "Supabase",
    "firebase": "Firebase", "firebase-admin": "Firebase", "mongodb": "MongoDB",
    "mongoose": "MongoDB", "pg": "PostgreSQL", "psycopg2": "PostgreSQL",
    "psycopg2-binary": "PostgreSQL", "redis": "Redis", "@auth0/auth0-react": "Auth0",
    "stripe": "Stripe", "twilio": "Twilio", "@clerk/clerk-react": "Clerk",
    "@vercel/postgres": "Vercel Postgres", "convex": "Convex",
    "pinecone-client": "Pinecone", "@pinecone-database/pinecone": "Pinecone",
    "weaviate-client": "Weaviate", "chromadb": "ChromaDB", "qdrant-client": "Qdrant",
    "boto3": "AWS", "@aws-sdk/client-s3": "AWS",
}

EXT_TO_LANG = {
    ".py": "Python", ".js": "JavaScript", ".jsx": "JavaScript", ".ts": "TypeScript",
    ".tsx": "TypeScript", ".go": "Go", ".rs": "Rust", ".java": "Java", ".kt": "Kotlin",
    ".swift": "Swift", ".rb": "Ruby", ".php": "PHP", ".c": "C", ".cpp": "C++",
    ".cs": "C#", ".html": "HTML", ".css": "CSS", ".scss": "CSS", ".sol": "Solidity",
    ".dart": "Dart", ".vue": "Vue", ".svelte": "Svelte",
}

SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist",
             "build", ".next", "out", "target", "vendor", ".expo", "coverage"}

DEMO_HINTS = ("vercel.json", "netlify.toml", "render.yaml", "fly.toml", "Procfile",
              "Dockerfile", "docker-compose.yml")
VIDEO_EXTS = (".mp4", ".mov", ".webm", ".gif")


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return ""


def _http_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "devpost-skill"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


# ----------------------------------------------------------------------------
# Dependency parsing
# ----------------------------------------------------------------------------
def parse_dependencies(root):
    deps = set()
    pj = os.path.join(root, "package.json")
    if os.path.exists(pj):
        try:
            data = json.loads(_read(pj))
            for key in ("dependencies", "devDependencies"):
                deps.update((data.get(key) or {}).keys())
        except json.JSONDecodeError:
            pass
    for fname in ("requirements.txt", "Pipfile"):
        fp = os.path.join(root, fname)
        if os.path.exists(fp):
            for line in _read(fp).splitlines():
                m = re.match(r"^\s*([A-Za-z0-9_.\-]+)", line)
                if m and not line.strip().startswith(("#", "[")):
                    deps.add(m.group(1).lower())
    pyproject = os.path.join(root, "pyproject.toml")
    if os.path.exists(pyproject):
        for m in re.finditer(r'"([A-Za-z0-9_.\-]+)(?:[<>=!~ ].*)?"', _read(pyproject)):
            deps.add(m.group(1).lower())
    # raw manifest presence -> framework-level tags
    extra = []
    if os.path.exists(os.path.join(root, "Cargo.toml")):
        extra.append("Rust")
    if os.path.exists(os.path.join(root, "go.mod")):
        extra.append("Go")
    return deps, extra


def deps_to_tags(deps, extra):
    tags = []
    for d in sorted(deps):
        key = d.lower()
        if key in DEP_TO_TAG and DEP_TO_TAG[key] not in tags:
            tags.append(DEP_TO_TAG[key])
    for e in extra:
        if e not in tags:
            tags.append(e)
    return tags


# ----------------------------------------------------------------------------
# Language breakdown by source-file counting
# ----------------------------------------------------------------------------
def language_breakdown(root):
    counts = Counter()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            lang = EXT_TO_LANG.get(os.path.splitext(fn)[1].lower())
            if lang:
                counts[lang] += 1
    total = sum(counts.values()) or 1
    return [{"language": l, "files": c, "pct": round(100 * c / total)}
            for l, c in counts.most_common()]


# ----------------------------------------------------------------------------
# README summary
# ----------------------------------------------------------------------------
def summarize_readme(root):
    for name in ("README.md", "Readme.md", "readme.md", "README"):
        fp = os.path.join(root, name)
        if os.path.exists(fp):
            text = _read(fp)
            title = ""
            first_para = ""
            headings = []
            for line in text.splitlines():
                s = line.strip()
                if s.startswith("#"):
                    h = s.lstrip("#").strip()
                    if not title:
                        title = h
                    else:
                        headings.append(h)
                elif s and not first_para and not s.startswith(("![", "[!", "<", "---")):
                    first_para = s
            links = re.findall(r"https?://[^\s)\"']+", text)
            demo_links = [l for l in links if any(
                k in l.lower() for k in ("vercel.app", "netlify.app", "youtu",
                                         "loom.com", "devpost.com", "herokuapp",
                                         "render.com", "fly.dev"))]
            return {"title": title, "first_paragraph": first_para,
                    "headings": headings[:12], "demo_links": demo_links[:6]}
    return {"title": "", "first_paragraph": "", "headings": [], "demo_links": []}


# ----------------------------------------------------------------------------
# Git build stats — "we built this in N hours" is a great honest detail
# ----------------------------------------------------------------------------
def git_stats(root):
    if not os.path.isdir(os.path.join(root, ".git")):
        return {}

    def git(*args):
        try:
            return subprocess.check_output(["git", "-C", root, *args],
                                           stderr=subprocess.DEVNULL,
                                           text=True).strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""

    count = git("rev-list", "--count", "HEAD")
    first = git("log", "--reverse", "--format=%cI", "--max-parents=0")
    first = first.splitlines()[0] if first else ""
    last = git("log", "-1", "--format=%cI")
    span_hours = None
    if first and last:
        try:
            t0 = datetime.fromisoformat(first)
            t1 = datetime.fromisoformat(last)
            span_hours = round((t1 - t0).total_seconds() / 3600, 1)
        except ValueError:
            pass
    subjects = git("log", "--format=%s", "-n", "40").splitlines()
    contributors = [c for c in git("log", "--format=%an").splitlines() if c]
    return {
        "commits": int(count) if count.isdigit() else None,
        "span_hours": span_hours,
        "contributors": sorted(set(contributors)),
        "sample_commit_subjects": subjects[:15],
    }


def detect_demo_assets(root):
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn in DEMO_HINTS:
                found.append(fn)
            if os.path.splitext(fn)[1].lower() in VIDEO_EXTS:
                found.append(fn)
    return sorted(set(found))


# ----------------------------------------------------------------------------
# GitHub URL path (public API, no token; rate-limited but fine for one repo)
# ----------------------------------------------------------------------------
def analyze_github(url):
    m = re.search(r"github\.com/([^/]+)/([^/#?]+)", url)
    if not m:
        sys.exit("Could not parse a GitHub owner/name from that URL.")
    owner, name = m.group(1), m.group(2).removesuffix(".git")
    api = f"https://api.github.com/repos/{owner}/{name}"
    brief = {"source": url, "name": name}
    try:
        meta = _http_json(api)
        brief["description"] = meta.get("description") or ""
        langs = _http_json(api + "/languages")
        total = sum(langs.values()) or 1
        brief["languages"] = [{"language": l, "pct": round(100 * b / total)}
                              for l, b in sorted(langs.items(), key=lambda x: -x[1])]
        try:
            readme_meta = _http_json(api + "/readme")
            import base64
            text = base64.b64decode(readme_meta.get("content", "")).decode("utf-8", "ignore")
            links = re.findall(r"https?://[^\s)\"']+", text)
            brief["readme"] = {
                "first_paragraph": next(
                    (l.strip() for l in text.splitlines()
                     if l.strip() and not l.strip().startswith(("#", "![", "<", "---"))), ""),
                "demo_links": [l for l in links if any(
                    k in l.lower() for k in ("vercel.app", "netlify.app", "youtu",
                                             "loom.com", "herokuapp"))][:6],
            }
        except Exception:
            brief["readme"] = {}
    except Exception as e:
        sys.exit(f"GitHub API request failed ({e}). Try cloning the repo and passing the local path.")
    brief["note"] = ("GitHub API mode can't read dependency manifests or git timing in "
                     "detail — clone locally and re-run for full 'Built With' + build-time stats.")
    return brief


def analyze_local(root):
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        sys.exit(f"Not a directory: {root}")
    deps, extra = parse_dependencies(root)
    return {
        "source": root,
        "name": os.path.basename(root),
        "built_with_tags": deps_to_tags(deps, extra),
        "raw_dependencies_detected": sorted(deps),
        "languages": language_breakdown(root),
        "readme": summarize_readme(root),
        "git": git_stats(root),
        "demo_assets": detect_demo_assets(root),
    }


def render_brief(b):
    L = []
    L.append("=" * 64)
    L.append(f"REPO BRIEF — {b.get('name', '?')}")
    L.append("=" * 64)
    if b.get("description"):
        L.append(f"\nDescription: {b['description']}")
    rd = b.get("readme") or {}
    if rd.get("title"):
        L.append(f"\nREADME title: {rd['title']}")
    if rd.get("first_paragraph"):
        L.append(f"README lede: {rd['first_paragraph']}")
    if rd.get("headings"):
        L.append("README sections: " + ", ".join(rd["headings"]))
    if rd.get("demo_links"):
        L.append("Demo/links found: " + ", ".join(rd["demo_links"]))
    if b.get("built_with_tags"):
        L.append("\nBuilt With (from manifests — VERIFIED, use these): "
                 + ", ".join(b["built_with_tags"]))
    if b.get("languages"):
        L.append("Languages: " + ", ".join(
            f"{x['language']} {x.get('pct','?')}%" for x in b["languages"][:6]))
    g = b.get("git") or {}
    if g:
        bits = []
        if g.get("commits") is not None:
            bits.append(f"{g['commits']} commits")
        if g.get("span_hours") is not None:
            bits.append(f"~{g['span_hours']}h from first to last commit")
        if g.get("contributors"):
            bits.append(f"{len(g['contributors'])} contributor(s)")
        if bits:
            L.append("\nBuild stats: " + ", ".join(bits))
        if g.get("sample_commit_subjects"):
            L.append("Recent commit subjects (clues for Challenges / What we learned):")
            for s in g["sample_commit_subjects"][:10]:
                L.append(f"  - {s}")
    if b.get("demo_assets"):
        L.append("\nDeploy/demo assets present: " + ", ".join(b["demo_assets"]))
    if b.get("note"):
        L.append(f"\nNote: {b['note']}")
    L.append("\n" + "-" * 64)
    L.append("JSON (feed this back into the submission workflow):")
    L.append(json.dumps(b, indent=2))
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Extract Devpost-submission signal from a repo.")
    ap.add_argument("repo", help="Local path to the repo, or a GitHub URL")
    ap.add_argument("--json", action="store_true", help="Print raw JSON only")
    args = ap.parse_args()

    if args.repo.startswith(("http://", "https://")) or args.repo.startswith("github.com"):
        brief = analyze_github(args.repo)
    else:
        brief = analyze_local(args.repo)

    if args.json:
        print(json.dumps(brief, indent=2))
    else:
        print(render_brief(brief))


if __name__ == "__main__":
    main()
````

---

## File: `references/winning-submissions.md`

````markdown
# What separates a winning Devpost submission from a forgettable one

Read this before drafting. The Devpost fields are easy to fill and easy to fill *badly*.
Judges at MLH-scale events skim dozens of projects; a submission earns attention by being
specific, honest, and skimmable — not by being long or hyped.

## The three rules that matter most

**1. Specific beats grand.** "Revolutionizing how people connect" says nothing. "Lets two
roommates settle where to eat in under 10 seconds by swiping instead of arguing" says
everything. Every claim should survive the question *"compared to what, exactly?"*

**2. Honest beats impressive.** Judges open the repo and click the demo. If the writeup
claims a feature the code doesn't have, that's worse than not claiming it — it reads as
either AI-generated filler or a lie. Only describe what actually exists. Build stats, real
bugs, and scoped-down decisions are *assets*, not weaknesses: they signal a real build.

**3. Human beats polished-but-hollow.** A submission that sounds like a language model wrote
it gets mentally discounted. Keep the team's actual voice. A little personality and one
genuine joke about the 3am bug beats five paragraphs of corporate gloss.

## Banned phrases (instant AI-slop tells — do not use)

Never write: "In today's fast-paced world", "seamlessly", "revolutionize / game-changer",
"leveraging cutting-edge", "the power of AI", "unlock / empower / elevate", "robust and
scalable solution", "user-friendly interface", "passion project born out of", "little did we
know", "and that's when the magic happened". If a sentence would survive being pasted into
any other project's submission, it's filler — cut it.

## Field-by-field guide

Devpost submissions use a standard set of fields. Write each to its actual job:

### Tagline (the gallery hook — ~10 words)
This is the one line shown under the project in the gallery. It decides whether a judge
clicks. Make it concrete and benefit-first. Not "AI-powered productivity, reimagined."
Yes: "Turn any GitHub repo into a finished Devpost submission in 60 seconds."

### Inspiration
One tight paragraph. Lead with the *specific* friction or moment that started it — ideally
a real one ("we'd just spent our last hour writing a submission instead of polishing the
demo"). Avoid global-problem throat-clearing. Two or three sentences is plenty.

### What it does
The most important field. Plainly state what the thing does *from the user's point of view*,
then the 2–4 features that matter. Lead with the outcome, not the tech. If there's a sponsor
prize for "Best Use of X", make sure X's role is visible *here* in plain language — this is
where prize matchers look first.

### How we built it
The architecture in human terms: the stack (use the VERIFIED tags from the repo analysis —
do not invent tech), how the pieces talk to each other, and one or two genuinely interesting
technical decisions. Name the actual hard part you solved, not a generic pipeline diagram.

### Challenges we ran into
Gold for credibility, and the repo's commit history usually hands you these directly (e.g. a
"fix CORS" or "cache audio to save budget" commit). Pick 1–3 *real* obstacles and say how you
got past them (or didn't). Specific bugs > "time management was hard."

### Accomplishments that we're proud of
Concrete things you got working, especially under time pressure. "Generated and cached audio
narration cheaply enough to demo live" beats "we're proud of our teamwork." One or two items.

### What we learned
Honest, specific takeaways — a tool you picked up, a wrong assumption you corrected, a limit
you hit. Skip the inspirational-poster version.

### What's next for [project]
Shows ambition and that you know your own gaps. 2–4 concrete next steps. Naming a current
limitation and how you'd fix it reads as maturity, not weakness.

### Built With (tags)
Use the verified tags from `analyze_repo.py` output. These must be TRUE — judges filter
sponsor prizes on them, and a wrong tag is a credibility hit. Include languages, frameworks,
APIs, and notable services. Don't pad with things you imported but never used.

## Aligning to judging criteria and sponsor prizes

If the user provides the rubric or prize list, tailor *without lying*:

- **Map each judging axis to a hook.** Most rubrics reduce to some mix of Technical
  Difficulty, Originality, Polish/Design, Impact, and Demo/Presentation. Make sure the
  writeup gives each axis at least one concrete handle (e.g. surface the hard technical bit
  for Technical Difficulty; name the user outcome for Impact).
- **Surface sponsor-API usage explicitly.** "Best Use of [Sponsor]" prizes are matched by
  someone scanning *What it does* / *How we built it* / *Built With* for that sponsor. If you
  used it meaningfully, say so plainly and say *what it did* — don't make them hunt.
- **Never claim a prize fit that isn't real.** If a sponsor's tool was used trivially, don't
  inflate it; suggest it as a stretch at most and tell the user honestly.

## Two quick before/afters

**Tagline**
- Weak: "An innovative platform leveraging AI to enhance group decision-making."
- Strong: "Settle 'where should we eat' with a 10-second group swipe instead of a 40-message thread."

**Challenges**
- Weak: "We faced many challenges with time management and technical issues."
- Strong: "Our TTS calls were going to blow the API budget mid-demo, so we added a content-hash
  cache the night of — repeated routes now cost nothing and the live demo never stalls."
````

---

## File: `assets/devpost-template.md`

````markdown
# Devpost submission — paste-ready output template

Fill every field below and hand it back as one block the user can paste straight into
Devpost. Keep the field headers exactly as named so they map 1:1 to Devpost's form.

---

**Project name:** [name]

**Tagline:** [~10 words, concrete, benefit-first]

**Elevator pitch / What inspired you:**
[1 short paragraph — the specific friction or moment]

## Inspiration
[2–3 sentences]

## What it does
[Plain-language outcome first, then 2–4 features that matter. Surface any sponsor-API role here.]

## How we built it
[Stack in human terms using VERIFIED tags + the 1–2 interesting technical decisions.]

## Challenges we ran into
[1–3 real obstacles, ideally drawn from commit history, with how you handled them.]

## Accomplishments that we're proud of
[1–2 concrete wins, especially under time pressure.]

## What we learned
[Specific, honest takeaways.]

## What's next for [name]
[2–4 concrete next steps, including a known limitation you'd fix.]

**Built With:** [comma-separated VERIFIED tags from analyze_repo.py]

**Try it out links:** [demo URL, repo URL, video URL if present]

---

## Pre-submit checklist (run through this before the user submits)

These are the things that get otherwise-good projects disqualified or marked down. Flag any
that are missing — don't silently assume they're handled.

- [ ] **Demo video** linked and ≤ the event's limit (often 2–3 min). This is the single
      highest-leverage asset; a project with no video rarely wins. If absent, say so loudly.
- [ ] **Public repo** linked, and it's actually public.
- [ ] **"Built With" tags accurate** — every tag reflects something actually used.
- [ ] **Sponsor-prize requirements met** for each prize the team is entering (required API
      actually used, any "must do X" satisfied). List which prizes the project plausibly fits.
- [ ] **Built-during-event** honesty — nothing in the writeup implies pre-event work that
      would violate rules.
- [ ] **All teammates added** on Devpost (a common, painful miss).
- [ ] **Tagline + thumbnail** present (the gallery hook).
- [ ] **Links work** — demo loads, video is viewable, repo opens.

If the user hasn't recorded a demo video yet, offer a 30-second shot list:
hook (problem) → live demo of the core flow → the one impressive technical moment → what's next.
````

---

## After creating the files

Run these to verify and commit:

```bash
chmod +x scripts/analyze_repo.py
python scripts/analyze_repo.py .        # smoke test — should print a REPO BRIEF
git init
git add -A
git commit -m "Add devpost-submission-writer skill"
```
