# importação de bibliotecas

import streamlit as st
import pandas as pd

# configuração da página

st.set_page_config(
    page_title="Catálogo de Sites e Ferramentas",
    page_icon="🔎",
    layout="wide"
)

# estilos

st.markdown("""
<style>

/* página */
.block-container {
    padding-top: 5rem;
}

/* selectbox */
div[data-baseweb="select"] {
    font-size: 18px;
}

div[data-baseweb="select"] * {
    text-align: center;
}

/* reduz espaços verticais */
[data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}

</style>
""", unsafe_allow_html=True)

# carregamento da planilha Google

@st.cache_data(ttl=300)
def carregar_dados():

    url = (
        "https://docs.google.com/spreadsheets/d/"
        "1k3NlSSkAoPs3u7gW4hRZAXTUggEYQcPeK1dsOdzUJNQ"
        "/export?format=xlsx"
    )

    return pd.read_excel(url)

df = carregar_dados()

# título

st.markdown("""
<h1 style="
    text-align:center;
    color:#102A4D;
    margin-bottom:10px;">
    🔎 Catálogo de Sites e Ferramentas
</h1>
""", unsafe_allow_html=True)

# apresentação

st.markdown("""
<div style="
    font-size:17px;
    line-height:1.3;">

<p><strong>Bem-vindo(a) ao Catálogo de Sites e Ferramentas da Equipe Técnica TRIEduc!</strong></p>

<p>
Este espaço reúne recursos que podem auxiliar na elaboração de itens,
incluindo bancos de imagens, obras em domínio público, mapas, gráficos,
simuladores e ferramentas de criação e edição.
</p>

<p>
Nossa base está em constante crescimento, por isso, novos recursos serão
adicionados à medida que forem identificados e avaliados pela equipe.
</p>

</div>
""", unsafe_allow_html=True)

# vamos começar

st.markdown("""
<div style="
    text-align:center;
    font-size:30px;
    font-weight:700;
    color:#102A4D;
    margin-top:5px;
    margin-bottom:0px;">
    Vamos começar?
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    text-align:center;
    font-size:18px;
    margin-bottom:10px;">
    Selecione a categoria do que está procurando
</div>
""", unsafe_allow_html=True)

# selectbox

col1, col2, col3 = st.columns([3, 1.8, 3])

with col2:
    categoria = st.selectbox(
        "",
        sorted(df["Categoria"].dropna().unique()),
        label_visibility="collapsed"
    )

# filtro

resultado = df[df["Categoria"] == categoria]

# contador

st.caption(f"{len(resultado)} recurso(s) encontrado(s)")

# cards

for _, linha in resultado.iterrows():

    with st.container(border=True):

        st.markdown(
            f"""
            <div style="
                font-size:22px;
                font-weight:600;
                margin-bottom:10px;">
                {linha["Nome do site"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="
                font-size:15px;
                margin-bottom:10px;
                line-height:1.4;">
                {linha["Descrição"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(f"Licença: {linha['Licença']}")

        st.write("")

        c1, c2, c3 = st.columns([2, 1.2, 2])

        with c2:
            st.link_button(
                "🌐 Acessar recurso",
                linha["URL"],
                use_container_width=True
            )

        st.write("")