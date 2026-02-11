import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="EDA Automática - CNSESI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 EDA Automática - CNSESI")
st.markdown("**Sistema Completo de Análise Exploratória de Dados**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("ℹ️ Sobre")
    st.info("Sistema avançado de Análise Exploratória de Dados Automática")
    st.markdown("---")
    st.markdown("**Desenvolvido por:** Joana Sampaio")
    st.markdown("**Versão:** 2.0")
    st.markdown("---")
    st.subheader("📋 Funcionalidades:")
    st.markdown("""
    - ✅ Suporte a múltiplos formatos
    - ✅ Análise estatística completa
    - ✅ Visualizações avançadas
    - ✅ Detecção de outliers
    - ✅ Análise de correlação
    - ✅ Geração de relatórios
    """)

# Upload de arquivo
st.header("📁 Carregar Dados")
uploaded_file = st.file_uploader(
    "Selecione um arquivo (CSV, Excel, TXT, etc.)", 
    type=['csv', 'xlsx', 'xls', 'txt']
)

def read_file_with_encoding(uploaded_file, file_extension):
    """Tenta ler arquivo com diferentes encodings"""
    try:
        if file_extension in ['xlsx', 'xls']:
            try:
                import openpyxl
            except ImportError:
                st.error("❌ Biblioteca openpyxl não disponível. Instalando...")
                import subprocess
                subprocess.check_call(['pip', 'install', 'openpyxl'])
                import openpyxl
            
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            return df
            
        elif file_extension == 'csv':
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'utf-16']
            for encoding in encodings:
                try:
                    df = pd.read_csv(uploaded_file, encoding=encoding)
                    return df
                except (UnicodeDecodeError, LookupError):
                    uploaded_file.seek(0)
                    continue
            return None
            
        elif file_extension == 'txt':
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'utf-16']
            for encoding in encodings:
                try:
                    df = pd.read_csv(uploaded_file, sep='\t', encoding=encoding)
                    return df
                except (UnicodeDecodeError, LookupError):
                    uploaded_file.seek(0)
                    continue
            return None
        else:
            return None
            
    except Exception as e:
        st.error(f"❌ Erro ao ler arquivo: {str(e)}")
        return None

