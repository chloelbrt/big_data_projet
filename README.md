# big_data_projet
### Présentation du dataset
Nous choisissons d'utiliser des logs d'un supercalculateur Thunderbird récupéré sur Git. Voici un extrait : 
![data](https://github.com/user-attachments/assets/c8980e77-52fb-4819-bef9-864d87be12e0)
Citation : 
Adam J. Oliner, Jon Stearley. What Supercomputers Say: A Study of Five System Logs. In Proc. of IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 2007.
Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu. Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics. IEEE International Symposium on Software Reliability Engineering (ISSRE), 2023.

Le but est d'analyer ces logs afin de mettre en évidence certaines caractéristiques telles que :
- Les pics d'activité de tâches cron
- 

## Mise en forme des données
Grâce à un script python, on parse les données du fichier texte brut sous la forme : 
![data_parsed](https://github.com/user-attachments/assets/a039b6ce-e1db-4b30-9b05-a9b735e79164)

Puis on créé un fichier parquet à partir du fichier texte parsé.

