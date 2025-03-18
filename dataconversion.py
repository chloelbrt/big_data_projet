from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, row_number, monotonically_increasing_id, col, lit, abs, hash, concat
from pyspark.sql.types import StringType, IntegerType, LongType, StructType, StructField
from pyspark.sql.window import Window
import os
import subprocess
import re
from pathlib import Path

# Initialize Spark session
spark = SparkSession.builder \
    .appName('Cron Activity Analysis Updated') \
    .config("spark.sql.files.maxPartitionBytes", "128MB") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()


import re

def parse_log_line(log_line):
    # Pattern corrigé avec des groupes appropriés
    pattern = r"^(-)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+(?:\[\S+\])?)(:)(\s+)(.+)$"
    
    match = re.match(pattern, log_line)
    if not match:
        return None, None, None, None, None, None, None, None, None, None, None
    
    # Extraction des groupes pertinents (en ignorant les espaces)
    label = match.group(1)             # -
    timestamp = match.group(3)         # 1131566461
    date = match.group(5)              # 2005.11.09
    hostname = match.group(7)          # dn228
    month = match.group(9)             # Nov
    day = match.group(11)              # 9
    time = match.group(13)             # 12:01:01
    location = match.group(15)         # dn228/dn228
    component_pid = match.group(17)    # crond(pam_unix)[2915]
    content = match.group(20)          # session closed for user root
    
    # Extraction du PID depuis component_pid (traitement du cas où il n'y a pas de PID)
    pid_match = re.search(r'\[(\d+)\]', component_pid)
    pid = int(pid_match.group(1)) if pid_match else None
    
    # Extraction du component (sans le PID)
    component = re.sub(r'\[\d+\]', '', component_pid)
    
    try:
        day = int(day)
    except ValueError:
        # En cas d'erreur de conversion
        pass
    
    return label, timestamp, date, hostname, month, day, time, location, component, pid, content


# Définition correcte de l'UDF avec le même nombre de champs que dans le return
parse_log_line_udf = udf(parse_log_line, 
    StructType([
        StructField("Label", StringType()),
        StructField("Timestamp", StringType()),
        StructField("Date", StringType()),
        StructField("User", StringType()),
        StructField("Month", StringType()),
        StructField("Day", IntegerType()),
        StructField("Time", StringType()),
        StructField("Location", StringType()),
        StructField("Component", StringType()),
        StructField("PID", IntegerType()),
        StructField("Content", StringType()),
    ])
)


def convert_logs_to_parquet_with_spark(log_file_path, output_parquet_path):
    # Vérifier que le fichier d'entrée existe
    if not os.path.exists(log_file_path):
        print(f"Le fichier {log_file_path} n'existe pas.")
        return
    
    # Assurer que le répertoire de sortie existe
    output_dir = os.path.dirname(output_parquet_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Lecture du fichier log
    df = spark.read.text(log_file_path)

    # Application du parsing
    parsed_df = df.select(
        parse_log_line_udf(col("value")).alias("parsed")
    )
    parsed_df.show()
    # Extraction correcte des colonnes du parsing
    columns = ["Label", "Timestamp", "Date", "User", "Month", "Day", "Time", "Location", "Component", "PID", "Content"]
    
    for col_name in columns:
        parsed_df = parsed_df.withColumn(col_name, col("parsed").getField(col_name))
    
    # Suppression de la colonne parsed qui n'est plus nécessaire
    parsed_df = parsed_df.drop("parsed")
    
    # Vérifier si le dataframe est vide
    if parsed_df.count() == 0:
        print("Attention: Aucune donnée valide n'a été trouvée après le parsing!")
        return
    
    try:
        # Supprimer le répertoire de sortie s'il existe déjà (pour éviter les erreurs)
        if os.path.exists(output_parquet_path):
            import shutil
            shutil.rmtree(output_parquet_path)
        
        # Sauvegarde au format Parquet 
        parsed_df.write.mode("overwrite").parquet(output_parquet_path)
        
        print(f"Conversion terminée. Fichier parquet créé: {output_parquet_path}")
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier parquet: {e}")


# Exemple d'utilisation
log_file_path = "./Thunderbird.log"
output_path = "./Thunderbird_parsed/"

try:
    convert_logs_to_parquet_with_spark(log_file_path, output_path)
except Exception as e:
    print(f"Une erreur s'est produite: {e}")
    
spark.stop()
