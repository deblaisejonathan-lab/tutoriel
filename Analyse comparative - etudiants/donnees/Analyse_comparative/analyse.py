import json
import os
import time as t

import pandas as pd

#dossier=r"C:\Users\HP\PythonProject\IIT_TRAV\Analyse comparative - etudiants\donnees"


# Exécution et affichage du journal de nettoyage


def generer_comparatif(df_lagune, df_baobab, df_comptoir):
    """
    Étape 4 : Comparatif des prix, identification du moins cher et export CSV.
    """
    print("\n=== 4. COMPARATIF DES PRIX ===")

    # 1. Uniformiser les tables pour ne garder que l'essentiel : produit_id et prix_net
    # (On s'assure d'exclure les lignes où le prix est NaN ou en rupture)
    lagune_clean = df_lagune[['produit_id', 'prix_net']].copy()
    lagune_clean['enseigne'] = 'Marché Lagune'

    baobab_clean = df_baobab[['produit_id', 'prix_net']].copy()
    baobab_clean['enseigne'] = 'Baobab Shop'

    comptoir_clean = df_comptoir[['produit_id', 'prix_net']].copy()
    comptoir_clean['enseigne'] = 'Comptoir Ivoire'

    # 2. Fusionner toutes les enseignes dans un seul grand tableau
    tous_les_prix = pd.concat([lagune_clean, baobab_clean, comptoir_clean], ignore_index=True)
    tous_les_prix = tous_les_prix.dropna(subset=['produit_id', 'prix_net'])

    # 3. Transformer en tableau croisé (Pivot Table) : un produit par ligne, une colonne par enseigne
    tableau_comparatif = tous_les_prix.pivot_table(
        index='produit_id',
        columns='enseigne',
        values='prix_net'
    ).reset_index()

    # 4. Filtrer pour ne garder que les produits présents dans AU MOINS DEUX enseignes
    # On compte combien de colonnes d'enseignes ont un prix non nul pour chaque produit
    colonnes_enseignes = [col for col in tableau_comparatif.columns if col != 'produit_id']
    tableau_comparatif['nb_enseignes'] = tableau_comparatif[colonnes_enseignes].notna().sum(axis=1)

    # On filtre (>= 2 enseignes)
    tableau_comparatif = tableau_comparatif[tableau_comparatif['nb_enseignes'] >= 2]

    # 5. Trouver l'enseigne la moins chère et calculer les écarts
    enseigne_moins_chere = []
    prix_min_list = []
    ecart_fcfa_list = []
    ecart_pct_list = []

    for index, row in tableau_comparatif.iterrows():
        # Extraire uniquement les prix des enseignes pour cette ligne
        prix_produits = row[colonnes_enseignes].dropna()

        if len(prix_produits) >= 2:
            p_min = prix_produits.min()
            p_max = prix_produits.max()
            moins_cher = prix_produits.idxmin()

            ecart_fcfa = p_max - p_min
            ecart_pct = (ecart_fcfa / p_min) * 100 if p_min > 0 else 0

            enseigne_moins_chere.append(moins_cher)
            prix_min_list.append(p_min)
            ecart_fcfa_list.append(ecart_fcfa)
            ecart_pct_list.append(round(ecart_pct, 2))
        else:
            enseigne_moins_chere.append(None)
            prix_min_list.append(None)
            ecart_fcfa_list.append(None)
            ecart_pct_list.append(None)

    tableau_comparatif['moins_cher'] = enseigne_moins_chere
    tableau_comparatif['prix_min'] = prix_min_list
    tableau_comparatif['ecart_fcfa'] = ecart_fcfa_list
    tableau_comparatif['ecart_pourcentage'] = ecart_pct_list

    # 6. Exporter le tableau final en CSV
    nom_fichier_sortie = "comparatif_prix_enseignes.csv"
    tableau_comparatif.to_csv(nom_fichier_sortie, index=False, encoding="utf-8-sig")
    print(f"[OK] Comparatif généré avec succès ! Fichier exporté : {nom_fichier_sortie}")

    return tableau_comparatif


