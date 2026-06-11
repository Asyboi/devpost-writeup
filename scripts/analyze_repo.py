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
