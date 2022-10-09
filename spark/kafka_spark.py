import findspark
import os
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, IntegerType, \
    StringType, FloatType, TimestampType

audio_data = "/mnt/10ac-batch-6/week7/chang/kafka"
topic_input = "test"

findspark.init('/opt/spark')

os.environ['PYSPARK_SUBMIT_ARGS'] =\
    '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 pyspark-shell'


def main():

    spark = SparkSession \
        .builder \
        .master('local[1]') \
        .appName("kafka-streaming-audio") \
        .getOrCreate()

    df_audio = read_from_kafka(spark)

    # summarize_sales(df_audio)


def read_from_kafka(spark):  # , params):
    options_read = {
        "kafka.bootstrap.servers":
            "localhost:9092",
        "subscribe":
            topic_input,
    }

    df_audio = spark.readStream \
        .format("kafka") \
        .options(**options_read) \
        .option("startingOffsets", "earliest") \
        .load()

    return df_audio
