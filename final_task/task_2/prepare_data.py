from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date
from pyspark.sql.types import IntegerType, StringType, BooleanType

#----------------------------------------
# Подъем сессии
#----------------------------------------
spark = SparkSession.builder.appName("transactions_pipeline").getOrCreate()
source = "s3a://final-task/transactions_v2.csv"
target = "s3a://final-task/transactions_v2_clean.csv"

try:
    df = spark.read.option("header", "true").option("inferSchema", "true").csv(source)

    df = (df.withColumn("msno", col("msno").cast(StringType())) \
        .withColumn("actual_amount_paid", col("actual_amount_paid").cast(IntegerType())) \
        .withColumn("is_auto_renew", col("is_auto_renew").cast(BooleanType())) \
        .withColumn("is_cancel", col("is_cancel").cast(BooleanType())) \
        .withColumn("membership_expire_date", to_date(col("membership_expire_date").cast("string"), "yyyyMMdd")) \
        .withColumn("payment_method_id", col("payment_method_id").cast(IntegerType())) \
        .withColumn("payment_plan_days", col("payment_plan_days").cast(IntegerType())) \
        .withColumn("plan_list_price", col("plan_list_price").cast(IntegerType())) \
        .withColumn("transaction_date", to_date(col("transaction_date").cast("string"), "yyyyMMdd")))


#--------------------
# Drop nulls
#--------------------
df = df.na.drop()
df.write.mode("overwrite").csv(target)

print('SUCCESS!')
except:
    print('Try another way....')
spark.stop()