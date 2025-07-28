from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, max, min
import random
import time

def generate_data(spark, num_records=10_000_000):
    # Simulate a dataset with user transactions
    data = [
        (random.randint(1, 1000), random.uniform(10, 1000), random.choice(['electronics', 'clothing', 'books']))
        for _ in range(num_records)
    ]
    return spark.createDataFrame(data, ['user_id', 'amount', 'category'])

if __name__ == "__main__":
    spark = SparkSession.builder.appName("K8sSparkDemoEnhanced").getOrCreate()

    print("Generating synthetic data...")
    df = generate_data(spark)

    print("Data schema:")
    df.printSchema()

    print("Running aggregations...")
    start_time = time.time()

    agg_result = df.groupBy("category").agg(
        count("*").alias("total_txns"),
        avg("amount").alias("avg_amount"),
        max("amount").alias("max_amount"),
        min("amount").alias("min_amount")
    )

    agg_result = agg_result.orderBy(col("total_txns").desc())
    agg_result.show(truncate=False)

    duration = time.time() - start_time
    print(f"Aggregation completed in {duration:.2f} seconds")

    spark.stop()
