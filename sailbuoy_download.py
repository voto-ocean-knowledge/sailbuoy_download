import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import json
import logging
from pathlib import Path

_log = logging.getLogger(__name__)
with open(f"sb_secrets.json") as json_file:
    secrets = json.load(json_file)
data_dir = Path("/home/pipeline/sailbuoy_download/nrt")


def download_sailbuoy(sb_id_list):
    _log.info("start sailbuoy download process")
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")
    service = FirefoxService(executable_path="/snap/bin/geckodriver")
    driver = webdriver.Firefox(service=service, options=firefox_options)
    _log.info("configured driver")
    driver.get("https://ids.sailbuoy.no")  # load webpage
    driver.find_element("id", "UserName").send_keys(secrets["sb_user"])
    driver.find_element("id", "Password").send_keys(secrets["sb_password"])
    element = driver.find_element(
        "css selector", "input[type='submit']"
    )  # find the submit button
    element.click()  # click the submit button
    time.sleep(2)  # give the page time to load
    _log.info("logged in ")
    # make the cookies accessible for the session
    session = requests.Session()
    cookies = driver.get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"])

    _log.info("start downloads")
    for sb_id in sb_id_list:
        download_link1 = f"https://ids.sailbuoy.no/GenCustomData/_DownloadAllAsCSV?instrName={sb_id}A"  # Autopilot
        download_link2 = f"https://ids.sailbuoy.no/GenCustomData/_DownloadAllAsCSV?instrName={sb_id}D"  # Payload
        response1 = session.get(download_link1)
        response2 = session.get(download_link2)
        # at this point, the downloadable csv files are stored in the response object
        _log.info(f"write {sb_id} to file")
        if not data_dir.exists():
            data_dir.mkdir(parents=True)
        with open(data_dir / f"{sb_id}_nav.csv", "w") as file:
            file.write(str(response1.text))
            _log.info(f"wrote {sb_id}_nav.csv")
        with open(data_dir / f"{sb_id}_pld.csv", "w") as file:
            file.write(str(response2.text))
            _log.info(f"wrote {sb_id}_pld.csv")
        extra_pld_url = f"https://ids.sailbuoy.no/GenCustomData/_DownloadAllAsCSV?instrName={sb_id}D2"
        extra_response = session.get(extra_pld_url)
        if extra_response.status_code == 200:
            _log.info(f"extra pld file {sb_id}_pld_2.csv")
            with open(data_dir / f"{sb_id}_pld_2.csv", "w") as file:
                file.write(str(extra_response.text))
        session.close()


if __name__ == "__main__":
    logging.basicConfig(
        filename="voto_add_sailbuoy.log",
        filemode="a",
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    download_sailbuoy(["SB2016",
                       "SB2017",
                       "SB2120",
                       "SB2121",])

_log.info("Finished download of sailbuoy data\n")
