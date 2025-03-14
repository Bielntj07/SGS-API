# Sistema de Gerenciamento de Salas (SGS)

Este projeto é um Sistema de Gerenciamento de Salas (SGS) desenvolvido para gerenciar o agendamento e a utilização de salas de aula em escolas e faculdades. A aplicação segue o padrão MVC, utiliza Flask como framework web e SQLAlchemy como ORM com banco de dados SQLite, com possibilidade de integração futura com MongoDB.

## Tabela de Conteúdos

- [Recursos](#recursos)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação e Configuração](#instalação-e-configuração)
- [Execução da Aplicação](#execução-da-aplicação)
- [Testes](#testes)
- [Documentação da API](#documentação-da-api)
- [Docker](#docker)
- [Extras Planejados](#extras-planejados)
- [Licença](#licença)

## Recursos

- **Verificação de Disponibilidade:** Consulta em tempo real a disponibilidade das salas.
- **Reserva de Salas:** Administradores e professores podem reservar salas para eventos e aulas.
- **Gestão de Conflitos:** Detecção e resolução de conflitos de agendamento.
- **Notificações:** Envio de notificações por e-mail ou SMS sobre reservas e alterações.
- **Relatórios:** Geração de relatórios semanais e mensais (PDF e Excel).
- **Autenticação e Segurança:** Mecanismos para autenticação de usuários e criptografia de dados sensíveis.
