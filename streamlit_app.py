# # # streamlit_app.py 수정
# # def main():
# #     st.set_page_config(
# #         page_title="안동농협공판장 사과 시세표",
# #         layout="wide"
# #     )
    
# #     st.title("안동농협공판장 사과 시세표")
    
# #     # 구글 스프레드시트 설정
# #     SHEET_ID = "1b2J9wmgG_INHpHfOh7PCrKXSYuJSSvtTDHhp3LZGtsw"
# #     SHEET_RANGE = "시트1!A1:G100"  # 실제 데이터 범위에 맞게 조정
    
# #     # 데이터 프로바이더 초기화
# #     data_provider = GoogleSheetDataProvider(SHEET_ID, SHEET_RANGE)
    
# #     # 세션 상태 초기화
# #     if 'current_item' not in st.session_state:
# #         st.session_state.current_item = '아리수'
    
# #     try:
# #         # 데이터 가져오기
# #         market_data = data_provider.get_market_data()
        
# #         if not market_data.empty:
# #             # 네비게이션
# #             items = ['홍로', '시나노골드', '노무라골드', '아리수', '감홍']
# #             cols = st.columns(len(items))
# #             for col, item in zip(cols, items):
# #                 if col.button(item):
# #                     st.session_state.current_item = item
            
# #             # 데이터 표시
# #             st.dataframe(
# #                 style_dataframe(market_data),
# #                 hide_index=True,
# #                 width=800,
# #                 height=450
# #             )
            
# #     except Exception as e:
# #         st.error(f"오류가 발생했습니다: {str(e)}")

# # if __name__ == "__main__":
# #     main()

# # streamlit_app.py
# import streamlit as st
# import pandas as pd
# from pathlib import Path
# from google_auth_oauthlib.flow import Flow
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from typing import Dict, List
# from datetime import datetime

# # 페이지 설정 및 스타일
# def setup_page():
#     st.set_page_config(
#         page_title="안동농협공판장 사과 시세표",
#         layout="wide",
#         initial_sidebar_state="collapsed"
#     )
    
#     # CSS 스타일 적용
#     st.markdown("""
#         <style>
#         .stButton button {
#             width: 100%;
#             background-color: #f0f2f6;
#             border: 1px solid #ddd;
#         }
#         .stDataFrame {
#             width: 100%;
#         }
#         </style>
#     """, unsafe_allow_html=True)

# # Google OAuth 인증 클래스
# class GoogleAuth:
#     def __init__(self):
#         self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
#         self.REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
    
#     def check_auth(self):
#         return 'google_token' in st.session_state
    
#     def authenticate(self):
#         if not self.check_auth():
#             try:
#                 client_config = {
#                     "installed": {
#                         "client_id": st.secrets["google_oauth"]["client_id"],
#                         "client_secret": st.secrets["google_oauth"]["client_secret"],
#                         "redirect_uris": [self.REDIRECT_URI],
#                         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#                         "token_uri": "https://oauth2.googleapis.com/token"
#                     }
#                 }
                
#                 flow = Flow.from_client_config(
#                     client_config,
#                     scopes=self.SCOPES,
#                     redirect_uri=self.REDIRECT_URI
#                 )
                
#                 auth_url, _ = flow.authorization_url(prompt='consent')
                
#                 st.write("구글 계정으로 로그인이 필요합니다.")
#                 st.markdown(f"1. [이 링크를 클릭하여 구글 로그인]({auth_url})하세요")
#                 st.markdown("2. 권한을 허용하고 받은 코드를 아래에 입력하세요")
                
#                 code = st.text_input("인증 코드를 입력하세요:")
#                 if code:
#                     flow.fetch_token(code=code)
#                     credentials = flow.credentials
#                     st.session_state['google_token'] = {
#                         'token': credentials.token,
#                         'refresh_token': credentials.refresh_token,
#                         'token_uri': credentials.token_uri,
#                         'client_id': credentials.client_id,
#                         'client_secret': credentials.client_secret,
#                         'scopes': credentials.scopes
#                     }
#                     st.success("인증이 완료되었습니다!")
#                     st.experimental_rerun()
                    
#             except Exception as e:
#                 st.error(f"인증 중 오류가 발생했습니다: {str(e)}")
#                 return False
#         return True
    
#     def get_credentials(self):
#         if self.check_auth():
#             return Credentials.from_authorized_user_info(
#                 st.session_state['google_token'],
#                 self.SCOPES
#             )
#         return None

# # 데이터 제공자 클래스
# class GoogleSheetDataProvider:
#     def __init__(self, sheet_id: str, sheet_range: str):
#         self.sheet_id = sheet_id
#         self.sheet_range = sheet_range
#         self.auth = GoogleAuth()
    
#     def get_sheet_data(self):
#         if not self.auth.authenticate():
#             return None
            
#         credentials = self.auth.get_credentials()
#         if not credentials:
#             return None
            
