# VitaFlow - Gestão Inteligente para Saúde

**O VitaFlow é a plataforma definitiva para gestão de clínicas e hospitais.** Nossa solução organiza filas, otimiza o tempo da equipe e eleva a experiência do paciente através de triagem inteligente e automação de notificações.

Este projeto foi desenvolvido como proposta de solução de software aplicando as melhores práticas de Engenharia de Software, incluindo Clean Code, SOLID, Design Patterns, TDD, BDD, Arquitetura Limpa, Microsserviços e Docker.

---

## 🎯 O Problema

Clínicas e hospitais frequentemente enfrentam desafios com a **desorganização das filas de atendimento** e a **falta de comunicação eficiente** com os pacientes.
A recepção manual não consegue priorizar pacientes de forma dinâmica (ex: idosos ou emergências muitas vezes esperam na mesma fila que atendimentos eletivos), e a ausência de lembretes automatizados gera uma alta taxa de "no-show" (ausência de pacientes), gerando ociosidade médica e prejuízos financeiros.

## 💡 A Solução (VitaFlow)

O **VitaFlow** resolve esses problemas através de um sistema inteligente de agendamento e triagem.
- **Smart Queue (Fila Inteligente):** O sistema aplica regras de negócio automáticas para priorizar pacientes com base na idade (> 60 anos recebem prioridade alta) e gravidade do agendamento (emergências recebem prioridade máxima).
- **Automação de Notificações:** Pacientes recebem confirmações e lembretes por um microsserviço isolado, não impactando a performance da aplicação principal.
- **Agendamento Flexível:** Suporte a consultas presenciais e online (Telemedicina).

---

## 🏗 Justificativas Técnicas e Decisões de Arquitetura

O projeto foi construído para ser escalável, de fácil manutenção e fortemente testado. Abaixo detalhamos como cada conceito foi aplicado:

### 1. Arquitetura Limpa (Pragmática)
O projeto `scheduling` está dividido em camadas lógicas:
- `domain`: Contém as regras de negócio puras (Estratégias de prioridade, Fábricas de agendamento).
- `services`: Contém os Casos de Uso (ex: `SchedulingFacade`), orquestrando o domínio e a infraestrutura.
- `ui`: (Views e Forms do Django) que lidam apenas com a apresentação e entrada de dados.

> **Nota de Decisão Arquitetural:** Adotamos uma "Arquitetura Limpa Pragmática". Como estamos no ecossistema Django, os objetos passados para o domínio são instâncias dos modelos ORM (`Patient`, `Appointment`). Optamos por não criar entidades puras e mapeadores (Repositories) para evitar over-engineering, tratando os modelos do Django como nossas entidades de domínio.

### 2. Princípios SOLID
- **Single Responsibility Principle (SRP):** Cada classe possui uma única responsabilidade. Por exemplo, a `AppointmentFactory` foca exclusivamente na criação de instâncias com base no tipo.
- **Open/Closed Principle (OCP):** A interface `PriorityStrategy` permite que novas regras de prioridade sejam adicionadas (ex: Gestantes, PCD) criando novas classes, sem modificar a classe `PriorityStrategySelector`.
- **Dependency Inversion Principle (DIP):** O sistema depende de abstrações. O `Observer` para notificações não depende de implementações concretas (acoplamento fraco).

### 3. Design Patterns (Padrões de Projeto)
Aplicamos mais de 4 padrões clássicos (GoF) para resolver problemas de design:
1. **Strategy** (`priority_strategy.py`): Permite trocar o algoritmo de cálculo de prioridade (Idoso, Normal, Emergência) dinamicamente.
2. **Factory Method** (`appointment_factory.py`): Centraliza e padroniza a criação de agendamentos, injetando locais e notas padrão de acordo com o tipo (Online, Presencial, Emergência).
3. **Facade** (`facade.py`): Oferece uma interface simplificada para os controllers (`views.py`), ocultando a complexidade de instanciar factories, calcular prioridades e disparar notificações.
4. **Observer** (`observers.py`): O agendamento atua como "Subject", e ao ser finalizado, notifica automaticamente os "Observers" (ex: serviço de e-mail/SMS).
5. **Builder** (`patient_builder.py`): Facilita a construção passo a passo de objetos complexos (como o prontuário do paciente).

### 4. Microsserviços e Docker
A solução foi quebrada em **Microsserviços** para garantir que gargalos em uma área não derrubem o sistema inteiro. O `docker-compose.yml` sobe 4 containers principais:
- **web:** Aplicação central (Monolito modular em Django).
- **notification:** Microsserviço responsável pelo disparo de e-mails/mensagens.
- **telemedicine:** Microsserviço gerador de links para consultas online.
- **ehr:** Serviço de Prontuário Eletrônico independente.

### 5. Clean Code e Testes (TDD / BDD)
- **Clean Code:** Nomenclatura explícita em inglês para classes e métodos, funções curtas, ausência de "magic numbers" e regras de negócio auto-explicativas no código.
- **TDD (Test Driven Development):** A lógica do `domain` (Factory e Strategy) foi coberta por testes unitários (`test_unit.py`, `test_priority_strategy.py`, `test_appointment_factory.py`) garantindo que as regras de priorização funcionem sem falhas antes mesmo de acoplarmos a interface.
- **BDD (Behavior Driven Development):** Comportamentos descritos em linguagem ubíqua (Gherkin) em `tests/features/agendamento.feature` e automatizados em `test_bdd.py`, garantindo que os fluxos do usuário (ex: idoso recebendo prioridade alta na triagem) estejam corretos sob a ótica do negócio.

---

## 🛠 Como rodar localmente (Desenvolvimento)

O ambiente do VitaFlow é completamente conteinerizado para rodar de forma simples e consistente em qualquer máquina.

### Pré-requisitos
- Docker e Docker Compose instalados.

### Passos

1. Clone o repositório e entre na pasta:
```bash
git clone https://github.com/Chromick/VitaFlow.git
cd VitaFlow
```

2. Suba a aplicação:
```bash
docker-compose up --build
```

3. Acesse no navegador: `http://localhost:8000`

---

## 🌐 Deploy em Produção

O sistema está publicado e operante.

🔗 **[Acessar VitaFlow em Produção (Railway)](https://vitaflow-production-1872.up.railway.app/)**
