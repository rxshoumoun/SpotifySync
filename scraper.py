import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_driver(headless=True):
    """
    Set up and return a Selenium Chrome WebDriver.
    :param headless: Run browser in headless mode if True.
    """
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_playlist_metadata(driver, wait):
    """
    Extract playlist metadata such as name, description, saves, song count, and duration.
    """
    playlist_name = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//h1[contains(@class, 'encore-text-headline-large')]"))).text
    desc_el = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//span[contains(@class, 'encore-text-body-small')]/div"))).text
    saves = driver.find_element(By.XPATH, "//span[contains(@class, 'w1TBi3o5CTM7zW1EB3Bm')]").text
    song_count = driver.find_element(By.XPATH, "//span[contains(@class, 'w1TBi3o5CTM7zW1EB3Bm') and contains(text(), 'songs')]").text
    duration = driver.find_element(By.XPATH, "//span[contains(@class, 'poz9gZKE7xqFwgk231J4')]").text
    return {
        "Playlist Name": playlist_name,
        "Description": desc_el if desc_el else "",
        "Total Saves": saves,
        "Number of Songs": song_count,
        "Total Duration": duration
    }

def scroll_to_load(driver, seconds=10):
    """
    Scroll to the bottom of the page to load all tracks.
    """
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(seconds)

def get_track_data(driver, wait):
    """
    Extract track data from the playlist page.
    Returns a list of dictionaries, one per track.
    """
    scroll_to_load(driver)
    rows = driver.find_elements(By.XPATH, "//div[@role='row' and .//div[@aria-colindex='2']]")[:21]
    data = []
    error_count = 0
    for idx, row in enumerate(rows):
        try:
            track_col = row.find_element(By.XPATH, ".//div[@aria-colindex='2']")
            track_name = track_col.find_element(By.XPATH, ".//div[@dir='auto' and contains(@class, 'encore-text-body-medium')]").text.strip()
            artist_links = track_col.find_elements(By.XPATH, ".//span[contains(@class, 'UudGCx16EmBkuFPllvss')]/div/a")
            artists = ", ".join([a.text.strip() for a in artist_links])
            album_elem = row.find_element(By.XPATH, ".//div[@aria-colindex='3']//a")
            album_name = album_elem.text.strip()
            date_added = row.find_element(By.XPATH, ".//div[@aria-colindex='4']//span").text.strip()
            duration = row.find_element(By.XPATH, ".//div[@aria-colindex='5']").text.strip()
            data.append({
                "Track Name": track_name,
                "Artist(s)": artists,
                "Album Name": album_name,
                "Date Added": date_added,
                "Duration (mm:ss)": duration
            })
        except Exception:
            # Count and report rows that could not be parsed
            error_count += 1
    if error_count > 0:
        print(f"{error_count} row(s) skipped due to missing elements.")
    return data