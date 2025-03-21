import streamlit as st
from langchain.chat_models import ChatOpenAI
from utils.mygpt import MyGPT

st.set_page_config(
    page_title="MY CHATGPT",
    page_icon="📖",
    layout='wide'
)

st.title("My ChatGPT")

# MyGPT 생성하기
mygpt = MyGPT()

# 사이드바 생성하기
with st.sidebar:
    reset_btn = st.button("대화 초기화")
    if reset_btn:
        mygpt.initialize_session()
        st.rerun()

    # 응답 번역 언어 설정
    language = st.selectbox("번역 언어(Translation Language)", ['한국어', '영어', '일본어'])

    # ChatGPT 응답 말투 설정
    tone = st.selectbox("말투(Tone)", ['기본', '건달', '나무늘보', '소심이'])

# 번역 언어 및 말투 설정
mygpt.set_rules(language, tone)

# 이전 대화 출력하기
mygpt.paint_history()

prompt = st.chat_input()

if prompt:
    mygpt.run(prompt)