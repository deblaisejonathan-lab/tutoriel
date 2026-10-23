# App/views/export.py
import json
import os
from datetime import datetime


class ExportView:
    def __init__(self, base_dir="data"):
        self.base_dir = base_dir

    def save_data(self, produits, subpath="general"):
        """
        Sauvegarde les produits dans un sous-dossier dynamique (ex: tech/informatique).
        """
        clean_path = str(subpath).strip().lower().replace("\\", "/")
        path_parts = [p.strip().replace(" ", "_") for p in clean_path.split("/") if p.strip()]

        target_dir = os.path.join(self.base_dir, *path_parts)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        category_name = path_parts[-1] if path_parts else "general"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(target_dir, f"produits_{category_name}_{timestamp}.json")

        # Conversion des objets produits en dictionnaires si nécessaire
        data = []
        for p in produits:
            if isinstance(p, dict):
                data.append(p)
            elif hasattr(p, "to_dict"):
                data.append(p.to_dict())
            else:
                data.append(vars(p))

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"\n[EXPORT] Données rangées avec succès dans : {filename}")