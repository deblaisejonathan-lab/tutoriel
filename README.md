PROJET DE SCRAPPING SUR AMAZONE

il est fait  sur format  MVC 


 Description du Projet

Conçu selon une architecture modulaire et structurée, l'outil garantit la discrétion opérationnelle grâce à un mode d'exécution silencieux (headless) .

---

Architecture Technique (Modèle MVC)
L'arborescence du projet sépare strictement les responsabilités pour assurer la maintenabilité et la robustesse des opérations :

App/scrapper: Modules d'automatisation de la navigation et d'extraction brute des flux cibles. driver.py` : Gestion du navigateur en mode furtif et silencieux (*Headless*).
parsing.py : Analyse syntaxique du code source pour extraire les indicateurs cibles (titres, prix, URLs, médias).
amazon_scrapper.py : Pilotage de la session vers la cible.
App/controller/ : Orchestration des flux de travail (*ScrapingController*).
App/views/: Interfaces de restitution et de stockage.
console_views.py : Interface textuelle interactive et module d'audit des rapports.
export.py : Moteur de sérialisation et d'exportation sécurisée au format JSON dans une arborescence dynamique.
data/ : Répertoire de stockage des preuves et rapports d'analyse classés par catégories.

---

 Fonctionnalités 

1. Collecte Cible Automatisée : Recherche et extraction des informations d'intérêt sur la cible.
2. Mode Furtif & Silencieux :Exécution en arrière-plan sans affichage de l'interface graphique du navigateur pour plus de discrétion.
3. Exportation Structurée :Sauvegarde automatique des rapports au format JSON horodatés dans des dossiers de classification dédiés (`data/[categorie]/`).
4. Module d'Audit Intégré : Consultation et relecture de l'historique des rapports de collecte directement depuis l'interface de l'outil.

---

 Guide d'Utilisation

1. Lancer le script principal depuis la console :
   ```bash
   python main.py

