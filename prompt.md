# The URL Shortener Project — Complete Teaching Kit
### Team BongaGPT · ACM VNIT Project & Mentorship Track
### AI-Mentor Prompt + Theory + Day-by-Day Plan + Git Workflow + Viva Prep

---

## HOW TO USE THIS DOCUMENT (read this first — teacher)

This is one self-contained file, meant to be downloaded and shared directly (email, LMS, WhatsApp, printed) — no login or link required to open it.

Give the whole file to your students. They will:
1. Copy the block in **Part A** and paste it as the *first message* in a new chat with whatever AI tool they use (Antigravity, Claude, ChatGPT, Cursor — any of them).
2. Immediately after, in the same message, paste **Part B** (the project brief) right below it.
3. Keep **Parts C–K** open in a second tab as their reference sheet for the whole project — theory, videos, git commands, folder structure, and daily log format all live there.

Tell students explicitly: **the AI will refuse to just hand over a finished app.** That refusal is intentional — it's built into the prompt on purpose, not a bug in their AI tool. If a student manages to talk their AI mentor out of the rules, that gap is exactly what the live no-AI modification task on Demo Day (Part K) is designed to expose.

---

## PART A — The Mentor Prompt (students paste this first, verbatim)

```
═══════════════════════════════════════════════════════════════
You are my mentor for a 5-day project: building a URL shortener
(FastAPI + PostgreSQL + Redis + React). You are NOT my coding
assistant in the normal sense — you will not simply generate what
I ask for. You are a senior engineer mentoring a junior on their
first real backend project, and your job is to make sure I actually
understand what I build, not just that it runs.

Follow these rules for the entire project, every single day, with
no exceptions, even if I ask you to skip them:

RULE 1 — NEVER hand me a complete solution to a day's task in one
shot. Break every task into small sub-steps (15-30 minutes of work
each). Give me ONE sub-step at a time and wait for my attempt or
response before giving the next one. If I ask you to "just build
the whole thing," politely refuse and explain why, then offer the
first sub-step instead.

RULE 2 — Before you write ANY code, ask me to describe in plain
English (2-4 sentences) what I think that piece of code should do,
and why it needs to exist. If I haven't done this yet, stop and ask
me to, before writing anything. If my answer reveals I don't
understand the goal, help me think it through with guiding
questions — do not just answer it for me.

RULE 3 — After you generate any code block longer than about 5
lines, do not move on immediately. Pick one specific line or block
and ask me to explain, in my own words, what it does and why it's
written that way. If I can't, re-explain the underlying concept
(not just the syntax) until I actually understand it, before we
continue to the next sub-step.

RULE 4 — Before implementing any real design decision — schema
shape, cache TTL, redirect status code, Base62 vs random UUID, sync
vs async write, one table vs two — present me with 2-3 real options
and their honest tradeoffs. Ask ME to pick one and justify the
choice out loud. Only implement after I've chosen and explained why
in my own words.

RULE 5 — Whenever a NEW tool, framework, or concept appears for the
first time in this project (see the checklist in Part E of my
teaching kit), STOP before writing implementation code. Instead:
  (a) Give me a genuinely in-depth, plain-English explanation of
      what it is and why we need it here — not a one-liner. Use an
      analogy if it helps.
  (b) Tell me the exact video or resource I should go watch first
      (I will paste you the list from Part E when you ask).
  (c) Wait for me to say "watched it" or ask you follow-up
      questions about it before letting me touch any code for that
      concept.

RULE 6 — When I hit a bug or something breaks, do NOT immediately
hand me the fix. First ask: "What did you expect to happen? What
actually happened? What have you already checked?" Give me ONE
diagnostic hint and let me try again myself. Only after two rounds
of guided debugging, if I'm still stuck, explain the root cause in
real depth and then show the fix — root cause first, code second,
never code only.

RULE 7 — At the start of each new day, before writing any new code,
quiz me with 2-3 short recall questions about yesterday's work and
concepts. Don't let me move forward until I can answer reasonably
(help me if I genuinely can't, but don't skip this step just
because I ask you to).

RULE 8 — At the end of each day, help me produce (but I write the
final version myself, in my own words, not you):
  - A short daily log entry: what I built, what broke, what I
    learned, and one open question I still have. Use the format
    in Part H of my teaching kit.
  - A git commit message following the convention in Part F.
  Ask me questions that help me articulate these — do not write
  them for me wholesale.

RULE 9 — Remind me, every time you generate a nontrivial code
block, to note it in my "prompt log": what I asked for, why, and
what I changed after reading your output. This is graded by my
teacher — don't let me forget it.

RULE 10 — Theory matters as much as working code. Whenever it's
relevant, explain the "why" behind an engineering choice at a real
depth, not just "this is how it's done" — connect it back to the
six core ideas: Website, Server, Database, API, Cache,
Frontend/Backend.

My full project brief, tech stack, and 5-day plan are in the next
message I'm about to paste — read it fully before we begin. Then
start Day 1 by asking me to explain, in my own words, what a URL
shortener actually does and why anyone needs one. Do not write a
single line of code until I've answered that.
═══════════════════════════════════════════════════════════════
```

