# Guia de Deploy no Render.com

## 📋 Checklist de Preparação

✅ Todas as alterações necessárias foram feitas:

- [x] `requirements.txt` atualizado com dependências de produção
- [x] `settings.py` configurado com variáveis de ambiente
- [x] `build.sh` criado para o processo de build
- [x] `render.yaml` criado para configuração automática
- [x] `.gitignore` configurado
- [x] `.env.example` como referência

## 🚀 Passo a Passo Completo

### 1. Preparar o Repositório Git

Certifique-se de que seu código está no GitHub:

```bash
# Se ainda não inicializou o git
git init
git add .
git commit -m "Preparar para deploy no Render"

# Criar repositório no GitHub e adicionar remote
git remote add origin https://github.com/seu-usuario/seu-repo.git
git branch -M main
git push -u origin main
```

### 2. Criar Conta no Render

1. Acesse https://render.com
2. Crie uma conta (pode usar GitHub para login)
3. Conecte sua conta do GitHub ao Render

### 3. Deploy Usando Blueprint (render.yaml)

Esta é a forma mais simples!

1. **No Render Dashboard:**
   - Clique em "New +" no canto superior direito
   - Selecione "Blueprint"

2. **Conectar Repositório:**
   - Selecione o repositório do GitHub onde está seu projeto
   - O Render detectará automaticamente o arquivo `render.yaml`

3. **Revisar Configurações:**
   - Verifique os serviços que serão criados:
     * Web Service (Django com Gunicorn)
     * PostgreSQL Database
   - Clique em "Apply"

4. **Aguardar a Criação:**
   - O Render criará automaticamente:
     * Banco de dados PostgreSQL
     * Web service com Django
     * Variáveis de ambiente necessárias

### 4. Configurar Variáveis de Ambiente

Após a criação, adicione/verifique as variáveis de ambiente no dashboard do Web Service:

**Obrigatórias:**
- `SECRET_KEY`: (gerada automaticamente pelo Render)
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: `seu-app.onrender.com` (substitua pelo seu domínio real)
- `DATABASE_URL`: (conectada automaticamente ao banco)

**Opcional (para produção):**
- `PYTHON_VERSION`: `3.11.0`

### 5. Primeiro Deploy

1. O Render iniciará automaticamente o primeiro deploy
2. Acompanhe os logs em tempo real no dashboard
3. O processo executará:
   ```bash
   chmod +x build.sh
   ./build.sh
   # Instala dependências
   # Coleta arquivos estáticos
   # Executa migrações
   ```

4. Após conclusão, seu app estará disponível em: `https://seu-app.onrender.com`

### 6. Criar Superusuário

Para acessar o admin do Django:

1. No dashboard do Render, acesse seu Web Service
2. Clique na aba "Shell" no menu lateral
3. Execute:
   ```bash
   python manage.py createsuperuser
   ```
4. Siga as instruções para criar o usuário admin

### 7. Testar a Aplicação

1. Acesse `https://seu-app.onrender.com`
2. Teste as funcionalidades principais
3. Acesse o admin em `https://seu-app.onrender.com/admin/`

## 🔧 Configuração Manual (Alternativa)

Se preferir não usar o render.yaml:

### Passo 1: Criar Banco de Dados

1. No Render Dashboard → "New +" → "PostgreSQL"
2. Configurações:
   - **Name**: `tierlist-db`
   - **Database**: `tierlist`
   - **User**: (gerado automaticamente)
   - **Region**: Escolha a mais próxima
   - **Plan**: Free
3. Clique em "Create Database"
4. **Importante**: Copie a "Internal Database URL"

### Passo 2: Criar Web Service

