import pandas as pd
from io import BytesIO
import base64

class FileHandler:
    @staticmethod
    def create_download_link(df: pd.DataFrame, filename: str) -> str:
        """Create download link for Excel file"""
        towrite = BytesIO()
        df.to_excel(towrite, index=False)
        towrite.seek(0)
        b64 = base64.b64encode(towrite.read()).decode()
        return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download {filename}</a>'
