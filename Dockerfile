# Usa uma imagem oficial e leve do Python
FROM python:3.12-slim

# Define variáveis de ambiente para otimizar o Python no Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instala as dependências
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o código do projeto para o contêiner
COPY . /app/