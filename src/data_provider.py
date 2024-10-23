# src/data_provider.py 수정
class GoogleSheetDataProvider(DataProvider):
    def __init__(self, sheet_id: str, sheet_range: str):
        self.sheet_id = sheet_id
        self.sheet_range = sheet_range
        self.auth = GoogleAuth()
        
    def _get_google_sheets_service(self):
        credentials = self.auth.get_credentials()
        if credentials:
            return build('sheets', 'v4', credentials=credentials)
        return None
    
    def get_market_data(self) -> pd.DataFrame:
        if not self.auth.authenticate():
            st.error("구글 인증이 필요합니다.")
            return pd.DataFrame()
            
        service = self._get_google_sheets_service()
        if not service:
            st.error("구글 시트 서비스 연결에 실패했습니다.")
            return pd.DataFrame()
            
        try:
            result = service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=self.sheet_range
            ).execute()
            
            values = result.get('values', [])
            if not values:
                st.warning("데이터가 없습니다.")
                return pd.DataFrame()
                
            headers = values[0]
            data = values[1:]
            
            df = pd.DataFrame(data, columns=headers)
            
            # 숫자 컬럼 변환
            numeric_columns = ['수량', '최고가', '최저가', '평균가']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    
            return df
            
        except Exception as e:
            st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {str(e)}")
            return pd.DataFrame()