def generer_synthese(df_comparatif):
    """
    Étape 5 : Synthèse du comparatif (moins cher, écart moyen, top 3 des économies)
    """
    print("\n=== 5. SYNTHÈSE DES PRIX ===")

    # 1. Combien de fois chaque enseigne est-elle la moins chère ?
    nb_moins_cher = df_comparatif['moins_cher'].value_counts()
    print("\n--- Nombre de fois où chaque enseigne est la moins chère ---")
    print(nb_moins_cher)

    # 2. Quel est l'écart moyen en % de chaque enseigne par rapport au prix le plus bas ?
    # Pour chaque enseigne présente dans le comparatif, on calcule l'écart en % par rapport à prix_min
    colonnes_enseignes = [col for col in ['Marché Lagune', 'Baobab Shop', 'Comptoir Ivoire'] if
                          col in df_comparatif.columns]

    ecarts_moyens = {}
    for enseigne in colonnes_enseignes:
        # Écart en % pour un produit donné = ((Prix Enseigne - Prix Min) / Prix Min) * 100
        ecart_pct_enseigne = ((df_comparatif[enseigne] - df_comparatif['prix_min']) / df_comparatif['prix_min']) * 100
        ecarts_moyens[enseigne] = ecart_pct_enseigne.mean()

    print("\n--- Écart moyen en pourcentage par rapport au prix le plus bas ---")
    for ens, val in ecarts_moyens.items():
        print(f"- {ens} : +{val:.2f}% en moyenne par rapport au moins cher")

    # 3. Quels sont les trois produits où il y a le plus à gagner à comparer ?
    # On trie le tableau par écart en FCFA décroissant et on prend les 3 premiers
    top_3_gains = df_comparatif.sort_values(by='ecart_fcfa', ascending=False).head(3)

    print("\n--- Top 3 des produits où il y a le plus à gagner (plus grand écart en FCFA) ---")
    for index, row in top_3_gains.iterrows():
        print(
            f"Produit ID : {row['produit_id']} | Écart maximal : {row['ecart_fcfa']} FCFA ({row['ecart_pourcentage']}%)")

    return nb_moins_cher, ecarts_moyens, top_3_gains


def analyser_historique_black_friday():
    """
    Étape 7 : Comparaison des prix du Black Friday (24-30 nov 2025) au prix moyen de l'année.
    """
    print("\n=== 7. ANALYSE HISTORIQUE & BLACK FRIDAY ===")

    # 1. Charger l'historique des prix
    df_hist = pd.read_csv("historique_prix.csv")

    # Conversion de la colonne date en type datetime
    df_hist['date'] = pd.to_datetime(df_hist['date'])

    # 2. Isoler la semaine du Black Friday (du 24 au 30 novembre 2025)
    mask_bf = (df_hist['date'] >= '2025-11-24') & (df_hist['date'] <= '2025-11-30')
    df_bf = df_hist[mask_bf]

    # 3. Calculer le prix moyen pendant la semaine du Black Friday par enseigne (source)
    moyenne_bf = df_bf.groupby('source')['prix_fcfa'].mean()

    # 4. Calculer le prix moyen sur toute l'année par enseigne (source)
    moyenne_annee = df_hist.groupby('source')['prix_fcfa'].mean()

    # 5. Regrouper les résultats dans un tableau de synthèse
    comparaison_df = pd.DataFrame({
        'Prix moyen Black Friday': moyenne_bf,
        'Prix moyen Annuel': moyenne_annee
    })

    # Calcul de l'écart en pourcentage (%)
    comparaison_df['Écart (%)'] = ((comparaison_df['Prix moyen Black Friday'] - comparaison_df['Prix moyen Annuel']) /
                                   comparaison_df['Prix moyen Annuel']) * 100

    print("\n--- Comparaison Black Friday vs Moyenne Annuelle par Enseigne ---")
    print(comparaison_df.round(2))

    print("\nInterprétation :")
    print("- Si l'écart est négatif (ex: -5%), le Black Friday était plus intéressant (prix plus bas).")
    print("- Si l'écart est positif, les prix étaient plus élevés ou la période n'offrait pas de rabais significatif.")

    return comparaison_df

def mesurer_performance_historique():
    """
    Étape 8 : Mesure du temps d'exécution sur l'historique de 20 000+ lignes.
    """
    print("\n=== 8. COMPLEXITÉ ET PERFORMANCE ===")

    # 1. Démarrage du chronomètre
    debut = t.time()

    # 2. Chargement du fichier volumineux (> 20 000 lignes)
    df_hist = pd.read_csv("historique_prix.csv")

    # 3. Traitement vectorisé (conversion de dates et regroupement)
    df_hist['date'] = pd.to_datetime(df_hist['date'])

    # Exemple d'agrégation lourde
    resultat_gp = df_hist.groupby(['source', 'produit_id'])['prix_fcfa'].mean()

    # 4. Arrêt du chronomètre
    fin = t.time()

    # Calcul du temps total
    temps_ecoule = fin - debut
    print(f"Nombre de lignes traitées : {len(df_hist):,}")
    print(f"Temps d'exécution : {temps_ecoule:.4f} secondes.")

    return temps_ecoule

