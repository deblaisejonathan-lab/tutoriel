import pandas as pd


def calculer_panier(df_lagune, df_baobab, df_comptoir):
    """
    Étape 6 : Coût du panier de rentrée par enseigne et panier optimal.
    """
    print("\n=== 6. PANIER DE RENTRÉE ===")

    # 1. Définition de la composition du panier (produit_id: quantité)
    panier_quantites = {
        "P04": 1,  # Tecno Spark 20
        "P12": 1,  # Lenovo IdeaPad 3
        "P14": 2,  # Clés USB SanDisk (x2)
        "P15": 1,  # Disque dur Seagate
        "P28": 1  # Micro-ondes Samsung
    }

    # 2. Préparation d'une fonction d'extraction du prix net
    def obtenir_dictionnaire_prix(df):
        # On ne garde que les lignes qui ont un produit_id et un prix_net valide
        df_valide = df.dropna(subset=['produit_id', 'prix_net'])
        return dict(zip(df_valide['produit_id'], df_valide['prix_net']))

    prix_lagune = obtenir_dictionnaire_prix(df_lagune)
    prix_baobab = obtenir_dictionnaire_prix(df_baobab)
    prix_comptoir = obtenir_dictionnaire_prix(df_comptoir)

    enseignes_prix = {
        "Marché Lagune": prix_lagune,
        "Baobab Shop": prix_baobab,
        "Comptoir Ivoire": prix_comptoir
    }

    # 3. Calcul du coût du panier chez chaque enseigne
    totaux_enseignes = {}
    print("--- Coût du panier par enseigne ---")

    for nom_enseigne, dico_prix in enseignes_prix.items():
        total = 0
        incomplet = False

        for p_id, qte in panier_quantites.items():
            if p_id in dico_prix and pd.notna(dico_prix[p_id]):
                total += dico_prix[p_id] * qte
            else:
                incomplet = True

        if incomplet:
            print(f"- {nom_enseigne} : Panier incomplet (au moins un produit en rupture ou non référencé)")
            totaux_enseignes[nom_enseigne] = None
        else:
            totaux_enseignes[nom_enseigne] = total
            print(f"- {nom_enseigne} : {total:,.0f} FCFA".replace(",", " "))

    # 4. Calcul du panier OPTIMAL (le moins cher produit par produit)
    total_optimal = 0
    detail_optimal = []

    for p_id, qte in panier_quantites.items():
        prix_disponibles = {}
        for nom_enseigne, dico_prix in enseignes_prix.items():
            if p_id in dico_prix and pd.notna(dico_prix[p_id]):
                prix_disponibles[nom_enseigne] = dico_prix[p_id]

        if prix_disponibles:
            # Enseigne la moins chère pour ce produit
            meilleure_enseigne = min(prix_disponibles, key=prix_disponibles.get)
            meilleur_prix = prix_disponibles[meilleure_enseigne]

            sous_total = meilleur_prix * qte
            total_optimal += sous_total

            detail_optimal.append({
                "produit_id": p_id,
                "quantite": qte,
                "enseigne": meilleure_enseigne,
                "prix_unitaire": meilleur_prix,
                "sous_total": sous_total
            })

    print("\n--- Coût du panier OPTIMAL (article par article) ---")
    print(f"Total optimal : {total_optimal:,.0f} FCFA".replace(",", " "))
    print("\nDétail des achats optimaux :")
    for d in detail_optimal:
        print(
            f"  * {d['produit_id']} (x{d['quantite']}) -> Acheté chez {d['enseigne']} à {d['prix_unitaire']:,.0f} FCFA/unité (Sous-total : {d['sous_total']:,.0f} FCFA)".replace(
                ",", " "))

    return totaux_enseignes, total_optimal, detail_optimal
