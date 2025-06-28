import time
import os
import json
from playwright.sync_api import sync_playwright

MAX_PAGE = 604
OUTPUT_DIR = "output"

###################
# Scrapes Qur'an, page by page, line by line, from quran.com.
# This generates a text file for each page with the real text of each line.
# This exactly matches the 'Uthmani script in the mushaf.
###################

def click_reading_button(page, clicks=3, delay=1.0):
    for _ in range(clicks):
        try:
            button = page.query_selector('button:has-text("Reading")')
            if button:
                button.click()
                time.sleep(delay)
            else:
                break
        except Exception:
            break

def get_page_lines_real_text(page, page_num):
    url = f"https://quran.com/page/{page_num}"
    page.goto(url)
    page.wait_for_load_state('networkidle')
    time.sleep(2)
    click_reading_button(page, clicks=3, delay=1.0)

    lines = []
    for i in range(1, 16):
        selector = f"#Page{page_num}-Line{i}"
        line_div = page.query_selector(selector)
        if not line_div:
            lines.append("")
            continue

        hidden_div = line_div.query_selector('div[class*="SeoTextForVerse_visuallyHidden"]')
        if not hidden_div:
            lines.append("")
            continue

        # Extract the text from the hidden div. First div has no tashkeel, second has tashkeel.
        text_elements = hidden_div.query_selector_all("div")
        if len(text_elements) != 2:
            raise RuntimeError(f"Unexpected number of text elements for page {page_num}, line {i}: {len(text_elements)}")
        text = text_elements[1].inner_text().strip()
        lines.append(text)

    if len(lines) != 15:
        print(f"Page {page_num} returned {len(lines)} lines instead of 15")

    return lines

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        all_pages = []
        start_time = time.time()

        for page_num in range(1, MAX_PAGE + 1):
            lines = get_page_lines_real_text(page, page_num)

            # Save each page to output/pageNNN.txt
            filename = os.path.join(OUTPUT_DIR, f"page{page_num:03}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

            all_pages.append(lines)

            # Every 5 pages, output progress info
            if page_num % 5 == 0:
                elapsed = time.time() - start_time
                ppm = page_num / (elapsed / 60)  # pages per minute
                pages_left = MAX_PAGE - page_num
                eta = pages_left / ppm if ppm > 0 else float('inf')
                print(f"Scraped {page_num} pages at {ppm:.1f} pages/min, ETA: {eta:.1f} minutes")

        browser.close()

    # Save all pages to pages.json
    with open("pages.json", "w", encoding="utf-8") as jf:
        json.dump(all_pages, jf, ensure_ascii=False, indent=2)

    print("Done! All pages saved to output/*.txt and pages.json")

if __name__ == "__main__":
    main()
