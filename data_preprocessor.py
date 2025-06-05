import pandas as pd
from typing import List, Dict, Tuple

class DataPreprocessor:
    @staticmethod
    def converter_para_string(df: pd.DataFrame) -> pd.DataFrame:
        """Converte todas as colunas para string e limpa os dados"""
        df_processado = df.copy()
        for coluna in df_processado.columns:
            df_processado[coluna] = df_processado[coluna].fillna('')
            df_processado[coluna] = df_processado[coluna].astype(str)
            df_processado[coluna] = df_processado[coluna].str.upper()
            df_processado[coluna] = df_processado[coluna].str.strip()
            df_processado[coluna] = df_processado[coluna].str.replace(r'\s+', ' ', regex=True)
        return df_processado

    @staticmethod
    def converter_para_data(df: pd.DataFrame, colunas_data: List[str], formatos: Dict[str, str]) -> pd.DataFrame:
        """Converte colunas especificadas para o formato de data padrão 'YYYY-MM-DD'"""
        df_processado = df.copy()
        for coluna in colunas_data:
            if coluna in df_processado.columns:
                formato_data = formatos.get(coluna, '%Y-%m-%d')
                df_processado[coluna] = pd.to_datetime(df_processado[coluna], format=formato_data, errors='coerce').dt.strftime('%Y-%m-%d')
        return df_processado

    @staticmethod
    def adicionar_id_unico(df: pd.DataFrame, prefixo: str) -> pd.DataFrame:
        """Adiciona uma coluna de ID único ao dataframe"""
        df = df.copy()
        df['ID_' + prefixo] = [f"{prefixo}_{i:06d}" for i in range(len(df))]
        return df
    
    @staticmethod
    def limpar_coluna_cpf(df: pd.DataFrame, nome_coluna: str) -> pd.DataFrame:
        """Remove caracteres não numéricos da coluna de CPF"""
        df = df.copy()
        if nome_coluna in df.columns: 
            df[nome_coluna] = df[nome_coluna].astype(str).str.replace(r'\D', '', regex=True)
        return df

    @staticmethod
    def normalizar_colunas_para_conciliacao(df: pd.DataFrame, colunas: List[str]) -> pd.DataFrame:
        """Normaliza colunas específicas para comparação: remove espaços, pontuação e deixa tudo em maiúsculo"""
        df = df.copy()
        for col in colunas:
            if col in df.columns:
                df[col] = df[col].astype(str)
                df[col] = df[col].str.upper()
                df[col] = df[col].str.strip()
                df[col] = df[col].str.replace(r'\s+', '', regex=True)
                df[col] = df[col].str.replace(r'[^\w]', '', regex=True)  # remove pontos, traços, etc.
        return df
