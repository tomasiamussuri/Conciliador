import pandas as pd
from io import BytesIO
import base64

class FileHandler:
    @staticmethod
    def criar_link_para_download(df: pd.DataFrame, nome_arquivo: str) -> str:
        """Cria link de download para arquivo Excel"""
        towrite = BytesIO()
        df.to_excel(towrite, index=False)
        towrite.seek(0)
        b64 = base64.b64encode(towrite.read()).decode()
        return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{nome_arquivo}">Download {nome_arquivo}</a>'