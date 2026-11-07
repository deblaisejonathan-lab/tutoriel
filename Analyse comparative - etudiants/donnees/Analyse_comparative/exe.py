from nettoyage import nettoyer_donnees
from rapprochement import rapprocher_donnees
from analyse import generer_comparatif, generer_synthese, mesurer_performance_historique
from panier import calculer_panier
from historique import analyser_historique_black_friday

def main():
    print("==================================================================")
    print("   ANALYSE COMPARATIVE DE MARCHÉ — DA PYTHON (EXÉCUTION DU MAIN)   ")
    print("==================================================================\n")

    print(">>> ÉTAPES 1 & 2 : CHARGEMENT ET NETTOYAGE DES DONNÉES")
    df_lagune, df_baobab, df_comptoir, journal_nettoyage = nettoyer_donnees()
    print("=== JOURNAL DE NETTOYAGE ===")
    for message in journal_nettoyage:
        print("-", message)

    print("\n>>> ÉTAPE 3 : RAPPROCHEMENT DES ARTICLES (ASSOCIATION AUX CODE P01-P30)")
    df_lagune, df_baobab, df_comptoir = rapprocher_donnees(df_lagune, df_baobab, df_comptoir)
    print("-" * 66)

    print("\n>>> ÉTAPE 4 : COMPARATIF ET SYNTHÈSE DE MARCHÉ")
    df_comparatif = generer_comparatif(df_lagune, df_baobab, df_comptoir)
    print(df_comparatif.head())

    print("-" * 66)
    print("\n>>> ÉTAPE 5 : SYNTHÈSE DES PRIX")
    nb_victoires, ecarts, top3 = generer_synthese(df_comparatif)

    print("\n>>> ÉTAPE 6 : EVALUATION DU PANIER DE RENTRÉE")
    calculer_panier(df_lagune, df_baobab, df_comptoir)
    print("-" * 66)

    print("\n>>> ÉTAPE 7 : ANALYSE DES TENDANCES HISTORIQUES ET BLACK FRIDAY")
    analyser_historique_black_friday()
    print("-" * 66)

    print("\n>>> ÉTAPE 8 : MESURE DES PERFORMANCES ET DE LA COMPLEXITÉ")
    mesurer_performance_historique()
    print("-" * 66)

    print("\n==================================================================")
    print("   EXÉCUTION DU PIPELINE TERMINÉE AVEC SUCCÈS !                   ")
    print("==================================================================")

if __name__ == "__main__":
    main()