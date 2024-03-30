import pyspark.sql.functions as func
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType, FloatType, LongType

spark = SparkSession.builder \
    .appName('spotify_de') \
    .getOrCreate()
json_schema = StructType([
    StructField("artists", StringType(), False),
    StructField("duration_ms", LongType(), False),
    StructField("popularity", IntegerType(), False),
    StructField("song_name", StringType(), False),
    StructField("song_preview", StringType(), False)
])
json_df = spark.read \
    .schema(json_schema) \
    .json(r"C:\Users\tapis\PycharmProjects\Spotify_project\API_DATA_CLEAN\final.json")
json_df = json_df.withColumn("duration", func.round(json_df.duration_ms / 60000, 1))
json_df.createOrReplaceTempView("Songs_table")

selected_df = spark.sql("SELECT *, dense_rank() over(order by popularity desc) as rank_on_chart FROM Songs_table")

selected_df.write.mode("overwrite").parquet(
    "C:/Users/tapis/PycharmProjects/Spotify_project/API_DATA_CLEAN/final.parquet")

selected_df.printSchema()

json_df.schema.json()