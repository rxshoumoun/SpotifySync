import streamlit as st
from scraper import setup_driver, get_playlist_metadata, get_track_data
from save_excel import save_to_excel
from selenium.webdriver.support.ui import WebDriverWait

st.set_page_config(page_title="Spotify Playlist Scraper", layout="wide")

st.title("Spotify Playlist Scraper")

playlist_url = st.text_input("Enter Spotify Playlist URL:")

if st.button("Scrape and Export"):
    if not playlist_url:
        st.error("Please enter a playlist URL.")
    else:
        st.info(f"Scraping: {playlist_url}")
        driver = setup_driver(headless=True)
        wait = WebDriverWait(driver, 20)
        try:
            driver.get(playlist_url)
            metadata = get_playlist_metadata(driver, wait)
            track_data = get_track_data(driver, wait)
        finally:
            driver.quit()
        output_path = "outputs/Spotify_Playlist_Export.xlsx"
        save_to_excel(metadata, track_data, output_path)
        st.success("Scraping complete! Download your file below:")
        with open(output_path, "rb") as f:
            st.download_button(
                label="Download Excel File",
                data=f,
                file_name="Spotify_Playlist_Export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )