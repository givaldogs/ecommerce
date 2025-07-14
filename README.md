echo "# Ecommerce Django

Projeto de ecommerce desenvolvido em Django.

## Requisitos

- Python 3.x  
- Django 5.2.3  
- Ambiente virtual (venv)  

## Como executar

1. Clone o repositório:

\`\`\`bash
git clone https://github.com/seuusuario/ecommerce.git
\`\`\`

2. Entre na pasta do projeto:

\`\`\`bash
cd ecommerce
\`\`\`

3. Ative o ambiente virtual:

No Windows:

\`\`\`bash
venv\Scripts\activate
\`\`\`

No Linux/Mac:

\`\`\`bash
source venv/bin/activate
\`\`\`

4. Instale as dependências:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

5. Rode as migrações do banco:

\`\`\`bash
python manage.py migrate
\`\`\`

6. Inicie o servidor:

\`\`\`bash
python manage.py runserver
\`\`\`

7. Acesse em \`http://localhost:8000\` no navegador.

## Tecnologias utilizadas

- Django  
- Python  
- SQLite (padrão)  

## Autor

Gival
" > README.md
✅ 1. Fixtures
Fixtures são arquivos (geralmente JSON ou YAML) com dados que podem ser 
carregados no banco.

Exemplo de fixture JSON (produto/fixtures/produtos_iniciais.json):
Crie uma pasta chamada fixtures dentro do app produto, e adicione 
um arquivo .json:

[
  {
    "model": "produto.produto",
    "pk": 1,
    "fields": {
      "nome": "Camiseta Básica",
      "descricao_curta": "Camiseta de algodão básica",
      "descricao_longa": "Camiseta confortável feita 100% de algodão.",
      "slug": "camiseta-basica",
      "preco_marketing": "59.90",
      "preco_marketing_promocional": "49.90",
      "tipo": "V"
    }
  },
  {
    "model": "produto.variacao",
    "pk": 1,
    "fields": {
      "produto": 1,
      "nome": "Tamanho M",
      "preco": "59.90",
      "estoque": 10
    }
  }
]
# Para carregar no banco:
python manage.py loaddata produtos_iniciais.json

# ========================================

✅ 2. Comando personalizado
Ideal para lógicas mais complexas, como gerar dados aleatórios com o Faker.

Etapas:
Crie um diretório chamado management/commands dentro do app (ex: pedido ou
ou produto):

produto/
  management/
    commands/
      __init__.py
      popula_dados.py

# ----------
Código exemplo (popula_dados.py):
# ---------------------------

from django.core.management.base import BaseCommand
from produto.models import Produto, Variacao
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Popula o banco com produtos e variações'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')
        for _ in range(10):
            produto = Produto.objects.create(
                nome=fake.word().capitalize(),
                descricao_curta=fake.sentence(),
                descricao_longa=fake.text(),
                slug=fake.slug(),
                preco_marketing=round(random.uniform(50, 200), 2),
                preco_marketing_promocional=round(random.uniform(30, 100), 2),
                tipo='V'
            )
            for _ in range(3):
                Variacao.objects.create(
                    produto=produto,
                    nome=f"Tamanho {random.choice(['P', 'M', 'G', 'GG'])}",
                    preco=produto.preco_marketing,
                    estoque=random.randint(1, 20)
                )
        self.stdout.write(self.style.SUCCESS(
            'Produtos e variações criados com sucesso!'))
# ------------
Para rodar:
# --------------
python manage.py popula_dados
# -------------------
Ótimo! Vamos ver as duas opções que você mencionou: **fixtures** e 
   **comandos personalizados**. Ambos são ótimos para popular seu 
   banco de dados, mas servem para casos diferentes.

---

## ✅ **1. Fixtures**

Fixtures são arquivos (geralmente JSON ou YAML) com dados que podem ser 
 carregados no banco.

### Exemplo de fixture JSON (produto/fixtures/produtos\_iniciais.json):

Crie uma pasta chamada `fixtures` dentro do app `produto`, e adicione 
 um arquivo `.json`:

```json
[
  {
    "model": "produto.produto",
    "pk": 1,
    "fields": {
      "nome": "Camiseta Básica",
      "descricao_curta": "Camiseta de algodão básica",
      "descricao_longa": "Camiseta confortável feita 100% de algodão.",
      "slug": "camiseta-basica",
      "preco_marketing": "59.90",
      "preco_marketing_promocional": "49.90",
      "tipo": "V"
    }
  },
  {
    "model": "produto.variacao",
    "pk": 1,
    "fields": {
      "produto": 1,
      "nome": "Tamanho M",
      "preco": "59.90",
      "estoque": 10
    }
  }
]
```

### Para carregar no banco:

```bash
python manage.py loaddata produtos_iniciais.json
```

---

## ✅ **2. Comando personalizado**

Ideal para lógicas mais complexas, como gerar dados aleatórios com o `Faker`.

### Etapas:

1. Crie um diretório chamado `management/commands` dentro do app (ex: `pedido`
    ou `produto`):

```
produto/
  management/
    commands/
      __init__.py
      popula_dados.py
