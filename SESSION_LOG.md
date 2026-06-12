# Session log — building the `devpost-submission-writer` skill

**Date:** June 12, 2026
**Author:** Aslan Wang (with Claude Code)
**Repo:** https://github.com/Asyboi/devpost-writeup

## What this is

A Claude **agent skill** that turns a hackathon project repo into a complete, paste-ready
Devpost submission — drafting every standard field (Inspiration, What it does, How we built
it, Challenges, Accomplishments, What we learned, What's next, Built With, tagline).

The core design idea: the two ways auto-written submissions fail are **(1) invented tech
stacks/features** that judges catch the moment they open the repo, and **(2) generic AI slop**
that gets mentally discounted. The skill avoids both by reading the *actual repo* —
dependency manifests, git history, README — so every claim is verified before it's written.

## What was built this session

| File | Purpose |
|---|---|
| `SKILL.md` | The skill definition: trigger description + 5-step workflow (gather inputs → analyze repo → draft to quality bar → tailor to judging criteria/sponsor prizes → self-check & deliver) |
| `scripts/analyze_repo.py` | Stdlib-only Python analyzer. Reads `package.json` / `requirements.txt` / `pyproject.toml` etc. for a **verified** "Built With" list, pulls build stats and commit subjects from git history (raw material for the Challenges section), summarizes the README, and finds demo links/assets. Works on a local path or a public GitHub URL. |
| `references/winning-submissions.md` | The quality bar: field-by-field writing guide, a banned-phrases list ("seamlessly", "revolutionize", "in today's fast-paced world"…), honesty rules, and before/after examples |
| `assets/devpost-template.md` | The paste-ready output skeleton with field headers matching Devpost's form 1:1, plus a pre-submit checklist (demo video, public repo, accurate tags, sponsor-prize requirements, teammates added) |
| `README.md` | Project overview and quickstart |

## Steps taken

1. Created the five files above.
2. Made the analyzer executable (`chmod +x scripts/analyze_repo.py`).
3. **Smoke test** — ran the analyzer on this repo itself:

   ```
   $ python scripts/analyze_repo.py .
   ================================================================
   REPO BRIEF — devpost-writeup
   ================================================================

   README title: devpost-submission-writer
   README sections: Why, How it works, Files, Quickstart, A note on honesty
   Languages: Python 100%

   Build stats: 1 commits, ~0.0h from first to last commit, 1 contributor(s)
   ...
   + a JSON block for feeding back into the skill workflow
   ```

   Ran clean — README parsing, language breakdown, and git stats all working.
4. Committed as `5294c54` ("Add devpost-submission-writer skill") and pushed to
   `https://github.com/Asyboi/devpost-writeup` (`main`).

## How to try it

```bash
git clone https://github.com/Asyboi/devpost-writeup
python devpost-writeup/scripts/analyze_repo.py /path/to/any/hackathon/repo
```

Or with the skill loaded into Claude: *"Write my Devpost submission for the repo at \<path\>."*
The skill runs the analyzer, drafts every field to the quality bar, and finishes with the
pre-submit checklist — flagging especially a missing demo video, the most common
high-leverage gap.
