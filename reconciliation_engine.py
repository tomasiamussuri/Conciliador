import pandas as pd
from typing import List, Dict, Tuple

class ReconciliationEngine:
    def __init__(self):
        self.ids_correspondidos_arquivo_A = set()
        self.ids_correspondidos_arquivo_B = set()

    def redefinir_correspondencias(self):
        """Redefinir conjuntos de IDs correspondidos"""
        self.ids_correspondidos_arquivo_A.clear()
        self.ids_correspondidos_arquivo_B.clear()

    def aplicar_regras_de_correspondencia(
        self,
        base_arquivo_A: pd.DataFrame,
        base_arquivo_B: pd.DataFrame,
        regras: List[Dict]
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Aplicar regras de correspondência em ordem de prioridade"""
        self.redefinir_correspondencias()
        base_arquivo_A_copy = base_arquivo_A.copy()
        base_arquivo_B_copy = base_arquivo_B.copy()

        for regra in regras:
            colunas_arquivo_A = regra['arquivo_A_columns']
            colunas_arquivo_B = regra['arquivo_B_columns']
            nome_regra = regra['name']

            chave_arquivo_A = base_arquivo_A_copy[colunas_arquivo_A].apply(lambda x: '|'.join(x), axis=1)
            chave_arquivo_B = base_arquivo_B_copy[colunas_arquivo_B].apply(lambda x: '|'.join(x), axis=1)

            arquivo_A_nao_correspondido = ~base_arquivo_A_copy['ID_ARQUIVO_A'].isin(self.ids_correspondidos_arquivo_A)
            arquivo_B_nao_correspondido = ~base_arquivo_B_copy['ID_ARQUIVO_B'].isin(self.ids_correspondidos_arquivo_B)

            for idx_arquivo_A in chave_arquivo_A[arquivo_A_nao_correspondido].index:
                chave = chave_arquivo_A[idx_arquivo_A]
                matches_B = chave_arquivo_B[arquivo_B_nao_correspondido] == chave

                if matches_B.any():
                    idx_arquivo_B = chave_arquivo_B[arquivo_B_nao_correspondido][matches_B].index[0]

                    id_arquivo_A = base_arquivo_A_copy.loc[idx_arquivo_A, 'ID_ARQUIVO_A']
                    id_arquivo_B = base_arquivo_B_copy.loc[idx_arquivo_B, 'ID_ARQUIVO_B']

                    # Marca correspondência nas duas bases
                    base_arquivo_A_copy.at[idx_arquivo_A, 'ID_CORRESPONDIDO'] = id_arquivo_B
                    base_arquivo_A_copy.at[idx_arquivo_A, 'REGRA_CORRESPONDENCIA'] = nome_regra

                    base_arquivo_B_copy.at[idx_arquivo_B, 'ID_CORRESPONDIDO'] = id_arquivo_A
                    base_arquivo_B_copy.at[idx_arquivo_B, 'REGRA_CORRESPONDENCIA'] = nome_regra

                    self.ids_correspondidos_arquivo_A.add(id_arquivo_A)
                    self.ids_correspondidos_arquivo_B.add(id_arquivo_B)

        return self._preparar_resultados(base_arquivo_A_copy, base_arquivo_B_copy)

    def _preparar_resultados(
        self,
        base_arquivo_A: pd.DataFrame,
        base_arquivo_B: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Preparar dataframes de resultados finais"""
        apenas_arquivo_A = base_arquivo_A[~base_arquivo_A['ID_ARQUIVO_A'].isin(self.ids_correspondidos_arquivo_A)]
        apenas_arquivo_B = base_arquivo_B[~base_arquivo_B['ID_ARQUIVO_B'].isin(self.ids_correspondidos_arquivo_B)]

        correspondencias_arquivo_A = base_arquivo_A[base_arquivo_A['ID_ARQUIVO_A'].isin(self.ids_correspondidos_arquivo_A)]
        correspondencias_arquivo_B = base_arquivo_B[base_arquivo_B['ID_ARQUIVO_B'].isin(self.ids_correspondidos_arquivo_B)]

        correspondencias = pd.merge(
            correspondencias_arquivo_A,
            correspondencias_arquivo_B,
            left_on='ID_CORRESPONDIDO',
            right_on='ID_ARQUIVO_B',
            suffixes=('_ARQUIVO_A', '_ARQUIVO_B')
        )

        return correspondencias, apenas_arquivo_A, apenas_arquivo_B
