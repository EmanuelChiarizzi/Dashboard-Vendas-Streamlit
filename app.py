import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Executivo", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    # Tenta converter colunas que parecem data
    for col in df.columns:
        if 'date' in col.lower():
            df[col] = pd.to_datetime(df[col])
    return df

try:
    df = load_data()

    # --- AJUSTE AUTOMÁTICO DE COLUNAS ---
    # Vamos separar o que é texto (categoria) do que é número (vendas)
    colunas_texto = df.select_dtypes(include=['object']).columns.tolist()
    colunas_numero = df.select_dtypes(include=['number']).columns.tolist()

    if not colunas_texto or not colunas_numero:
        st.error("O arquivo precisa ter pelo menos uma coluna de texto e uma de número.")
    else:
        col_cat = colunas_texto[0]  # Pega a primeira coluna de texto (ex: Produto)
        col_val = colunas_numero[0] # Pega a primeira coluna de número (ex: Vendas)

        # --- SIDEBAR ---
        st.sidebar.header("🔍 Filtros")
        filtro_cat = st.sidebar.multiselect(
            f"Filtrar por {col_cat}:",
            options=df[col_cat].unique(),
            default=df[col_cat].unique()
        )
        df_filtrado = df[df[col_cat].isin(filtro_cat)]

        # --- DASHBOARD ---
        st.title("📊 Dashboard Executivo de Vendas")
        st.markdown("---")

        m1, m2, m3 = st.columns(3)
        total_vendas = df_filtrado[col_val].sum()
        media_vendas = df_filtrado[col_val].mean()

        m1.metric("Faturamento Total", f"R$ {total_vendas:,.2f}")
        m2.metric("Ticket Médio", f"R$ {media_vendas:,.2f}")
        m3.metric("Qtd Registros", len(df_filtrado))

        st.markdown("---")
        col_esq, col_dir = st.columns(2)

        fig_bar = px.bar(df_filtrado, x=col_cat, y=col_val, title=f"Vendas por {col_cat}", color=col_cat)
        col_esq.plotly_chart(fig_bar, use_container_width=True)

        fig_pie = px.pie(df_filtrado, values=col_val, names=col_cat, title="Distribuição %", hole=0.4)
        col_dir.plotly_chart(fig_pie, use_container_width=True)

        with st.expander("Ver base de dados"):
            st.dataframe(df_filtrado)

except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")