if uploaded_file is not None:
    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        df = read_file_with_encoding(uploaded_file, file_extension)
        
        if df is None:
            st.error("❌ Não foi possível ler o arquivo. Tente outro formato ou encoding.")
        else:
            # ===== SEÇÃO 1: INFORMAÇÕES GERAIS =====
            st.header("📊 Informações Gerais")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            total_rows = len(df)
            total_cols = len(df.columns)
            missing_percent = (df.isnull().sum().sum() / (total_rows * total_cols)) * 100
            duplicates = df.duplicated().sum()
            memory_usage = df.memory_usage(deep=True).sum() / 1024**2
            
            with col1:
                st.metric("📈 Linhas", f"{total_rows:,}")
            with col2:
                st.metric("📋 Colunas", total_cols)
            with col3:
                st.metric("💾 Memória (MB)", f"{memory_usage:.2f}")
            with col4:
                st.metric("⚠️ Ausentes (%)", f"{missing_percent:.1f}%")
            with col5:
                st.metric("🔄 Duplicatas", duplicates)
            
            # ===== SEÇÃO 2: PREVIEW =====
            st.header("👀 Preview dos Dados")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Primeiras Linhas:**")
                st.dataframe(df.head(10), use_container_width=True)
            with col2:
                st.write("**Estatísticas Básicas:**")
                st.write(f"- Shape: {df.shape}")
                st.write(f"- Colunas: {', '.join(df.columns.tolist())}")
                st.write(f"- Índice: {df.index.name if df.index.name else 'Padrão'}")
            
            # ===== SEÇÃO 3: TIPOS DE DADOS =====
            st.header("🔍 Tipos de Dados")
            data_types_list = []
            for col in df.columns:
                dtype = df[col].dtype
                is_numeric = pd.api.types.is_numeric_dtype(df[col])
                unique = df[col].nunique()
                missing = df[col].isnull().sum()
                
                data_types_list.append({
                    "Coluna": col,
                    "Tipo": "Numérico" if is_numeric else "Texto",
                    "Python Type": str(dtype),
                    "Únicos": unique,
                    "Ausentes": missing,
                    "Preenchimento (%)": f"{((total_rows - missing) / total_rows * 100):.1f}%"
                })
            
            types_df = pd.DataFrame(data_types_list)
            st.dataframe(types_df, use_container_width=True)
            
            # ===== SEÇÃO 4: VALORES FALTANTES =====
            st.header("⚠️ Análise de Valores Faltantes")
            missing_data = []
            for col in df.columns:
                missing_count = df[col].isnull().sum()
                if missing_count > 0:
                    missing_pct = (missing_count / total_rows) * 100
                    missing_data.append({
                        "Coluna": col,
                        "Faltantes": missing_count,
                        "Percentual": f"{missing_pct:.2f}%"
                    })
            
            if missing_data:
                missing_df = pd.DataFrame(missing_data)
                st.dataframe(missing_df, use_container_width=True, hide_index=True)
                
                # Gráfico de valores faltantes
                fig_missing = go.Figure(data=[
                    go.Bar(y=[d["Coluna"] for d in missing_data], 
                           x=[d["Faltantes"] for d in missing_data],
                           orientation='h',
                           marker_color='#ef553b')
                ])
                fig_missing.update_layout(
                    title="Contagem de Valores Faltantes por Coluna",
                    xaxis_title="Quantidade Faltante",
                    yaxis_title="Coluna",
                    height=400
                )
                st.plotly_chart(fig_missing, use_container_width=True)
            else:
                st.success("✅ Sem valores faltantes!")
            
            # ===== SEÇÃO 5: DUPLICATAS =====
            st.header("🔄 Análise de Duplicatas")
            if duplicates > 0:
                st.warning(f"⚠️ Encontradas {duplicates} linhas duplicadas!")
                if st.checkbox("Mostrar linhas duplicadas"):
                    st.dataframe(df[df.duplicated(keep=False)].sort_values(by=list(df.columns)), use_container_width=True)
            else:
                st.success("✅ Sem linhas duplicadas!")
            
            # ===== SEÇÃO 6: COLUNAS NUMÉRICAS =====
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
            
            if len(numeric_columns) > 0:
                st.header("📈 Análise de Colunas Numéricas")
                
                # Estatísticas descritivas
                st.subheader("Estatísticas Descritivas")
                stats_df = df[numeric_columns].describe().round(4)
                st.dataframe(stats_df, use_container_width=True)
                
                # Distribuições
                st.subheader("📊 Distribuições")
                cols_per_row = 2
                for i in range(0, len(numeric_columns), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, col_idx in enumerate(range(i, min(i + cols_per_row, len(numeric_columns)))):
                        col = numeric_columns[col_idx]
                        with cols[j]:
                            fig = px.histogram(df, x=col, nbins=30, 
                                             title=f"Distribuição: {col}",
                                             marginal="box")
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True)
                
                # Box plots
                st.subheader("📦 Box Plots")
                cols_per_row = 2
                for i in range(0, len(numeric_columns), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, col_idx in enumerate(range(i, min(i + cols_per_row, len(numeric_columns)))):
                        col = numeric_columns[col_idx]
                        with cols[j]:
                            fig = go.Figure(data=[go.Box(y=df[col], name=col)])
                            fig.update_layout(title=f"Box Plot: {col}", height=400)
                            st.plotly_chart(fig, use_container_width=True)
                
                # Detecção de Outliers
                st.subheader("🎯 Detecção de Outliers (IQR)")
                outlier_info = []
                for col in numeric_columns:
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
                    
                    outlier_info.append({
                        "Coluna": col,
                        "Q1": f"{Q1:.4f}",
                        "Q3": f"{Q3:.4f}",
                        "IQR": f"{IQR:.4f}",
                        "Outliers": outliers,
                        "% Outliers": f"{(outliers/total_rows*100):.2f}%"
                    })
                
                st.dataframe(pd.DataFrame(outlier_info), use_container_width=True, hide_index=True)
                
                # Correlação
                if len(numeric_columns) > 1:
                    st.subheader("🔗 Matriz de Correlação")
                    corr_matrix = df[numeric_columns].corr()
                    fig_corr = px.imshow(corr_matrix, 
                                        color_continuous_scale="RdBu",
                                        zmin=-1, zmax=1,
                                        title="Matriz de Correlação",
                                        labels=dict(color="Correlação"))
                    st.plotly_chart(fig_corr, use_container_width=True)
                    
                    # Correlações mais fortes
                    st.subheader("Top Correlações")
                    corr_pairs = []
                    for i in range(len(corr_matrix.columns)):
                        for j in range(i+1, len(corr_matrix.columns)):
                            corr_pairs.append({
                                "Coluna 1": corr_matrix.columns[i],
                                "Coluna 2": corr_matrix.columns[j],
                                "Correlação": f"{corr_matrix.iloc[i, j]:.4f}"
                            })
                    
                    corr_df = pd.DataFrame(corr_pairs).sort_values(
                        by="Correlação", 
                        key=abs, 
                        ascending=False
                    ).head(10)
                    st.dataframe(corr_df, use_container_width=True, hide_index=True)
            
            # ===== SEÇÃO 7: COLUNAS CATEGÓRICAS =====
            if len(categorical_columns) > 0:
                st.header("📂 Análise de Colunas Categóricas")
                
                for col in categorical_columns[:5]:  # Limitar a 5 colunas
                    st.subheader(f"Coluna: {col}")
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        value_counts = df[col].value_counts().head(10)
                        fig = px.bar(value_counts, 
                                    title=f"Top 10 Valores: {col}",
                                    labels={"index": col, "value": "Contagem"})
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.write("**Resumo Estatístico:**")
                        st.write(f"- Total de valores únicos: {df[col].nunique()}")
                        st.write(f"- Valor mais comum: {df[col].mode()[0] if len(df[col].mode()) > 0 else 'N/A'}")
                        st.write(f"- Frequência do mais comum: {df[col].value_counts().iloc[0] if len(df[col].value_counts()) > 0 else 'N/A'}")
                        st.write(f"- Valores ausentes: {df[col].isnull().sum()}")
            
            # ===== SEÇÃO 8: RELATÓRIO PARA DOWNLOAD =====
            st.header("📄 Gerar Relatório")
            
            report_content = f"""
╔════════════════════════════════════════════════════════════════╗
║          RELATÓRIO DE ANÁLISE EXPLORATÓRIA DE DADOS            ║
║                  EDA Automática - CNSESI                       ║
╚════════════════════════════════════════════════════════════════╝

INFORMAÇÕES GERAIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Arquivo: {uploaded_file.name}
Data da Análise: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}
Analista: Joana Sampaio

DIMENSÕES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total de Linhas: {total_rows:,}
Total de Colunas: {total_cols}
Memória Utilizada: {memory_usage:.2f} MB
Linhas Duplicadas: {duplicates}
Percentual de Dados Faltantes: {missing_percent:.2f}%

TIPOS DE DADOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{types_df.to_string(index=False)}

VALORES FALTANTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{pd.DataFrame(missing_data).to_string(index=False) if missing_data else 'Nenhum valor faltante encontrado!'}

ESTATÍSTICAS DESCRITIVAS (COLUNAS NUMÉRICAS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{df[numeric_columns].describe().to_string() if numeric_columns else 'Sem colunas numéricas'}

COLUNAS CATEGÓRICAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            for col in categorical_columns[:5]:
                report_content += f"\n{col}:\n{df[col].value_counts().to_string()}\n"
            
            report_content += f"""

CONCLUSÕES E RECOMENDAÇÕES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Análise concluída com sucesso
✓ Total de registros analisados: {total_rows:,}
✓ Total de variáveis: {total_cols}
"""
            
            if missing_percent > 10:
                report_content += "\n⚠️ ATENÇÃO: Percentual elevado de dados faltantes (>10%)"
            
            if duplicates > 0:
                report_content += f"\n⚠️ ATENÇÃO: {duplicates} linhas duplicadas encontradas"
            
            report_content += """

═══════════════════════════════════════════════════════════════════
Relatório gerado automaticamente pelo Sistema EDA Automática
© 2025 Joana Sampaio
═══════════════════════════════════════════════════════════════════
"""
            
            st.download_button(
                label="📥 Baixar Relatório Completo (TXT)",
                data=report_content,
                file_name=f"relatorio_eda_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
            
            # Exportar dados processados
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="💾 Exportar Dados em CSV",
                data=csv_data,
                file_name=f"dados_processados_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    except Exception as e:
        st.error(f"❌ Erro ao processar: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>© 2025 Joana Sampaio - EDA Automática CNSESI</strong></p>
    <p><small>Sistema de Análise Exploratória de Dados v2.0</small></p>
</div>
""", unsafe_allow_html=True)
