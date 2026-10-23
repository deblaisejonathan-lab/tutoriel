# App/scrapper/amazon_scrapper.py
import time
from selenium.webdriver.common.by import By
from App.scrapper.driver import Driver
from App.scrapper.parsing import Parsing


class AmazonScraper:
    def __init__(self):
        self.driver_manager = Driver()

    def search_products(self, query: str) -> list:
        driver = self.driver_manager.get_driver()
        produits = []

        try:
            driver.get("https://www.amazon.fr")
            time.sleep(4)

            box = driver.find_element(By.ID, "twotabsearchtextbox")
            box.send_keys(query)

            bouton = driver.find_element(By.ID, "nav-search-submit-button")
            bouton.click()

            time.sleep(5)

            html_content = driver.page_source
            produits = Parsing.parse_products(html_content)

        except Exception as e:
            print(f"[ERREUR SCRAPER] {e}")

        finally:
            driver.quit()
            print("[SCRAPER] Navigateur fermé.")

        return produits