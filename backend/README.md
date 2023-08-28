### Como rodar o backend

1) Instale o Pipenv usando pip (pode ser necessário usar pip3 em vez de pip):   
  
    ~~~
    pip install pipenv 
    ~~~

2) Ative um novo ambiente virtual:

    ~~~
    pipenv shell
    ~~~

3) Execute o comando para baixar as dependências:

    ~~~
    pipenv install -r requirements.txt
    ~~~

4) Execute o flask (pode ser necessário usar python3 ao inves de python):

    ~~~
    python app.py
    ~~~