Feature: Agendamento de Consultas
  Como um paciente do VitaFlow
  Eu quero agendar uma consulta com um médico
  Para ser atendido com comodidade e segurança

  Scenario: Criação de um agendamento com sucesso (Prioridade Normal)
    Given que existe um paciente chamado "João Silva" com "30" anos
    And que existe um médico chamado "Dr. Carlos" da especialidade "Cardiologia"
    When o paciente solicita um agendamento "presencial" para o dia seguinte
    Then um agendamento deve ser criado no banco de dados com status "agendada"
    And a prioridade definida deve ser "Normal"

  Scenario: Criação de agendamento com prioridade por idade (Idoso)
    Given que existe um paciente chamado "Dona Odete" com "75" anos
    And que existe um médico chamado "Dra. Ana" da especialidade "Geriatria"
    When o paciente solicita um agendamento "presencial" para o dia seguinte
    Then um agendamento deve ser criado no banco de dados com status "agendada"
    And a prioridade definida deve ser "Alta"

  Scenario: Criação de agendamento emergencial
    Given que existe um paciente chamado "Marcos" com "40" anos
    And que existe um médico chamado "Dr. Plantonista" da especialidade "Geral"
    When o paciente solicita um agendamento "emergencial" para hoje
    Then um agendamento deve ser criado no banco de dados com status "agendada"
    And a prioridade definida deve ser "Maxima"
