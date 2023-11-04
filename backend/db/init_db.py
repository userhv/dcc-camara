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
            'aprovado boolean,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);'
            )

# Insert data into the table

cur.execute('INSERT INTO usuario (nome, role)'
            'VALUES (%s, %s)',
            ('Discente',
             'Representante Discente')
            )
cur.execute('INSERT INTO usuario (nome, role)'
            'VALUES (%s, %s)',
            ('eu',
             'Representante Discente')
            )
cur.execute('INSERT INTO usuario (nome, role)'
            'VALUES (%s, %s)',
            ('Chefe',
             'Chefia')
            )
cur.execute('INSERT INTO reuniao (titulo,date_added)'
            'VALUES (%s, %s)',
            ('REUNIÃO DE 22/10/2023',"2023-10-22")
            )
cur.execute('INSERT INTO reuniao (titulo,date_added)'
            'VALUES (%s, %s)',
            ('REUNIÃO DE 29/10/2023',"2023-10-29")
            )
cur.execute('INSERT INTO reuniao (titulo,date_added)'
            'VALUES (%s, %s)',
            ('REUNIÃO DE 01/11/2023',"2023-11-02")
            )
cur.execute('INSERT INTO reuniao (titulo,date_added)'
            'VALUES (%s, %s)',
            ('REUNIÃO DE 26/11/2023',"2023-11-26")
            )
cur.execute('INSERT INTO reuniao (titulo,date_added)'
            'VALUES (%s, %s)',
            ('REUNIÃO DE 18/11/2023',"2023-11-18")
            )
 
cur.execute('INSERT INTO pauta (titulo,reuniao_id, documento,aprovado)'
            'VALUES (%s, %s, %s,%s)',
            ("Gráfico de Contributors",3,"\\assets\\Contributions.png",True,)
            )
cur.execute('INSERT INTO pauta (titulo,reuniao_id, documento,aprovado)'
            'VALUES (%s, %s, %s,%s)',
            ("DCC Week", 3,"\\assets\\Documento.pdf",True,)
            )
cur.execute('INSERT INTO pauta (titulo,reuniao_id, documento,aprovado)'
            'VALUES (%s, %s, %s,%s)',
            ("Disciplina de Ciência de Dados",1,"\\assets\\Documento.pdf",True,)
            )
cur.execute('INSERT INTO pauta (titulo,reuniao_id, documento,aprovado)'
            'VALUES (%s, %s, %s,%s)',
            ("Mudança no percurso curricular de Ciência da Computação",2,"\\assets\\Documento.pdf",True,)
            )
cur.execute('INSERT INTO pauta (titulo,reuniao_id, documento,aprovado)'
            'VALUES (%s, %s, %s,%s)',
            ("Matriz curricular comum para CC e SI",3,"\\assets\\Documento.pdf",True,)
            )
cur.execute('INSERT INTO pauta (titulo,reuniao_id, documento,aprovado)'
            'VALUES (%s, %s, %s,%s)',
            ("Mudança de horário de disciplinas",4,"\\assets\\Documento.pdf",True,)
            )


conn.commit()

cur.close()
conn.close()