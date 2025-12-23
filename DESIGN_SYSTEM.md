# Sistema de Design - Tier List

## Paleta de Cores

### Cores Principais
- **Preto**: `#000000` - Elementos primários, textos principais, botões de ação
- **Branco**: `#FFFFFF` - Background principal, espaços em branco
- **Cinza Claro**: `#F9FAFB` - Backgrounds secundários, cards
- **Cinza Médio**: `#6B7280` - Textos secundários, ícones

### Cor de Destaque
- **Verde Accent**: `#22c55e` (green-500)
  - Usado para: Botões primários, badges de status "Aberto", elementos de destaque
  - Variações: 
    - Hover: `#16a34a` (green-600)
    - Light: `#dcfce7` (green-100)

## Tipografia

### Fonte Principal
**Space Grotesk** (Google Fonts)
- Característica: Formas únicas e modernas
- Pesos utilizados: 300, 400, 500, 600, 700

### Hierarquia de Tamanhos
- **Títulos H1**: 36px (text-4xl), font-bold
- **Títulos H2**: 24px (text-2xl), font-bold
- **Títulos H3**: 20px (text-xl), font-bold
- **Body**: 14px (text-sm), font-medium
- **Small**: 12px (text-xs), font-medium

## Componentes

### Botões

#### Botão Primário (Accent)
- Background: Verde Accent
- Texto: Branco
- Hover: Verde mais escuro
- Uso: Ações principais (Criar, Salvar, Confirmar)

#### Botão Secundário (Preto)
- Background: Preto
- Texto: Branco
- Hover: Cinza escuro
- Uso: Ações importantes mas não primárias

#### Botão Outline
- Border: Cinza
- Texto: Cinza escuro
- Hover: Background cinza claro
- Uso: Ações terciárias, filtros

### Cards

#### Estrutura
- Border: 1px solid cinza claro
- Border Radius: 8px (rounded-lg)
- Hover: Border preta
- Transition: suave (200ms)

#### Seções do Card
1. **Header** (branco)
   - Badge de status
   - Título em preto bold
   - Subtítulo em cinza

2. **Body** (cinza claro)
   - Informações secundárias
   - Grid de dados
   - Botão de ação

### Badges de Status

- **Aberto**: Verde accent com background verde claro
- **Em Andamento**: Cinza com background cinza claro
- **Finalizado**: Preto com texto branco
- **Cancelado**: Outline cinza

### Inputs

- Border: Cinza claro
- Focus: Ring preto (2px)
- Border Radius: 8px
- Padding: 12px 16px

## Layout

### Header
- Background: Branco
- Border bottom: Cinza claro
- Height: 73px
- Fixed top

### Sidebar
- Background: Branco
- Border right: Cinza claro
- Width: 256px (64rem)
- Item ativo: Background preto, texto branco

### Main Content
- Background: Branco
- Padding: 32px
- Max-width: 1280px (7xl)

## Princípios de Design

1. **Minimalismo**: Apenas elementos essenciais
2. **Contraste**: Preto e branco para hierarquia clara
3. **Destaque Sutil**: Verde apenas para ações importantes
4. **Espaçamento Generoso**: Respiração entre elementos
5. **Tipografia Clara**: Fonte única com pesos variados
6. **Formas Simples**: Bordas arredondadas sutis (8px)
7. **Transições Suaves**: Feedback visual imediato

## Grid System

- **Desktop**: 3 colunas
- **Tablet**: 2 colunas
- **Mobile**: 1 coluna
- Gap: 24px (gap-6)

## Estados Interativos

### Hover
- Cards: Border preta
- Botões: Escurecimento
- Links: Background cinza claro

### Focus
- Inputs: Ring preto 2px
- Elementos navegáveis: Outline visível

### Active
- Sidebar: Background preto, texto branco
- Filtros: Background preto, texto branco

## Iconografia

**Lucide Icons**
- Estilo: Stroke (outline)
- Tamanho padrão: 20px (w-5 h-5)
- Cor: Herda do contexto
- Stroke width: 2

## Responsividade

### Breakpoints
- **sm**: 640px
- **md**: 768px
- **lg**: 1024px
- **xl**: 1280px

### Comportamento Mobile
- Sidebar: Colapsável
- Grid: 1 coluna
- Search: Oculto, expandível
- Espaçamentos reduzidos
