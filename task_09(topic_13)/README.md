# Потоковая обработка данных
Ссылка на [инструкцию](https://yandex.cloud/ru/docs/managed-kafka/tutorials/data-processing)


Ловлю ошибку:
"Exception in thread "main" java.nio.file.AccessDeniedException: s3a://kafka-bucket/kafka-write.py: open s3a://kafka-bucket/kafka-write.py at 0 on s3a://kafka-bucket/kafka-write.py: com.amazonaws.services.s3.model.AmazonS3Exception: Access Denied (Service: Amazon S3; Status Code: 403; Error Code: AccessDenied; Request ID: 63785915adb55547; S3 Extended Request ID: null; Proxy: null), S3 Extended Request ID: null:AccessDenied"