# Daily Brief

**An AI-written morning briefing on AI, tech and PM careers, published fresh every day.**

**Read today's brief:** [tgraharms.github.io/daily-brief](https://tgraharms.github.io/daily-brief/)

![Screenshot of the Daily Brief page](docs/screenshot.png)

## Why I built this

AI moves fast, and as a product manager I need to know what changed this week to make good calls at work. Keeping up meant hopping between newsletters, social feeds and news sites every morning, and I still missed things.

So I built a researcher that does the reading for me. Every morning it scans the last day or two of news, picks what matters, ranks it, and puts it on one page I can read over coffee. This is how I stay on top of trends in a few minutes a day.

I built it for myself, a PM based in Malaysia. The page is public, so anyone who wants a quick daily read on AI and product careers can use it too.

## What's in each brief

- **AI:** model launches, big company moves, research and regulation
- **Tech:** Big Tech, chips and cloud
- **Career:** how the PM role is changing, hiring and pay, split into Malaysia and Global
- **Consumer:** AI news for everyday users

Every story gets an importance score from 1 to 10, a short note on why it matters, and a link to the source. The sidebar keeps every brief since June 2026.

## How it works

1. Every day at 7:30am Malaysia time, GitHub starts a small script.
2. The script asks Claude to search the web and write the brief, following instructions I wrote in `prompt.md`.
3. The script checks the brief has every section and enough stories, then saves it to this repo.
4. The web page picks up the newest brief and keeps past days in the sidebar.

<!-- To show cost, replace this comment with: Each run costs about $X in API credits. (The amount is on each run's summary under the Actions tab.) -->

## Built with

- **Claude API** (Sonnet 5.5 with web search) to research and write
- **Python** for the script (`generate.py`)
- **GitHub Actions** to run it on a daily schedule
- **GitHub Pages** to host the page, written in plain HTML and JavaScript

## Run it yourself

You'll need Python 3.10 or newer and a Claude API key from the [Claude Console](https://platform.claude.com/).

```bash
git clone https://github.com/tgraharms/daily-brief.git
cd daily-brief
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
python generate.py
```

Today's brief lands in the `briefs/` folder. To change what it covers, edit `prompt.md`.

To get your own daily copy, fork this repo, add your key under **Settings > Secrets and variables > Actions** as `ANTHROPIC_API_KEY`, and point `BRIEFS_URL` at the top of `index.html` to your fork.
