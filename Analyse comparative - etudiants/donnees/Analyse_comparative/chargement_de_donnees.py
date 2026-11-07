import json

import pandas as pd


def ChargerFichier():
    try:
        df_lagune = pd.read_csv("marche_lagune.csv",sep=";")
        print("lagune charge")
    except FileNotFoundError:
        print("[ERREUR] Le fichier 'marche_lagune.csv' est introuvable.")
        df_lagune=None

    try:
        with open("baobab_shop.json","r",encoding="utf-8") as f:
            data_baobab=json.load(f)
            items_baobab=data_baobab.get("items",[])
            df_baobab=pd.DataFrame(items_baobab)
            print("baobab charge")
    except FileNotFoundError:
        print("[ERREUR] Le fichier 'baobab_shop.json' est introuvable.")
        df_baobab=None
        # Selon la consigne : Feuille "Tarifs octobre 2026", en-têtes en ligne 3 (skiprows=2)
    try:
            df_comptoir = pd.read_excel(
                "comptoir_ivoire.xlsx",
                sheet_name="Tarifs octobre 2026",
                skiprows=2
            )
            print(f"[OK] Comptoir Ivoire chargé : {len(df_comptoir)} lignes.")
    except FileNotFoundError:
            print("[ERREUR] Le fichier 'comptoir_ivoire.xlsx' est introuvable.")
            df_comptoir = None


    return df_lagune, df_baobab, df_comptoir
