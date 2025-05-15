# 🛠️ Automação de Edição de Produtos com Selenium

Este projeto automatiza o processo de login e edição de produtos (SKUs) em uma plataforma web utilizando **Selenium** e **Python**, com base em uma lista de códigos de produtos lida de uma planilha Excel.

## 🚀 Funcionalidades

- Login automático no sistema via Selenium.
- Leitura de códigos de produto a partir de um arquivo `.xlsx`.
- Navegação até o menu de produtos.
- Busca por produtos e verificação de condições específicas (ex: quantidade = 0 e tipo = "Sku").
- Edição automática de produtos: exclusão de endereço, alteração para "Kit virtual - Kit" e salvamento.
- Logs detalhados de execução e erros.
- Armazenamento de falhas em `erro.html` para análise posterior.

## 📁 Estrutura Esperada

```
.
├── main.py              # Script principal de automação
├── .env                 # Variáveis de ambiente sensíveis
├── app.log              # Log de execução
├── errors.log           # Log de erros
├── erro.html            # Dump da página em caso de erro
├── requirements.txt     # Dependências Python
└── produtos.xlsx        # Planilha com os códigos dos produtos
```

## 📦 Requisitos

- Python 3.10 (ou compatível)
- Google Chrome
- Chromedriver instalado (e caminho configurado corretamente no script)
- Biblioteca Selenium
- Biblioteca Pandas
- Biblioteca `python-dotenv`

## 🔧 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure seu arquivo `.env` com as seguintes variáveis:

```dotenv
SITE=https://seusite.com/login
USUARIO=seu@email.com
SENHA=sua_senha
PLANILHA=/caminho/absoluto/para/produtos.xlsx
```

## ▶️ Como executar

```bash
python main.py
```

> O script abrirá o navegador, fará login, processará os produtos e gravará logs durante todo o processo.

## 📝 Notas

- O script depende fortemente de elementos específicos da estrutura HTML do site. Caso o layout da página mude, o código pode precisar ser ajustado.
- Logs de execução ficam registrados em `app.log`, e falhas críticas em `errors.log`.

## 🛡️ Segurança

- O `.env` **não deve ser versionado** (adicione no `.gitignore`) pois contém dados sensíveis como usuário e senha.

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).