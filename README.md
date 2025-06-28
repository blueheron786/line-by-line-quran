# Line By Line Qur'an

Scrapes the Qur'an text, from quran.com, and generates one page per file, with one line per line of the mushaf. This is the "15 line mushaf" which is also known as the Uthmani and Madini mushaf.

These lines exactly match the 'Uthmani script, line by line, page by page. If you're interested in the output, it's available in two formats:

- `output/pageNNN.txt` with each individual page's 15 lines
- `pages.json` with an array of 604 pages; each page is an array of 15 lines. No meta-data.

# Setup

If you're interested in running the scraper yourself, you can find instructions below. I **highly recommend you don't do this,** and instead, run scripts against the static data instead.

Run `pip install playwright` and then `playwright intall`, then you're clear for lift-off. `python scrape.py` launches the scraper.

