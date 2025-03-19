# Présentation du Dataset

Nous avons choisi d'utiliser des logs d'un supercalculateur Thunderbird récupérés sur Git. Voici un extrait des données :

![data](https://github.com/user-attachments/assets/c8980e77-52fb-4819-bef9-864d87be12e0)

**Citation :**
Adam J. Oliner, Jon Stearley. What Supercomputers Say: A Study of Five System Logs. In Proc. of IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 2007.
Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu. Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics. IEEE International Symposium on Software Reliability Engineering (ISSRE), 2023.

Le but est d'analyser ces logs afin de mettre en évidence certaines caractéristiques telles que :
- Les pics d'activité de tâches cron
- Les composants avec le plus d'échecs
- Les nœuds bruyants (noisy nodes)
- Les sessions root et leur durée
- Les logs par heure

# Mise en forme des données

Grâce à un script Python, nous avons parsé les données du fichier texte brut sous la forme suivante :

![data_parsed](https://github.com/user-attachments/assets/a039b6ce-e1db-4b30-9b05-a9b735e79164)

Ensuite, nous avons créé un fichier Parquet à partir du fichier texte parsé (cf: dataconversion.py).

# Analyse des données

Les analyses sont directement faites sur les fichiers Parquet. Les fichiers Parquet sont stockés dans un bucket sur GCP et nous utilisons Spark via un notebook pour lancer nos analyses. Voici quelques résultats :

## Nombre de tâches cron par heure

C'est une moyenne calculée sur les jours de captation des logs.

![moyenne_cron_heure](https://github.com/user-attachments/assets/f61a9af1-d44f-4027-b602-3685a1b93ed1)

**Ce que cela nous apporte :**
Cela permet d'identifier les pics d'activité des tâches cron, ce qui peut être utile pour détecter des comportements anormaux ou des périodes de charge élevée.

## Connexions root par utilisateur

Pour une date donnée et par heure, le nombre de connexions root qu'a ouvert l'utilisateur qui en a ouvert le plus durant l'heure (on précise également l'utilisateur). Dans l'exemple suivant, on a affiché pour le 12 janvier, les utilisateurs qui ont ouvert le plus de connexions root pour chaque heure. Plusieurs utilisateurs peuvent avoir ouvert un même nombre de connexions.

![rootconnexion12_01](https://github.com/user-attachments/assets/02352548-68b2-4071-985e-e28aafc93860)

**Ce que cela nous apporte :**
Cela permet de surveiller les accès root et de détecter des comportements suspects ou des tentatives d'intrusion.

## Moyenne des logs par heure

![moyenne log heure](https://github.com/user-attachments/assets/53e102f7-171c-4a3f-bae8-73c8ed9ffd89)

**Ce que cela nous apporte :**
Cela permet de comprendre les périodes de forte activité et d'identifier les moments où le système est le plus sollicité.

## Composants avec le plus d'échecs

![Composant echec](https://github.com/user-attachments/assets/bf2af5f9-9bb4-48d1-abb1-80a15811ae72)

**Ce que cela nous apporte :**
Cela permet d'identifier les composants les plus susceptibles de causer des échecs et de cibler les efforts de maintenance et de correction.

## Nœuds bruyants (noisy nodes)

![Noisy node](https://github.com/user-attachments/assets/8776906b-5bd6-4954-aae3-9d57396de89c)

**Ce que cela nous apporte :**
Cela permet d'identifier les nœuds qui génèrent le plus de logs ou d'erreurs, ce qui peut indiquer des problèmes matériels ou logiciels.

## Durée des sessions root

![Root time session](https://github.com/user-attachments/assets/52d502a6-d6a9-48ef-a15d-aa16d8e0a5c4)

**Ce que cela nous apporte :**
Cela permet de surveiller la durée des sessions root et de détecter des sessions anormalement longues qui pourraient indiquer une activité suspecte.

# Paramétrage de Spark

Pour optimiser les performances de Spark, nous avons ajusté plusieurs paramètres dans notre notebook. Voici quelques détails supplémentaires :

## Configuration des exécuteurs

Nous avons configuré les exécuteurs pour qu'ils aient suffisamment de mémoire et de cœurs pour traiter les données efficacement. Par exemple :

```python
spark.conf.set("spark.executor.memory", "4g")
spark.conf.set("spark.executor.cores", "2")
```

## Partitionnement des données

Nous avons utilisé des techniques de partitionnement pour améliorer l'efficacité des requêtes. Par exemple, nous avons partitionné les données par date pour accélérer les requêtes basées sur des plages de dates.

```python
df = df.repartition("date")
```

## Gestion de la mémoire

Nous avons également ajusté les paramètres de gestion de la mémoire pour éviter les débordements de mémoire et les erreurs de type "OutOfMemoryError".

```python
spark.conf.set("spark.memory.fraction", "0.8")
spark.conf.set("spark.memory.storageFraction", "0.2")
```

# Difficultés rencontrées

Plusieurs difficultés ont été rencontrées :
- La récupération des données et leur dépôt sur GCP
- La gestion des sessions Spark

# Conclusion

L'analyse des logs du supercalculateur Thunderbird nous a permis de mettre en évidence plusieurs caractéristiques importantes pour la sécurité et la maintenance du système. Ces informations peuvent être utilisées pour améliorer la surveillance et la gestion des supercalculateurs.
