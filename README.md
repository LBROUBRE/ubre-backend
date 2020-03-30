# ubre-backend

Necesita de una base de datos externa PostgreSQL. Lo primero que hay que hacer es instalarla (si no la tenemos ya) en Ubuntu 18.04 LTS:
1.- sudo apt update
2.- sudo apt install postgresql postgresql-contrib

Instalar el conector para PostgreSQL.
1.- pip3 install psycopg2

Tenemos que crear el usuario 'ubre' y la base de datos 'ubre'. Por lo que escribimos:
1.- sudo -i -u postgres
2.- psql
3.- CREATE USER ubre WITH PASSWORD 'ubredatabase';
4.- CREATE DATABASE ubre;
5.- GRANT ALL PRIVILEGES ON DATABASE ubre TO ubre;

Ahora que tenemos el usuario y la base de datos creada tenemos que ir a un fichero específico para cambiar un ajuste de inicio, para que nos pida la contraseña para este usuario.
1.- sudo nano /etc/postgresql/10/main/pg_hba.conf
2.- En la parte donde pone: " 'local' is for Unix domain..." cambiamos la línea inmediatamente posterior de: local all all peer > local all all md5
3.- Guardamos y salimos del documento.

Para entrar a la base de datos PostgreSQL que hemos creado:
1.- sudo -i -u postgres
2.- psql -U ubre ubre (Ahora sí nos pedirá la contraseña que le hemos dado antes al usuario ubre)

Desde Django, tenemos que crear las tablas en la base de datos. Usaremos los siguientes comandos donde se encuentre el fichero manage.py:
1.- python3 manage.py makemigrations
2.- python3 manage.py migrate
