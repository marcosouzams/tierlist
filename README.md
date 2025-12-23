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
- Gunicorn (servidor WSGI)
- WhiteNoise (arquivos estáticos)

## Configurações

- **Idioma**: Português Brasileiro (pt-br)
- **Timezone**: America/Sao_Paulo
- **Banco de Dados**: PostgreSQL

## Deploy no Render.com

### Método 1: Usando render.yaml (Recomendado)

1. **Faça push do código para o GitHub**
   ```bash
   git add .
   git commit -m "Preparar para deploy no Render"
   git push origin main
   ```

2. **No Render.com:**
   - Acesse https://render.com e faça login
   - Clique em "New +" e selecione "Blueprint"
   - Conecte seu repositório do GitHub
   - O Render detectará automaticamente o arquivo `render.yaml`
   - Clique em "Apply" para criar os serviços

3. **Configure as variáveis de ambiente:**
   - O Render criará automaticamente `SECRET_KEY` e `DATABASE_URL`
   - Adicione manualmente `ALLOWED_HOSTS` com o valor do seu domínio Render (ex: `tierlist.onrender.com`)

### Método 2: Configuração Manual

1. **Crie o PostgreSQL Database:**
   - No dashboard do Render, clique em "New +" → "PostgreSQL"
   - Escolha um nome (ex: `tierlist-db`)
   - Selecione o plano Free
   - Clique em "Create Database"
   - Copie a URL de conexão interna

2. **Crie o Web Service:**
   - No dashboard, clique em "New +" → "Web Service"
   - Conecte seu repositório do GitHub
   - Configure:
     - **Name**: tierlist
     - **Runtime**: Python 3
     - **Build Command**: `./build.sh`
     - **Start Command**: `gunicorn tierlist.wsgi:application`

3. **Configure as variáveis de ambiente:**
   - `SECRET_KEY`: Gere uma chave segura
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Seu domínio Render (ex: `tierlist.onrender.com`)
   - `DATABASE_URL`: Cole a URL do banco criado no passo 1

4. **Deploy:**
   - Clique em "Create Web Service"
   - O Render iniciará o build e deploy automaticamente

### Após o Deploy

- O primeiro deploy pode levar alguns minutos
- Acesse a URL fornecida pelo Render
- Para acessar o admin: `https://seu-app.onrender.com/admin/`
- Crie um superusuário executando um shell no Render:
  - No dashboard → Shell → `python manage.py createsuperuser`

### Importante sobre o Plano Free

- O serviço entra em modo sleep após 15 minutos de inatividade
- Pode levar 50+ segundos para "acordar" na primeira requisição
- O banco de dados é gratuito mas tem limites de armazenamento

### Troubleshooting

Se houver problemas:
- Verifique os logs no dashboard do Render
- Certifique-se de que todas as variáveis de ambiente estão configuradas
- Confirme que `ALLOWED_HOSTS` inclui seu domínio Render
- Verifique se o `build.sh` tem permissão de execução (`chmod +x build.sh`)

````
