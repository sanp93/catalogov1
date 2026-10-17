# importação de bibliotecas

import streamlit as st
import pandas as pd
import math

# configuração da página

st.set_page_config(
    page_title="Catálogo de Sites e Ferramentas",
    page_icon="🔎",
    layout="wide"
)

# estilos

st.markdown("""
<style>

/* cor de fundo da página (troque #FFFFFF pela cor que quiser) */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {
    background-color: #FFFFFF;
}

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

/* paginação: texto de resultados */
.pag-resultados {
    font-size: 16px;
    color: #333;
    text-align: right;
}

/* paginação: setas circulares */
.st-key-nav_prev button,
.st-key-nav_next button {
    width: 40px;
    height: 40px;
    min-height: 40px;
    padding: 0;
    border-radius: 50%;
    background: #102A4D;
    border: none;
}

.st-key-nav_prev button p,
.st-key-nav_next button p {
    color: #fff !important;
    font-size: 14px;
}

.st-key-nav_prev button:hover:not(:disabled),
.st-key-nav_next button:hover:not(:disabled) {
    background: #1B3F73;
}

.st-key-nav_prev button:disabled,
.st-key-nav_next button:disabled {
    background: #6C8EB5;
    opacity: 1;
}

/* paginação: números das páginas */
[class*="st-key-pg_"] button {
    width: 100%;
    min-height: auto;
    padding: 2px 0;
    background: transparent;
    border: none;
    border-bottom: 1px solid #C5CCD6;
    border-radius: 0;
}

[class*="st-key-pg_"] button p {
    color: #555;
    font-size: 17px;
}

[class*="st-key-pg_"] button[data-testid="stBaseButton-primary"] {
    border-bottom: 2px solid #102A4D;
}

[class*="st-key-pg_"] button[data-testid="stBaseButton-primary"] p {
    color: #102A4D;
    font-weight: 700;
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

<p><strong>Bem-vindo(a) ao Catálogo de Sites e Ferramentas!</strong></p>

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
        "Categoria",
        sorted(df["Categoria"].dropna().unique()),
        label_visibility="collapsed"
    )

# filtro

resultado = df[df["Categoria"] == categoria]

# controle de página (inicialização)

if "pagina" not in st.session_state:
    st.session_state.pagina = 1

# volta para página 1 ao trocar categoria

if "categoria_anterior" not in st.session_state:
    st.session_state.categoria_anterior = categoria

if st.session_state.categoria_anterior != categoria:
    st.session_state.pagina = 1
    st.session_state.categoria_anterior = categoria

# opções de visualização

modo = st.radio(
    "Modo de visualização",
    ["📋 Lista", "🗂️ Cards"],
    horizontal=True
)

# itens por página (o seletor aparece na paginação, abaixo dos resultados;
# aqui só lemos o valor guardado)

st.session_state.setdefault("itens_por_pagina", 10)
itens_por_pagina = st.session_state.itens_por_pagina

# cálculo do total de páginas

total_paginas = max(1, math.ceil(len(resultado) / itens_por_pagina))

if st.session_state.pagina > total_paginas:
    st.session_state.pagina = total_paginas

pagina = st.session_state.pagina

# recorte da página atual

inicio = (pagina - 1) * itens_por_pagina
fim = inicio + itens_por_pagina

resultado_pagina = resultado.iloc[inicio:fim]


def texto(valor):
    """Evita mostrar 'nan' quando a célula está vazia."""
    return "" if pd.isna(valor) else valor


def botao_link(linha):
    url = texto(linha["URL"])
    if url:
        st.link_button(
            "🌐 Acessar recurso",
            url,
            use_container_width=True
        )


# visualização em lista

if modo == "📋 Lista":

    for _, linha in resultado_pagina.iterrows():

        with st.container(border=True):

            st.markdown(
                f"""
                <div style="
                    font-size:22px;
                    font-weight:600;
                    margin-bottom:10px;">
                    {texto(linha["Nome do site"])}
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
                    {texto(linha["Descrição"])}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.caption(f"Licença: {texto(linha['Licença'])}")

            botao_link(linha)

# visualização em cards

else:

    col1, col2 = st.columns(2)

    for i, (_, linha) in enumerate(resultado_pagina.iterrows()):

        coluna = col1 if i % 2 == 0 else col2

        with coluna:

            with st.container(border=True):

                st.markdown(
                    f"""
                    <div style="
                        font-size:20px;
                        font-weight:600;
                        margin-bottom:10px;">
                        {texto(linha["Nome do site"])}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div style="
                        font-size:14px;
                        margin-bottom:10px;
                        line-height:1.4;">
                        {texto(linha["Descrição"])}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.caption(f"Licença: {texto(linha['Licença'])}")

                botao_link(linha)

# navegação de páginas

def ir_para(p):
    st.session_state.pagina = p


def resetar_pagina():
    st.session_state.pagina = 1


st.write("")
st.write("")

# janela com até 5 números de página visíveis
janela = 5
ini = max(1, pagina - janela // 2)
fim_j = min(total_paginas, ini + janela - 1)
ini = max(1, fim_j - janela + 1)
numeros = list(range(ini, fim_j + 1))

total = len(resultado)
rotulo = "resultado" if total == 1 else "resultados"

n = len(numeros)

cols = st.columns(
    [2, 1.6, 0.5, *[0.35] * n, 0.5, 2, 1.6],
    vertical_alignment="center"
)

# quantidade de resultados
with cols[1]:
    st.markdown(
        f'<div class="pag-resultados">{total} {rotulo}</div>',
        unsafe_allow_html=True
    )

# seta voltar
with cols[2]:
    st.button(
        "❮",
        key="nav_prev",
        disabled=pagina <= 1,
        on_click=ir_para,
        args=(pagina - 1,)
    )

# números das páginas
for col, num in zip(cols[3:3 + n], numeros):
    with col:
        st.button(
            str(num),
            key=f"pg_{num}",
            type="primary" if num == pagina else "secondary",
            on_click=ir_para,
            args=(num,)
        )

# seta avançar
with cols[3 + n]:
    st.button(
        "❯",
        key="nav_next",
        disabled=pagina >= total_paginas,
        on_click=ir_para,
        args=(pagina + 1,)
    )

# exibir por página
with cols[4 + n]:
    st.selectbox(
        "Exibir por página",
        [6, 10, 20, 50],
        key="itens_por_pagina",
        format_func=lambda x: f"{x} resultados",
        on_change=resetar_pagina
    )