import streamlit as st
from typing import List, Dict
from data_loader import DataLoader
from reconciliation_engine import ReconciliationEngine
from ui_components import UIComponents

class ReconciliationApp:
    def __init__(self):
        self.data_loader = DataLoader()
        self.reconciliation_engine = ReconciliationEngine()
        self.ui = UIComponents()
        self.base_blue = None
        self.base_gama = None

    def run(self):
        st.set_page_config(page_title="Conciliador de Bases", layout="wide")
        
        self.ui.render_header()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Upload Base Blue")
            blue_file = st.file_uploader(
                "Drag and drop file here",
                type=["xlsx"],
                help="Limit 200MB per file • XLSX",
                key="blue_uploader"
            )
            
        with col2:
            st.subheader("Upload Base Gama")
            gama_file = st.file_uploader(
                "Drag and drop file here",
                type=["xlsx"],
                help="Limit 200MB per file • XLSX",
                key="gama_uploader"
            )
            
        if blue_file and gama_file:
            self.base_blue, blue_error = self.data_loader.load_and_prepare_data(blue_file, "blue")
            self.base_gama, gama_error = self.data_loader.load_and_prepare_data(gama_file, "gama")
            
            if blue_error or gama_error:
                if blue_error:
                    st.error(f"Error loading blue file: {blue_error}")
                if gama_error:
                    st.error(f"Error loading gama file: {gama_error}")
                return
            
            # Applying the preprocessing steps again to ensure transformations are made
            if not self.base_blue.empty:
                self.base_blue = self.data_loader.preprocessor.convert_to_string(self.base_blue)
            if not self.base_gama.empty:
                self.base_gama = self.data_loader.preprocessor.clean_cpf_column(self.base_gama, 'cpfusu')
                self.base_gama = self.data_loader.preprocessor.convert_to_date(
                    self.base_gama, ['data_inicio_vigencia'], {'data_inicio_vigencia': '%Y-%m-%d'}
                )
                self.base_gama = self.data_loader.preprocessor.convert_to_string(self.base_gama)

            st.success("Both files loaded and processed successfully!")
            
            if not self.base_blue.empty and not self.base_gama.empty:
                st.subheader("Preprocessed Data Sample")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Base Blue Sample")
                    st.dataframe(self.base_blue.head())
                with col2:
                    st.write("Base Gama Sample")
                    st.dataframe(self.base_gama.head())
                
                rules = self._configure_rules()
                
                if st.button("Reconcile Data") and rules:
                    matches, only_blue, only_gama = self.reconciliation_engine.apply_matching_rules(
                        self.base_blue, self.base_gama, rules
                    )
                    self.ui.render_results(matches, only_blue, only_gama)

    def _configure_rules(self) -> List[Dict]:
        """Configure matching rules"""
        st.subheader("Configure Matching Rules")
        
        blue_columns = self.base_blue.columns.tolist()
        gama_columns = self.base_gama.columns.tolist()
        
        rules = []
        rule_count = st.number_input("Number of matching rules", min_value=1, max_value=5, value=1)
        
        for i in range(rule_count):
            st.write(f"Rule {i+1}")
            col1, col2 = st.columns(2)
            with col1:
                blue_cols = st.multiselect(
                    f"Select Blue columns for Rule {i+1}",
                    blue_columns,
                    key=f"blue_rule_{i}"
                )
            with col2:
                gama_cols = st.multiselect(
                    f"Select Gama columns for Rule {i+1}",
                    gama_columns,
                    key=f"gama_rule_{i}"
                )
            
            if blue_cols and gama_cols:
                rules.append({
                    'name': f"Rule {i+1}",
                    'blue_columns': blue_cols,
                    'gama_columns': gama_cols
                })
        
        return rules
    
# Run the application
if __name__ == "__main__":
    app = ReconciliationApp()
    app.run()
