# import streamlit as st
# import pandas as pd
# import math
# from pathlib import Path

# # Set the title and favicon that appear in the Browser's tab bar.
# st.set_page_config(
#     page_title='GDP dashboard',
#     page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
# )

# # -----------------------------------------------------------------------------
# # Declare some useful functions.

# @st.cache_data
# def get_gdp_data():
#     """Grab GDP data from a CSV file.

#     This uses caching to avoid having to read the file every time. If we were
#     reading from an HTTP endpoint instead of a file, it's a good idea to set
#     a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
#     """

#     # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
#     DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
#     raw_gdp_df = pd.read_csv(DATA_FILENAME)

#     MIN_YEAR = 1960
#     MAX_YEAR = 2022

#     # The data above has columns like:
#     # - Country Name
#     # - Country Code
#     # - [Stuff I don't care about]
#     # - GDP for 1960
#     # - GDP for 1961
#     # - GDP for 1962
#     # - ...
#     # - GDP for 2022
#     #
#     # ...but I want this instead:
#     # - Country Name
#     # - Country Code
#     # - Year
#     # - GDP
#     #
#     # So let's pivot all those year-columns into two: Year and GDP
#     gdp_df = raw_gdp_df.melt(
#         ['Country Code'],
#         [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
#         'Year',
#         'GDP',
#     )

#     # Convert years from string to integers
#     gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

#     return gdp_df

# gdp_df = get_gdp_data()

# # -----------------------------------------------------------------------------
# # Draw the actual page

# # Set the title that appears at the top of the page.
# '''
# # :earth_americas: GDP dashboard

# Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
# notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
# But it's otherwise a great (and did I mention _free_?) source of data.
# '''

# # Add some spacing
# ''
# ''

# min_value = gdp_df['Year'].min()
# max_value = gdp_df['Year'].max()

# from_year, to_year = st.slider(
#     'Which years are you interested in?',
#     min_value=min_value,
#     max_value=max_value,
#     value=[min_value, max_value])

# countries = gdp_df['Country Code'].unique()

# if not len(countries):
#     st.warning("Select at least one country")

# selected_countries = st.multiselect(
#     'Which countries would you like to view?',
#     countries,
#     ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'])

# ''
# ''
# ''

# # Filter the data
# filtered_gdp_df = gdp_df[
#     (gdp_df['Country Code'].isin(selected_countries))
#     & (gdp_df['Year'] <= to_year)
#     & (from_year <= gdp_df['Year'])
# ]

# st.header('GDP over time', divider='gray')

# ''

# st.line_chart(
#     filtered_gdp_df,
#     x='Year',
#     y='GDP',
#     color='Country Code',
# )

# ''
# ''


# first_year = gdp_df[gdp_df['Year'] == from_year]
# last_year = gdp_df[gdp_df['Year'] == to_year]

# st.header(f'GDP in {to_year}', divider='gray')

# ''

# cols = st.columns(4)

# for i, country in enumerate(selected_countries):
#     col = cols[i % len(cols)]

#     with col:
#         first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
#         last_gdp = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1000000000

#         if math.isnan(first_gdp):
#             growth = 'n/a'
#             delta_color = 'off'
#         else:
#             growth = f'{last_gdp / first_gdp:,.2f}x'
#             delta_color = 'normal'

#         st.metric(
#             label=f'{country} GDP',
#             value=f'{last_gdp:,.0f}B',
#             delta=growth,
#             delta_color=delta_color
#         )

# data_provider.py
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
        # TODO: 구글 스프레드시트 연동 로직 구현
        # 현재는 샘플 데이터 반환
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

# business_logic.py
class MarketDataProcessor:
    def __init__(self, data_provider: DataProvider):
        self.data_provider = data_provider
    
    def get_processed_market_data(self) -> pd.DataFrame:
        df = self.data_provider.get_market_data()
        # 필요한 데이터 처리 로직 추가
        return df
    
    def get_summary(self) -> Dict:
        return self.data_provider.get_daily_summary()
    
    def get_available_items(self) -> List[str]:
        return ['홍로', '시나노골드', '노무라골드', '아리수', '감홍']

# ui_utils.py
def style_dataframe(df: pd.DataFrame):
    def highlight_values(val):
        if isinstance(val, (int, float)):
            return f'color: {"red" if "최고가" in str(val) else "blue" if "평균가" in str(val) else "black"}'
        return ''
    
    return df.style.applymap(highlight_values)

# main.py
import streamlit as st
from data_provider import GoogleSheetDataProvider
from business_logic import MarketDataProcessor

def init_session_state():
    if 'current_item' not in st.session_state:
        st.session_state.current_item = '아리수'

def create_navigation(items: List[str]):
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        if col.button(item):
            st.session_state.current_item = item

def main():
    # 앱 설정
    st.set_page_config(
        page_title="안동농협공판장 사과 시세표",
        layout="wide"
    )
    
    # 초기화
    init_session_state()
    
    # 데이터 프로바이더 및 프로세서 설정
    data_provider = GoogleSheetDataProvider(
        sheet_id="your_sheet_id",
        sheet_name="your_sheet_name"
    )
    processor = MarketDataProcessor(data_provider)
    
    # 데이터 가져오기
    market_data = processor.get_processed_market_data()
    summary = processor.get_summary()
    
    # UI 렌더링
    st.title(summary['date'])
    st.subheader("안동농협공판장 사과 시세표")
    
    # 네비게이션
    create_navigation(processor.get_available_items())
    
    # 반입량 정보
    st.write(f"{summary['item']} 반입량 : {summary['total_boxes']} 상자")
    
    # 데이터 테이블
    st.dataframe(
        style_dataframe(market_data),
        hide_index=True,
        width=800,
        height=450
    )

if __name__ == "__main__":
    main()

# config.py
class Config:
    SHEET_ID = "your_sheet_id"
    SHEET_NAME = "your_sheet_name"
    GCP_CREDENTIALS_PATH = "path/to/credentials.json"