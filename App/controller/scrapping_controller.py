# App/controller/scrapping_controller.py

class ScrappingController:
    def __init__(self, scraper, console_view, export_view):
        self.scraper = scraper
        self.console_view = console_view
        self.export_view = export_view

    def run(self, search_query: str, category: str):
        """Pilote le flux de scraping, l'affichage console et l'enregistrement."""
        self.console_view.display_message(f"Recherche en cours  '{search_query}'")


        produits = self.scraper.search_products(search_query)

        if not produits:
            self.console_view.display_error("Aucun produit récupéré.")
            return

        self.console_view.display_results(produits)

        self.export_view.save_data(produits, subpath=category)