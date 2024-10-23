# src/data_provider.py
import pandas as pd
from typing import Dict, List
from abc import ABC, abstractmethod

class DataProvider(ABC):
    @abstractmethod
    def get_market_data(self) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def get_daily_summary(self) -> Dict:
        pass

class GoogleSheetDataProvider(DataProvider):
    def __init__(self, sheet_id: str, sheet_name: str):
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name
    
    def get_market_data(self) -> pd.DataFrame:
        # 샘플 데이터
        data = {
            '등급': ['특3', '특4', '특5', '특6', '특7', '특8', '상1', '상2', '상3', '등외', '보1'],
            '규격': ['박스 20kg'] * 11,
            '수량': [37, 103, 89, 42, 20, 4, 210, 211, 76, 25, 63],
            '최고가': [108900, 126600, 135500, 120000, 68900, 30100, 53900, 63000, 46900, 35100, 29300],
            '최저가': [60100, 33000, 20000, 15000, 13300, 19900, 17000, 14900, 12900, 11200, 11100],
            '평균가': [100986, 93873, 68842, 43419, 32200, 27250, 47845, 38673, 32187, 21264, 18524]
        }
        return pd.DataFrame(data)
    
    def get_daily_summary(self) -> Dict:
        return {
            'date': '2024년 10월 4일',
            'item': '아리수',
            'total_boxes': 880
        }