# Итоговое задание ETL

### Этапы проекта:

- Установка и настройка инструментов командной строки: Yandex CLI и YDB CLI, включая настройку авторизации;
- Создание базы данных в Yandex Database (YDB) и организация переноса данных в Yandex Object Storage (S3);
- Развертывание и конфигурация Apache Airflow, интеграция с Yandex MetaDataHub и Yandex Data Processing;
- Разработка PySpark-скриптов и создание DAG для автоматизации процессов обработки данных;
- Работа с Apache Kafka®: настройка взаимодействия топиков Kafka и обработка данных через PySpark-задания в Yandex Data Processing (в процессе доработки);
- Визуализация данных с использованием Yandex DataLens (в процессе доработки).

### Задание 1. Работа с Yandex DataTransfer

[Ссылка на документацию](https://yandex.cloud/ru/docs/data-transfer/tutorials/ydb-to-object-storage)

Создал табличку для данных с [kaggle](https://www.kaggle.com/datasets)

####DDL скрипт
```    
    CREATE TABLE transactions_v2 (
          msno Utf8,
          payment_method_id Int32,
          payment_plan_days Int32,
          plan_list_price Int32,
          actual_amount_paid Int32,
          is_auto_renew Int8,
          transaction_date Utf8,
          membership_expire_date Utf8,
          is_cancel Int8,
          PRIMARY KEY (msno)
      );
```

- В созданную таблицу с помощью CLI загружен датасет transaction_v2

#### bash скрипт

```  
    ### bash-скрипт загрузки датасета
    
    ydb  `
    --endpoint grpcs://ydb.serverless.yandexcloud.net:2135 `
    --database /ru-central1/[эндпоинт]/['эндпоинт] `
    --sa-key-file key.json `
    import file csv `
    --path transactions_v2 `
    --delimiter "," `
    --skip-rows 1 `
    --null-value "" `
    --verbose `
    transactions_v2.csv
```
- Создан трансфер данных с источником в YDB и приемником в Object Storage
  `s3a://final_task/transactions_v2.parquet`
  
#### Скриншоты
![Скриншот_1](.assets/task_1_1.jpg)
![Скриншот_2](.assets/task_1_2.jpg)
![Скриншот_3](.assets/task_1_3.jpg)

### Задание 2: Автоматизация работы с Yandex Data Processing при помощи Apache AirFlow

[Ссылка на документацию](https://yandex.cloud/ru/docs/managed-airflow/tutorials/data-processing-automation)

* Настроен Yandex MetaDataHub для централизованного управления метаданными;
* Развернут и настроен Yandex Data Processing для выполнения распределённых вычислений;
* Конфигурирован Apache Airflow для оркестрации ETL-процессов;
* Разработан скрипт обработки данных, включающий:
  + Приведение типов к заданному формату;
  + Фильтрацию и удаление пустых строк.

```
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
```

- Написан DAG для переноса в s3 с запуском скрипта обработки:

```
    import uuid
	import datetime
	from airflow import DAG
	from airflow.utils.trigger_rule import TriggerRule
	from airflow.providers.yandex.operators.yandexcloud_dataproc import (
	    DataprocCreateClusterOperator,
	    DataprocCreatePysparkJobOperator,
	    DataprocDeleteClusterOperator,
	)
	
	# Данные вашей инфраструктуры
	YC_DP_AZ = 'ru-central1-a'
	YC_DP_SSH_PUBLIC_KEY = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICXx7PPXYXh9Esb7JncJxsMLeV7jRUCBhnzRmYAxeCJa ключ для airflow в yandex cloud'
	YC_DP_SUBNET_ID = 'e9bpnl521v34p5hjvat9'
	YC_DP_SA_ID = 'ajejp630v9a9o94n7htt'
	YC_DP_METASTORE_URI = '10.128.0.8'
	YC_BUCKET = 'final-task'
	
	# Настройки DAG
	with DAG(
	        'FINAL-TASK',
	        schedule_interval='@hourly',
	        tags=['data-processing-and-airflow'],
	        start_date=datetime.datetime.now(),
	        max_active_runs=1,
	        catchup=False
	) as ingest_dag:
	    # 1 этап: создание кластера Yandex Data Proc
	    create_cluster = DataprocCreateClusterOperator(
	        task_id='dp-cluster-create-task',
	        cluster_name=f'tmp-dp-{uuid.uuid4()}',
	        cluster_description='Кластер для выполнения PySpark таски',
	        ssh_public_keys=YC_DP_SSH_PUBLIC_KEY,
	        service_account_id=YC_DP_SA_ID,
	        subnet_id=YC_DP_SUBNET_ID,
	        s3_bucket=YC_BUCKET,
	        zone=YC_DP_AZ,
	        cluster_image_version='2.1',
	        masternode_resource_preset='s2.small',
	        masternode_disk_type='network-hdd',
	        masternode_disk_size=32,
	        computenode_resource_preset='s2.small',
	        computenode_disk_type='network-hdd',
	        computenode_disk_size=32,
	        computenode_count=1,
	        computenode_max_hosts_count=3,
	        services=['YARN', 'SPARK'],
	        datanode_count=0,
	        properties={
	            'spark:spark.hive.metastore.uris': f'thrift://{YC_DP_METASTORE_URI}:9083',
	        },
	    )

    # 2 этап: запуск задания PySpark
    spark_processing = DataprocCreatePysparkJobOperator(
        task_id='dp-cluster-pyspark-task',
        main_python_file_uri=f's3a://{YC_BUCKET}/scripts/prepare-data.py',
    )

    # 3 этап: удаление кластера Yandex Data Processing
    delete_cluster = DataprocDeleteClusterOperator(
        task_id='dp-cluster-delete-task',
        trigger_rule=TriggerRule.ALL_DONE,
    )

    # Формирование DAG из указанных выше этапов
    create_cluster >> spark_processing >> delete_cluster

```


#### Скриншоты
![Скриншот_1](.assets/task_2_1.jpg)
![Скриншот_2](.assets/task_2_2.jpg)
![Скриншот_3](.assets/task_2_3.jpg)
