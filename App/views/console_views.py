# App/views/console_views.py
import os
import json

class ConsoleView:
    @staticmethod
    def show_menu() -> str:
        """Affiche le menu principal et retourne le choix de l'utilisateur."""
        print("\n" + "="*45)
        print("          AMAZON SCRAPER & DATA MANAGER      ")
        print("="*45)
        print("1.  Lancer un nouveau scraping Amazon")
        print("2.  Voir les sauvegardes / résultats")
        print("3.  Quitter")
        print("="*45)
        return input("Choisis une option (1-3) : ").strip()

    @staticmethod
    def display_message(msg: str):
        print(f"\n[INFO] {msg}")

    @staticmethod
    def display_error(msg: str):
        print(f"\n[ERREUR] {msg}")

    @staticmethod
    def display_results(produits: list):
        """Affiche la liste des produits extraits de manière lisible."""
        if not produits:
            print("\nAucun produit à afficher.")
            return

        print(f"\n--- {len(produits)} Produits Trouvés ---")
        for i, p in enumerate(produits, 1):
            # Compatibilité si p est un dictionnaire ou un objet
            if isinstance(p, dict):
                titre = p.get('titre', 'N/A')
                prix = p.get('prix', 'N/A')
                note = p.get('note', 'N/A')
                img = p.get('image_url', 'N/A')
            else:
                titre = getattr(p, 'titre', 'N/A')
                prix = getattr(p, 'prix', 'N/A')
                note = getattr(p, 'note', 'N/A')
                img = getattr(p, 'image_url', 'N/A')

            print(f"{i}. {titre}")
            print(f"   Prix : {prix} | Note : {note}")
            print(f"   Image: {img}")
            print("-" * 40)

    @staticmethod
    def list_and_show_backups(base_dir="data"):
        """Parcourt récursivement le dossier data/ et affiche les sauvegardes JSON trouvées."""
        print("\n" + "="*45)
        print("  HISTORIQUE DES SAUVEGARDES         ")
        print("="*45)

        if not os.path.exists(base_dir):
            print("Aucune sauvegarde trouvée (dossier data/ inexistant).")
            return

        json_files = []
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".json"):
                    full_path = os.path.join(root, file)
                    json_files.append(full_path)

        if not json_files:
            print("Aucun fichier JSON de sauvegarde trouvé.")
            return

        for idx, filepath in enumerate(json_files, 1):
            print(f"{idx}. {filepath}")

        choice = input("\nEntrez le numéro du fichier à consulter (ou Entrée pour revenir) : ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(json_files):
                selected_file = json_files[index]
                ConsoleView._read_json_file(selected_file)

    @staticmethod
    def _read_json_file(filepath: str):
        """Lit et affiche le contenu d'un fichier JSON de sauvegarde."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            print(f"\n=== Contenu de : {filepath} ({len(data)} éléments) ===")
            for i, p in enumerate(data, 1):
                print(f"{i}. {p.get('titre', 'N/A')}")
                print(f"   Prix : {p.get('prix', 'N/A')} | Note : {p.get('note', 'N/A')}")
                print(f"   Image: {p.get('image_url', 'N/A')}")
                print("-" * 35)
        except Exception as e:
            print(f"[ERREUR] Impossible de lire le fichier : {e}")