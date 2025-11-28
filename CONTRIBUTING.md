# Guia de Contribuição

Obrigado por considerar contribuir para a API Antecedentes Criminais! 🎉

## Como Contribuir

### 1. Fork e Clone

```bash
# Fork o repositório no GitHub e depois clone
git clone https://github.com/seu-usuario/api-atecedentescriminais.git
cd api-atecedentescriminais

# Adicione o repositório original como upstream
git remote add upstream https://github.com/Enio11/api-atecedentescriminais.git
```

### 2. Crie uma Branch

Sempre crie uma branch para suas mudanças:

```bash
git checkout -b tipo/descricao-curta
```

**Tipos de branches:**
- `feature/` - Nova funcionalidade
- `fix/` - Correção de bug
- `docs/` - Documentação
- `refactor/` - Refatoração de código
- `test/` - Adição/correção de testes
- `chore/` - Tarefas de manutenção

**Exemplos:**
- `feature/adicionar-endpoint-historico`
- `fix/corrigir-busca-cpf`
- `docs/melhorar-readme`

### 3. Padrão de Commits

Seguimos a convenção **Conventional Commits**:

```
<tipo>(<escopo>): <descrição curta>

<descrição detalhada (opcional)>

<footer (opcional)>
```

#### Tipos de Commit

- **feat**: Nova funcionalidade
- **fix**: Correção de bug
- **docs**: Mudanças na documentação
- **style**: Formatação, ponto e vírgula, etc (sem mudança de código)
- **refactor**: Refatoração de código
- **test**: Adição ou correção de testes
- **chore**: Tarefas de manutenção, atualização de dependências
- **perf**: Melhorias de performance
- **ci**: Mudanças em CI/CD

#### Exemplos de Commits

```bash
# Feature
git commit -m "feat(scraper): adicionar suporte para busca por nome"

# Bugfix
git commit -m "fix(api): corrigir validação de CPF inválido"

# Documentação
git commit -m "docs(readme): atualizar instruções de instalação"

# Refatoração
git commit -m "refactor(database): simplificar queries de consulta"

# Teste
git commit -m "test(api): adicionar testes para endpoint de histórico"

# Com descrição detalhada
git commit -m "feat(api): adicionar rate limiting

Implementa limitação de requisições para prevenir abuso:
- 100 requisições por minuto por IP
- Retorna erro 429 quando excedido
- Adiciona header X-RateLimit-Remaining"
```

### 4. Padrões de Código

#### Python Style Guide

Seguimos o **PEP 8** com algumas especificidades:

- **Indentação**: 4 espaços
- **Comprimento de linha**: máximo 100 caracteres
- **Imports**: agrupados e ordenados (stdlib, terceiros, locais)
- **Docstrings**: use docstrings para funções e classes

#### Exemplo de código bem formatado

```python
from typing import Optional, Dict, Any
import re
from datetime import datetime

from fastapi import HTTPException
from selenium import webdriver


class ConsultaCPF:
    """
    Classe para consulta de CPF no Portal da Transparência.
    
    Attributes:
        cpf (str): CPF a ser consultado
        timeout (int): Tempo máximo de espera em segundos
    """
    
    def __init__(self, cpf: str, timeout: int = 30):
        """
        Inicializa a consulta de CPF.
        
        Args:
            cpf: CPF no formato XXX.XXX.XXX-XX
            timeout: Tempo máximo de espera
            
        Raises:
            ValueError: Se o CPF for inválido
        """
        self.cpf = self._validar_cpf(cpf)
        self.timeout = timeout
    
    def _validar_cpf(self, cpf: str) -> str:
        """Valida formato do CPF."""
        pattern = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
        if not re.match(pattern, cpf):
            raise ValueError(f"CPF inválido: {cpf}")
        return cpf
    
    def consultar(self) -> Optional[Dict[str, Any]]:
        """
        Realiza a consulta do CPF.
        
        Returns:
            Dicionário com os dados encontrados ou None
        """
        # Implementação
        pass
```

#### Boas Práticas

✅ **FAÇA:**
- Use nomes descritivos para variáveis e funções
- Escreva docstrings para funções públicas
- Use type hints quando possível
- Mantenha funções pequenas e focadas
- Adicione comentários para lógica complexa
- Escreva testes para novas funcionalidades
- Trate exceções adequadamente

❌ **NÃO FAÇA:**
- Commits diretos na branch `main`
- Código sem testes
- Variáveis com nomes genéricos (x, data, temp)
- Funções com mais de 50 linhas
- Hardcode de credenciais ou dados sensíveis
- Alterar múltiplas funcionalidades em um único commit

### 5. Testes

Sempre adicione testes para novas funcionalidades:

```bash
# Execute os testes antes de commitar
pytest test_api.py -v

# Verifique a cobertura (se configurado)
pytest --cov=. --cov-report=html
```

### 6. Pull Request

Quando estiver pronto para submeter:

1. **Atualize sua branch com a main:**
```bash
git fetch upstream
git rebase upstream/main
```

2. **Push para seu fork:**
```bash
git push origin sua-branch
```

3. **Abra um Pull Request no GitHub**

**Template de PR:**

```markdown
## Descrição
Descrição clara do que foi alterado e por quê.

## Tipo de Mudança
- [ ] Bug fix (mudança que corrige um problema)
- [ ] Nova feature (mudança que adiciona funcionalidade)
- [ ] Breaking change (mudança que quebra compatibilidade)
- [ ] Documentação

## Como Testar
Passos para testar as mudanças:
1. ...
2. ...

## Checklist
- [ ] Meu código segue o style guide do projeto
- [ ] Revisei meu próprio código
- [ ] Comentei código complexo
- [ ] Atualizei a documentação
- [ ] Minhas mudanças não geram novos warnings
- [ ] Adicionei testes que provam que minha correção/feature funciona
- [ ] Todos os testes passam localmente
```

### 7. Code Review

- Seja respeitoso e construtivo nos comentários
- Responda a todos os comentários de revisão
- Faça as alterações solicitadas em novos commits
- Marque conversas como resolvidas quando aplicável

## Reportar Bugs

Use as [GitHub Issues](https://github.com/Enio11/api-atecedentescriminais/issues) para reportar bugs.

**Template de Bug Report:**

```markdown
**Descrição do Bug**
Descrição clara do problema.

**Como Reproduzir**
1. ...
2. ...

**Comportamento Esperado**
O que deveria acontecer.

**Screenshots**
Se aplicável.

**Ambiente:**
- OS: [ex: macOS, Windows, Linux]
- Python: [ex: 3.9]
- Versão: [ex: 1.0.0]
```

## Sugerir Melhorias

Sugestões são bem-vindas! Abra uma issue com:
- Descrição clara da melhoria
- Por que seria útil
- Possível implementação (se tiver ideias)

## Dúvidas?

Abra uma [Discussion](https://github.com/Enio11/api-atecedentescriminais/discussions) ou entre em contato.

---

**Obrigado por contribuir! 🚀**
