# AI Product Trend Radar

**An AI-written morning briefing on AI, tech and PM careers, published fresh every day.**

**Read today's brief:** [tgraharms.github.io/ai-product-trend-radar](https://tgraharms.github.io/ai-product-trend-radar/)

<img src="docs/screenshot.png" alt="AI Product Trend Radar on a desktop screen" width="72%"> <img src="docs/screenshot-phone.png" alt="AI Product Trend Radar on a phone" width="24%">

## Why I built this

AI moves fast, and as a product manager I need to know what changed this week to make good calls at work. Keeping up meant hopping between newsletters, social feeds and news sites every morning, and I still missed things.

So I built a researcher that does the reading for me. Every morning it scans the last day or two of news, picks what matters, ranks it, and puts it on one page I can read over coffee. This is how I stay on top of trends in a few minutes a day.

I built it for myself, a PM based in Malaysia. The page is public, so anyone who wants a quick daily read on AI and product careers can use it too.

## What's in each brief

- **AI:** model launches, big company moves, research and regulation
- **Tech:** Big Tech, chips and cloud
- **Community:** what developers, hackers and open-source folks are doing to big tech products, like AI-built clones of paid apps, jailbreaks and leaks
- **Career:** how the PM role is changing, hiring and pay, split into Malaysia and Global
- **Consumer:** AI news for everyday users

Every story gets an importance score from 1 to 10, a short note on why it matters, and a link to the source. Quiet days get fewer stories. On a big news day a section can carry extra stories, as long as each one scores 7 or higher.

The page works on phones and desktops. On a phone, past briefs sit behind the Archive button, and every brief since June 2026 is kept.

## How it works

1. Early every morning, GitHub starts a small script so the brief is ready before 8am Malaysia time.
2. The script asks Claude to search the web and write the brief, following instructions I wrote in `prompt.md`.
3. The script checks the brief has every section and enough stories, then saves it to this repo.
4. The web page picks up the newest brief and keeps past days in the archive.

Each run costs about $1 in Claude API credits, roughly $30 a month, which fits inside the monthly API credit that comes with my Claude plan. Every run's cost shows at the top of its page under the Actions tab.

## Built with

- **Claude API** (Sonnet 5.5 with web search) to research and write
- **Python** for the script (`generate.py`)
- **GitHub Actions** to run it on a daily schedule
- **GitHub Pages** to host the page, written in plain HTML and JavaScript

## Run it yourself

You'll need Python 3.10 or newer and a Claude API key from the [Claude Console](https://platform.claude.com/).

```bash
git clone https://github.com/tgraharms/ai-product-trend-radar.git
cd ai-product-trend-radar
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
python generate.py
```

Today's brief lands in the `briefs/` folder. To change what it covers, edit `prompt.md`.

To get your own daily copy, fork this repo, add your key under **Settings > Secrets and variables > Actions** as `ANTHROPIC_API_KEY`, turn on workflows in the **Actions** tab, and switch on GitHub Pages. The page finds your fork's briefs on its own.
