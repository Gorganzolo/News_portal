from playwright.sync_api import sync_playwright
import time
import os

def run_cuj(page):
    # Открываем список новостей
    page.goto("http://localhost:8000/news/")
    page.wait_for_timeout(1000)

    # Делаем скриншот списка
    page.screenshot(path="/home/jules/verification/screenshots/news_list.png")
    page.wait_for_timeout(1000)

    # Находим первую ссылку на новость и кликаем
    first_news_link = page.locator(".post-title a").first
    if first_news_link.count() > 0:
        first_news_link.click()
        page.wait_for_timeout(1500)

        # Делаем скриншот детали новости
        page.screenshot(path="/home/jules/verification/screenshots/news_detail.png")
        page.wait_for_timeout(2000)
    else:
        print("Нет новостей для клика, скриншот детальной страницы пропущен.")

if __name__ == "__main__":
    os.makedirs("/home/jules/verification/videos", exist_ok=True)
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()  # MUST close context to save the video
            browser.close()
