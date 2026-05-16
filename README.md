# VitaFlow Clinic

Sistema de agendamento hospitalar criado em Django para demonstrar a aplicacao integrada de padroes de projeto em uma arquitetura simples, funcional e facil de manter.

## Identidade

- Nome: VitaFlow Clinic
- Proposta: agendamento hospitalar claro, humano e inteligente
- Dominio: consultas presenciais, online e emergenciais

## Como rodar

No PowerShell, dentro da pasta do projeto:

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

Depois acesse:

```text
http://127.0.0.1:8000/
```

Se precisar recriar o banco:

```powershell
python manage.py migrate
python manage.py seed_demo
```

## Arquitetura

```text
vitaflow/
  settings.py        configuracao do Django
  urls.py            rotas globais

scheduling/
  models.py          entidades persistidas
  forms.py           formulario de agendamento
  views.py           views finas, sem regra pesada
  domain/            regras de dominio e Design Patterns
  services/          casos de uso da aplicacao
  ui/                identidade e componentes de contexto visual
  management/        comando para dados de demonstracao

templates/
  base.html
  scheduling/        telas do produto

static/
  css/app.css        design system minimalista
```

## Padroes de projeto aplicados

- Builder: `scheduling/domain/patient_builder.py`
  - Monta a ficha do paciente com dados obrigatorios e opcionais.

- Factory Method: `scheduling/domain/appointment_factory.py`
  - Cria consultas presenciais, online ou emergenciais com configuracoes proprias.

- Strategy: `scheduling/domain/priority_strategy.py`
  - Calcula a prioridade usando regras trocaveis, como normal, idoso e emergencia.

- Observer: `scheduling/domain/observers.py`
  - Notifica paciente, medico e recepcao quando uma consulta e criada ou cancelada.

- Facade: `scheduling/services/facade.py`
  - Centraliza o caso de uso de agendar e cancelar consulta, mantendo a view simples.

## Roteiro curto para o video

1. Apresente o problema: hospitais precisam organizar consultas, prioridades e notificacoes.
2. Mostre o painel inicial e um novo agendamento.
3. Explique a arquitetura de pastas.
4. Abra `services/facade.py` e mostre a orquestracao.
5. Mostre cada arquivo dentro de `domain/` e explique o papel de cada padrao.
6. Finalize mostrando a consulta criada e os logs de notificacao.
