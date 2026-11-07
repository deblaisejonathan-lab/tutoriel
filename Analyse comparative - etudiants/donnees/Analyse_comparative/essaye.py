import time
from datetime import datetime
import json
import numpy as np
import pandas as pd


# ==========================================
# CONFIGURATION ET CHARGEMENT DES DONNÉES
# ==========================================
DOSSIER = r"C:\Users\HP\PythonProject\IIT_TRAV\Analyse comparative - etudiants\donnees/"

# 1. Chargement des sources
df_ref = pd.read_csv(DOSSIER + "catalogue_reference.csv")
df_lagune = pd.read_csv(DOSSIER + "marche_lagune.csv", sep=";")

with open(DOSSIER + "baobab_shop.json", "r", encoding="utf-8") as f:
  data_baobab = json.load(f)
df_baobab = pd.json_normalize(data_baobab["items"])

df_comptoir = pd.read_excel(
    DOSSIER + "comptoir_ivoire.xlsx",
    sheet_name="Tarifs octobre 2026",
    skiprows=2,
)

df_histo = pd.read_csv(DOSSIER + "historique_prix.csv")

print("--- 1. CHARGEMENT TERMINÉ ---")

# ==========================================
# 2. NETTOYAGE DES DONNÉES ET JOURNALISATION
# ==========================================
journal_anomalies = []


def nettoyer_prix_lagune(val):
  if pd.isna(val):
    return np.nan
  val_clean = (
      str(val)
      .replace("FCFA", "")
      .replace("\xa0", "")
      .replace(" ", "")
      .strip()
  )
  try:
    return float(val_clean)
  except ValueError:
    journal_anomalies.append(f"[Lagune] Prix invalide détecté : {val}")
    return np.nan


# Calcul des prix nets payés par le client (incluant livraison/remises selon les règles)
df_lagune["prix_net"] = df_lagune["prix"].apply(nettoyer_prix_lagune)
df_baobab["prix_net"] = (
    df_baobab["pricing.amount"] + df_baobab["pricing.delivery_fee"]
)
# 1. Nettoyer et convertir le prix catalogue en nombres (au cas où il y aurait du texte)
df_comptoir["Prix catalogue (FCFA)"] = pd.to_numeric(
    df_comptoir["Prix catalogue (FCFA)"]
    .astype(str)
    .str.replace("FCFA", "", regex=False)
    .str.replace(" ", "", regex=False)
    .str.replace("\xa0", "", regex=False)
    .str.replace(",", ".", regex=False),
    errors="coerce",
)

# 2. Idem pour la remise (%) au cas où elle contiendrait du texte ou des pourcentages (%)
df_comptoir["Remise (%)"] = pd.to_numeric(
    df_comptoir["Remise (%)"]
    .astype(str)
    .str.replace("%", "", regex=False)
    .str.replace(" ", "", regex=False)
    .str.replace(",", ".", regex=False),
    errors="coerce",
).fillna(0)  # Si la remise est vide, on met 0%

# 3. Calcul du prix net
df_comptoir["prix_net"] = df_comptoir["Prix catalogue (FCFA)"] * (
    1 - df_comptoir["Remise (%)"] / 100
)


print(
    f"--- 2. NETTOYAGE TERMINÉ (Anomalies répertoriées :"
    f" {len(journal_anomalies)}) ---"
)

# ==========================================
# 3. RAPPROCHEMENT ET COMPARATIF
# ==========================================
# (Exemple de structure pour le comparatif global des prix par produit_id)
start_time = time.time()

# ------------------------------------------
# 6. CALCUL DU PANIER DE RENTRÉE
# ------------------------------------------
# Panier : 1 Tecno Spark 20 (P04), 1 Lenovo IdeaPad 3 (P12), 2 clés USB SanDisk (P14), 1 disque dur Seagate (P15), 1 micro-ondes Samsung (P28)
panier = {"P04": 1, "P12": 1, "P14": 2, "P15": 1, "P28": 1}
print("--- 6. PANIER DE RENTRÉE PRÊT À ÊTRE ÉVALUÉ ---")

# ==========================================
# 7. ANALYSE HISTORIQUE (BLACK FRIDAY)
# ==========================================
df_histo["date"] = pd.to_datetime(df_histo["date"])
mask_bf = (df_histo["date"] >= "2025-11-24") & (
    df_histo["date"] <= "2025-11-30"
)
prix_bf = df_histo[mask_bf].groupby("source")["prix_fcfa"].mean()
prix_moyen = df_histo.groupby("source")["prix_fcfa"].mean()

comparatif_bf = pd.DataFrame(
    {"Prix Moyen Black Friday": prix_bf, "Prix Moyen Annuel": prix_moyen}
)
print("\n--- 7. SYNTHÈSE BLACK FRIDAY VS MOYENNE ANNUELLE ---")
print(comparatif_bf)

# ==========================================
# 8. COMPLEXITÉ ET PERFORMANCE
# ==========================================
execution_time = time.time() - start_time
print(f"\n--- 8. PERFORMANCE ---")
print(
    f"Temps d'exécution global de traitement : {execution_time:.4f} secondes"
)
print(
    "Choix de structure : Utilisation de Pandas (vecteurs C sous-jacents) pour"
    " traiter les > 20 000 lignes de l'historique sans boucles lentes."
)