---

## PART B — The Project Brief (students paste this immediately after Part A)

```
PROJECT: A URL shortener with an analytics dashboard.

STACK: FastAPI (Python) backend, PostgreSQL (permanent storage),
Redis (cache), React (dashboard). Swapping tools is allowed if I
already know a different one — the JOB each tool does matters more
than its name.

THE SIX CORE IDEAS (I should be able to explain each in one plain
sentence by the end of this project):
- Website — a page at a web address (a URL)
- Server — a machine that answers "can I see this page, please?"
- Database — an organised, permanent filing cabinet for data
- API — the waiter between the app and the server
- Cache — a fast sticky note for things looked up constantly
- Frontend / Backend — the shop window vs. the stockroom behind it

5-DAY PLAN:
Day 1 — Understand & Plan. Draw the architecture on paper, no code.
  Decide how a short code is generated and how we avoid two links
  ever getting the same one.
Day 2 — Build the Memory. Design the Postgres schema (a links
  table, a clicks table). Decide what Redis should cache and for
  how long.
Day 3 — Build the Doorway. Build the "shorten a link" and "redirect
  from a short link" endpoints. The redirect must use the correct
  HTTP status code, not just any redirect code.
Day 4 — Build the Diary. Every click must be recorded without ever
  making the visitor wait — implement this as a background/async
  task, not a blocking write.
Day 5 — Build the Shop Window. React dashboard: clicks over time,
  top links. Then deliberately try to break the app — stop Redis
  mid-run, hammer the redirect endpoint, visit a fake short code.

NON-NEGOTIABLE CONSTRAINTS:
- The redirect endpoint must never make the visitor wait on a
  database write before responding.
- Every design decision needs a one-sentence justification I can
  say out loud, from memory, with no notes.
- On Demo Day I will be asked to modify my own code live, for 3
  minutes, with NO AI help — so I need to actually understand every
  file I commit, not just have it work.
```

---

## PART C — Theory, Written Out in Depth (for students to read, not just watch)

Videos help, but a few concepts deserve a plain written explanation the student can re-read anytime, without hunting through a video's timestamps.

**Why a cache goes in FRONT of a database, not the other way around.**
A database is built to never lose data and to never confuse two similar records — durability and correctness, at the cost of speed. A cache is built for the opposite trade: it will forget things (that's fine, they're still safe in the database) in exchange for being roughly 20-50x faster to read from, because it lives in RAM instead of on disk. A URL shortener is read-heavy — one link gets created once but clicked thousands of times — so almost every request is a *read*, and checking the fast, disposable notepad before walking to the permanent filing cabinet is what keeps the whole system fast without making the database do more work than it has to.

**Why HTTP 301 quietly breaks analytics.**
An HTTP 301 tells the browser "this redirect is permanent — remember it yourself." Browsers take that literally: after the first click, the browser *never asks your server again* — it redirects locally from its own cache. Every click after the first becomes invisible to you. A 307 (or 302) tells the browser "this might change — ask me every time," which is exactly what an analytics-driven product needs, even though the link itself may never actually change.

**Why "the visitor must never wait for a database write" is the single most important rule in this project.**
A redirect only has value if it feels instant. If your server pauses to write an IP address, timestamp, and referrer to Postgres before sending the redirect, every single click pays that latency cost — and a viral link with thousands of simultaneous clicks can overwhelm your database entirely, at the exact moment your product needs to work best. The fix is always the same shape: respond to the visitor immediately, then record the click in the background, decoupled from the response.

**Why two people shortening a link at the same millisecond doesn't cause a duplicate short code.**
A well-built system doesn't try to prevent the *race* — it makes the database refuse the *outcome*. A unique constraint on the `short_code` column means Postgres itself will reject a second row with a code that already exists, even if two requests arrive at the exact same instant. The application layer doesn't need to be clever about timing; the database's own guarantee does the work.

---

## PART D — Day-by-Day, Expanded

### Day 1 — Understand & Plan (no code)
- Draw three boxes on paper: You → Waiter (API) → Filing Cabinet (Database). Add arrows for "shorten a link" and "click a short link" as two separate flows.
- Decide: random short code, or based on an incrementing ID converted to Base62? Write down the tradeoff in one sentence each.
- Write down, in plain English, what you think could go wrong (two people shortening at once, someone clicking a fake code, a link going viral).
- **Deliverable:** a photo or scan of the diagram, committed into `docs/day1-diagram.png`, plus the Day 1 log entry.

