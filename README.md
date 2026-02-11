# EDA Automática - CNSESI

Sistema de Análise Exploratória de Dados Automática desenvolvido por Joana Sampaio.

## Funcionalidades

- Upload de múltiplos tipos de arquivo: CSV, Excel (.xlsx, .xls), TXT
- Análise automática de dados:
  - Contagem de linhas e colunas
  - Identificação de tipos de dados
  - Detecção de valores faltantes
  - Estatísticas descritivas
  - Visualizações com gráficos
- Geração de relatórios para download

## Como executar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o aplicativo:
```bash
streamlit run app.py
```

3. Acesse no navegador: http://localhost:8501

## Deploy na Web

Para fazer deploy do sistema na web, você pode usar:

### Streamlit Cloud
1. Faça upload do código para um repositório Git (GitHub, GitLab, etc.)
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte sua conta GitHub
4. Selecione o repositório e o arquivo `app.py`
5. Clique em "Deploy"

### Outras opções
- **Heroku**: Crie um arquivo `Procfile` e faça deploy
- **AWS**: Use EC2 ou Lambda
- **Google Cloud**: Use App Engine
- **Azure**: Use App Service

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- NumPy
- Plotly

## Desenvolvido por

Joana Sampaio - Análise Exploratória de Dados

