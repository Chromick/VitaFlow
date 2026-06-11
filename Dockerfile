# Usa uma imagem oficial do Python, versão 3.12, enxuta (slim)
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Variáveis de ambiente para não gerar arquivos .pyc e para logs irem direto pro terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema operacional necessárias para compilar o psycopg2 (PostgreSQL)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências do Python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o restante do código do projeto para dentro do container
COPY . /app/

# Expõe a porta 8000 para podermos acessar do navegador
EXPOSE 8000

# Comando padrão ao rodar o container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
