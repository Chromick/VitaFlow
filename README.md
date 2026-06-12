# VitaFlow Clinic - Sistema de Agendamento Hospitalar

Este projeto é uma solução completa de software para gestão de agendamentos hospitalares, construído para demonstrar de forma prática a aplicação de boas práticas de engenharia de software, incluindo **Clean Code**, **SOLID**, **Design Patterns**, **TDD/BDD**, **Arquitetura Limpa** e **Microsserviços**.

---

## 1. Descrição do Problema e Proposta de Solução

**Problema:** Hospitais e clínicas frequentemente lidam com sistemas de agendamento monolíticos e acoplados, onde regras de prioridade (como idade avançada ou urgência) se misturam com a interface de usuário. Isso gera código frágil, difícil de testar e escalar. Além disso, a comunicação com o paciente (notificações) costuma estar travada no mesmo fluxo do banco de dados, causando lentidão.

**Solução (VitaFlow):** O VitaFlow é um sistema de agendamento focado em código limpo e arquitetura modular. A solução separa claramente as regras de negócio da interface web. Os agendamentos possuem fluxos específicos (presencial, online, emergência) geridos por *Design Patterns*, e o processo de notificação do paciente foi desacoplado em um **microsserviço independente**, permitindo que a clínica dimensione apenas o serviço de mensageria caso haja pico de consultas.

---

## 2. Divisão da Solução em Microsserviços

Para garantir a escalabilidade e a separação de responsabilidades, a solução foi dividida nos seguintes serviços isolados (orquestrados via Docker Compose):

1. **Web App (Django):** Serviço principal. Lida com a interface do usuário, formulários, persistência de dados de agendamento e regras de domínio hospitalar.
2. **Notification Service (Flask):** Um microsserviço independente localizado na pasta `notification_service`. Expõe uma API REST (`/notify`) e tem a responsabilidade exclusiva de disparar comunicações (e-mail/SMS).
3. **Database (PostgreSQL):** Serviço de banco de dados rodando em um container dedicado para armazenamento seguro e isolado.

*Justificativa Técnica:* Separar o serviço de notificações impede que o sistema principal fique bloqueado (gargalo de I/O) enquanto aguarda respostas de servidores de e-mail de terceiros.

---

## 3. Arquitetura Limpa e Organização das Camadas

O projeto foi estruturado seguindo os preceitos da **Clean Architecture**, isolando o domínio das ferramentas externas (como o framework Django):

- **Entidades de Domínio (`scheduling/models.py`):** Classes que representam o coração do negócio (`Patient`, `Doctor`, `Appointment`).
- **Casos de Uso (`scheduling/services/`):** Contém a lógica orquestrada da aplicação (ex: `facade.py` lida com a ação do usuário de "Marcar Consulta").
- **Adaptadores de Interface (`scheduling/views.py` e `scheduling/forms.py`):** Traduzem dados da web (HTTP/HTML) para o formato que os casos de uso entendem.
- **Frameworks e Drivers (`vitaflow/settings.py` e `urls.py`):** A camada mais externa, lidando puramente com configuração do framework Django e rotas.

---

## 4. Aplicação dos Princípios SOLID

- **SRP (Single Responsibility Principle):** A classe `AppointmentFacade` (em `services/facade.py`) tem a única responsabilidade de orquestrar o agendamento, delegando a criação para factories e a notificação para observers.
- **OCP (Open/Closed Principle):** O cálculo de prioridade (`priority_strategy.py`) está aberto para extensão (podemos criar `VipPriorityStrategy` facilmente) mas fechado para modificação (não precisamos alterar a interface base).
- **LSP (Liskov Substitution Principle):** Qualquer implementação de `AppointmentObserver` pode substituir a classe base na lista de observadores sem quebrar o sujeito (`AppointmentSubject`).
- **ISP (Interface Segregation Principle):** As interfaces de observers (em `observers.py`) e strategies possuem métodos pequenos e diretos (`update`, `calculate`), forçando os clientes a implementarem apenas o necessário.
- **DIP (Dependency Inversion Principle):** O domínio não depende de implementações concretas de envio de email. Ele depende de abstrações (`AppointmentObserver`), permitindo que a camada de infraestrutura injete o microsserviço real.