1. No Render Dashboard → "New +" → "Web Service"
2. Conecte seu repositório do GitHub
3. Configurações:
   - **Name**: `tierlist`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn tierlist.wsgi:application`
   - **Plan**: Free

4. Variáveis de Ambiente (Environment):
   - `SECRET_KEY`: Gere uma nova em https://djecrety.ir/
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `.onrender.com`
   - `DATABASE_URL`: Cole a Internal Database URL do passo anterior

5. Clique em "Create Web Service"

## 📝 Atualizações e Redesploy

### Deploy Automático

O Render faz deploy automático quando você faz push para o branch principal:

```bash
git add .
git commit -m "Sua mensagem de commit"
git push origin main
```

### Deploy Manual

No dashboard do Render:
1. Acesse seu Web Service
2. Clique em "Manual Deploy" → "Deploy latest commit"

### Ver Logs

Para debugar problemas:
1. Acesse seu Web Service no Render
2. Clique na aba "Logs"
3. Veja logs em tempo real do build e runtime

## ⚠️ Limitações do Plano Free

- **Web Service:**
  - 750 horas/mês gratuitas
  - Entra em sleep após 15 minutos de inatividade
  - 50+ segundos para acordar
  - 512 MB RAM

- **PostgreSQL:**
  - 1 GB de armazenamento
  - Expira após 90 dias (precisa criar novo)
  - Sem backups automáticos

- **Bandwidth:**
  - 100 GB/mês de transferência

## 🔒 Segurança

### Checklist de Segurança

- [x] `DEBUG = False` em produção
- [x] `SECRET_KEY` diferente do desenvolvimento
- [x] `ALLOWED_HOSTS` configurado corretamente
- [x] Arquivos `.env` no `.gitignore`
- [x] Credenciais do banco não hardcoded
- [x] WhiteNoise configurado para servir estáticos

### Recomendações

1. **Nunca commite o arquivo `.env`** com credenciais reais
2. **Gere uma nova SECRET_KEY** para produção
3. **Use HTTPS** (Render fornece automaticamente)
4. **Configure CORS** se tiver frontend separado
5. **Monitore os logs** regularmente

## 🐛 Troubleshooting Comum

### Erro: "Application failed to respond"

**Causa**: Geralmente problema com o comando de start ou porta.

**Solução**:
- Verifique que o comando de start é: `gunicorn tierlist.wsgi:application`
- Gunicorn deve estar em `requirements.txt`

### Erro: "Build failed"

**Causa**: Problema no `build.sh` ou dependências.

**Solução**:
```bash
# Localmente, teste o build.sh
chmod +x build.sh
./build.sh
```
- Verifique se todas as dependências estão em `requirements.txt`
- Veja os logs para identificar o erro específico

### Erro: "Database connection failed"

**Causa**: `DATABASE_URL` incorreta ou banco não criado.

**Solução**:
- Verifique se o banco PostgreSQL está rodando
- Confirme que `DATABASE_URL` está configurada
- Use a "Internal Database URL" do Render

### Erro: "Bad Request (400)"

**Causa**: `ALLOWED_HOSTS` não configurado corretamente.

**Solução**:
- Adicione seu domínio Render em `ALLOWED_HOSTS`
- Exemplo: `seu-app.onrender.com`
- Ou use: `.onrender.com` para aceitar qualquer subdomínio

### App muito lento

**Causa**: Plano free entra em sleep.

**Solução**:
- Use um serviço de "ping" para manter ativo (não recomendado)
- Ou considere upgrade para plano pago
- Ou aceite o delay inicial

### Arquivos estáticos não carregam

**Causa**: `collectstatic` não executou ou WhiteNoise mal configurado.

**Solução**:
- Verifique que `build.sh` executa `collectstatic`
- Confirme WhiteNoise em `MIDDLEWARE` e `STORAGES`
- Execute manualmente: `python manage.py collectstatic --no-input`

## 📚 Recursos Adicionais

- [Documentação Oficial do Render](https://render.com/docs)
- [Deploy Django no Render](https://render.com/docs/deploy-django)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

## 💡 Próximos Passos

Após o deploy bem-sucedido:

1. **Domínio Customizado**: Configure um domínio próprio no Render
2. **Emails**: Configure serviço de email (SendGrid, Mailgun, etc.)
3. **Monitoramento**: Adicione Sentry para rastreamento de erros
4. **CDN**: Configure CloudFlare para melhor performance
5. **Backup**: Implemente rotina de backup do banco de dados
6. **CI/CD**: Configure testes automáticos antes do deploy

## 🆘 Suporte

Se tiver problemas:

1. Consulte os logs no Render Dashboard
2. Verifique a documentação oficial
3. Procure no Stack Overflow
4. Abra um ticket no suporte do Render

---

**Boa sorte com seu deploy! 🚀**
