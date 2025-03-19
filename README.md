# Présentation du dataset
Nous choisissons d'utiliser des logs d'un supercalculateur Thunderbird récupéré sur Git. Voici un extrait : 
![data](https://github.com/user-attachments/assets/c8980e77-52fb-4819-bef9-864d87be12e0)
Citation : 
Adam J. Oliner, Jon Stearley. What Supercomputers Say: A Study of Five System Logs. In Proc. of IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 2007.
Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu. Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics. IEEE International Symposium on Software Reliability Engineering (ISSRE), 2023.

Le but est d'analyer ces logs afin de mettre en évidence certaines caractéristiques telles que :
- Les pics d'activité de tâches cron
- 

# Mise en forme des données
Grâce à un script python, on parse les données du fichier texte brut sous la forme : 
![data_parsed](https://github.com/user-attachments/assets/a039b6ce-e1db-4b30-9b05-a9b735e79164)

Puis on crée un fichier parquet à partir du fichier texte parsé (cf: dataconversion.py).

# Analyse des données
Les analyses sont directement faites sur les fichiers parquets. 
Les fichiers parquets sont dans un buckets sur GCP et nous utilisons Spark via un notebook pour lancer nos analyses.
Voici quelques résultats : 
- Nombre de tâches cron par heure (c'est un moyenne calculée sur les jours de captation des logs)
![moyenne_cron_heure](https://github.com/user-attachments/assets/f61a9af1-d44f-4027-b602-3685a1b93ed1)

- On affiche, pour une date donnée et par heure, le nombre de connexion root qu'a ouvert l'utilisateur qui en a ouvert le plus durant l'heure (on précise égalemet l'utilisateur). Dans l'exemple suivant, on a affiché pour le 12 janvier, les utilisateurs qui ont ouvert le plus de connexion root pour chaque heure. Plusieurs utilisateurs peuvent avoir ouvert un même nombre de connexion.
-  ![rootconnexion12_01](https://github.com/user-attachments/assets/02352548-68b2-4071-985e-e28aafc93860)

# Difficultés rencontrées
Plusieurs difficultés ont été rencontrées : 
- la récupération des données et leur dépôt sur GCP
- les gestions des sessions Spark
# Paramétrage de Spark
