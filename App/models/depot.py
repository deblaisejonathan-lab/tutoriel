import json
import os

class DepotProduit:
    def __init__(self, filepath="data/tech/informatique/data.json"):
        self.filepath = filepath
        self._existance_fichier()

    def _existance_fichier(self):
        """S'assure que le dossier 'data' existe."""
        dir_name = os.path.dirname(self.filepath)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)

    def sauvegarder(self, produits):
        """Sauvegarde une liste de produits (objets Produit ou dictionnaires) dans un fichier."""
        data = [p.to_dict() if hasattr(p, 'to_dict') else p for p in produits]
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"[DEPOT] {len(produits)} produits enregistrés dans {self.filepath}")

    def charger(self) -> list:
        """Charge les produits depuis le fichier."""
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []