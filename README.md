# ubre-backend

Necesita de una base de datos externa PostgreSQL. Lo primero que hay que hacer es instalarla (si no la tenemos ya) en Ubuntu 18.04 LTS:
1.- sudo apt update
2.- sudo apt install postgresql postgresql-contrib

Instalar el conector para PostgreSQL.
1.- pip3 install psycopg2

Para entrar a la base de datos PostgreSQL que hemos creado:
1.- sudo -i -u postgres
2.- psql -U ubre ubre

Desde Django, tenemos que crear las tablas en la base de datos. Usaremos los siguientes comandos donde se encuentre el fichero manage.py:
1.- python3 manage.py makemigrations
2.- python3 manage.py migrate
