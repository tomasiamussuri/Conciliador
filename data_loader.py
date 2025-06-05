import pandas as pd
from typing import Tuple
from data_preprocessor import DataPreprocessor

class DataLoader:
    def __init__(self):
        self.preprocessor = DataPreprocessor()

    def carregar_e_preparar_dados(self, arquivo, tipo_base: str) -> Tuple[pd.DataFrame, str]:
        """Carregar e preprocessar arquivo Excel ou CSV"""
        try:
            nome_arquivo = arquivo.name.lower()

            # Detecta o tipo de arquivo
            if nome_arquivo.endswith(".csv"):
                # Tenta ler como CSV com separador padrão ','
                try:
                    df = pd.read_csv(arquivo, encoding='utf-8', sep=',')
                except Exception:
                    # Se falhar, tenta como ';'
                    arquivo.seek(0)
                    df = pd.read_csv(arquivo, encoding='utf-8', sep=';')
            else:
                # Leitura de Excel
                df = pd.read_excel(arquivo, engine='openpyxl' if nome_arquivo.endswith('.xlsx') else 'xlrd')

            # Adiciona ID único
            df = self.preprocessor.adicionar_id_unico(df, tipo_base.upper())

            # Pré-processamento específico do tipo B
            if tipo_base.lower() == 'arquivo_b':
                df = self.preprocessor.limpar_coluna_cpf(df, 'cpfusu')
                df = self.preprocessor.converter_para_data(df, ['data_inicio_vigencia'], {'data_inicio_vigencia': '%Y-%m-%d'})

            # Converte tudo para string
            df = self.preprocessor.converter_para_string(df)

            # Adiciona colunas de correspondência
            df['ID_CORRESPONDIDO'] = None
            df['REGRA_CORRESPONDENCIA'] = None

            return df, None

        except Exception as e:
            return None, str(e)
