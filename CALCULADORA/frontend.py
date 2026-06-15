import streamlit as st
import pandas as pd
import os

# 1. Rastreador automático de arquivos
def encontrar_arquivo(nome_arquivo):
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    caminhos = [
        nome_arquivo, 
        os.path.join(dir_atual, nome_arquivo), 
        f"CALCULADORA/{nome_arquivo}"
    ]
    for caminho in caminhos:
        if os.path.exists(caminho):
            return caminho
    return None

# Procura os arquivos com os nomes exatos que você criou
caminho_logo = encontrar_arquivo("MJ_new_icon_png.png")
caminho_icone = encontrar_arquivo("MJ_new_icon.ico")

# 2. Configuração da Página usando o seu arquivo .ico
st.set_page_config(
    page_title="Romaneio MJ Madeiras", 
    page_icon=caminho_icone if caminho_icone else "🪵", 
    layout="wide"
)

# 3. CSS Global (Fonte moderna e limpa)
st.markdown("""
    <style>
    * {
        font-family: 'Arial', sans-serif !important;
    }
    .subtitulo-logo {
        font-size: 22px;
        font-weight: bold;
        color: #2E8B57;
        margin-top: -15px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Exibição do LOGÓTIPO (.png) e Subtítulo
if caminho_logo:
    st.image(caminho_logo, width=230)
    st.markdown('<p class="subtitulo-logo">Calculadora de Romaneio Bruto</p>', unsafe_allow_html=True)
else:
    st.error("⚠️ A logo 'MJ_new_icon_png.png' não foi encontrada no GitHub!")
    st.markdown('<p class="subtitulo-logo">Calculadora de Romaneio Bruto</p>', unsafe_allow_html=True)

st.divider()

# Inicialização da memória da sessão
if 'lotes' not in st.session_state:
    st.session_state.lotes = []

comprimentos = [1.50, 2.00, 2.50, 3.00, 3.50, 4.00, 4.50, 5.00, 5.50, 6.00, 6.50, 7.00, 7.50, 8.00]

# --- SEÇÃO 1: ENTRADA DE DADOS ---
st.subheader("1. Adicionar Novo Lote")

# Menu de Seleção de Madeiras
lista_madeiras = ["Pinus", "Eucalipto", "Cambará", "Cedro", "Angelim", "Cumaru", "Garapeira", "Roxinho", "Outra"]
tipo_selecionado = st.selectbox("Selecione o Tipo de Madeira", lista_madeiras)

if tipo_selecionado == "Outra":
    tipo_madeira = st.text_input("Digite o nome da madeira:")
else:
    tipo_madeira = tipo_selecionado

col1, col2 = st.columns(2)
with col1:
    largura = st.number_input("Largura (cm)", min_value=0.0, step=0.5, format="%.2f")
with col2:
    espessura = st.number_input("Espessura (cm)", min_value=0.0, step=0.5, format="%.2f")
    
st.write("**Quantidade de peças por comprimento:**")

# Formulário otimizado
with st.form("form_quantidades", clear_on_submit=True):
    colunas_grid = st.columns(7)
    quantidades = {}

    for i, comp in enumerate(comprimentos):
        with colunas_grid[i % 7]:
            quantidades[comp] = st.number_input(f"{comp:.2f}m", min_value=0, step=1)
            
    submeteu = st.form_submit_button("➕ Adicionar ao Romaneio", type="primary", use_container_width=True)
    
    if submeteu:
        if largura > 0 and espessura > 0:
            volume_lote = 0.0
            metragem_linear_lote = 0.0
            metragem_quadrada_lote = 0.0
            pecas_detalhes = []
            
            for comp, qtd in quantidades.items():
                if qtd > 0:
                    largura_m = largura / 100
                    espessura_m = espessura / 100
                    
                    vol_item = largura_m * espessura_m * comp * qtd
                    volume_lote += vol_item
                    
                    area_item = largura_m * comp * qtd
                    metragem_quadrada_lote += area_item
                    
                    metragem_linear_lote += (comp * qtd)
                    
                    pecas_detalhes.append(f"{qtd}x de {comp:.2f}m")
            
            if volume_lote > 0:
                st.session_state.lotes.append({
                    "Madeira": tipo_madeira if tipo_madeira else "Não especificada",
                    "Largura (cm)": largura,
                    "Espessura (cm)": espessura,
                    "Detalhes das Peças": ", ".join(pecas_detalhes),
                    "Metr. Linear (m)": round(metragem_linear_lote, 2),
                    "Metr. Quadrada (m²)": round(metragem_quadrada_lote, 2),
                    "Volume (m³)": round(volume_lote, 4)
                })
                st.success("Lote adicionado com sucesso!")
            else:
                st.warning("Adicione pelo menos uma peça para registrar o lote.")
        else:
            st.error("A largura e a espessura devem ser maiores que zero.")

st.divider()

# --- SEÇÃO 2: TABELA E RESUMO ---
st.subheader("2. Resumo do Romaneio")

if st.session_state.lotes:
    df = pd.DataFrame(st.session_state.lotes)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        st.metric(label="Volume Total Acumulado", value=f"{df['Volume (m³)'].sum():.4f} m³")
    with res_col2:
        st.metric(label="Metragem Linear Total", value=f"{df['Metr. Linear (m)'].sum():.2f} m")
    with res_col3:
        st.metric(label="Metragem Quadrada Total", value=f"{df['Metr. Quadrada (m²)'].sum():.2f} m²")
    
    if st.button("🗑️ Limpar Tudo"):
        st.session_state.lotes = []
        st.rerun()
else:
    st.info("Nenhum lote adicionado ainda.")