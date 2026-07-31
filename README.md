🧭 L'objectif général du programme
Ce code est le moteur d'une application pour console destinée aux pêcheurs du Port de Lomé (Togo). Son but est d'améliorer leur sécurité en mer (météo, alertes d'urgence) et de les aider à respecter les règles de pêche locales pour protéger l'environnement.

📋 Détail des fonctionnalités (Menu Principal)
Lorsque le pêcheur lance le programme, il fait face à un menu avec 5 choix :

1. Consulter la météo marine (Option 1)
Ce qu'elle fait : L'application se connecte à internet pour récupérer la météo du jour et l'état de la mer (vitesse du vent, hauteur des vagues, force des courants, visibilité).

Le petit plus : Le programme analyse ces données et affiche automatiquement un voyant de sécurité :

🟢 SAFE : Tout va bien, vous pouvez pêcher.

⚠️ CAUTION : Attention, la mer commence à s'agiter.

🔴 DANGER : Rester au port, les conditions sont trop dangereuses (grosses vagues ou vents violents).

Sécurité déconnexion : Si la pirogue s'éloigne trop et perd internet, l'application ne plante pas. Elle affiche un message d'avertissement propre indiquant que la connexion satellite est perdue.

2. Guide des poissons et réglementations (Option 2)
Ce qu'elle fait : Le pêcheur tape le nom d'un poisson (comme la Sardinelle ou l'Anchois). L'application lui indique la taille minimale légale pour le pêcher et des conseils pour éviter la surpêche.

Si le poisson est inconnu : L'application propose au pêcheur d'enregistrer lui-même ce nouveau poisson. Elle lui demande son nom scientifique, sa taille et sa réglementation, puis sauvegarde tout cela dans un fichier sur l'ordinateur nommé User_contribution.json.

3. Lancer une alerte SOS d'urgence (Option 3)
Ce qu'elle fait : En cas de problème grave en mer (panne, tempête), le pêcheur entre son numéro d'immatriculation.

Comment ça marche : L'application simule la position géographique (GPS) de la pirogue autour de Lomé, crée automatiquement un lien Google Maps précis pour les secours, et enregistre cette alerte dans le fichier central des urgences.

4. Voir les alertes au centre de commande à terre (Option 4)
Ce qu'elle fait : Cette option est utilisée par l'équipe de secours restée au port. Elle lit le fichier des urgences (sos_repository.json) et affiche la liste de toutes les pirogues en détresse avec leur position GPS exacte et leur lien Google Maps pour envoyer les sauveteurs au bon endroit.

5. Quitter (Option 5)
Ce qu'elle fait : Ferme proprement l'application en saluant le pêcheur ("Stay safe on the water! We love what you do.").

🛠️ Les fonctions "cachées" (Sous le capot)
Pour que tout cela fonctionne, le code utilise plusieurs petits outils en arrière-plan :

simulate_gps() : Comme un vrai GPS n'est pas branché à l'ordinateur, cette fonction invente de fausses coordonnées géographiques, mais toujours très proches des côtes de Lomé/Gbétsogbé pour que les tests restent réalistes.

calculate_safety_flag() : C'est le cerveau qui décide si la météo est verte, orange ou rouge en fonction des limites fixées (ex: danger si les vagues dépassent 1,8 mètre).

read_shore_alerts() : Un petit assistant qui va lire le fichier des alertes SOS sans bloquer ou faire bugger le programme si le fichier est vide ou n'existe pas encore.
