# Daily Brief

A daily AI, tech and PM-careers news brief, written by Claude every morning and published at
[tgraharms.github.io/daily-brief](https://tgraharms.github.io/daily-brief/).

## How it works

1. **GitHub Actions** runs `generate.py` every day at 7:30am Malaysia time (`.github/workflows/daily-brief.yml`).
2. **`generate.py`** sends `prompt.md` to the Claude API (Sonnet 5.5 with web search) and checks the reply has the right sections.
3. **The brief is saved** to `briefs/YYYY-MM-DD.md`, and `briefs/index.json` is updated with the list of dates.
4. **The workflow commits** both files. The page (`index.html`) reads them from the repo, so today's brief shows up right away.

Each run's log ends with a line showing the item count, searches used and the approximate cost.

## Setup

1. In the Claude Console, create an API key in the organization that receives your plan's monthly API credits.
2. In this repo, go to **Settings → Secrets and variables → Actions** and add it as `ANTHROPIC_API_KEY`.
3. Go to **Actions → Daily brief → Run workflow** to run it once and check the result.

## Changing things

- **What the brief covers:** edit `prompt.md`. Keep the section headers and item format, since the page parses them.
- **Model:** set the `BRIEF_MODEL` environment variable in the workflow (for example `claude-opus-5-5`).
- **Time:** edit the `cron` line in the workflow. It's in UTC, so subtract 8 hours from Malaysia time.

## Notes

- If the API credits run out, the run fails without charging anything, and GitHub emails you about the failed run.
- The page reads briefs from `raw.githubusercontent.com`, which only works while this repo is public.
