# Exemplos de Commits

Este documento fornece exemplos práticos de como escrever boas mensagens de commit seguindo a convenção Conventional Commits.

## 📝 Formato Básico

```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

## ✨ Features (feat)

```bash
# Simples
feat(api): adicionar endpoint de busca por nome

# Com descrição detalhada
feat(scraper): implementar retry automático em caso de timeout

Adiciona mecanismo de retry para melhorar confiabilidade:
- Máximo de 3 tentativas
- Delay exponencial entre tentativas
- Log de cada tentativa

# Com breaking change
feat(api)!: migrar autenticação para OAuth2

BREAKING CHANGE: A autenticação por API key foi removida.
Agora é necessário usar OAuth2 com tokens JWT.

Migração:
1. Obter credenciais OAuth2 no painel
2. Atualizar código para usar bearer token
3. Renovar token a cada 24h
```

## 🐛 Bugfixes (fix)

```bash
# Simples
fix(scraper): corrigir parsing de CPF com zeros à esquerda

# Com contexto
fix(database): prevenir duplicate key error em consultas simultâneas

Adiciona lock de transação para prevenir condição de corrida
quando múltiplas requisições tentam inserir o mesmo CPF.

Fixes #42

# Hotfix crítico
fix(api)!: corrigir vulnerabilidade de injeção SQL

CRITICAL: Esta correção resolve uma vulnerabilidade de segurança
que permitia injeção SQL no endpoint de consulta.

Todas as queries agora usam prepared statements.
```

## 📚 Documentação (docs)

```bash
# Simples
docs(readme): corrigir typo na seção de instalação

# Mais complexo
docs(contributing): adicionar guia de setup do ambiente local

Adiciona seção detalhada sobre:
- Instalação de dependências
- Configuração do ChromeDriver
- Variáveis de ambiente necessárias
- Troubleshooting comum
```

## 🎨 Estilo (style)

```bash
# Formatação
style(scraper): formatar código com black

# Linting
style: corrigir warnings do flake8

# Organização
style(imports): organizar imports seguindo PEP 8
```

## ♻️ Refatoração (refactor)

```bash
# Simples
refactor(database): simplificar query de histórico

# Com justificativa
refactor(scraper): extrair lógica de parsing para classe separada

Move a lógica de parsing de HTML para a classe HTMLParser
para melhorar testabilidade e reutilização.

# Performance
refactor(api): otimizar consulta de histórico

Reduz tempo de resposta de ~500ms para ~50ms usando:
- Index no campo timestamp
- Paginação com cursor em vez de offset
- Cache de 5 minutos para resultados
```

## 🧪 Testes (test)

```bash
# Adicionar testes
test(api): adicionar testes para endpoint de consulta

# Melhorar cobertura
test(scraper): aumentar cobertura de testes para 90%

# Corrigir testes
test(database): corrigir testes flaky de concorrência
```

## ⚡ Performance (perf)

```bash
# Otimização
perf(scraper): reduzir uso de memória em 40%

Implementa streaming de resultados em vez de carregar
tudo em memória, permitindo processar datasets maiores.

# Cache
perf(api): adicionar cache em memória para consultas frequentes

Adiciona Redis cache com TTL de 1 hora para CPFs consultados,
reduzindo carga no scraper em ~60%.
```

## 🔧 Manutenção (chore)

```bash
# Dependências
chore(deps): atualizar selenium para v4.15.0

# Build
chore: adicionar script de build para produção

# CI/CD
chore(ci): adicionar GitHub Actions para testes automáticos
```

## 🔨 Build (build)

```bash
# Docker
build: adicionar Dockerfile para containerização

# Scripts
build: adicionar script de deploy automático
```

## 👷 CI (ci)

```bash
# GitHub Actions
ci: adicionar workflow de testes no PR

# Deploy
ci: configurar deploy automático para staging
```

## 🎯 Múltiplas Mudanças

Quando um commit afeta múltiplas áreas, escolha o tipo mais significativo:

```bash
# Mesmo que afete scraper e api, a feature principal é na API
feat(api): adicionar endpoint de estatísticas

Adiciona novo endpoint GET /stats que retorna:
- Total de consultas
- Consultas por dia
- CPFs mais consultados

Também atualiza o scraper para coletar metadados adicionais
necessários para as estatísticas.
```

## ❌ Exemplos de MAUS Commits

Evite escrever commits assim:

```bash
# ❌ Muito vago
git commit -m "fix bug"
git commit -m "update code"
git commit -m "changes"

# ❌ Sem tipo
git commit -m "adicionar nova feature"

# ❌ Descrição muito longa na primeira linha
git commit -m "feat(api): adicionar novo endpoint de consulta que permite buscar por CPF e também por nome e retorna os dados em formato JSON"

# ❌ Múltiplas mudanças não relacionadas
git commit -m "feat: adicionar endpoint de stats, corrigir bug no scraper, atualizar readme"

# ❌ Não descritivo
git commit -m "feat: stuff"
git commit -m "fix: fix"
```

## ✅ Dicas de Ouro

1. **Primeira linha**: Máximo 72 caracteres
2. **Imperative mood**: "adicionar" não "adicionado" ou "adicionando"
3. **Sem ponto final**: Na primeira linha
4. **Commits pequenos**: Um commit = uma mudança lógica
5. **Seja específico**: Descreva O QUE e POR QUE, não COMO
6. **Referencie issues**: Use `Fixes #123` ou `Closes #456`
7. **Breaking changes**: Sempre documente com `BREAKING CHANGE:`

## 🔗 Referências de Issues

```bash
# Fecha uma issue
fix(api): corrigir validação de CPF

Fixes #23

# Relacionado mas não fecha
feat(api): adicionar paginação

Related to #15

# Múltiplas issues
fix(scraper): corrigir timeout e encoding

Fixes #12, #34, #56
```

## 📊 Resumo de Tipos

| Tipo | Quando Usar | Exemplo |
|------|-------------|---------|
| `feat` | Nova funcionalidade | Novo endpoint, nova feature |
| `fix` | Correção de bug | Corrigir erro, bug fix |
| `docs` | Documentação | README, comentários |
| `style` | Formatação | Linting, formatação |
| `refactor` | Refatoração | Melhorar código |
| `test` | Testes | Adicionar/corrigir testes |
| `perf` | Performance | Otimizações |
| `chore` | Manutenção | Deps, scripts |
| `build` | Build | Docker, scripts |
| `ci` | CI/CD | GitHub Actions, deploy |

---

💡 **Lembre-se**: Bons commits facilitam code review, debugging e manutenção do projeto!
