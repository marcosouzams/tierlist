# Tier List

Projeto Django para criar e gerenciar tier lists.

## Requisitos

- Python 3.11+
- PostgreSQL

## Configuração do Ambiente

### 1. Clone o repositório (se aplicável)
```bash
git clone <seu-repositorio>
cd tier-list
```

### 2. Crie e ative o ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate  # No Linux/Mac
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Certifique-se de que o PostgreSQL está instalado e rodando.

Crie o banco de dados:
```bash
psql -U postgres
CREATE DATABASE tierlist;
CREATE USER marco_ps WITH PASSWORD '3231+tom';
GRANT ALL PRIVILEGES ON DATABASE tierlist TO marco_ps;
\q
```

### 5. Execute as migrações
```bash
python manage.py migrate
```

### 6. Crie um superusuário
```bash
python manage.py createsuperuser
```

### 7. Execute o servidor
```bash
python manage.py runserver
```

Acesse o projeto em: http://localhost:8000

## Estrutura do Projeto

```
tier-list/
├── manage.py
├── tierlist/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── static/
├── media/
├── venv/
├── requirements.txt
├── .gitignore
└── README.md
```

## Tecnologias Utilizadas

- Django 5.2.9
- PostgreSQL
- Python 3.11

## Configurações

- **Idioma**: Português Brasileiro (pt-br)
- **Timezone**: America/Sao_Paulo
- **Banco de Dados**: PostgreSQL
