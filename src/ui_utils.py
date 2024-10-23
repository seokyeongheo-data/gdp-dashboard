# src/ui_utils.py
import pandas as pd

def style_dataframe(df: pd.DataFrame):
    def highlight_values(val):
        if isinstance(val, (int, float)):
            return f'color: {"red" if "최고가" in str(val) else "blue" if "평균가" in str(val) else "black"}'
        return ''
    
    return df.style.applymap(highlight_values)