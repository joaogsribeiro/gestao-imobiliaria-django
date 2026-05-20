# Sistema de Gestão Imobiliária

Aplicação web sendo desenvolvida com Django para gerenciamento de imóveis, clientes e contratos de aluguel.

## Funcionalidades

- **Área administrativa** (Django Admin): cadastro e gestão de clientes, imóveis, fotos e contratos
- **Área do usuário**: visualização de imóveis disponíveis, detalhes e login protegido por senha
- **Upload de imagens** por imóvel com legendas
- **Controle de status** do imóvel (disponível, alugado, em manutenção)
- **Validação de contratos**: impede contratos em imóveis indisponíveis e datas inválidas

## Tecnologias

- **Backend**: Python 3.12 + Django 6.0
- **Banco de dados**: PostgreSQL 15
- **Frontend**: Bootstrap 5
- **Admin**: django-unfold
- **Conteinerização**: Docker + Docker Compose

## Modelo de Dados

```
Cliente ──< Imovel ──< ImagemImovel
   └──────────────────< ContratoAluguel >──┘
```

- `Cliente`: nome, CPF (único), telefone, e-mail
- `Imovel`: proprietário (FK Cliente), título, endereço, bairro, valor do aluguel, status
- `ImagemImovel`: imóvel (FK Imovel), arquivo de imagem, legenda
- `ContratoAluguel`: imóvel (FK Imovel), locatário (FK Cliente), datas, valor fechado

## Como Rodar

### Com Docker (recomendado)

```bash
docker-compose up --build
```

Acesse em: http://localhost:8000

### Sem Docker

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Acessos

| Ambiente | URL | Credenciais |
|----------|-----|-------------|
| Admin | `/admin/` | superusuário criado via `createsuperuser` |
| Usuário | `/` | login via `/accounts/login/` |

## Estrutura do Projeto

```
gestao-imobiliaria-django/
├── imoveis/          # App principal (models, views, admin)
├── setup/            # Configurações do projeto Django
├── templates/        # Templates HTML (Bootstrap 5)
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Disciplina

GAC116 — Programação Web — 2026/1
