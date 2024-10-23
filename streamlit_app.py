# streamlit_app.py 수정
def main():
    st.set_page_config(
        page_title="안동농협공판장 사과 시세표",
        layout="wide"
    )
    
    st.title("안동농협공판장 사과 시세표")
    
    # 구글 스프레드시트 설정
    SHEET_ID = "1b2J9wmgG_INHpHfOh7PCrKXSYuJSSvtTDHhp3LZGtsw"
    SHEET_RANGE = "시트1!A1:G100"  # 실제 데이터 범위에 맞게 조정
    
    # 데이터 프로바이더 초기화
    data_provider = GoogleSheetDataProvider(SHEET_ID, SHEET_RANGE)
    
    # 세션 상태 초기화
    if 'current_item' not in st.session_state:
        st.session_state.current_item = '아리수'
    
    try:
        # 데이터 가져오기
        market_data = data_provider.get_market_data()
        
        if not market_data.empty:
            # 네비게이션
            items = ['홍로', '시나노골드', '노무라골드', '아리수', '감홍']
            cols = st.columns(len(items))
            for col, item in zip(cols, items):
                if col.button(item):
                    st.session_state.current_item = item
            
            # 데이터 표시
            st.dataframe(
                style_dataframe(market_data),
                hide_index=True,
                width=800,
                height=450
            )
            
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()