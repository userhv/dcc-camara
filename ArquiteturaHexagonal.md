Este projeto utiliza arquitetura hexagonal e assim a estrutura do back end é a seguinte:

├── Core
│   ├── adapters
│   │   ├── documentService.py
│   │   ├── meetingService.py
│   │   └── userService.py
│   ├── models
│   │   ├── document.py
│   │   ├── meeting.py
│   │   └── user.py
│   └── ports
│       ├── documentRepo.py
│       ├── meetingRepo.py
│       └── userRepo.py
├── db
│   ├── init_db.py
│   └── README.md
├── hexagonal.py
├── README.md
├── requirements.txt

Outros arquivos que estão no diretório e nao se encotram nessa árvove são simplemente arquivos gerados
automaticamente pelo flask e não possuem importância para a arquitetura hexagonal.

Observando como os arquivos estão organizados, podemos perceber que existem 3 diretórios que separam
o funcionamento do backend, Adapters, models e ports.

Em Models estão as classes de dominio, que nesse caso são User, meeting e document. Sendo que essas
classes conseguem representar o dominio da aplicação.

No diretorio ports estão as portas de entradas e saida que foram feitas a partir de classes "repositorios"
que  nada mais são do que interfaces implementadas no python a partir de métodos tipados e o decorador
"@abstractmethod"

Já em adapters encontram-se os adaptores desenvolvidos que são responsáveis por implementar as classes
abstratas criadas nos repósitorios.

Assim, o arquivo Hexagonal.py utiliza esses adaptadores em conjunto com o flask para poder criar  os endpoints
da api.