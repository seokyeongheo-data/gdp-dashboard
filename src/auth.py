import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
from pathlib import Path

class GoogleAuth:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
    
    def _create_flow(self):
        client_config = {
            "installed": {
                "client_id": st.secrets["google_oauth"]["client_id"],
                "client_secret": st.secrets["google_oauth"]["client_secret"],
                "redirect_uris": [self.REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }
        
        return Flow.from_client_config(
            client_config,
            scopes=self.SCOPES,
            redirect_uri=self.REDIRECT_URI
        )
    
    def check_auth(self):
        """Check if user is authenticated"""
        return 'google_token' in st.session_state
    
    def authenticate(self):
        """Authenticate user with Google OAuth"""
        if not self.check_auth():
            flow = self._create_flow()
            auth_url, _ = flow.authorization_url(prompt='consent')
            
            st.write("구글 계정으로 로그인이 필요합니다.")
            st.markdown(f"""
            1. [이 링크를 클릭하여 구글 로그인]({auth_url})하세요
            2. 권한을 허용하고 받은 코드를 아래에 입력하세요
            """)
            
            code = st.text_input("인증 코드를 입력하세요:")
            if code:
                try:
                    flow.fetch_token(code=code)
                    credentials = flow.credentials
                    st.session_state['google_token'] = {
                        'token': credentials.token,
                        'refresh_token': credentials.refresh_token,
                        'token_uri': credentials.token_uri,
                        'client_id': credentials.client_id,
                        'client_secret': credentials.client_secret,
                        'scopes': credentials.scopes
                    }
                    st.success("인증이 완료되었습니다!")
                    st.rerun()
                except Exception as e:
                    st.error(f"인증 중 오류가 발생했습니다: {str(e)}")
                    return False
        return True

    def get_credentials(self):
        """Get credentials from session state"""
        if self.check_auth():
            return Credentials.from_authorized_user_info(
                st.session_state['google_token'],
                self.SCOPES
            )
        return None