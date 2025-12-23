#!/usr/bin/env bash
# Script para testar as configurações antes do deploy

echo "🔍 Verificando configurações para deploy..."
echo ""

# Verificar se os arquivos necessários existem
echo "📋 Verificando arquivos necessários:"

files=("requirements.txt" "build.sh" "render.yaml" ".env.example" ".gitignore" "manage.py" "tierlist/settings.py")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file - FALTANDO!"
    fi
done

echo ""
echo "📦 Verificando dependências no requirements.txt:"

deps=("Django" "gunicorn" "whitenoise" "dj-database-url" "python-decouple" "psycopg2-binary")

for dep in "${deps[@]}"; do
    if grep -q "$dep" requirements.txt; then
        echo "✅ $dep"
    else
        echo "❌ $dep - FALTANDO!"
    fi
done

echo ""
echo "🔐 Verificando configurações de segurança:"

# Verificar se .env está no .gitignore
if grep -q "\.env" .gitignore; then
    echo "✅ .env está no .gitignore"
else
    echo "⚠️  .env NÃO está no .gitignore!"
fi

# Verificar se build.sh é executável
if [ -x "build.sh" ]; then
    echo "✅ build.sh é executável"
else
    echo "⚠️  build.sh NÃO é executável. Execute: chmod +x build.sh"
fi

echo ""
echo "📝 Próximos passos:"
echo "1. Crie um repositório no GitHub (se ainda não tiver)"
echo "2. Faça commit e push do código:"
echo "   git add ."
echo "   git commit -m 'Preparar para deploy no Render'"
echo "   git push origin main"
echo "3. Acesse https://render.com e faça login"
echo "4. Crie um novo Blueprint e conecte seu repositório"
echo "5. Configure a variável ALLOWED_HOSTS com seu domínio Render"
echo ""
echo "✨ Para mais detalhes, consulte o arquivo DEPLOY.md"
