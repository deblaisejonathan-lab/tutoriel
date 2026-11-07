# main.py
from App.controller.scrapping_controller import ScrappingController
from App.scrapper.amazon_scrapper import AmazonScraper
from App.views.console_views import ConsoleView
from App.views.export import ExportView


def main():
    scraper = AmazonScraper()
    console_view = ConsoleView()
    export_view = ExportView()

    controller = ScrappingController(
        scraper=scraper,
        console_view=console_view,
        export_view=export_view
    )

    while True:
        choice = console_view.show_menu()

        if choice == "1":
            query = input("\nQue cherchez-vous sur Amazon ? : ").strip()
            if not query:
                print("La recherche ne peut pas être vide.")
                continue

            category = input(
                "Sous quelle catégorie/dossier classer cette recherche ? (ex: tech/informatique, cuisine) : ").strip()
            if not category:
                category = query

            controller.run(search_query=query, category=category)

        elif choice == "2":
            console_view.list_and_show_backups()

        elif choice == "3":
            print("\nAu revoir ")
            break
        else:
            print("Option invalide, choisis entre 1, 2 ou 3.")


if __name__ == "__main__":
    main()