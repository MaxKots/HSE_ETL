This repo contains ETL process examples in Apache NiFi



docker run --name nifi \
  -p 8443:8443 \
  -d \
  -e SINGLE_USER_CREDENTIALS_USERNAME=admin \
  -e SINGLE_USER_CREDENTIALS_PASSWORD=ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB \
  -v /home/max/HSE_ETL:/opt/nifi/nifi-current/data \
  apache/nifi:latest


NiFi доступен по адресу:
https://localhost:8443/nifi/#/login

Все датафреймы кладем на локалку в /home/max/HSE_ETL, они монтируются в том и с ними можно работать из apache Nifi


1) Создаем новую группу процессов через вкладку Process group, пишем имя нашей задачи

2) Для добавления файла с данными в работу, добавляем новый процессор через вкладку Processor, ищем прцоессор с названием GetFile 
Фото

3) Открываем задачу, в ней переходим на вкладку properties, в поле Input Directory пишем путь, по которому мы загружали csv-файл: /opt/nifi/nifi-current/data
В поле File filter добавляем наименование csv-файла: IOT-temp.csv и жмем на кнопку Verification, проверяя, что все сделали правильно:
фото

4) Создаем прцоесс типа QueryRecord, который поддерживает написание запросов на диалекте Apache

5) Добавляем Funnel и тянем связь от предыдущего процессора связью с флагом Relationships: original
Также тянем связь от GetFile до QueryRecord

6) Конфигурируем QueryRecord. Для того, чтобы добавить обработчик CSV, нужно добавить параметры чтения и записи:
 - на вкладке Properties напротив Record Reader нажать 3 точки и выбрать Create new service, где выбрать CSVReader
 - аналогично для Record Writer, ставим CSVRecordSetWriter  
ФОТО
7) Для прехода в сервис для настройки чтения и записи, жмем на три точки напроитив выбранной опции чтения\записи и выбираем "Go to service", после чего процессы нужно перевести в состояние Enabled, после чего можем выходить из настройки чтения и записи (кнопка Back to Processor)
ФОТО

8) Нажав на икнонку плюса (Add Property) в процессоре QueryRecord, можем добавить  поле с произвольным названием
ФОТО