#         try:
#             service = build('sheets', 'v4', credentials=credentials)
#             result = service.spreadsheets().values().get(
#                 spreadsheetId=self.sheet_id,
#                 range=self.sheet_range
#             ).execute()
            
#             return result.get('values', [])
            
#         except Exception as e:
#             st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {str(e)}")
#             return None

# # 데이터프레임 스타일링 함수
# def style_dataframe(df: pd.DataFrame):
#     def highlight_values(val):
#         if isinstance(val, (int, float)):
#             return f'color: {"red" if "최고가" in str(val) else "blue" if "평균가" in str(val) else "black"}'
#         return ''
    
#     return df.style.applymap(highlight_values)

# # 메인 애플리케이션
# def main():
#     setup_page()
    
#     st.title("안동농협공판장 사과 시세표")
#     st.write(f"조회 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
#     # 구글 스프레드시트 설정
#     SHEET_ID = "1b2J9wmgG_INHpHfOh7PCrKXSYuJSSvtTDHhp3LZGtsw"
#     SHEET_RANGE = "시트1!A1:G100"  # 실제 데이터 범위에 맞게 조정
    
#     data_provider = GoogleSheetDataProvider(SHEET_ID, SHEET_RANGE)
    
#     # 세션 상태 초기화
#     if 'current_item' not in st.session_state:
#         st.session_state.current_item = '아리수'
    
#     # 데이터 가져오기
#     values = data_provider.get_sheet_data()
    
#     if values:
#         headers = values[0]
#         data = values[1:]
        
#         df = pd.DataFrame(data, columns=headers)
        
#         # 숫자 컬럼 변환
#         numeric_columns = ['수량', '최고가', '최저가', '평균가']
#         for col in numeric_columns:
#             if col in df.columns:
#                 df[col] = pd.to_numeric(df[col], errors='coerce')
        
#         # 네비게이션
#         items = ['홍로', '시나노골드', '노무라골드', '아리수', '감홍']
#         cols = st.columns(len(items))
#         for col, item in zip(cols, items):
#             if col.button(item):
#                 st.session_state.current_item = item
        
#         # 데이터 표시
#         st.dataframe(
#             style_dataframe(df),
#             hide_index=True,
#             width=800,
#             height=450
#         )
#     else:
#         st.warning("데이터를 불러올 수 없습니다. 인증을 확인해주세요.")

# if __name__ == "__main__":
#     main()

# streamlit_app.py
import streamlit as st
import pandas as pd
from datetime import datetime

def load_data():
    # CSV 파일 읽기
    df = pd.read_csv("./안동농협_시세표 - 사과_전체.csv")
    
    # 컬럼명 매핑
    column_mapping = {
        'sale_date': '날짜',
        'variety': '품종',
        'level': '등급',
        'quantity': '수량',
        'today_highest_price': '최고가',
        'today_lowest_price': '최저가',
        'today_average_price': '평균가'
    }
    
    # 필요한 컬럼만 선택하고 이름 변경
    df = df[column_mapping.keys()].rename(columns=column_mapping)
    
    # 날짜 형식 변환
    df['날짜'] = pd.to_datetime(df['날짜'], format='%Y. %m. %d').dt.strftime('%Y-%m-%d')
    
    return df

def style_dataframe(df):
    def highlight_values(val):
        if isinstance(val, (int, float)):
            return f'color: {"red" if "최고가" in str(val) else "blue" if "평균가" in str(val) else "black"}'
        return ''
    
    return df.style.applymap(highlight_values)

def main():
    # 페이지 설정
    st.set_page_config(
        page_title="안동농협공판장 사과 시세표",
        layout="wide"
    )
    
    st.title("안동농협공판장 사과 시세표")
    st.write(f"조회 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 데이터 불러오기
        df = load_data()
        
        # 최신 날짜 데이터만 필터링
        latest_date = df['날짜'].max()
        df_latest = df[df['날짜'] == latest_date]
        
        # 품종 선택
        available_items = ['전체'] + sorted(df_latest['품종'].unique().tolist())
        cols = st.columns(len(available_items))
        
        for col, item in zip(cols, available_items):
            if col.button(item):
                st.session_state['current_item'] = item
                
        # 세션 상태 초기화
        if 'current_item' not in st.session_state:
            st.session_state['current_item'] = '전체'
            
        # 선택된 품종에 따라 데이터 필터링
        if st.session_state['current_item'] != '전체':
            df_display = df_latest[df_latest['품종'] == st.session_state['current_item']]
        else:
            df_display = df_latest
            
        # 품종별 총 수량 계산
        total_quantity = df_display['수량'].sum()
        st.write(f"{st.session_state['current_item']} 반입량: {total_quantity:,} 상자")
        
        # 데이터 표시
        st.dataframe(
            style_dataframe(df_display[['등급', '수량', '최고가', '최저가', '평균가']]),
            hide_index=True,
            width=800,
            height=450
        )
        
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")
        st.error("CSV 파일이 올바른 경로에 있는지 확인해주세요.")

if __name__ == "__main__":
    main()