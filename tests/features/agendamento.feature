Feature: Agendamento de Consultas
  Como um paciente do VitaFlow
  Eu quero agendar uma consulta com um médico
  Para ser atendido com comodidade

  Scenario: Criação de um agendamento com sucesso
    Given que existe um paciente chamado "João Silva"
    And que existe um médico chamado "Dr. Carlos" da especialidade "Cardiologia"
    When o paciente solicita um agendamento "presencial" para o dia seguinte
    Then um agendamento deve ser criado no banco de dados com status "agendada"
