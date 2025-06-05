import streamlit as st
from typing import List, Dict
from data_loader import DataLoader
from reconciliation_engine import ReconciliationEngine
from ui_components import UIComponents

class ReconciliadorApp:
    def __init__(self):
        self.data_loader = DataLoader()
        self.reconciliation_engine = ReconciliationEngine()
        self.ui = UIComponents()
        self.base_arquivo_A = None
        self.base_arquivo_B = None

    def executar(self):
        st.set_page_config(page_title="Conciliador de Bases", layout="wide")
        self.ui.renderizar_cabecalho()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Upload Base Arquivo A")
            arquivo_A = st.file_uploader(
                "Arraste e solte o arquivo aqui",
                type=["xlsx", "xls", "csv"],
                help="Limite de 200MB por arquivo • XLSX, XLS, CSV",
                key="arquivo_A_uploader"
            )

        with col2:
            st.subheader("Upload Base Arquivo B")
            arquivo_B = st.file_uploader(
                "Arraste e solte o arquivo aqui",
                type=["xlsx", "xls", "csv"],
                help="Limite de 200MB por arquivo • XLSX, XLS, CSV",
                key="arquivo_B_uploader"
            )

        if arquivo_A and arquivo_B:
            self.base_arquivo_A, erro_A = self.data_loader.carregar_e_preparar_dados(arquivo_A, "arquivo_a")
            self.base_arquivo_B, erro_B = self.data_loader.carregar_e_preparar_dados(arquivo_B, "arquivo_b")

            if erro_A:
                st.error(f"Erro ao carregar Arquivo A: {erro_A}")
            if erro_B:
                st.error(f"Erro ao carregar Arquivo B: {erro_B}")

            if self.base_arquivo_A is not None and self.base_arquivo_B is not None:
                st.success("Arquivos carregados com sucesso!")

                with st.expander("📊 Visualizar dados carregados"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.subheader("📄 Base A")
                        st.dataframe(self.base_arquivo_A)
                    with col_b:
                        st.subheader("📄 Base B")
                        st.dataframe(self.base_arquivo_B)

                st.subheader("⚙️ Definir regras de correspondência")
                colunas_a = self.base_arquivo_A.columns.tolist()
                colunas_b = self.base_arquivo_B.columns.tolist()

                colunas_selecionadas_a = st.multiselect(
                    "Selecione as colunas da Base A para a correspondência:",
                    colunas_a, key="colunas_a"
                )
                colunas_selecionadas_b = st.multiselect(
                    "Selecione as colunas da Base B para a correspondência:",
                    colunas_b, key="colunas_b"
                )

                nome_regra = st.text_input("Nome da regra (ex: CPF e NOME)")

                # Inicializa lista de regras se não existir
                if "regras" not in st.session_state:
                    st.session_state["regras"] = []

                # Botão para adicionar regra à lista
                if st.button("➕ Adicionar regra"):
                    if not colunas_selecionadas_a or not colunas_selecionadas_b:
                        st.warning("Você deve selecionar colunas nas duas bases.")
                    elif len(colunas_selecionadas_a) != len(colunas_selecionadas_b):
                        st.warning("As quantidades de colunas selecionadas nas duas bases devem ser iguais.")
                    else:
                        st.session_state["regras"].append({
                            "name": nome_regra or f"Regra {len(st.session_state['regras']) + 1}",
                            "arquivo_A_columns": colunas_selecionadas_a,
                            "arquivo_B_columns": colunas_selecionadas_b
                        })

                # Exibir as regras já adicionadas
                if st.session_state["regras"]:
                    st.markdown("📋 **Regras cadastradas:**")
                    for i, regra in enumerate(st.session_state["regras"], 1):
                        st.markdown(f"{i}. **{regra['name']}** → `{regra['arquivo_A_columns']}` ⇔ `{regra['arquivo_B_columns']}`")

                # Botão para executar a conciliação
                if st.button("🔍 Executar correspondência"):
                    # Normaliza os dados das colunas usadas nas regras
                    for regra in st.session_state["regras"]:
                        self.base_arquivo_A = self.data_loader.preprocessor.normalizar_colunas_para_conciliacao(self.base_arquivo_A, regra["arquivo_A_columns"])
                        self.base_arquivo_B = self.data_loader.preprocessor.normalizar_colunas_para_conciliacao(self.base_arquivo_B, regra["arquivo_B_columns"])

                    correspondencias, apenas_a, apenas_b = self.reconciliation_engine.aplicar_regras_de_correspondencia(
                        self.base_arquivo_A, self.base_arquivo_B, st.session_state["regras"]
                    )
                    self.ui.renderizar_resultados(correspondencias, apenas_a, apenas_b)

if __name__ == "__main__":
    app = ReconciliadorApp()
    app.executar()
