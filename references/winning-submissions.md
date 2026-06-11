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
