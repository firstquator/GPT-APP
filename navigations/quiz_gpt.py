import streamlit as st
from utils.quizgpt import QuizGPT

st.set_page_config(
    page_title="QuizGPT",
    page_icon="📒",
    layout='wide'
)

st.title("QuizGPT")

# 사이드바에 설정창
with st.sidebar:
    with st.popover("⚙️ 설정"):
        st.markdown("#### 퀴즈 생성 설정")
        num_questions = st.number_input("문제 개수", value=10, min_value=1, max_value=20, step=1)
        num_choices = st.number_input("객관식 보기 개수", value=3, min_value=1, max_value=5, step=1)
        language = st.selectbox("번역 언어", ['한국어', 'English'])
 
    topic = st.text_input("주제 입력", placeholder="생성할 퀴즈 주제를 입력해 주세요.")

quiz_gpt = QuizGPT(num_questions=num_questions, num_choices=num_choices, language=language)

if topic:
    quiz_gpt.run(topic)