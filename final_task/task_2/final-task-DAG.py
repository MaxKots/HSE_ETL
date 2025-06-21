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