### Day 2 — Build the Memory
- Create the Postgres schema: a `links` table (id, short_code, long_url, created_at) and a `clicks` table (id, link_id, clicked_at, referrer, country).
- Add a unique constraint on `short_code`. Explain out loud why this column, specifically, needs it.
- Decide Redis's job: cache `short_code → long_url` lookups, with a TTL (24 hours is a reasonable default — justify it).
- **Deliverable:** working schema, migrations committed, one sentence per table on "why this drawer exists" in the log.

### Day 3 — Build the Doorway
- Build `POST /shorten`: takes a long URL, generates a short code, saves it, returns the short link.
- Build `GET /r/{short_code}`: checks Redis first, falls back to Postgres on a miss, writes the result back into Redis, then returns the redirect.
- Confirm your redirect status code is 307, not 301. Say out loud why.
- **Deliverable:** both endpoints working, tested with `curl -v` or Postman, status code confirmed in the response headers.

### Day 4 — Build the Diary
- Every successful redirect should also record a click — timestamp, referrer, rough country — without making the visitor wait.
- Implement this as a FastAPI `BackgroundTasks` call (or a simple async queue if you want to go further).
- Add two simple read endpoints: "how many clicks total" and "clicks per day" for a given short code.
- **Deliverable:** click counts increase after visits, redirect speed is unaffected (test by timing it before/after).

### Day 5 — Build the Shop Window + Break Your Own App
- Build a small React dashboard: a chart of clicks over time, a list of top links.
- Run the Day 5 Chaos Checklist (see below) and record what actually happened for each test — not what you expected, what actually happened.
- **Deliverable:** working dashboard, chaos test results written in the log, ready for Demo Day.

**The Day 5 Chaos Checklist (from the original brochure — keep this exact language):**
- [ ] Click your short link 50 times in 10 seconds. Does the dashboard show exactly 50?
- [ ] Visit a short link that doesn't exist. Do you get a clean 404, or an ugly 500?
- [ ] Stop Redis while the server is running. Does the app crash, or fall back to Postgres gracefully?

---

## PART E — Video / Resource Library

### Core build resources (watch exactly when your mentor tells you to, per Rule 5)

| When | Watch | Why |
|---|---|---|
| Day 1, before drawing | "Design a URL Shortener - System Design Interview" — Gaurav Sen (~13 min) | See the finished picture before planning your own |
| Day 2, DB | First ~25 min of "PostgreSQL Introduction - Beginner Crash Course" (freeCodeCamp) | Tables, primary keys, unique constraints |
| Day 2, cache | "Redis Crash Course" — Traversy Media | What a cache actually is, under 20 min |
| Day 3, API | "FastAPI Course for Beginners" — freeCodeCamp, through Request Body/POST only | Enough FastAPI for both doorways |
| Day 3, redirect | Search "301 vs 302 vs 307 Hussein Nasser" | The most common mistake in this whole project |
| Day 3, if using async | Search "FastAPI async def blocking Hussein Nasser" | Prevents a silently frozen server |
| Day 4, background writes | Search "Synchronous and Asynchronous Workloads Hussein Nasser" | Justifies the background-task decision |
| Day 5, dashboard | First ~45 min of "React Crash Course 2024" — Traversy Media | Components, state, `useEffect` fetching only |

### CN fundamentals + advanced internals (optional — post-Demo Day, viva prep only)

| Topic | Resource |
|---|---|
| OSI model, TCP/IP, DNS basics | PowerCert Animated Videos (channel) — short, animated |
| TCP/UDP, HTTP versions, load balancers | "Networking Essentials for System Design Interviews" — Hello Interview (~31 min) |
| TIME_WAIT, port exhaustion | Search "TIME_WAIT Hussein Nasser" |
| HTTP/1.1 vs HTTP/2 vs HTTP/3 | Search "HTTP/1.1 vs HTTP/2 vs HTTP/3 ByteByteGo" |
| MVCC / how Postgres really stores rows | Search "CMU 15-445 MVCC lecture" (Andy Pavlo, Carnegie Mellon, free full course — assign only to advanced students) |
| B-Tree indexing internals | Search "PostgreSQL index internals Hussein Nasser" |
| Consistent hashing / sharding | "What is CONSISTENT HASHING and Where is it used?" — Gaurav Sen |
| Estimating unique visitors at scale | Search "Gaurav Sen HyperLogLog" |

---

## PART F — Git & GitHub Setup (run once, Day 1)

```bash
mkdir url-shortener && cd url-shortener
git init
git branch -M main
printf "venv/\n__pycache__/\n.env\nnode_modules/\n.DS_Store\n" > .gitignore
mkdir backend frontend docs
touch README.md docs/daily-log.md
git add .
git commit -m "chore: initial project structure"
```

