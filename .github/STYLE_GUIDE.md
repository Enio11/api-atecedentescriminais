# Style Guide - Python

Guia de estilo de código para o projeto API Antecedentes Criminais.

## 📋 Visão Geral

Este projeto segue o **PEP 8** como base, com algumas adaptações e extensões.

## 🎨 Formatação

### Indentação

- Use **4 espaços** (nunca tabs)
- Continue linhas longas com 4 espaços extras

```python
# ✅ BOM
def funcao_com_muitos_parametros(
    parametro1: str,
    parametro2: int,
    parametro3: bool = False
) -> Dict[str, Any]:
    pass

# ❌ RUIM
def funcao_com_muitos_parametros(parametro1: str,
  parametro2: int, parametro3: bool = False) -> Dict[str, Any]:
    pass
```

### Comprimento de Linha

- **Máximo 100 caracteres** (não 79 como PEP 8 padrão)
- Para strings longas, use concatenação ou f-strings multi-linha

```python
# ✅ BOM
mensagem_erro = (
    f"CPF {cpf} não encontrado no sistema. "
    f"Verifique se o formato está correto (XXX.XXX.XXX-XX)"
)

# ✅ BOM - fstring multi-linha
query = f"""
    SELECT * FROM consultas
    WHERE cpf = '{cpf}'
    AND data >= '{data_inicio}'
    ORDER BY data DESC
"""

# ❌ RUIM - linha muito longa
mensagem_erro = f"CPF {cpf} não encontrado no sistema. Verifique se o formato está correto (XXX.XXX.XXX-XX) e tente novamente."
```

### Linhas em Branco

- **2 linhas** entre definições de classe e funções top-level
- **1 linha** entre métodos de uma classe
- **1 linha** para separar grupos lógicos de código

```python
# ✅ BOM
import os
from typing import Optional


class ConsultaCPF:
    """Classe para consulta de CPF."""
    
    def __init__(self, cpf: str):
        self.cpf = cpf
    
    def validar(self) -> bool:
        """Valida o CPF."""
        return True


class OutraClasse:
    """Outra classe."""
    pass


def funcao_top_level():
    """Função top-level."""
    pass
```

## 📦 Imports

### Ordem dos Imports

1. Standard library
2. Bibliotecas de terceiros
3. Imports locais

Cada grupo separado por uma linha em branco.

```python
# ✅ BOM
# Standard library
import os
import sys
from datetime import datetime
from typing import Optional, Dict, Any

# Terceiros
from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.common.by import By

# Locais
from database import Database
from scraper import Scraper
```

### Imports Absolutos vs Relativos

- Prefira **imports absolutos**
- Imports relativos só para estruturas complexas

```python
# ✅ BOM
from database import Database
from scraper.cpf_scraper import CPFScraper

# ⚠️ OK, mas evite quando possível
from .database import Database
from ..utils.validators import validar_cpf
```

## 🏷️ Nomenclatura

### Variáveis e Funções

- Use **snake_case**
- Nomes descritivos e significativos

```python
# ✅ BOM
nome_completo = "João Silva"
cpf_consultado = "123.456.789-00"

def buscar_por_cpf(cpf: str) -> Optional[dict]:
    """Busca dados por CPF."""
    pass

# ❌ RUIM
nomeCompleto = "João Silva"  # camelCase
nc = "João Silva"  # muito curto
cpf_que_foi_consultado_no_sistema = "123.456.789-00"  # muito longo

def bpc(c):  # nomes não descritivos
    pass
```

### Classes

- Use **PascalCase**
- Substantivos descritivos

```python
# ✅ BOM
class ConsultaCPF:
    pass

class PortalTransparenciaScaper:
    pass

class DatabaseManager:
    pass

# ❌ RUIM
class consultacpf:  # snake_case
    pass

class Consultar:  # verbo em vez de substantivo
    pass
```

### Constantes

- Use **UPPER_SNAKE_CASE**
- Defina no topo do módulo

