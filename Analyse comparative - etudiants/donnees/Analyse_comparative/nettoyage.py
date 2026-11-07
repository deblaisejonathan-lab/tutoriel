import json
import os

import pandas as pd


def nettoyer_donnees():
    # Journal de nettoyage requis par l'étape 2
    journal = []

    # -------------------------------------------------------------------------
    # 1. NETTOYAGE : MARCHÉ LAGUNE (CSV)
    # -------------------------------------------------------------------------
    chemin_lagune = os.path.join( "marche_lagune.csv")
    df_lagune = pd.read_csv(chemin_lagune, sep=";")

    # Nettoyage de la désignation (noms des produits)
    df_lagune['designation_propre'] = df_lagune['designation'].astype(str).str.strip()

    # Nettoyage de la colonne 'prix' (ex: "102 900 FCFA" -> 102900.0)
    def nettoyer_prix_lagune(val):
        if pd.isna(val):
            return None
        # Convertir en chaîne, supprimer 'FCFA', espaces et remplacer la virgule
        val_str = str(val).replace('FCFA', '').replace('fcfa', '').strip()
        val_str = pd.Series([val_str]).str.replace(r'\s+', '', regex=True).iloc[0]
        val_str = val_str.replace(',', '.')
        try:
            return float(val_str)
        except ValueError:
            return None

    df_lagune['prix_net'] = df_lagune['prix'].apply(nettoyer_prix_lagune)

    # Enregistrement des anomalies dans le journal
    nb_prix_nan_lagune = df_lagune['prix_net'].isna().sum()
    if nb_prix_nan_lagune > 0:
        journal.append(
            f"[Marché Lagune] {nb_prix_nan_lagune} prix invalides ou manquants détectés et convertis en NaN.")
    journal.append(f"[Marché Lagune] {len(df_lagune)} lignes chargées et désignations nettoyées.")

    # -------------------------------------------------------------------------
    # 2. NETTOYAGE : BAOBAB SHOP (JSON)
    # -------------------------------------------------------------------------
    chemin_baobab = os.path.join("baobab_shop.json")
    with open(chemin_baobab, "r", encoding="utf-8") as f:
        data_baobab = json.load(f)

    items_baobab = []
    for item in data_baobab.get("items", []):
        amount = item.get("pricing", {}).get("amount")
        delivery = item.get("pricing", {}).get("delivery_fee", 0)

        # Le client paie amount + delivery_fee
        if amount is not None:
            prix_total = float(amount) + float(delivery)
        else:
            prix_total = None

        items_baobab.append({
            "sku": item.get("sku"),
            "title_propre": str(item.get("title", "")).strip(),
            "prix_net": prix_total,
            "stock": item.get("stock"),
            "note": item.get("rating", {}).get("average")
        })

    df_baobab = pd.DataFrame(items_baobab)
    nb_prix_nan_baobab = df_baobab['prix_net'].isna().sum()
    if nb_prix_nan_baobab > 0:
        journal.append(f"[Baobab Shop] {nb_prix_nan_baobab} prix manquants détectés.")
    journal.append(
        f"[Baobab Shop] {len(df_baobab)} articles chargés, frais de livraison inclus (amount + delivery_fee).")

    # -------------------------------------------------------------------------
    # 3. NETTOYAGE : COMPTOIR IVOIRE (Excel)
    # -------------------------------------------------------------------------
    chemin_comptoir = os.path.join( "comptoir_ivoire.xlsx")
    df_comptoir = pd.read_excel(chemin_comptoir, sheet_name="Tarifs octobre 2026", skiprows=2)

    # Nettoyage des noms d'articles
    df_comptoir['article_propre'] = df_comptoir['Article'].astype(str).str.strip()

    # Calcul du prix net : Prix catalogue - Remise (%)
    prix_catalogue = pd.to_numeric(df_comptoir['Prix catalogue (FCFA)'], errors='coerce')
    remise = pd.to_numeric(df_comptoir['Remise (%)'], errors='coerce').fillna(0)

    df_comptoir['prix_net'] = prix_catalogue * (1 - remise / 100)

    nb_prix_nan_comptoir = df_comptoir['prix_net'].isna().sum()
    if nb_prix_nan_comptoir > 0:
        journal.append(f"[Comptoir Ivoire] {nb_prix_nan_comptoir} prix catalogues invalides détectés.")
    journal.append(
        f"[Comptoir Ivoire] {len(df_comptoir)} articles chargés, application des remises en pourcentage effectuée.")

    return df_lagune, df_baobab, df_comptoir, journal
