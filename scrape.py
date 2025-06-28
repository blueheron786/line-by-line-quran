import time
from playwright.sync_api import sync_playwright

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
                print("Clicking Reading button...")
                button.click()
                time.sleep(delay)
            else:
                print("Reading button not found")
                break
        except Exception as e:
            print(f"Error clicking Reading button: {e}")
            break

def get_page_lines_real_text(page_num):
    url = f"https://quran.com/page/{page_num}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        print(f"Loading page {page_num}...")
        page.goto(url)
        page.wait_for_load_state('networkidle')
        time.sleep(2)

        click_reading_button(page, clicks=3, delay=1.0)

        lines = []
        for i in range(1, 16):
            selector = f"#Page{page_num}-Line{i}"
            line_div = page.query_selector(selector)
            if not line_div:
                print(f"Line {i} not found")
                lines.append("")
                continue

            hidden_div = line_div.query_selector('div[class*="SeoTextForVerse_visuallyHidden"]')
            if not hidden_div:
                print(f"Hidden text div not found in line {i}")
                lines.append("")
                continue

            first_child = hidden_div.query_selector("div")
            text = first_child.inner_text().strip() if first_child else hidden_div.inner_text().strip()
            lines.append(text)

        browser.close()
        return lines

if __name__ == "__main__":
    page_num = 7
    lines = get_page_lines_real_text(page_num)

    filename = f"page{page_num}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Saved page {page_num} text to {filename}")
