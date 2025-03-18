import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, date_format, avg
import pandas as pd

# Ce script permet d'afficher le nombre de taches cron par heure, moyenne calculée sur tous les jours des logs

# Chemin du répertoire contenant tous les fichiers Parquet
parquet_path = "gs://bucket_test_spark/notebooks/jupyter/Thunderbird_parsed/"  

# Lire tous les fichiers Parquet dans le répertoire
df = spark.read.parquet(parquet_path)

# Filtrer les tâches cron (basé sur le champ Component ou Content)
cron_df = df.filter((col("Component").like("%cron%")) | (col("Content").like("%cron%")))

# Extraire l'heure à partir du champ Time et la convertir en entier pour un tri correct
cron_df = cron_df.withColumn("Hour", date_format(col("Time"), "HH").cast("int"))

# Compter les tâches par jour et par heure
cron_count = cron_df.groupBy("Date", "Hour").agg(count("*").alias("Cron_Count"))

# Calculer la moyenne des tâches cron par heure sur tous les jours
average_cron = cron_count.groupBy("Hour").agg(avg("Cron_Count").alias("Avg_Cron_Count"))

# Conversion en Pandas pour Matplotlib et tri des heures
average_pd = average_cron.toPandas().sort_values(by="Hour")

# Tracer et enregistrer le graphique
plt.figure(figsize=(10, 6))
plt.plot(average_pd['Hour'], average_pd['Avg_Cron_Count'], marker='o', color='b', label="Moyenne par heure")
plt.xlabel("Heure (24h)")
plt.ylabel("Nombre moyen de tâches cron")
plt.title("Moyenne des tâches cron par heure sur tous les jours")
plt.xticks(range(24))  
plt.legend()

plt.savefig("cron_average_per_hour.png")
plt.show()
plt.close()

spark.stop()
