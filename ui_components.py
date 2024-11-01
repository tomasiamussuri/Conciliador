import pandas as pd
import streamlit as st
from file_handler import FileHandler

class UIComponents:
    @staticmethod
    def render_header():
        """Render application header"""
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
        
        # Carrega e exibe uma imagem no centro do cabeçalho
        st.markdown(
            """
            <div class="centered">
                <img src="data:image/png;base64,{}" width="100">
            </div>
            """.format(UIComponents.load_image_as_base64("img/logo.png")),
            unsafe_allow_html=True
        )
        
        st.markdown("<div class='centered'><h1>Conciliador de Bases</h1></div>", unsafe_allow_html=True)
        st.markdown("<div class='centered'><h2>Upload de Bases</h2></div>", unsafe_allow_html=True)

    @staticmethod
    def load_image_as_base64(path):
        """Converte a imagem para base64 para garantir o carregamento no Streamlit"""
        import base64
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    @staticmethod
    def render_results(matches: pd.DataFrame, only_blue: pd.DataFrame, only_gama: pd.DataFrame):
        """Render reconciliation results"""
        st.subheader("Reconciliation Results")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Matching Records", len(matches))
        with col2:
            st.metric("Only in Blue", len(only_blue))
        with col3:
            st.metric("Only in Gama", len(only_gama))
        
        file_handler = FileHandler()
        
        tab1, tab2, tab3 = st.tabs(["Matches", "Only in Blue", "Only in Gama"])
        
        with tab1:
            st.dataframe(matches)
            st.markdown(file_handler.create_download_link(matches, 
                "matching_records.xlsx"), unsafe_allow_html=True)
            
        with tab2:
            st.dataframe(only_blue)
            st.markdown(file_handler.create_download_link(only_blue, 
                "only_in_blue.xlsx"), unsafe_allow_html=True)
            
        with tab3:
            st.dataframe(only_gama)
            st.markdown(file_handler.create_download_link(only_gama, 
                "only_in_gama.xlsx"), unsafe_allow_html=True)
