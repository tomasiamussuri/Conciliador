import pandas as pd
import streamlit as st
from file_handler import FileHandler
import base64

class UIComponents:
    @staticmethod
    def load_imagem_como_base64(caminho: str) -> str:
        """Carrega imagem e converte para base64, com tratamento de erro"""
        try:
            with open(caminho, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except FileNotFoundError:
            st.warning(f"Imagem não encontrada: {caminho}")
        except Exception as e:
            st.error(f"Erro ao carregar imagem: {e}")
        return ""

    @staticmethod
    def renderizar_cabecalho():
        """Renderiza o cabeçalho da aplicação"""
        st.markdown("""
        <style>
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)

        # Tenta carregar e exibir o logo, se disponível
        logo_base64 = UIComponents.load_imagem_como_base64("img/logo.png")
        if logo_base64:
            st.markdown(
                f"""
                <div class="centered">
                    <img src="data:image/png;base64,{logo_base64}" width="100">
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div class='centered'><h1>Conciliador de Bases</h1></div>", unsafe_allow_html=True)
        st.markdown("<div class='centered'><h2>Upload de Bases</h2></div>", unsafe_allow_html=True)

    @staticmethod
    def renderizar_resultados(correspondencias: pd.DataFrame, apenas_arquivo_A: pd.DataFrame, apenas_arquivo_B: pd.DataFrame):
        """Renderiza resultados da reconciliação"""
        st.subheader("Resultados da Reconciliação")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Registros Correspondentes", len(correspondencias))
        with col2:
            st.metric("Somente no Arquivo A", len(apenas_arquivo_A))
        with col3:
            st.metric("Somente no Arquivo B", len(apenas_arquivo_B))
        
        file_handler = FileHandler()
        
        tab1, tab2, tab3 = st.tabs(["Correspondências", "Somente no Arquivo A", "Somente no Arquivo B"])
        
        with tab1:
            st.dataframe(correspondencias)
            st.markdown(file_handler.criar_link_para_download(correspondencias, 
                "registros_correspondentes.xlsx"), unsafe_allow_html=True)
            
        with tab2:
            st.dataframe(apenas_arquivo_A)
            st.markdown(file_handler.criar_link_para_download(apenas_arquivo_A, 
                "somente_no_arquivo_a.xlsx"), unsafe_allow_html=True)
            
        with tab3:
            st.dataframe(apenas_arquivo_B)
            st.markdown(file_handler.criar_link_para_download(apenas_arquivo_B, 
                "somente_no_arquivo_b.xlsx"), unsafe_allow_html=True)
