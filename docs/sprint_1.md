## Sprint 1

### Tarefas técnicas

* Criar o banco de dados de reunioes e perfis de acesso. [HELIO]
    - Criar uma API para comunicação com o banco de dados.
    - Criar o banco de dados de acordo com o modelo.

* Criar duas contas de acesso, chefia e Outros e popular no banco de dados. [HELIO]
    - Criar uma conta de chefia.
    - Criar uma conta de usuario.

* Criar a arquitetura de integração do flask com Angular. [HELIO]
    - Criar o projeto do Angular.
    - Criar o projeto do Flask.
    - Criar o projeto do Docker.

### Tarefas de negócio

* Como usuario, gostaria de fazer login e logout na aplicação. [SAMUEL]
    - Estilizar a tela de login do sistema.

* Tela de navegação do sistema. [SAMUEL]
    - Criar e estilizar o componente navbar e mostrar as guias de acordo com o perfil de acesso.
    - Criar as rotas de navegação do sistema.

* Como chefia, gostaria de cadastrar e remover reunioes. [GABRIEL]
    - Criar o modal de adicionar/remover reunião.
    - Criar a tela de reunião seguindo a tela "nova_reuniao_vazia" no prototipo.

* Como chefia, gostaria de adicionar pautas para reunião. [GABRIEL]
    - Criar os componentes para adicionar pautas.
    - Criar o modal de pautas como está no prototipo mas não implementar as funcionalidades de gerenciamento.
    - Listar as pautas na tela de reunião.

* Como usuario, gostaria de ver as reunioes na tela home. [MATHEUS]
    - Estilizar a tela principal de acordo com o prototipo.
    - Para o perfil Chefia, adicionar o botão de preferencias.

* Como chefia, gostaria de editar, remover e baixar pautas. [SAMUEL]
    - No modal de pautas, implementar as funcionalidades de gerenciamento.
    - Criar os modais associados ao gerenciamento das pautas.
    - Não implementar a visualização das pautas.

* Como usuario, gostaria de visualizar, dar zoom e navegar pelas pautas. [MATHEUS]
    - Visualizar as pautas por meio de um modal dentro do sistema.
    - Adicionar essa funcionalidade no card de pautas.

### Tarefas para fazer

* Como usuario gostaria de solicitar uma pauta para reunião.
    - O perfil do usuario pode solicitar uma pauta para a reunião. A solicitação estara vigente apenas para a próxima reunião.
    - O perfil chefia pode controlar as solicitações, aprovando, reprovando ou marcando como pendente para adicionar algum documento.
    - Caso marcado como pendente, deve aparecer o campo pra inserir novos documentos, ver figma.
    - Ao marcar como aprovar ou reprovar, os botoes de gerenciamento da solicitação de pauta somem no perfil da chefia.


* Diversas correções de bugs
    - No modal de pautas, implementar as funcionalidades de gerenciamento, editar, remver, visualizar, baixar
    - Ajustar o modal de cadastrar pauta para se parecer com o do prototipo.
    - Adicionar a remoção de reuniao
    - Adicionar o botao de sair
    - Corrigir funcionalidades que nao estao de acordo com o prototipo.

