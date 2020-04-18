# ubre-backend

Necesita de una base de datos externa PostgreSQL. Lo primero que hay que hacer es instalarla (si no la tenemos ya) en Ubuntu 18.04 LTS:
```
sudo apt update
sudo apt install postgresql postgresql-contrib libpq-dev
```

Instalar el conector para PostgreSQL.
```
pip3 install psycopg2
```

Tenemos que crear el usuario 'ubre' y la base de datos 'ubre'. Por lo que escribimos:
```
sudo -i -u postgres
psql
CREATE USER ubre WITH PASSWORD 'ubredatabase';
CREATE DATABASE ubre;
GRANT ALL PRIVILEGES ON DATABASE ubre TO ubre;
```

Ahora que tenemos el usuario y la base de datos creada tenemos que ir a un fichero específico para cambiar un ajuste de inicio, para que nos pida la contraseña para este usuario.
```
sudo nano /etc/postgresql/10/main/pg_hba.conf
sudo service postgresql restart
```
En la parte donde pone: " 'local' is for Unix domain..." cambiamos la línea inmediatamente posterior: local all all peer > local all all md5
Guardamos y salimos del documento.

Para entrar a la base de datos PostgreSQL que hemos creado:
```
sudo -i -u postgres
psql -U ubre ubre (Ahora sí nos pedirá la contraseña que le hemos dado antes al usuario ubre)
```

Desde Django, tenemos que crear las tablas en la base de datos. Usaremos los siguientes comandos donde se encuentre el fichero manage.py:
```
python3 manage.py makemigrations
python3 manage.py migrate
```

Para insertar un usuario en la base de datos se haría de la siguiente forma:
```
{
 "email":"pablotria98@gmail.com",
 "password":"123456",
 "profile": {
 		"dni": "34285964W",
        "name": "Pablo",
        "last_name": "Cachafeiro",
        "tlf": "690814618",
        "age": 21
 }
}
```
