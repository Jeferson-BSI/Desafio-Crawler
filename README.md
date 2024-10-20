<div align="center">

![Python Badge](https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=white) ![Playwright Badge](https://img.shields.io/badge/Playwright-000000?style=for-the-badge&logo=microsoft&logoColor=white) ![Git Badge](https://img.shields.io/badge/GIT-000000?style=for-the-badge&logo=git&logoColor=white) ![Github Badge](https://img.shields.io/badge/GitHub-000000?style=for-the-badge&logo=github&logoColor=white)

</div>
<!-- # Desafio React Native -->
<h2 align="center">
  Desafio Crawler
</2>

## Sobre o Projeto

O objetivo do projeto foi criar um script em Python utilizando Playwright para acessar o site do Tribunal de Justiça do Estado de Rondônia, navegar pelo calendário, buscar o PDF correspondente à data fornecida e, em seguida, calcular o hash MD5 do arquivo, e fazer o download do pdf renomeando com o hash MD5 correspondente. Essa aplicação garante que os diários sejam processados corretamente e evita duplicação no sistema.

---

## Dificuldades Encontradas

1. **Carregamento do calendário dinâmico**

   - O calendário não carregava automaticamente, exigindo navegação manual entre meses e anos.
   - **Solução**: Foi utilizado `Playwright` para clicar nos botões "próximo" e "anterior" e lidar com a navegação pelo calendário.

2. **Filtragem dos elementos HTML**

   - A dificuldade foi capturar apenas os botões com **os dois atributos**: `data-date` e `data-url`.
   - **Solução**: Foi utilizado o método `locator` com seletores CSS precisos para garantir que apenas os botões corretos fossem acessados.

3. **Baixar e validar PDFs**
   - Garantir que o PDF fosse baixado corretamente e o hash MD5 fosse gerado sem erros.

---

## Justificativas dos Métodos Utilizados

- **Playwright**:  
  Escolhido pela capacidade de lidar com páginas dinâmicas e interativas, è uma ótima escolha para scraping dinâmico em servidores, já que ele oferece suporte nativo para execução em modo headless e trabalha de forma mais eficiente com conteúdo dinâmico (JavaScript).

- **Requests**:  
  Utilizado para realizar o download dos PDFs via URL e garantir o stream dos dados.

- **Hash MD5**:  
  Escolhido para validar a integridade dos arquivos e evitar duplicidade de processamento.

- **Locale em Português (Brasil)**:  
  Necessário para interpretar corretamente os meses exibidos no calendário

## Explicação das Funções

#### **`handle_calendar_date(page: Page, publication_date: str)`**:

Navega pelo calendário da página para encontrar o mês e ano desejado.

- **Parâmetros:**

  - `page`: Instância da página do navegador aberta pelo Playwright.
  - `publication_date`: Data fornecida pelo usuário no formato `YYYY-MM-DD`.

- **Funcionamento:**
  - A função lê o título do calendário atual e compara com o mês e o ano desejados.
  - Caso necessário, clica nos botões "próximo" ou "anterior" até encontrar a data correta.

---

#### **`handle_pdf_url(page: Page, formatted_date: str)`**

Localiza o botão correspondente à data fornecida que contém o atributo `data-url` e retorna a URL do PDF.

- **Parâmetros:**

  - `page`: Instância da página do navegador aberta pelo Playwright.
  - `formatted_date`: Data formatada no formato esperado para a busca (`YYYY-M-D`).

- **Retorno:**
  - URL completa do PDF se encontrada, ou `None` caso contrário.

---

#### **`search_diaries(publication_date: str)`**

Essa função coordena o fluxo principal: acessa o site, navega até a data desejada no calendário e busca a URL do PDF correspondente.

- **Parâmetros:**

  - `publication_date`: Data fornecida pelo usuário no formato `YYYY-MM-DD`.

- **Retorno:**
  - URL do PDF se encontrado, ou `None` caso não haja um PDF disponível para a data.

---

#### **`download_pdf(response: requests.Response, output_folder: str, pdf_filename: str)`**

Faz o download do PDF a partir da resposta HTTP e salva o arquivo em disco.

- **Parâmetros:**

  - `response`: Resposta HTTP da requisição feita ao PDF.
  - `output_folder`: Pasta onde o PDF será salvo.
  - `pdf_filename`: Nome do arquivo PDF baseado no hash MD5.

- **Retorno:**
  - Caminho completo do arquivo salvo, ou `None` em caso de erro.

---

#### **`handle_hash_md5(pdf_url: str)`**

Gera o hash MD5 do conteúdo do PDF para garantir sua integridade e evita duplicações.

- **Parâmetros:**

  - `pdf_url`: URL do PDF a ser baixado e verificado.

- **Funcionamento:**

  - Faz a requisição para obter o conteúdo do PDF.
  - Gera o hash MD5 do conteúdo baixado.
  - Salva o PDF com o nome baseado no hash gerado.

- **Retorno:**
  - Hash MD5 do arquivo PDF.

---

## 🏃‍♂️Como rodar o projeto

## 📃 Requisitos

- **Git**;
- **Python**;
- **pip**;

- **Recomendado**: Ambiente virtual para isolamento das dependências

Realize um clone deste repositório em sua máquina local:

```bash
git clone https://github.com/Jeferson-BSI/Desafio-Crawler.git
```

Abra a pasta `Desafio-Crawler` presente no repositório:

```bash
cd Desafio-Crawler
```

**Criando o ambiente virtual**:

```bash
python3 -m venv venv
source venv/bin/activate
```

ou

**Para terminal fish Shell**

```bash
python3 -m venv venv
. ./venv/bin/activate.fish
```

---

**Instalando o Playwright**:

```bash
pip install playwright
playwright install
```

**Instale as dependências necessárias**:

```bash
pip install -r requirements.txt
```

## Como Executar

Execute o script no terminal, fornecendo a data desejada no formato YYYY-MM-DD:

```bash
python main.py "2024-10-04"
```

Exemplo de Saída:

```bash
PDF salvo em: pdf/259e1cb251c377da0a253d580461741d.pdf
Hash MD5 do diário: 259e1cb251c377da0a253d580461741d

```

---

## Fontes de Pesquisa Acessadas

- **Playwright**: [https://playwright.dev/python/docs/intro](https://playwright.dev/python/docs/intro)
- **Requests**: [https://docs.python-requests.org](https://docs.python-requests.org)
