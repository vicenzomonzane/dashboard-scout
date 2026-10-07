import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------------------------
# CONFIGURAÇÃO DE CORES
# -------------------------------------------------------------------
COR_PRINCIPAL = "#6f42c1" # Novo tom de Roxo
COR_SECUNDARIA = "lightgray"

st.set_page_config(page_title="Insight Analysis | Scout", layout="wide")

@st.cache_data
def carregar_dados():
    # Lê o ficheiro completo
    df = pd.read_excel("Player stats A. González (4).xlsx")
    
    # Mapeamento COMPLETO
    df = df.rename(columns={
        "Minutos jogados:": "Minutos",
        "Ações totais/bem sucedidos": "Ações Totais",
        "Unnamed: 6": "Ações Bem Sucedidas",
        "Remates/à baliza": "Remates",
        "Unnamed: 10": "Remates à Baliza",
        "Passes/certos": "Passes",
        "Unnamed: 13": "Passes Certos",
        "Passes longos/certos": "Passes Longos",
        "Unnamed: 15": "Passes Longos Certos",
        "Cruzamentos/certos": "Cruzamentos",
        "Unnamed: 17": "Cruzamentos Certos",
        "Dribbles/com sucesso": "Dribles",
        "Unnamed: 19": "Dribles com Sucesso",
        "Duelos/ganhos": "Duelos",
        "Unnamed: 21": "Duelos Ganhos",
        "Duelos aéreos/ganhos": "Duelos Aéreos",
        "Unnamed: 23": "Duelos Aéreos Ganhos",
        "Perdas/no seu meio-campo": "Perdas de Bola",
        "Unnamed: 26": "Perdas (Meio-Campo Próprio)",
        "Recuperações/no meio-campo do adversário": "Recuperações",
        "Unnamed: 28": "Recuperações (Meio-Campo Adv)"
    })
    
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by="Date")
    return df

dados = carregar_dados()

# -------------------------------------------------------------------
# MENU LATERAL
# -------------------------------------------------------------------
try:
    st.sidebar.image("logo.png", width=180)
except:
    try:
        st.sidebar.image("logo.jpg", width=180)
    except:
        st.sidebar.markdown("*(Adicione o arquivo logo.png na Mesa)*")
        
st.sidebar.title("Insight Analysis")
st.sidebar.divider()

competicoes = ["Todas"] + list(dados["Competition"].dropna().unique())
comp_selecionada = st.sidebar.selectbox("Filtro de Competição:", competicoes)

if comp_selecionada != "Todas":
    dados = dados[dados["Competition"] == comp_selecionada]

# -------------------------------------------------------------------
# CABEÇALHO
# -------------------------------------------------------------------
col_foto, col_titulo = st.columns([1, 6])
with col_foto:
    try:
        st.image("foto_jogador.png", width=120)
    except:
        try:
            st.image("foto_jogador.jpg", width=120)
        except:
            st.image("https://cdn.sofifa.net/players/232/656/24_120.png", width=120)

with col_titulo:
    st.title("A. González")
    st.markdown("**Posição:** Avançado Centro (CF) | **Análise de Desempenho e Scout**")

# Métricas Gerais
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Jogos Analisados", len(dados))
c2.metric("Minutos Jogados", dados["Minutos"].sum())
c3.metric("Golos", dados["Golos"].sum())
c4.metric("Assistências", dados["Assistências"].sum())
c5.metric("Total xG", round(dados["xG"].sum(), 2))

st.divider()

# -------------------------------------------------------------------
# SESSÕES (TABS)
# -------------------------------------------------------------------
aba1, aba2, aba3, aba4 = st.tabs(["🎯 Fase Ofensiva", "👟 Distribuição e Criação", "🛡️ Fase Defensiva", "📊 Base de Dados"])

# SESSÃO 1: OFENSIVA
with aba1:
    st.subheader("Análise de Finalização e Geração de Perigo")
    col1_aba1, col2_aba1 = st.columns(2)
    
    with col1_aba1:
        metricas_ofensivas = ["xG", "Remates", "Remates à Baliza", "Ações Totais"]
        metrica_ofensiva = st.selectbox("Selecione a métrica ofensiva:", metricas_ofensivas, key="ofensiva")
        
        fig_ofensiva = px.line(dados, x="Date", y=metrica_ofensiva, markers=True, hover_data=["Jogo"])
        fig_ofensiva.update_traces(line_color=COR_PRINCIPAL, marker=dict(size=6, color=COR_PRINCIPAL))
        st.plotly_chart(fig_ofensiva, use_container_width=True)
        
    with col2_aba1:
        fig_remates = go.Figure()
        fig_remates.add_trace(go.Bar(x=dados["Date"], y=dados["Remates"], name="Remates Totais", marker_color=COR_SECUNDARIA))
        fig_remates.add_trace(go.Bar(x=dados["Date"], y=dados["Remates à Baliza"], name="À Baliza", marker_color=COR_PRINCIPAL))
        fig_remates.update_layout(title="Volume de Remates", barmode='group', hovermode="x unified", margin=dict(t=30))
        st.plotly_chart(fig_remates, use_container_width=True)

# SESSÃO 2: DISTRIBUIÇÃO E CRIAÇÃO
with aba2:
    st.subheader("Análise de Passes, Cruzamentos e Dribles")
    metricas_distribuicao = ["Passes", "Passes Certos", "Passes Longos", "Passes Longos Certos", "Cruzamentos", "Dribles", "Dribles com Sucesso"]
    metrica_dist = st.selectbox("Selecione a métrica de construção:", metricas_distribuicao, key="distribuicao")
    
    fig_dist = px.bar(dados, x="Date", y=metrica_dist, hover_data=["Jogo"])
    fig_dist.update_traces(marker_color=COR_PRINCIPAL)
    st.plotly_chart(fig_dist, use_container_width=True)

# SESSÃO 3: DEFENSIVA
with aba3:
    st.subheader("Análise de Duelos, Perdas e Recuperações")
    metricas_defensivas = ["Duelos", "Duelos Ganhos", "Duelos Aéreos", "Duelos Aéreos Ganhos", "Perdas de Bola", "Recuperações", "Intercepções"]
    metrica_def = st.selectbox("Selecione a métrica defensiva:", metricas_defensivas, key="defensiva")
    
    fig_def = px.area(dados, x="Date", y=metrica_def, hover_data=["Jogo"])
    fig_def.update_traces(line_color=COR_PRINCIPAL, fillcolor=COR_PRINCIPAL)
    st.plotly_chart(fig_def, use_container_width=True)

# SESSÃO 4: TABELA COMPLETA
with aba4:
    st.subheader("Base de Dados Completa")
    st.markdown("Histórico detalhado de todos os 183 jogos. Role lateralmente para visualizar todas as métricas.")
    st.dataframe(
        dados.style.format({"Date": lambda x: x.strftime('%d/%m/%Y') if pd.notnull(x) else ""}), 
        use_container_width=True, 
        hide_index=True
    )