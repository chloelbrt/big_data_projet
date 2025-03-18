from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, window, hour, minute, count
import matplotlib.pyplot as plt
import os

# Initialize Spark session with GCS connector
spark = SparkSession.builder \
    .appName('Cron Activity Analysis') \
    .config('spark.sql.files.maxPartitionBytes', 134217728) \
    .config('spark.hadoop.fs.gs.impl', 'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem') \
    .config('spark.hadoop.fs.AbstractFileSystem.gs.impl', 'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS') \
    .getOrCreate()
