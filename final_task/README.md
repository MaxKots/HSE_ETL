<<<<<<< HEAD
# Итоговое задание ETL

## Общая архитектура

- **Источник данных:** `transactions_v2.csv`  в Object Storage
- **ETL-пайплайн:** Airflow → Dataproc (PySpark) → Kafka → PostgreSQL (Managed Service)
- **Форматы:** CSV → Parquet → JSON → Kafka message → PostgreSQL

### Задание 1. Работа с Yandex DataTransfer

Создал табличку для данных с [kaggle](https://www.kaggle.com/datasets)
  <details>
    <summary><i>DDL скрипт</i></summary>
    
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

  </details> 
- В созданную таблицу с помощью CLI загружен датасет transaction_v2
  <details>
    <summary><i>bash скрипт</i></summary>
  
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
  </details> 
- Создан трансфер данных с источником в YDB и приемником в Object Storage
  `s3a://etl-data-transform/transactions_v2.parquet`
    	<details>
    	<summary><i>Тут скриншоты</i></summary>
		- ![Скриншот](.assets/task_1_1.jpg)
  		- ![Скриншот](screenshots/task_1_2.jpg)
  		- ![Скриншот](screenshots/task_1_3.jpg)
	</details> 
=======
# Итоговое задание ETL

## Общая архитектура

- **Источник данных:** `transactions_v2.csv`  в Object Storage
- **ETL-пайплайн:** Airflow → Dataproc (PySpark) → Kafka → PostgreSQL (Managed Service)
- **Форматы:** CSV → Parquet → JSON → Kafka message → PostgreSQL

### Задание 1. Работа с Yandex DataTransfer

Создал табличку для данных с [kaggle](https://www.kaggle.com/datasets)
  <details>
    <summary><i>DDL скрипт</i></summary>
    
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

  </details> 
- В созданную таблицу с помощью CLI загружен датасет transaction_v2
  <details>
    <summary><i>bash скрипт</i></summary>
  
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
  </details> 
- Создан трансфер данных с источником в YDB и приемником в Object Storage
  `s3a://etl-data-transform/transactions_v2.parquet`
    	<details>
    	<summary><i>Тут скриншоты</i></summary>
		- ![Скриншот](.assets/task_1_1.jpg)
  		- ![Скриншот](screenshots/task_1_2.jpg)
  		- ![Скриншот](screenshots/task_1_3.jpg)
	</details>