```python
# ✅ BOM
MAX_TENTATIVAS = 3
TIMEOUT_PADRAO = 30
URL_BASE = "https://portaldatransparencia.gov.br"

# Constantes complexas
HEADERS_PADRAO = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html"
}
```

### Métodos Privados

- Use **underscore** prefix para métodos privados
- Duplo underscore para name mangling (raro)

```python
class Scraper:
    def buscar(self, cpf: str):
        """Método público."""
        return self._processar_resultado(cpf)
    
    def _processar_resultado(self, cpf: str):
        """Método privado - uso interno."""
        pass
    
    def __inicializar_driver(self):
        """Método com name mangling - muito privado."""
        pass
```

## 📝 Type Hints

Use type hints sempre que possível:

```python
# ✅ BOM
from typing import Optional, Dict, List, Any

def consultar_cpf(cpf: str, timeout: int = 30) -> Optional[Dict[str, Any]]:
    """Consulta CPF com timeout."""
    pass

def processar_resultados(resultados: List[Dict[str, str]]) -> List[str]:
    """Processa lista de resultados."""
    return [r["nome"] for r in resultados]

# Para tipos complexos
from typing import TypedDict

class ResultadoConsulta(TypedDict):
    nome: str
    cpf: str
    data: str

def buscar(cpf: str) -> ResultadoConsulta:
    pass
```

## 📚 Docstrings

Use docstrings estilo Google:

```python
def consultar_cpf(cpf: str, timeout: int = 30) -> Optional[Dict[str, Any]]:
    """
    Consulta informações de um CPF no Portal da Transparência.
    
    Esta função realiza web scraping do portal para obter informações
    relacionadas ao CPF fornecido.
    
    Args:
        cpf: CPF no formato XXX.XXX.XXX-XX
        timeout: Tempo máximo de espera em segundos (padrão: 30)
    
    Returns:
        Dicionário com as informações encontradas ou None se não encontrado.
        Exemplo:
        {
            "nome": "João Silva",
            "cpf": "123.456.789-00",
            "data_consulta": "2024-01-01"
        }
    
    Raises:
        ValueError: Se o CPF estiver em formato inválido
        TimeoutError: Se a consulta exceder o timeout
    
    Example:
        >>> resultado = consultar_cpf("123.456.789-00")
        >>> print(resultado["nome"])
        João Silva
    """
    pass
```

## ⚠️ Tratamento de Erros

### Exceções Específicas

```python
# ✅ BOM
try:
    resultado = consultar_cpf(cpf)
except ValueError as e:
    logger.error(f"CPF inválido: {e}")
    raise HTTPException(status_code=400, detail=str(e))
except TimeoutError:
    logger.warning(f"Timeout na consulta do CPF {cpf}")
    raise HTTPException(status_code=504, detail="Timeout na consulta")

# ❌ RUIM
try:
    resultado = consultar_cpf(cpf)
except Exception as e:  # Muito genérico
    print(f"Erro: {e}")  # Usar logger, não print
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

# ✅ BOM
logger.info(f"Iniciando consulta para CPF: {cpf}")
logger.warning(f"Tentativa {tentativa} falhou, retrying...")
logger.error(f"Erro ao processar CPF {cpf}: {erro}")
logger.debug(f"Response HTML: {html[:100]}...")

# ❌ RUIM
print(f"Processando {cpf}")  # Usar logger
```

## 🎯 Boas Práticas

### Funções Pequenas

```python
# ✅ BOM - funções focadas
def validar_cpf(cpf: str) -> bool:
    """Valida formato do CPF."""
    pattern = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
    return bool(re.match(pattern, cpf))

def formatar_cpf(cpf: str) -> str:
    """Formata CPF para XXX.XXX.XXX-XX."""
    numeros = re.sub(r'\D', '', cpf)
    return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"

# ❌ RUIM - função faz muitas coisas
def processar_cpf(cpf):
    # valida
    # formata
    # consulta
    # salva
    # envia email
    # ...
    pass  # Muito código aqui
```

