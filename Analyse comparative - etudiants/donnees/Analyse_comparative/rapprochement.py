import pandas as pd


def rapprocher_donnees(df_lagune, df_baobab, df_comptoir):
    """
    Étape 3 : Rapprochement des données (Association de chaque article à son produit_id de P01 à P30)
    """
    print("\n=== 3. RAPPROCHEMENT DES CATALOGUES ===")

    # 1. Charger le catalogue de référence
    df_catalogue = pd.read_csv("catalogue_reference.csv")
    print(f"Catalogue de référence chargé : {len(df_catalogue)} produits de référence.")

    # -------------------------------------------------------------------------
    # A. Rapprochement pour Marché Lagune
    # -------------------------------------------------------------------------
    # Dictionnaire complet de correspondance (Désignation exacte -> P01 à P30)
    mapping_lagune = {
        "SAMSUNG GALAXY A15 (128GB)": "P01",
        "SAMSUNG GALAXY A25 (128GB)": "P02",
        "SAMSUNG GALAXY A55 (256GB)": "P03",
        "TECNO SPARK 20 - 128GB": "P04",
        "TECNO CAMON 30 - 256GB": "P05",
        "INFINIX HOT 40I 128GB": "P06",
        "INFINIX NOTE 40 256GB": "P07",
        "ITEL A70 64GB": "P08",
        "IPHONE 13 128GB": "P09",
        "XIAOMI REDMI NOTE 13 128GB": "P10",
        "PC PORTABLE HP 250 G9 I5 8GB/512GB": "P11",
        "PC PORTABLE LENOVO IDEAPAD 3 I3 8GB/256GB": "P12",
        "PC PORTABLE DELL INSPIRON 15 I5 16GB/512GB": "P13",
        "CLE USB SANDISK 64GB": "P14",
        "DISQUE DUR EXTERNE SEAGATE 1TB": "P15",
        "SOURIS SANS FIL LOGITECH M185": "P16",
        "IMPRIMANTE HP DESKJET 2720E": "P17",
        "ECRAN SAMSUNG 24\"": "P18",
        "REFRIGERATEUR HISENSE 205L": "P19",
        "CONGELATEUR NASCO 200L": "P20",
        "TV SAMSUNG 43\" CRYSTAL UHD 4K": "P21",
        "TV HISENSE 32\"": "P22",
        "CLIMATISEUR LG 1CV": "P23",
        "VENTILATEUR BINATONE 16\"": "P24",
        "MIXEUR MOULINEX 1.5L": "P25",
        "FER A REPASSER PHILIPS": "P26",
        "MICRO-ONDES SAMSUNG 23L": "P27",
        "CLIMATISEUR HISENSE 1.5CV": "P28"
    }

    # On nettoie la colonne designation de Lagune pour qu'elle corresponde exactement (majuscules, espaces)
    if 'designation' in df_lagune.columns:
        df_lagune['designation_clean'] = df_lagune['designation'].astype(str).str.strip().str.upper()
        df_lagune['produit_id'] = df_lagune['designation_clean'].map(mapping_lagune)
    else:
        df_lagune['produit_id'] = None
    print("Marché Lagune : association des produit_id effectuée.")

    # -------------------------------------------------------------------------
    # B. Rapprochement pour Baobab Shop
    # -------------------------------------------------------------------------
    # Si le champ 'sku' ou le titre permet de faire le lien direct
    try:
        if 'sku' in df_baobab.columns:
          df_baobab['produit_id'] = df_baobab['sku'].astype(str).str.strip()
        else:
           df_baobab['produit_id'] = None
           print("Baobab Shop : association des produit_id via le SKU effectuée.")
    except Exception as e:
                       print(f"[ERREUR] Problème lors du rapprochement Baobab Shop : {e}")
                       df_baobab['produit_id'] = None
    # -------------------------------------------------------------------------
    # C. Rapprochement pour Comptoir Ivoire
    # -------------------------------------------------------------------------
    # La colonne 'Code' contient déjà les identifiants P01-P30
    if 'Code' in df_comptoir.columns:
        df_comptoir['produit_id'] = df_comptoir['Code'].astype(str).str.strip()
    elif 'code' in df_comptoir.columns:
        df_comptoir['produit_id'] = df_comptoir['code'].astype(str).str.strip()
    else:
        df_comptoir['produit_id'] = None
    print("Comptoir Ivoire : association des produit_id via la colonne Code effectuée.")

    return df_lagune, df_baobab, df_comptoir