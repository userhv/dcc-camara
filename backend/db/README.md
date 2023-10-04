## Executar o banco local

Para criar o banco de dados local execute o codigo abaixo: 

```shell
foo@bar:~$ sudo -iu postgres psql
```

```shell
CREATE DATABASE camara_db;
```

```shell
CREATE USER admin WITH PASSWORD '123456';
```

```shell
GRANT ALL PRIVILEGES ON DATABASE camara_db TO admin;
```


Apos isso, rode 

```shell
   python3 init_db.py
```


[Mais informações ou dúvidas](https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application)