### List Comprehensions

```python
# ✅ BOM - simples e legível
cpfs_validos = [cpf for cpf in cpfs if validar_cpf(cpf)]

# ✅ BOM - complexo mas ainda legível
resultados = [
    {"cpf": cpf, "nome": buscar_nome(cpf)}
    for cpf in cpfs
    if validar_cpf(cpf)
]

# ❌ RUIM - muito complexo
dados = [
    x.upper() if len(x) > 5 else x.lower()
    for sublist in lista
    for x in sublist
    if x and not x.startswith('_')
]
# Melhor usar loop for normal
```

### Context Managers

```python
# ✅ BOM
with open('arquivo.txt', 'r') as f:
    conteudo = f.read()

# Para recursos customizados
from contextlib import contextmanager

@contextmanager
def driver_context():
    driver = webdriver.Chrome()
    try:
        yield driver
    finally:
        driver.quit()

with driver_context() as driver:
    driver.get(url)
```

### F-Strings

```python
# ✅ BOM
nome = "João"
idade = 30
mensagem = f"Olá, {nome}! Você tem {idade} anos."

# Com formatação
valor = 1234.56
print(f"Valor: R$ {valor:.2f}")

# ❌ RUIM - string concatenation
mensagem = "Olá, " + nome + "! Você tem " + str(idade) + " anos."

# ❌ RUIM - % formatting (obsoleto)
mensagem = "Olá, %s! Você tem %d anos." % (nome, idade)
```

## 🧪 Testes

### Nomenclatura de Testes

```python
# ✅ BOM
def test_validar_cpf_com_formato_correto():
    """Testa validação de CPF com formato correto."""
    assert validar_cpf("123.456.789-00") is True

def test_validar_cpf_com_formato_incorreto():
    """Testa validação de CPF com formato incorreto."""
    assert validar_cpf("123456789") is False

def test_consultar_cpf_inexistente_retorna_none():
    """Testa que CPF inexistente retorna None."""
    assert consultar_cpf("000.000.000-00") is None
```

### Estrutura de Testes (AAA)

```python
def test_salvar_consulta_no_banco():
    """Testa salvamento de consulta no banco."""
    # Arrange (preparar)
    db = Database(":memory:")
    cpf = "123.456.789-00"
    dados = {"nome": "João Silva", "cpf": cpf}
    
    # Act (executar)
    db.salvar_consulta(cpf, dados)
    
    # Assert (verificar)
    resultado = db.buscar_consulta(cpf)
    assert resultado["nome"] == "João Silva"
```

## 🚫 Code Smells a Evitar

```python
# ❌ Magic Numbers
if status_code == 200:  # O que é 200?
    pass

# ✅ Use constantes
HTTP_OK = 200
if status_code == HTTP_OK:
    pass

# ❌ Código comentado
# def funcao_antiga():
#     pass

# ✅ Delete código não usado (Git guarda histórico)

# ❌ Comentários óbvios
x = x + 1  # incrementa x

# ✅ Comentários úteis
x = x + 1  # Ajuste para indexação 1-based do banco

# ❌ Variáveis desnecessárias
temp = calcular_total()
return temp

# ✅ Retorne direto
return calcular_total()
```

## 🔍 Ferramentas Recomendadas

```bash
# Formatação automática
pip install black
black .

# Linting
pip install flake8
flake8 . --max-line-length=100

# Type checking
pip install mypy
mypy .

# Import sorting
pip install isort
isort .
```

## 📄 Configuração (.flake8)

```ini
[flake8]
max-line-length = 100
extend-ignore = E203, W503
exclude = .git,__pycache__,venv,.env
```

## 📄 Configuração (pyproject.toml)

```toml
[tool.black]
line-length = 100
target-version = ['py39']

[tool.isort]
profile = "black"
line_length = 100
```

---

**Lembre-se**: Código é lido muito mais vezes do que é escrito. Priorize legibilidade! 📖
