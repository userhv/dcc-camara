import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="camara_db",
    user='admin',
    password='123456')

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS usuario CASCADE; ')
cur.execute('DROP TABLE IF EXISTS reuniao CASCADE;')
cur.execute('DROP TABLE IF EXISTS pauta CASCADE;')
cur.execute('DROP TABLE IF EXISTS usuario_reuniao CASCADE;')
cur.execute('CREATE TABLE usuario (id serial PRIMARY KEY,'
            'nome varchar (150) NOT NULL,'
            'role varchar (50) NOT NULL,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);'
            )

cur.execute('CREATE TABLE reuniao (id serial PRIMARY KEY,'
            'titulo varchar (150) NOT NULL,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);'
            )

cur.execute('CREATE TABLE pauta (id serial PRIMARY KEY,'
            'titulo varchar (150) NOT NULL,'
            'reuniao_id serial NOT NULL,'
            'FOREIGN KEY(reuniao_id) REFERENCES reuniao(id)  ON UPDATE CASCADE ON DELETE CASCADE,'
            'documento varchar (150) NOT NULL,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);'
            )
cur.execute('CREATE TABLE usuario_reuniao (usuario_id integer '
            'REFERENCES usuario(id),reuniao_id integer '
            'REFERENCES reuniao(id),PRIMARY KEY (usuario_id,reuniao_id) );'
            )
# Insert data into the table

cur.execute('INSERT INTO usuario (nome, role)'
            'VALUES (%s, %s)',
            ('Discente',
             'Representante Discente')
            )
cur.execute('INSERT INTO usuario (nome, role)'
            'VALUES (%s, %s)',
            ('Chefe',
             'Chefia')
            )
cur.execute('INSERT INTO reuniao (titulo,date_added)'
            'VALUES (%s, %s)',
            ('Teste1',"2023-10-26")
            )
cur.execute('INSERT INTO reuniao (titulo,date_added)'
            'VALUES (%s, %s)',
            ('Teste2',"2023-10-26")
            )
cur.execute('INSERT INTO reuniao (titulo,date_added)'
            'VALUES (%s, %s)',
            ('Teste3',"2023-10-26")
            )



conn.commit()

cur.close()
conn.close()
