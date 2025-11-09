import os
from playwright.sync_api import sync_playwright
import random, time

URLS_FILE = "product_urls.txt"
BASE_DIR = "guests"

def load_urls():
    with open(URLS_FILE) as f:
        return [l.strip() for l in f if l.strip() and 'etsy.com' in l]

def add_all(guest_id):
    urls = load_urls()
    print(f"\n[GUEST #{guest_id}] {len(urls)} products...")
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=f"{BASE_DIR}/guest_{guest_id}",
            headless=False,
            viewport={"width": 1024, "height": 768},
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu"]
        )
        page = context.new_page()
        for url in urls:
            try:
                page.goto(url, timeout=90000)
                time.sleep(random.uniform(10, 18))
                btn = page.locator('button[data-add-to-cart-button]').first
                btn.click(force=True)
                print(f" → ADDED: {url}")
                time.sleep(random.uniform(60, 120))
            except: print(f" → FAILED: {url}")
        context.close()

os.makedirs(BASE_DIR, exist_ok=True)
for day in range(1, 61):
    print(f"\nDAY {day}/60")
    for i in range(1, 26):
        add_all(i)
        time.sleep(1800)
    time.sleep(6 * 3600)
