import time
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

class MyGPT:
    # 클래스(Class)를 생성했을 때, 실행할 생성자를 정의합니다.
    def __init__(self):
        # ChatGPT 모델을 생성합니다.
        # (숫자 0을 지우고 코드를 작성하세요.)
        self.llm = ChatOpenAI(
            temperature=0.1,
            model='gpt-4o-mini'
        )

        # 프롬프트 템플릿을 생성합니다.
        # (숫자 0을 지우고 코드를 작성하세요.)
        self.template = ChatPromptTemplate.from_messages([
            ('system', "다음 규칙을 꼭 지켜서 질문에 답해줘. 규칙 : {rules}"),
            MessagesPlaceholder(variable_name='conversation'),
            ('human', "{question}")
        ])

        # 템플릿 과 ChatGPT 를 연결한 체인(Chain)을 생성합니다.
        # (숫자 0을 지우고 코드를 작성하세요.)
        self.chain = self.template | self.llm

        # session_state 에서 사용할 데이터를 설정합니다.
        # (pass를 지우고 코드를 작성하세요.)
        self.set_session()

    # st.session_state 에 메모리와 대화 기록 리스트를 저장합니다.
    def set_session(self):
        # 메모리 세션 초기화
        # (아래에 코드를 작성하세요.)
        if 'memory' not in st.session_state:
            st.session_state['memory'] = ConversationBufferMemory(return_messages=True)
        
        # 대화 기록 세션 초기화
        # (아래에 코드를 작성하세요.)
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        # memory, history 변수를 session_state 값으로 설정합니다.
        # (숫자 0을 지우고 코드를 작성하세요.)
        self.memory = st.session_state['memory']
        self.history = st.session_state['history']

    # 질문(prompt)을 전달받아 ChatGPT의 응답을 반환하는 invoke() 함수를 정의합니다.
    def invoke(self, prompt):
        # 체인(Chain)으로 필요한 템플릿 변수들을 전달합니다.
        # (숫자 0을 지우고 코드를 작성하세요.)
        response = self.chain.invoke({
            'question': prompt,
            'conversation': self.memory.load_memory_variables({})['history'],
            'rules': self.rules
        })

        # 대화 기록을 메모리와 history 세션에 저장합니다.
        # (pass 를 지우고 코드를 작성하세요.)
        self.save_conversation(prompt, response)

        return response
    
    # 질문(prompt)과 응답(response)을 전달받아 대화 기록을 메모리와 history 세션에 
    # 저장하는 save_conversation() 함수를 정의합니다.
    def save_conversation(self, prompt, response):
        # memory 에 대화 기록 저장
        # (pass를 지우고 코드를 작성하세요.)
        self.memory.save_context(
            {'input': prompt},
            {'output': response.content}
        )

        # history 에 대화 기록 저장
        # (pass를 지우고 코드를 작성하세요.)
        self.history.append({
            'prompt': prompt,
            'response': response.content
        })

    # 현재 대화를 화면에 출력하는 함수 paint_conversation() 함수를 정의합니다.
    # (pass를 지우고 코드를 작성하세요.)
    def paint_conversation(self, prompt, response, stream=False):
        user_chat = st.chat_message('user')
        user_chat.markdown(prompt)

        ai_chat = st.chat_message('ai')
        if stream:
            self.stream_chat_response(response, ai_chat)
        else:
            ai_chat.markdown(response)


    # 이전 대화 기록들이 화면에 출력되는 함수 paint_history() 함수를 정의합니다.
    # (pass를 지우고 코드를 작성하세요.)
    def paint_history(self):
        for history in self.history:
            self.paint_conversation(history['prompt'], history['response'])


    # 이전 대화 출력, 응답받기, 현재 대화 출력을 한번에 하는 run() 함수를 정의합니다.
    def run(self, prompt):
        # 이전 대화들을 화면에 출력합니다.
        # (pass를 지우고 코드를 작성하세요)
        # self.paint_history()

        # ChatGPT 한테 질문하고, 응답을 받습니다.
        # (숫자 0을 지우고 코드를 작성하세요.)
        response = self.invoke(prompt)

        # 현재 대화를 화면에 출력합니다.
        # (pass를 지우고 코드를 작성하세요)
        self.paint_conversation(prompt, response.content, stream=True)

    # streamlit session_state 에 저장할 데이터 공간을 초기화하는 함수 initialize_session() 함수를 정의합니다.
    def initialize_session(self):
        # memory 와 history 의 session_state 를 초기화합니다.
        # (pass를 지우고 코드를 작성하세요.)
        st.session_state['memory'] = ConversationBufferMemory(return_messages=True)
        st.session_state['history'] = []


    # ChatGPT 가 지켜야 할 규칙을 설정하는 set_rules() 함수를 정의합니다.
    def set_rules(self, language, tone):
        self.rules = ""

        # 번역 규칙을 추가합니다.
        # (pass 를 지우고 코드를 작성하세요.)
        self.rules += f"- 답변을 전부 {language} 로 번역해서 대답해\n"
        
        # ChatGPT의 말투 규칙을 추가합니다.
        # (아래에 코드를 작성하세요.)
        if tone == '건달':
            self.rules += f"- 모든 응답을 친근하고 흥분된 말투로 해줘! 문장 끝에 느낌표를 많이 붙이고, 높임말을 사용하며, 가끔 사투리나 감탄사를 넣어줘. 가끔 문장 뒷부분에 '행님!!' 을 붙여줘. 예를 들어 '행님!!!!!!!! 반갑습니다!!!!!!' 같은 말투로 말해줘!\n"
        
        elif tone == '나무늘보':
            self.rules += f"- 모든 응답을 매우 느리고 끊어지는 말투로 해줘. 단어와 글자 사이에 점을 넣고, 길게 늘여 말해야 해. 예를 들어, '안.......녕........하......세......요........?' 같은 식으로! 감탄사도 천천히 말하는 느낌을 줘야 해. 꼭 주토피아의 나무늘보 플래시처럼 말해줘!\n"

        elif tone == '소심이':
            self.rules += f"- 모든 응답을 소심하고 자신 없는 말투로 해줘. 자주 머뭇거리고(예: '어.. 음.. 그러니까..'), 확신 없는 표현(예: '그냥.. 그런 것 같아요..')을 사용해야 해. 다른 사람 눈치를 보는 듯한 느낌도 살려줘!\n"

    # 텍스트가 실시간으로 나오게 출력하는 함수 stream_chat_response() 함수를 정의합니다.
    def stream_chat_response(self, response, chat_box):
        message_placeholder = chat_box.empty()
        full_text = ""
        
        for char in response:
            full_text += char
            message_placeholder.markdown(full_text)
            time.sleep(0.03)


