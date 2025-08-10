import sys
from scraper import setup_driver, get_playlist_metadata, get_track_data
from save_excel import save_to_excel
from selenium.webdriver.support.ui import WebDriverWait

def main():
    """
    Main entry point for scraping a Spotify playlist and exporting to Excel.
    """
    if len(sys.argv) < 2:
        print("Usage: python spotify_scraper.py <playlist_url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"Scraping: {url}")
    driver = setup_driver(headless=False)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(url)
        metadata = get_playlist_metadata(driver, wait)
        track_data = get_track_data(driver, wait)
    finally:
        driver.quit()

    save_to_excel(metadata, track_data, "outputs/Spotify_Playlist_Export.xlsx")

if __name__ == "__main__":
    main()
 