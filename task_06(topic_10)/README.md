Создаем сертификат

Windows powershell:
mkdir $HOME\.postgresql; curl.exe -o $HOME\.postgresql\root.crt https://storage.yandexcloud.net/cloud-certs/CA.pem

Linux:
mkdir -p ~/.postgresql && \
wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
     --output-document ~/.postgresql/root.crt && \
chmod 0600 ~/.postgresql/root.crt


Подключаемся к БД, к примеру, из jupyter:
import psycopg2

conn = psycopg2.connect("""
    host=rc1a-tdpt9v6mju67l8qb.mdb.yandexcloud.net,rc1b-q68urnpd2p6djg1m.mdb.yandexcloud.net
    port=6432
    sslmode=verify-full
    dbname=test-bd
    user=knoll
    password=<пароль пользователя>
    target_session_attrs=read-write
""")

q = conn.cursor()
q.execute('SELECT version()')

print(q.fetchone())

conn.close()