---

## 5. Aplicação de Design Patterns

O projeto implementa intensamente os padrões GoF:

1. **Builder (`patient_builder.py`):** Facilita a construção complexa da ficha do paciente, permitindo adição opcional de histórico médico de forma fluída.
2. **Factory Method (`appointment_factory.py`):** Centraliza a criação de agendamentos. Decide dinamicamente a duração e regras da consulta baseando-se no tipo (Presencial vs Emergência).
3. **Strategy (`priority_strategy.py`):** Encapsula os algoritmos de cálculo de prioridade na fila de espera, permitindo alternar a lógica em tempo de execução.
4. **Observer (`observers.py`):** Desacopla as notificações. Quando uma consulta é agendada, o Subject notifica de forma assíncrona o Microsserviço, os médicos e a recepção.
5. **Facade (`facade.py`):** Esconde a complexidade de instanciar Builders, Factories e Observers atrás de um único método simples exposto para a View.

---

## 6. Evidências de Clean Code

- **Nomes Significativos:** Funções como `schedule_appointment_for_patient` descrevem exatamente o que fazem.
- **Funções Pequenas e Focadas:** As views (`views.py`) não contêm regras de negócio, apenas recebem o form e repassam para o Facade.
- **Ausência de Magic Numbers:** Constantes e Enums (como `Appointment.Kind.IN_PERSON`) são usados no lugar de strings soltas.
- **Tratamento de Erros:** Exceções do microsserviço são capturadas com logs apropriados no Observer, sem quebrar a tela do usuário.

---

## 7 e 8. Testes com TDD e BDD

O sistema possui uma suíte de testes robusta localizada na pasta `tests/`:

- **TDD (Test-Driven Development):** Testes unitários (`test_unit.py`) focados em garantir as regras de domínio, como o salvamento correto de um agendamento válido no banco de dados.
- **BDD (Behavior-Driven Development):** Testes de comportamento (`test_bdd.py` e `features/`) que mapeiam requisitos de negócio (em linguagem Gherkin) diretamente para o código, garantindo que "Dado um paciente X, Quando ele agenda, Então o status é agendado".

Para rodar os testes localmente:
```bash
pytest tests/
```

---

## 9. Configuração com Docker e Docker Compose

O ambiente está totalmente conteinerizado:
- `Dockerfile` principal na raiz (Django Web App).
- `Dockerfile` na pasta `notification_service` (Microsserviço).
- `docker-compose.yml` unificando Web, Notificações e o banco PostgreSQL.

Para rodar o ecossistema completo localmente:
```bash
docker-compose up --build
```
Isso subirá:
- Aplicação principal em: `http://localhost:8000`
- Microsserviço em: `http://localhost:8001`

---

## 10 e 11. Deploy Ativo e Link de Acesso

O sistema principal foi publicado com sucesso utilizando a plataforma **Railway**, o que demonstra o fluxo de integração e entrega contínuas (CI/CD) a partir do repositório GitHub.

🔗 **Link de Acesso (Produção):** [https://vitaflow-production-1872.up.railway.app/](https://vitaflow-production-1872.up.railway.app/)

*(Nota: Na nuvem, o frontend se conecta ao banco de dados provisionado pelo Railway, garantindo persistência real.)*

---

## 12. Justificativa Técnica das Escolhas

1. **Python/Django:** Escolhido pela velocidade de desenvolvimento e facilidade de expressar regras complexas usando orientação a objetos nativa.
2. **Flask para o Microsserviço:** Por ser minimalista (microframework), é ideal para um serviço pequeno e rápido que recebe payloads JSON.
3. **PostgreSQL:** Banco de dados relacional robusto, escolhido por manter a consistência transacional ACID necessária para agendamentos médicos.
4. **Arquitetura Baseada em Padrões:** Embora a aplicação pareça simples no momento, a escolha por Design Patterns e Clean Architecture garante que a adição de novos tipos de consultas, novos canais de notificação ou novas regras de prioridade ocorrerá sem modificar o código existente (OCP), reduzindo o custo de manutenção a longo prazo.
