from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws, count, rank, hour
from pyspark.sql.window import Window
import matplotlib.pyplot as plt
import pandas as pd

# Chemin vers le fichier parquet
parquet_path = "gs://bucket_test_spark/notebooks/jupyter/Thunderbird_parsed/"  

# Lire les données parquet
df = spark.read.parquet(parquet_path)


# Si on veut afficher que pour le 12 du mois de Janvier
df = df.filter((col("Month") == "Jan") & (col("Day") == "12"))

df = df.withColumn("hour_of_day", hour(col("Time")))


# Filtrer uniquement les sessions ouvertes pour root
df_root_sessions = df.filter(col("Content").like("%session opened for user root%"))

# Compter le nombre de sessions root ouvertes par utilisateur et par jour
user_root_sessions_by_hour = df_root_sessions.groupBy("hour_of_day", "User").count()

# Pour chaque jour, trouver l'utilisateur qui a ouvert le plus de sessions root
window_spec = Window.partitionBy("hour_of_day").orderBy(col("count").desc())
top_users_by_hour = user_root_sessions_by_hour \
    .withColumn("rank", rank().over(window_spec)) \
    .filter(col("rank") == 1) \
    .select("hour_of_day", "User", "count") \
    .orderBy("hour_of_day")


print("Utilisateur avec le plus de connexions root par heure le 12 janvier:")
top_users_by_hour.show(24, False)

# Convertir en pandas DataFrame pour visualisation
pandas_df = top_users_by_hour.toPandas()

# Vérifier si nous avons des données
if len(pandas_df) > 0:
    # Créer un DataFrame avec toutes les heures de la journée (0-23)
    all_hours = pd.DataFrame({'hour_of_day': range(24)})
    pandas_df = pd.merge(all_hours, pandas_df, on='hour_of_day', how='left')
    pandas_df = pandas_df.fillna({'count': 0, 'User': 'Aucun'})
    pandas_df['count'] = pandas_df['count'].astype(int)
    
    # Créer un graphique à barres
    plt.figure(figsize=(16, 8))
    
    # Créer le graphique à barres
    bars = plt.bar(pandas_df['hour_of_day'], pandas_df['count'], color='skyblue')
    
    # Ajouter les noms d'utilisateurs au-dessus des barres qui ont des connexions
    for i, row in pandas_df.iterrows():
        if row['count'] > 0:
            users = pandas_df[pandas_df['hour_of_day'] == row['hour_of_day']]['User'].tolist()
            user_text = "\n".join(users)
            plt.text(row['hour_of_day'], row['count'] + 0.5, user_text, 
                    ha='center', va='bottom', fontsize=9, rotation=45)
    
    # Configurer les axes et le titre
    plt.xlabel('Heure de la journée')
    plt.ylabel('Nombre de connexions root')
    plt.title('Utilisateur avec le plus de connexions root par heure - 12 janvier')
    plt.xticks(range(24))
    plt.xlim(-0.5, 23.5)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Sauvegarder le graphique
    plt.savefig("most_active_root_user_jan12_by_hour.png")
    
    # Afficher le graphique
    plt.show()
    plt.close()
    
else:
    print("Aucune donnée trouvée pour les connexions root le 12 janvier.")
