import pandas as pd


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

