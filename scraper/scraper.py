from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time
from locations import asia_places, indian_subcontinent_places, middle_east_and_red_sea_places, africa_places, America_places


class EmiratesOfficeScraper:
    def __init__(self, download_dir="/downloads", country = "India"):
        self.country = country
        self.download_dir = download_dir
        self.driver = self._init_driver()
        self.wait = WebDriverWait(self.driver, 10)

    def _init_driver(self):
        service = Service("/opt/homebrew/bin/chromedriver")  # customize as needed
        options = Options()
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": self.download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            },
        )
        return webdriver.Chrome(service=service, options=options)

    def open_website(self, url):
        self.driver.get(url)

    def search_country(self):
        search_box = self.driver.find_element(By.XPATH, "/html/body/section[3]/div/div/form/div/input")
        search_box.send_keys(self.country)
        search_box.submit()
        time.sleep(5)

    def select_demurrage_option(self):
        demurrage_select = self.driver.find_element(By.XPATH, "/html/body/section[3]/div/div/ul/li[3]")
        demurrage_select.click()
        time.sleep(5)

    def get_dropdown_items(self):
        dropdown = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/section[3]/div/div/div/div[3]/div/div[4]/div[1]/div/div")
        ))
        dropdown.click()

        li_elements = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "/html/body/section[3]/div/div/div/div[3]/div/div[4]/div[1]/div/ul/li")
        ))

        time.sleep(0.5)  # extra wait for full text
        options = []
        for li in li_elements:
            text = li.text.strip() or li.get_attribute("textContent").strip()
            options.append(text)
        return options

    def scrape_data_for_option(self, index, option_text):
        try:
            self.open_dropdown_and_select(index)

            self.expand_charges_section()

            for table_index in range(1, 4):
                self.extract_and_save_table(option_text, table_index)

            time.sleep(3)  # Optional pause between iterations

        except Exception as e:
            print(f"❌ Error on dropdown item {index + 1} ({option_text}): {e}")

    def open_dropdown_and_select(self, index):
        dropdown = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/section[3]/div/div/div/div[3]/div/div[4]/div[1]/div/div")
        ))
        dropdown.click()

        li_elements = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "/html/body/section[3]/div/div/div/div[3]/div/div[4]/div[1]/div/ul/li")
        ))

        if index >= len(li_elements):
            raise IndexError("Dropdown index out of range")

        li_elements[index].click()
        print(f"Selecting option: {li_elements[index].text.strip()}")

    def expand_charges_section(self):
        expand_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/section[3]/div/div/div/div[3]/div/div[5]/div[5]/button")
        ))
        expand_button.click()

        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/section[3]/div/div/div/div[3]/div/div[5]/div[5]/div/div/h4[1]")
        ))

    def extract_and_save_table(self, option_text, table_index):
        try:
            h4_xpath = f"/html/body/section[3]/div/div/div/div[3]/div/div[5]/div[5]/div/div/h4[{table_index}]"
            h4_elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, h4_xpath))
            )
            WebDriverWait(self.driver, 10).until(lambda d: h4_elem.text.strip() != "")
            h4_text = h4_elem.text.strip().replace(" ", "_").replace("/", "_")
            print(f"→ Processing table: {h4_text}")

            table_xpath = f"/html/body/section[3]/div/div/div/div[3]/div/div[5]/div[5]/div/div/table[{table_index}]"
            table_elem = self.driver.find_element(By.XPATH, table_xpath)

            headers = [th.text.strip() for th in table_elem.find_elements(By.XPATH, ".//thead/tr/th")]
            rows = table_elem.find_elements(By.XPATH, ".//tbody/tr")
            data = [[td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")] for row in rows]

            if headers and data:
                dir_path = os.path.join("downloads",self.country ,option_text)
                os.makedirs(dir_path, exist_ok=True)
                filename = os.path.join(dir_path, f"{h4_text}.csv")
                df = pd.DataFrame(data, columns=headers)
                df.to_csv(filename, index=False, encoding="utf-8-sig")
                print(f"✅ Saved: {filename}")
            else:
                print(f"⚠️ Table {table_index} under '{option_text}' is empty or malformed.")
        except Exception as e:
            print(f"❌ Error processing table {table_index} for '{option_text}': {e}")

    def run(self):
        self.open_website("https://www.emiratesline.com/our-offices/")
        self.search_country()
        self.select_demurrage_option()


        try:
            dropdown_options = self.get_dropdown_items()
        except Exception as e:
            print(f"⚠️ Skipping '{self.country}' due to error while fetching dropdown items: {e}")
            return  # Skip this country and move to the next one

        for i, option in enumerate(dropdown_options):
            self.scrape_data_for_option(i, option)


        self.driver.quit()


if __name__ == "__main__":
    for i in asia_places:
        scraper = EmiratesOfficeScraper(download_dir="downloads", country=i)
        scraper.run()
    for i in indian_subcontinent_places:
        scraper = EmiratesOfficeScraper(download_dir="downloads", country=i)
        scraper.run()
    for i in middle_east_and_red_sea_places:
        scraper = EmiratesOfficeScraper(download_dir="downloads", country=i)
        scraper.run()
    for i in africa_places:
        scraper = EmiratesOfficeScraper(download_dir="downloads", country=i)
        scraper.run()
    for i in America_places:
        scraper = EmiratesOfficeScraper(download_dir="downloads", country=i)
        scraper.run()
    print("All data scraped successfully!")
    
