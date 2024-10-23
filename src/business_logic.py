# src/business_logic.py
from typing import List, Dict
import pandas as pd
from .data_provider import DataProvider

class MarketDataProcessor:
    def __init__(self, data_provider: DataProvider):
        self.data_provider = data_provider
    
    def get_processed_market_data(self) -> pd.DataFrame:
        return self.data_provider.get_market_data()
    
    def get_summary(self) -> Dict:
        return self.data_provider.get_daily_summary()
    
    def get_available_items(self) -> List[str]:
        return ['홍로', '시나노골드', '노무라골드', '아리수', '감홍']