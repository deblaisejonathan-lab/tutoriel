# App/scrapper/parsing.py
from bs4 import BeautifulSoup


class Parsing:
    @staticmethod
    def parse_products(html_content: str) -> list:
        soup = BeautifulSoup(html_content, 'html.parser')
        produits = []

        items = soup.select('div.s-result-item[data-component-type="s-search-result"]')

        nombre_limite = 10
        for item in items[:nombre_limite]:
            try:
                title_elem = item.select_one("h2")
                titre = title_elem.get_text(strip=True) if title_elem else "N/A"

                rating_elem = item.select_one(".a-icon-alt") or item.select_one(".a-size-small")
                etoiles = rating_elem.get_text(strip=True).replace("\xa0", " ") if rating_elem else "N/A"


                price_elem = item.select_one(".a-price")
                prix = price_elem.get_text(strip=True).replace("\xa0", " ") if price_elem else "N/A"

                img_elem = item.select_one("img.s-image")
                photo = img_elem if img_elem and "src" in img_elem else "N/A"



                produits.append({
                    "titre": titre,
                    "prix": prix,
                    "note": etoiles,
                    "image_url": photo
                })
            except Exception as e:
                print(f"[AVERTISSEMENT] Erreur sur un produit : {e}")
                continue

        return produits