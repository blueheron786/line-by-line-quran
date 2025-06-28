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

        first_child = hidden_div.query_selector("div")
        text = first_child.inner_text().strip() if first_child else hidden_div.inner_text().strip()
        lines.append(text)

    return lines

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        all_pages = []
        for page_num in range(1, MAX_PAGE + 1):
            print(f"Processing page {page_num}...")
            lines = get_page_lines_real_text(page, page_num)

            # Save each page to output/pageNNN.txt
            filename = os.path.join(OUTPUT_DIR, f"page{page_num:03}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

            all_pages.append(lines)

        browser.close()

    # Save all pages to pages.json
    with open("pages.json", "w", encoding="utf-8") as jf:
        json.dump(all_pages, jf, ensure_ascii=False, indent=2)

    print("Done! All pages saved to output/*.txt and pages.json")

if __name__ == "__main__":
    main()
