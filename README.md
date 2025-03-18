# big_data_projet
Nous choisissons d'utiliser des logs d'un supercalculateur Thunderbird récupéré sur Git. Voici un extrait : 
![data](https://github.com/user-attachments/assets/c8980e77-52fb-4819-bef9-864d87be12e0)
Citation : 
Adam J. Oliner, Jon Stearley. What Supercomputers Say: A Study of Five System Logs. In Proc. of IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 2007.
Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu. Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics. IEEE International Symposium on Software Reliability Engineering (ISSRE), 2023.

Le but est d'analyer ces logs afin de mettre en évidence certaines caractéristiques telles que :
- Les pics d'activité de tâches cron
- 
### Présentation du dataset

### Conversion du fichier texte en parquet
Nous récupérons une archive contenant un fichier texte et nous choisissons de le transformer en fichier parquet. Grâce à un script python, on lit le fichier texte et on extrait les données 
u![schema_parquetfile](https://github.com/user-attachments/assets/a13a7435-d495-4644-86d9-50a76b50de15)