```

2. Código exemplo (`popula_dados.py`):

```python
from django.core.management.base import BaseCommand
from produto.models import Produto, Variacao
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Popula o banco com produtos e variações'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')
        for _ in range(10):
            produto = Produto.objects.create(
                nome=fake.word().capitalize(),
                descricao_curta=fake.sentence(),
                descricao_longa=fake.text(),
                slug=fake.slug(),
                preco_marketing=round(random.uniform(50, 200), 2),
                preco_marketing_promocional=round(random.uniform(30, 100), 2),
                tipo='V'
            )
            for _ in range(3):
                Variacao.objects.create(
                    produto=produto,
                    nome=f"Tamanho {random.choice(['P', 'M', 'G', 'GG'])}",
                    preco=produto.preco_marketing,
                    estoque=random.randint(1, 20)
                )
        self.stdout.write(self.style.SUCCESS(
            'Produtos e variações criados com sucesso!'))
```

### Para rodar:

```bash
python manage.py popula_dados
```

---

## Qual usar?

* Use **fixtures** quando quiser dados estáticos e previsíveis (como em testes).
* Use **comandos personalizados** quando quiser gerar dados variados ou 
      automatizar processos.

Quer que eu gere um fixture real com base no seu modelo, ou criamos um comando
   juntos com base nos campos que você tem?
=====================================================
# Nao entendi esse comando , verificar
email = 'teste@email.com'

if re.fullmatch(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
    print('E-mail válido')
else:
    print('E-mail inválido')
# ==============================

🧠 Conceito:
site para aprender mais: https://regex101.com/
youtube curso regex https://www.youtube.com/watch?v=d2uqo6PhdM4
Expressões Regulares são padrões que descrevem conjuntos de strings. Você usa para buscar, substituir ou validar dados com precisão.

🛠 Principais símbolos:
| Símbolo  | Significado                     | Exemplo                    |
| -------- | ------------------------------- | -------------------------- |
| `.`      | Qualquer caractere (menos `\n`) | `a.b` casa "acb", "arb"    |
| `\d`     | Dígito (`0-9`)                  | `\d+` casa "123", "9"      |
| `\w`     | Letra, número ou `_`            | `\w+` casa "abc", "a1\_b"  |
| `\s`     | Qualquer espaço                 | `\s+` casa espaço ou tab   |
| `^`      | Início da string                | `^abc` casa "abc123"       |
| `$`      | Fim da string                   | `123$` casa "abc123"       |
| `[...]`  | Um dos caracteres               | `[abc]` casa "a", "b", "c" |
| `[^...]` | Qualquer caractere exceto       | `[^0-9]` → não-número      |
| `*`      | 0 ou mais                       | `a*` casa "", "a", "aaa"   |
| `+`      | 1 ou mais                       | `a+` casa "a", "aaa"       |
| `?`      | 0 ou 1                          | `a?` casa "", "a"          |
| `{n}`    | Exatamente n vezes              | `\d{3}` casa "123"         |
| -------- | ------------------------------- | -------------------------- |









