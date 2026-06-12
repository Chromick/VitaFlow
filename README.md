# VitaFlow - Gestão Inteligente para Saúde

**O VitaFlow é a plataforma definitiva para gestão de clínicas e hospitais.** 
Nossa solução organiza filas, otimiza o tempo da equipe e eleva a experiência do paciente através de triagem inteligente e automação de notificações.

---

## 🚀 Principais Funcionalidades

- **Agendamento Flexível:** Suporte a consultas presenciais e online (Telemedicina).
- **Triagem Inteligente (Smart Queue):** O sistema reordena a fila de pacientes de forma autônoma, dando prioridade para emergências, idosos e casos preferenciais sem a necessidade de intervenção manual da recepção.
- **Automação de Notificações:** Pacientes e médicos são avisados em tempo real sobre confirmações, atrasos ou cancelamentos via E-mail, SMS e Painel Interno.
- **Micro-arquitetura Escalável:** O envio de mensagens não afeta a velocidade do sistema principal, garantindo alta disponibilidade mesmo em horários de pico.

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

2. Suba a aplicação (Banco de Dados + API Principal + Serviço de Notificação):
```bash
docker-compose up --build
```

3. Acesse no navegador:
- **Painel Administrativo:** `http://localhost:8000`

---

## 🌐 Deploy em Produção

O VitaFlow já está configurado para deploy contínuo em plataformas modernas.
Acesse o ambiente de produção aqui:

🔗 **[https://vitaflow-production-1872.up.railway.app/](https://vitaflow-production-1872.up.railway.app/)**

---

## 🏗 Arquitetura Escalável

O sistema foi desenhado para crescer com a sua clínica:
- **Banco de Dados Seguro:** Utiliza PostgreSQL para garantir a integridade dos prontuários médicos.
- **Notificações Assíncronas:** Serviço isolado que garante a entrega de lembretes aos pacientes de forma rápida e segura.
- **Código Testado:** Cobertura de testes automatizados garantem que as regras de triagem funcionem 100% das vezes sem falhas humanas.
