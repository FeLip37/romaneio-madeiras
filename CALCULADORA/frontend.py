import streamlit as st
import pandas as pd

st.set_page_config(page_title="Romaneio de Madeiras", layout="wide")

st.title("🪵 Sistema de Romaneio de Material Bruto MJ")

if 'lotes' not in st.session_state:
    st.session_state.lotes = []

# variavel nova para forçar o reset apenas das quantidades sem dar erro
if 'reset_contador' not in st.session_state:
    st.session_state.reset_contador = 0

comprimentos = [1.50, 2.00, 2.50, 3.00, 3.50, 4.00, 4.50, 5.00, 5.50, 6.00, 6.50, 7.00, 7.50, 8.00]

st.subheader("1. Adicionar Novo Lote")

# campo para o Tipo de Madeira
tipo_madeira = st.text_input("Tipo de Madeira (ex: Pinus, Eucalipto, Cambará, etc.)")

# organiza largura e espessura lado a lado
col1, col2 = st.columns(2)
with col1:
    largura = st.number_input("Largura (cm)", min_value=0.0, step=0.5, format="%.2f")
with col2:
    espessura = st.number_input("Espessura (cm)", min_value=0.0, step=0.5, format="%.2f")
    
st.write("**Quantidade de peças por comprimento:**")

# cria uma grade organizada com 7 colunas
colunas_grid = st.columns(7)
quantidades = {}

for i, comp in enumerate(comprimentos):
    with colunas_grid[i % 7]:
        # TRUQUE: O 'reset_contador' na chave cria campos "novos" zerados a cada adição
        quantidades[comp] = st.number_input(
            f"{comp:.2f}m", 
            min_value=0, 
            step=1, 
            key=f"comp_{comp}_{st.session_state.reset_contador}"
        )
        
# botao para calcular e adicionar à tabela
if st.button("➕ Adicionar ao Romaneio", use_container_width=True, type="primary"):
    if largura > 0 and espessura > 0:
        volume_lote = 0.0
        metragem_lote = 0.0
        pecas_detalhes = []
        
        for comp, qtd in quantidades.items():
            if qtd > 0:
                # volume (m³)
                vol_item = (largura / 100) * (espessura / 100) * comp * qtd
                volume_lote += vol_item
                
                # metragem Linear (m)
                metragem_lote += (comp * qtd)
                
                pecas_detalhes.append(f"{qtd}x de {comp:.2f}m")
        
        if volume_lote > 0:
            st.session_state.lotes.append({
                "Madeira": tipo_madeira if tipo_madeira else "Não especificada",
                "Largura (cm)": largura,
                "Espessura (cm)": espessura,
                "Detalhes das Peças": ", ".join(pecas_detalhes),
                "Metr. Linear (m)": round(metragem_lote, 2),
                "Volume (m³)": round(volume_lote, 4)
            })
            
            # atualiza o contador para recriar os campos de quantidade do zero
            st.session_state.reset_contador += 1
            
            st.success("Lote adicionado com sucesso!")
            st.rerun() # atualiza a página imediatamente
        else:
            st.warning("Adicione pelo menos uma peça para registrar o lote.")
    else:
        st.error("A largura e espessura devem ser maiores que zero.")

st.divider()

st.subheader("2. Resumo do Romaneio")

if st.session_state.lotes:
    df = pd.DataFrame(st.session_state.lotes)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # divide os resultados totais em duas colunas para ficar bonito
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        volume_total = df["Volume (m³)"].sum()
        st.metric(label="Volume Total Acumulado", value=f"{volume_total:.4f} m³")
    with res_col2:
        metragem_total = df["Metr. Linear (m)"].sum()
        st.metric(label="Metragem Linear Total", value=f"{metragem_total:.2f} m")
    
    if st.button("🗑️ Limpar Tudo"):
        # zera a tabela e o contador
        st.session_state.lotes = []
        st.session_state.reset_contador = 0
        st.rerun()
else:
    st.info("Nenhum lote adicionado ainda. Preencha os dados acima e clique em 'Adicionar ao Romaneio'.")