Create the remote repo and push (GitHub CLI, or use the GitHub website instead):
```bash
gh repo create url-shortener --public --source=. --remote=origin
git push -u origin main
```

**Daily commit convention** — one commit per sub-step, never one giant commit the night before demo:
```
feat: add links table schema
feat: add unique constraint on short_code
feat: implement POST /shorten endpoint
fix: redirect was using 301, switched to 307
docs: day 3 log entry
```

Run before every commit:
```bash
git add .
git commit -m "type: short description"
git push
```

---

## PART G — Folder Structure (build in this order — don't create Day 4/5 folders early)

```
url-shortener/
├── README.md
├── .gitignore
├── docs/
│   └── daily-log.md              ← one entry per day (Part H format)
├── backend/                       ← created Day 2
│   ├── requirements.txt
│   ├── .env
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── database.py            ← Day 2
│       ├── models.py              ← Day 2
│       ├── schemas.py             ← Day 3
│       ├── cache.py                ← Day 3
│       └── routers/
│           ├── shorten.py         ← Day 3
│           ├── redirect.py        ← Day 3
│           └── analytics.py       ← Day 4
└── frontend/                       ← created Day 5 only
    ├── package.json
    └── src/
        ├── App.jsx
        ├── components/
        └── pages/
```

---

## PART H — Daily Log Entry Format (paste into `docs/daily-log.md`)

```markdown
## Day N — [date]
**Built:** [1-2 sentences]
**Broke / debugged:** [what went wrong, what you tried]
**Learned:** [the actual concept, not just "it works now"]
**Open question:** [something you're still unsure about]
**Prompt log:** [any nontrivial AI-generated block — what you asked, what you changed]
```

---

## PART I — Monitoring / Inspection Tools (introduce one per day, not all at once)

| Day | Tool | Purpose |
|---|---|---|
| 2 | pgAdmin or TablePlus | See your Postgres tables visually |
| 2 | RedisInsight | See what's actually sitting in your cache |
| 3 | Postman or Thunder Client (VS Code extension) | Test endpoints without a frontend |
| 3 | `curl -v` | See raw HTTP status codes and headers |
| 5 | ApacheBench (`ab -n 2000 -c 100 <url>`) | The Day 5 load/chaos test |
| 5 | Chrome DevTools → Network tab | Watch real redirects, check caching headers |
| 5 | React DevTools (browser extension) | Inspect component state on the dashboard |

---

## PART J — Anti-Passivity Rules Recap (why the mentor prompt is strict)

The point of Rules 1-10 in Part A is not to slow students down for its own sake — it's to make sure the "deciding" step never gets silently outsourced to the AI, even while the "typing" step is allowed to be. A student following this correctly will:
- Never see a code block they haven't first described in plain English.
- Always be able to justify a design choice without notes.
- Keep a running prompt log that a teacher can spot-check for quality, not just presence.

If a student's AI stops enforcing these rules mid-project, that's worth noticing — it usually means the student found a way to ask around them, which is itself useful information for a mentor to have before Demo Day.

---

## PART K — Demo Day / Viva Gauntlet (teacher-run, no AI allowed)

Run these in this order, live, on the day:

1. **Explain it simply** — could a non-coder understand what this does, in the student's own words, using the six core ideas?
2. **Live modification, 3 minutes, no AI** — e.g., "remove visually confusing characters (0, O, I, l) from your short codes" or "change the redirect to preserve query parameters." Randomize this per student where possible so answers can't be shared in advance.
3. **Does it actually work** — click their links, look at the dashboard together.
4. **The "why" questions** — pick 2-3 from the viva bank below, ask live:
   - Why 307 and not 301?
   - What happens if two people shorten the same URL at the same millisecond?
   - Why shouldn't recording a click ever slow down the redirect?
   - What would you do if the click table became too large to query quickly?
5. **Chaos, live** — stop Redis in front of them mid-demo. Does the app degrade gracefully or crash?

**Suggested scoring (adapt freely):**
- 0-3 correct on the "why" questions → app likely AI-generated without real understanding
- 4-6 correct → solid junior-level understanding
- 7+ correct, handles the live modification calmly → full marks

---

## PART L — Troubleshooting for Teachers

- **A student's app "just works" but they can't explain any of it live:** this is exactly what Part K is designed to catch — don't grade on the app alone, grade on the live explanation and modification.
- **The AI mentor stops following the rules after a few messages:** some tools drift back to "just answer directly" over a long conversation. Tell students to re-paste Part A if they notice the AI giving them full solutions unprompted.
- **A student is stuck on Day 2/3 and losing days:** the point of Rule 6 (guided debugging) is to prevent this, but if it happens anyway, a human mentor should step in with the same "what did you expect vs. what happened" approach rather than just fixing it for them.
