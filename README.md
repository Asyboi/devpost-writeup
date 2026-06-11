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
