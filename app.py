import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

st.set_page_config(
    page_title="EDA Automática - CNSESI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 EDA Automática - CNSESI")
st.markdown("**Análise Exploratória de Dados**")

# Sidebar com informações
st.sidebar.header("Sobre")
st.sidebar.info("Sistema de Análise Exploratória de Dados Automática")
st.sidebar.markdown("---")
st.sidebar.markdown("**Desenvolvido por:** Joana Sampaio")

# Upload de arquivo
st.header("📁 Carregar Dados")
uploaded_file = st.file_uploader("Selecione um arquivo (CSV, Excel, PDF, Word, JPG, etc.)", type=['csv', 'xlsx', 'xls', 'pdf', 'docx', 'doc', 'jpg', 'jpeg', 'png', 'gif', 'txt'])

if uploaded_file is not None:
    try:
        # Determinar o tipo de arquivo e ler adequadamente
        file_extension = uploaded_file.name.split('.')[-1].lower()

        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        elif file_extension == 'txt':
            df = pd.read_csv(uploaded_file, sep='\t')
        else:
            # Para outros tipos de arquivo, mostrar informações básicas
            st.info(f"Arquivo {uploaded_file.name} carregado. Tipo: {file_extension}")
            st.write(f"Tamanho: {uploaded_file.size} bytes")
            df = None

        if df is not None:
            # Análise básica
            total_rows = len(df)
            total_columns = len(df.columns)

            # Exibir informações gerais
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Linhas", total_rows)
            with col2:
                st.metric("Total de Colunas", total_columns)
            with col3:
                st.metric("Arquivo", uploaded_file.name)

            # Preview dos dados
            st.header("👀 Preview dos Dados")
            st.dataframe(df.head(), use_container_width=True)

            # Análise de tipos de dados
            st.header("🔍 Tipos de Dados")
            data_types = []
            for col in df.columns:
                dtype = "Numérico" if pd.api.types.is_numeric_dtype(df[col]) else "Texto"
                unique_values = df[col].nunique()
                data_types.append({
                    "Coluna": col,
                    "Tipo": dtype,
                    "Valores Únicos": unique_values
                })

            types_df = pd.DataFrame(data_types)
            st.dataframe(types_df, use_container_width=True)

            # Valores faltantes
            st.header("⚠️ Valores Faltantes")
            missing_data = []
            for col in df.columns:
                missing_count = df[col].isnull().sum()
                missing_percentage = (missing_count / total_rows) * 100
                missing_data.append({
                    "Coluna": col,
                    "Valores Faltantes": missing_count,
                    "Percentual": f"{missing_percentage:.1f}%"
                })

            missing_df = pd.DataFrame(missing_data)
            st.dataframe(missing_df, use_container_width=True)

            # Estatísticas descritivas para colunas numéricas
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            if len(numeric_columns) > 0:
                st.header("📈 Estatísticas Descritivas")
                st.dataframe(df[numeric_columns].describe(), use_container_width=True)

                # Gráficos para colunas numéricas
                st.header("📊 Visualizações")

                # Histogramas
                for col in numeric_columns[:3]:  # Limitar a 3 colunas para não sobrecarregar
                    fig = px.histogram(df, x=col, title=f"Distribuição de {col}")
                    st.plotly_chart(fig, use_container_width=True)

            # Relatório para download
            st.header("📄 Relatório Completo")

            report = f"""
RELATÓRIO DE ANÁLISE EXPLORATÓRIA DE DADOS
Sistema: EDA Automática - CNSESI
Analista: Joana Sampaio
Data: {pd.Timestamp.now().strftime('%d/%m/%Y')}

========================================
INFORMAÇÕES GERAIS
========================================
Arquivo: {uploaded_file.name}
Total de Linhas: {total_rows}
Total de Colunas: {total_columns}

========================================
TIPOS DE DADOS
========================================
{types_df.to_string(index=False)}

========================================
VALORES FALTANTES
========================================
{missing_df.to_string(index=False)}

========================================
ESTATÍSTICAS DESCRITIVAS
========================================
{df[numeric_columns].describe().to_string() if len(numeric_columns) > 0 else "Nenhuma coluna numérica encontrada"}
            """

            st.download_button(
                label="📥 Baixar Relatório Completo",
                data=report,
                file_name=f"relatorio_eda_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**© 2025 Joana Sampaio - Análise Exploratória de Dados**")
