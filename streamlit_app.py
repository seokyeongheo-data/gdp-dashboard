# streamlit_app.py
import streamlit as st
import pandas as pd
from datetime import datetime

def load_data():
    # CSV 파일 읽기
    df = pd.read_csv("./apple_market_price_241023.csv")
    
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

def create_grid_buttons(items, num_cols=4):  # 매개변수 이름이 num_cols
    # 빈 항목을 포함하여 전체 그리드를 구성할 수 있는 개수 계산
    num_items = len(items)
    num_rows = (num_items + num_cols - 1) // num_cols
    
    for row_idx in range(num_rows):
        cols = st.columns(num_cols)
        for col_idx in range(num_cols):
            item_idx = row_idx * num_cols + col_idx
            if item_idx < num_items:
                if cols[col_idx].button(items[item_idx], use_container_width=True):
                    st.session_state['current_item'] = items[item_idx]

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
    
    # CSS 스타일 적용
    st.markdown("""
        <style>
        .stButton > button {
            font-size: 16px;
            height: 50px;
            margin: 5px;
        }
        div[data-testid="stHorizontalBlock"] {
            gap: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("안동농협공판장 사과 시세표")
    
    try:
        # 데이터 불러오기
        df = load_data()
        
        # 날짜 목록 가져오기
        available_dates = sorted(df['날짜'].unique(), reverse=True)
        
        # 세션 상태 초기화
        if 'current_date_index' not in st.session_state:
            st.session_state['current_date_index'] = 0
        if 'current_item' not in st.session_state:
            st.session_state['current_item'] = '전체'
            
        # 날짜 네비게이션
        col1, col2, col3 = st.columns([1, 3, 1])
        
        # 이전 버튼
        if col1.button('◀ 이전', key='prev'):
            if st.session_state['current_date_index'] < len(available_dates) - 1:
                st.session_state['current_date_index'] += 1
                st.experimental_rerun()
        
        # 현재 날짜 표시
        current_date = available_dates[st.session_state['current_date_index']]
        col2.markdown(f"### {current_date} 시세")
        
        # 다음 버튼
        if col3.button('다음 ▶', key='next'):
            if st.session_state['current_date_index'] > 0:
                st.session_state['current_date_index'] -= 1
                st.experimental_rerun()
        
        st.write(f"조회 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 현재 날짜의 데이터만 필터링
        df_current = df[df['날짜'] == current_date]
        
        # 품종 선택 버튼 그리드
        st.markdown("### 품종 선택")
        available_items = ['전체'] + sorted(df_current['품종'].unique().tolist())
        # create_grid_buttons(available_items, cols=4)
        create_grid_buttons(available_items, cols=4)  # 매개변수 이름을 cols로 사용
        
        # 선택된 품종에 따라 데이터 필터링
        if st.session_state['current_item'] != '전체':
            df_display = df_current[df_current['품종'] == st.session_state['current_item']]
        else:
            df_display = df_current
            
        # 품종별 총 수량 계산
        total_quantity = df_display['수량'].sum()
        st.markdown(f"### {st.session_state['current_item']} 반입량: {total_quantity:,} 상자")
        
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