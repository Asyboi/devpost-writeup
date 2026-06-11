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
