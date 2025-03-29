# 🚀 Análise de Sentimentos com Language Studio no Azure AI & Sistema de IA para Análise de Imagens

## 📌 Conteúdo da Aula (Azure AI)
- 🔍 **Análise de texto e resposta a perguntas** – Uso de IA para entender e responder perguntas com base em texto.
- 🤖 **Serviço de Bot do Azure** – Como criar e integrar chatbots inteligentes.
- 🗣️ **Compreensão da linguagem coloquial** – Técnicas para processar e interpretar linguagem natural.
- 🎙️ **Conhecendo o Studio de Fala** – Uso do Azure Speech Studio para reconhecimento e síntese de fala.
- 📌 **Conhecendo o Language Studio** – Ferramentas do Azure AI para processamento de linguagem natural (NLP).
- 🎯 **Entendendo o Desafio** – Aplicação prática dos conceitos abordados.

### Links Úteis (Azure AI)
- [Azure Language Studio](https://portal.azure.com/)
- [Azure Speech Studio](https://speech.microsoft.com/)
- [Documentação Oficial do Azure AI](https://learn.microsoft.com/en-us/azure/cognitive-services/)

💡 **Objetivo**: Aprender a usar os serviços de IA do Azure para **análise de sentimentos, chatbot e processamento**.

---

## Sistema de IA para Análise de Imagens

### 📋 Visão Geral

Esta aplicação é um sistema de análise e processamento de imagens alimentado por IA, que automatiza a interpretação de conteúdo visual. Ela combina capacidades de processamento em lote com uma interface de chat interativa, aproveitando o Gemini AI do Google para gerar análises detalhadas de imagens.

### ✨ Principais Características

#### 🖼️ Processamento de Imagens em Lote
- Analisa automaticamente imagens armazenadas em uma pasta de ativos (assets)
- Gera resumos detalhados para cada imagem usando o Gemini AI
- Organiza as imagens processadas movendo-as para uma pasta dedicada

#### 📄 Documentação Automática
- Cria documentos estruturados (Word e Markdown) com os resultados da análise
- Mantém um registro organizado de todas as imagens processadas
- Incorpora imagens em relatórios Markdown para fácil visualização

#### 💬 Interface de Chat Interativa
- Permite conversas em tempo real com a IA
- Suporta upload de imagens via navegador de arquivos ou área de transferência
- Permite perguntas específicas sobre as imagens carregadas

### 🛠️ Problemas Resolvidos

#### 🤖 Automação da Análise Visual
- Elimina a necessidade de análise manual de grandes volumes de imagens
- Padroniza a extração de informações visuais

#### ⏱️ Controle da Taxa de Requisições
- Implementa limitação de taxa para evitar sobrecarga da API
- Gerencia eficientemente filas de processamento

#### 📊 Documentação Consistente
- Gera automaticamente relatórios estruturados sem intervenção manual
- Mantém o histórico de todas as análises realizadas

#### 🔍 Acessibilidade da IA para Análise Visual
- Democratiza o acesso à análise de imagens por IA através de uma interface amigável
- Permite interações naturais com o modelo de IA via chat

### 🚀 Casos de Uso Potenciais
- Análise de imagens médicas ou científicas
- Catalogação e descrição automatizada de coleções visuais
- Inspeção visual automatizada para controle de qualidade
- Assistente de análise para profissionais que trabalham com conteúdo visual
- Ferramenta educacional para explicar conteúdo visual

### 💡 Abordagem
A aplicação combina análise sistemática em lote com uma interface interativa para consultas ad-hoc, oferecendo flexibilidade para diferentes necessidades de análise visual com IA.

### 🔧 Stack Tecnológico
- **Backend**: Python com rate limiting e capacidades de logging
- **Integração de IA**: Modelo Google Gemini AI para processamento de imagem e texto
- **Documentação**: Geração automatizada de relatórios Word e Markdown
- **Frontend**: Interface de chat interativa baseada em Streamlit
- **Manipulação de Imagens**: Suporte para diversos formatos de imagem e integração com a área de transferência

---

### Documentação do Assistente Visual Inteligente com Gemini AI

### 1. Visão Geral
O Assistente Visual Inteligente é uma aplicação Python que combina processamento de imagens e interação conversacional, utilizando o modelo Gemini AI da Google. A aplicação possui dois modos principais:

*   **Processamento em Lote:** Analisa automaticamente todas as imagens em uma pasta, gera resumos e cria documentação em formatos Word e Markdown.
*   **Interface Conversacional:** Permite que os usuários façam upload de imagens, colem da área de transferência e interajam com a IA através de uma interface de chat.

### 2. Funcionalidades
*   **Análise de Imagens:** Processa imagens usando o Gemini AI para extrair informações e gerar resumos.
*   **Geração de Documentação:** Cria automaticamente documentos Word e Markdown com os resumos das análises.
*   **Interface Conversacional:** Interface de chat estilo ChatGPT com suporte a imagens.
*   **Captura da Área de Transferência:** Permite colar imagens diretamente da área de transferência.
*   **Controle de Taxa:** Gerencia requisições à API do Gemini para evitar limites de taxa.
*   **Logging Detalhado:** Registra todas as operações para facilitar o diagnóstico de problemas.
*   **Prompts Dinâmicos:** Carrega prompts de arquivos externos para fácil personalização.

### 3. Arquitetura
A aplicação segue uma arquitetura modular com os seguintes componentes:

*   **Core:** Componentes fundamentais como configuração, logging e controle de taxa.
*   **Services:** Serviços para interação com a API do Gemini, geração de documentos e Markdown.
*   **Handlers:** Gerenciadores para processamento de imagens e interação com o modelo Gemini.
*   **Interface:** Interface de usuário construída com Streamlit.

### 4. Requisitos
*   Python 3.8+
*   Conta Google com acesso à API Gemini
*   Chave de API do Gemini

### 5. Instalação
1.  Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/assistente-visual-inteligente.git
    cd assistente-visual-inteligente
    ```

2.  Crie um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

### 6. Configuração
1.  Crie um arquivo `.env` na raiz do projeto com sua chave de API:
    ```plaintext
    API_KEY_GEMINI=sua_chave_api_aqui
    ```

2.  Crie as pastas necessárias:
    ```bash
    mkdir -p assets processed_images logs
    ```

3.  Configure os prompts:
    *   Crie um arquivo `prompt_doc.txt` em `src/prompt/` para o processamento de imagens.
    *   Crie um arquivo `prompt_chat.txt` em `src/prompt/` para a interface de chat.

### 7. Uso

#### 7.1. Processamento em Lote
1.  Coloque as imagens que deseja analisar na pasta `assets/`.

2.  Execute o processador de imagens:
    ```bash
    python src/main.py
    ```

3.  Os resultados serão salvos em:
    *   `resumo_analises_imagens.docx` (documento Word)
    *   `resumo_analises_imagens.md` (documento Markdown)

4.  As imagens processadas serão movidas para `processed_images/`.

#### 7.2. Interface Conversacional
1.  Inicie a aplicação Streamlit:
    ```bash
    streamlit run src/app.py
    ```

2.  Acesse a interface no navegador (geralmente em `http://localhost:8501`).

3.  Você pode:
    *   Digitar mensagens no campo de chat.
    *   Fazer upload de imagens usando o botão de upload.
    *   Colar imagens da área de transferência usando o botão "Colar".
    *   Limpar a conversa usando o botão "Limpar conversa".

### 8. Estrutura do Projeto
```plaintext
assistente-visual-inteligente/
├── assets/                  # Pasta para imagens a serem processadas
├── processed_images/        # Pasta para imagens já processadas
├── logs/                    # Logs da aplicação
├── src/
│   ├── core/
│   │   ├── config.py        # Configurações globais
│   │   ├── logger_config.py # Configuração de logging
│   │   ├── rate_limiter.py  # Controle de taxa para API
│   │   └── signal_handler.py # Manipulador de sinais
│   ├── handlers/
│   │   └── gemini_handler.py # Manipulador para o modelo Gemini
│   ├── prompt/
│   │   ├── prompt_doc.txt   # Prompt para processamento de documentos
│   │   └── prompt_chat.txt  # Prompt para interface de chat
│   ├── services/
│   │   ├── document_service.py # Serviço para geração de documentos Word
│   │   ├── gpt_services.py     # Serviço para interação com Gemini AI
│   │   └── markdown_service.py # Serviço para geração de Markdown
│   ├── utils/
│   │   └── file_utils.py    # Utilitários para manipulação de arquivos
│   ├── app.py               # Aplicação Streamlit
│   ├── image_processor.py   # Processador de imagens em lote
│   └── main.py              # Ponto de entrada principal
├── .env                     # Variáveis de ambiente (não versionado)
├── requirements.txt         # Dependências do projeto
└── README.md                # Este arquivo