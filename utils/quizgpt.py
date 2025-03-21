import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
# JSON 모듈을 불러옵니다.
# (pass를 지우고 코드를 작성하세요.)
import json

# 캐시(Cache)를 적용하여 퀴즈를 생성하는 make_quiz() 함수를 정의합니다.
# (아래에 코드를 작성하세요.)
@st.cache_resource()
def make_quiz(topic, _final_chain, num_questions, num_choices, language):
    # 퀴즈 정보들을 생성해 변수 questions 에 반환합니다.
    # (숫자 0을 지우고 코드를)
    questions = _final_chain.invoke({
        'topic': topic,
        'num_questions': num_questions,
        'num_choices': num_choices,
        'language': language
    })

    return questions


# 퀴즈를 생성하고, 맞추는 QuizGPT 클래스를 정의합니다.
class QuizGPT:
    def __init__(self, num_questions, num_choices, language):
        # 전달받은 변수를 클래스 변수에서 사용할 수 있도록 저장하세요.
        # (아래에 코드를 작성하세요.)
        self.num_questions = num_questions
        self.num_choices = num_choices
        self.language = language

        # ChatGPT 모델을 생성합니다.
        # (숫자 0을 지우고 코드를 작성하세요.)
        self.llm = ChatOpenAI(temperature=0.2, model='gpt-4o-mini')

        # 퀴즈 생성 프롬프트 템플릿을 생성합니다.
        # (숫자 0을 지우고 코드를 작성하세요.)
        self.question_template = ChatPromptTemplate.from_messages([
            ('system', self.get_question_template()),
            ('human', "{topic}")
        ])

        # 퀴즈 생성 체인을 생성합니다.
        # (숫자 0을 지우고 코드를 작성하세요.)
        self.question_chain = self.question_template | self.llm

        # 퀴즈 정보 변환 프롬프트 템플릿을 생성합니다.
        # (숫자 0을 지우고 코드를 작성하세요.)
        self.formatting_template = ChatPromptTemplate.from_messages([
            ('system', self.get_formatting_template()),
            ('human', "{questions}")
        ])

        # 퀴즈 정보 변환 체인을 생성합니다.
        # (숫자 0을 지우고 코드를 작성하세요.)
        self.format_chain = self.formatting_template | self.llm

        # 퀴즈 생성과 변환을 연결하는 체인을 생성합니다.
        # (숫자 0을 지우고 코드를 작성하세요.)
        self.final_chain = {"questions": self.question_chain} | self.format_chain

    # 퀴즈 주제(topic)를 전달받아 퀴즈를 생성하고, 화면에 출력하고, 정답을 체크하는 run() 함수를 정의합니다.
    def run(self, topic):
        # [ 코드 체크 ] 테스트할 코드를 아래에 작성합니다.
        # (아래에 코드를 작성하세요.)
        

        # 퀴즈 정보들을 생성해 변수 questions 에 반환합니다.
        # (숫자 0을 지우고 코드를 작성하세요.)
        questions = self.invoke(topic)
    
        # 퀴즈를 화면에 출력하고, 정답인지 체크하는 코드를 실행합니다.
        # (pass를 지우고 코드를 작성하세요.)
        self.paint_and_check_quiz(questions)
        
    # JSON 을 python 자료형 형태로 변환해주는 json_parse() 함수를 정의합니다.
    def json_parse(self, text):
        # 전달받은 JSON 형태의 text 에서 ```json 과 ``` 문자열 부분을 제거합니다.
        # (숫자 0을 지우고 코드를 작성하세요.)
        text = text.replace("```json", "").replace("```", "")

        # JSON 을 Python 에서 사용할 수 있는 자료형 형태로 변환한 후, 반환(return) 합니다.
        # (pass를 지우고 코드를 작성하세요.)
        return json.loads(text)

    # 주제(topic)를 전달받아, 해당 퀴즈 문제들을 받은 후 JSON 형태를 Python 자료형으로 변환하는 invoke() 함수를 정의합니다.
    def invoke(self, topic):
        # # 주제(topic)를 전달받아, JSON 형태의 퀴즈 문제들을 받도록 코드를 작성하세요.
        # (아래에 코드를 작성하세요.)
        questions = make_quiz(topic, self.final_chain, self.num_questions, self.num_choices, self.language)

        # # JSON 을 python 자료형 형태로 변환하는 코드를 작성하세요.
        # (숫자 0을 지우고 코드를 작성하세요.)
        questions = self.json_parse(questions.content)

        return questions

    # 데이터화된 퀴즈 문제들을 웹 페이지 화면에 출력하고, 정답인지 아닌지 체크하는 paint_and_check_quiz() 함수를 정의합니다.
    def paint_and_check_quiz(self, questions):
        # 퀴즈 폼(Form)을 생성합니다.
        with st.form('questions_form'):
            # 정답 개수를 저장할 변수를 생성합니다.
            # (pass를 지우고 코드를 작성하세요.)
            correct = 0

            # 총 문제 개수를 저장합니다.
            # (pass를 지우고 코드를 작성하세요.)
            total_question = len(questions)

            # 퀴즈 문제를 하나씩 가져옵니다.
            # (pass를 지우고 코드를 작성하세요.)
            for idx, question in enumerate(questions):
                # 퀴즈 문제가 들어갈 박스를 생성합니다. (테두리 있음)
                # (pass를 지우고 코드를 작성하세요.)
                container = st.container(border=True)

                # 박스 안에 가져온 퀴즈의 지문을 출력합니다.
                # (pass를 지우고 코드를 작성하세요.)
                container.markdown(f"### Q{idx + 1}. {question['question']}")
    
                # 문제 보기를 선택할 수 있도록 그려줍니다.
                # (아래에 코드를 작성하세요.)
                select = container.radio(
                    "정답을 선택해 주세요.", 
                    options=[answer['answer'] for answer in question['answers']],
                    index=None,
                    label_visibility="hidden"
                )

                # 정답이 맞는지 확인합니다.
                # (아래에 코드를 작성하세요.)
                if {"answer": select, "correct": True} in question['answers']:
                    correct += 1
                    container.success("✅ 정답!")
                elif select != None:
                    container.error("❌ 오답!")
                    container.markdown(f"📖 {question['explaination']}")

            # 모든 문제를 맞추면, 풍선이 나오도록 합니다.
            # (아래에 코드를 작성해 주세요.)
            if correct == total_question:
                st.balloons()

            # 전송 버튼을 생성합니다. (Form 을 만들면 무조건 전송 버튼을 생성해줘야 합니다.)
            # (pass를 지우고 코드를 작성하세요.)
            st.form_submit_button()

    # 퀴즈 출제 프롬프트를 반환하는 get_question_template() 함수입니다.
    def get_question_template(self):
        prompt = """
            ### Instruction (지시) ###
            너는 주어지는 주제(topic)에 대한 퀴즈를 만드는 뛰어난 퀴즈 출제자야.
            다음 정보를 바탕으로 퀴즈 문제를 출제해줘.

            ```
            문제 개수 : {num_questions}
            객관식 보기 개수: {num_choices}
            번역 언어 : {language}
            ```
            
            객관식 보기 중에 하나만 정답이고 나머지는 오답이어야 해.

            꼭 위 지시를 지켜줘야 해. 반드시 이것을 성공해야 하고, 못하면 너는 벌점을 받게 될 거야.
            특히, 잘못된 정답이 없는지 여러 번 확인해. 절대 틀린 내용이 있어서는 안돼.
            
            ### Example (예시) ###
            퀴즈 출력은 무조건 다음 예시에 맞춰 출력해줘.
            다음 예시는 4개의 문제가 있고, 각각 5개의 보기(선택지)가 있어. 꼭 하나의 답과 나머지의 오답으로 되어있고, 정답 옆에 (O) 로 표시해줘. 보기(선택지)의 개수는 달라질 수 있어.
            그리고 답에 대한 해설을 찾아서 작성해줘.

            ```
            Question: 바다 색깔은 무슨 색이야 ?
            Answers: 빨강 | 노랑 | 초록 | 파랑 (O) | 주황
            Explaination: 바다는 빛의 산란 때문인데, 특히 파란빛이 가장 많이 산란되어 파랗게 보입니다.
                
            Question: 영국의 수도는 어디야 ?
            Answers: 런던 (O) | 리스본 | 서울 | 워싱턴 D.C | 베이징
            Explaination: 런던은 테임즈강을 따라 발전한 영국의 정치·경제 중심지로, 역사적으로 수도가 되었습니다.
                
            Question: 영화 아바타의 개봉년도는 ?
            Answers: 2007 | 2001 | 2009 (O) | 1998 | 2015
            Explaination: 영화 《아바타》는 제임스 카메론 감독이 제작하여 2009년에 개봉했습니다.
                
            Question: 5 x 4 x 3 x 2 x 1 의 답은 ?
            Answers: 600 | 120 (O) | 0 | 150 | 320
            Explaination: 5 × 4 × 3 × 2 × 1은 **5! (팩토리얼)**이며, 계산하면 120입니다.
            ```
        """

        return prompt
    
    def get_formatting_template(self):
        prompt = """
            ### Instruction (지시) ###
            너는 강력한 포맷 알고리즘이야. 너는 주어지는 퀴즈를 JSON 형태로 변환해야 해.
            꼭 위 지시를 지켜줘야 해. 반드시 이것을 성공해야 하고, 못하면 너는 벌점을 받게 될 거야.

            ### Example Input (입력 예시) ###
            ```
            Question: 바다 색깔은 무슨 색이야 ?
            Answers: 빨강 | 노랑 | 초록 | 파랑 (O) | 주황
            Explaination: 바다는 빛의 산란 때문인데, 특히 파란빛이 가장 많이 산란되어 파랗게 보입니다.
                
            Question: 영국의 수도는 어디야 ?
            Answers: 런던 (O) | 리스본 | 서울 | 워싱턴 D.C | 베이징
            Explaination: 런던은 테임즈강을 따라 발전한 영국의 정치·경제 중심지로, 역사적으로 수도가 되었습니다.
                
            Question: 영화 아바타의 개봉년도는 ?
            Answers: 2007 | 2001 | 2009 (O) | 1998 | 2015
            Explaination: 영화 《아바타》는 제임스 카메론 감독이 제작하여 2009년에 개봉했습니다.
                
            Question: 5 x 4 x 3 x 2 x 1 의 답은 ?
            Answers: 600 | 120 (O) | 0 | 150 | 320
            Explaination: 5 × 4 × 3 × 2 × 1은 **5! (팩토리얼)**이며, 계산하면 120입니다.
            ```

            ### Format (변환) ###
            ```json
            [
                {{
                    "question": "바다 색깔은 무슨 색이야 ?",
                    "answers" : [
                        {{"answer": "빨강", "correct": False}},
                        {{"answer": "노랑", "correct": False}},
                        {{"answer": "초록", "correct": False}},
                        {{"answer": "파랑", "correct": True}},
                        {{"answer": "주황", "correct": False}},
                    ],
                    "explaination": "바다는 빛의 산란 때문인데, 특히 파란빛이 가장 많이 산란되어 파랗게 보입니다."
                }},
                {{
                    "question": "영국의 수도는 어디야 ?",
                    "answers" : [
                        {{"answer": "런던", "correct": True}},
                        {{"answer": "리스본","correct": False}},
                        {{"answer": "서울", "correct": False}},
                        {{"answer": "워싱턴 D.C", "correct": True}},
                        {{"answer": "베이징", "correct": False}},
                    ],
                    "explaination": "런던은 테임즈강을 따라 발전한 영국의 정치·경제 중심지로, 역사적으로 수도가 되었습니다."
                }},
                {{
                    "question": "영화 아바타의 개봉년도는 ?",
                    "answers" : [
                        {{"answer": "2007", "correct": False}},
                        {{"answer": "2001", "correct": False}},
                        {{"answer": "2009", "correct": True}},
                        {{"answer": "1998", "correct": False}},
                        {{"answer": "2015", "correct": False}},
                    ],
                    "explaination": "영화 《아바타》는 제임스 카메론 감독이 제작하여 2009년에 개봉했습니다."
                }},
                {{
                    "question": "5 x 4 x 3 x 2 x 1 의 답은 ?",
                    "answers" : [
                        {{"answer": "600", "correct": False}},
                        {{"answer": "120", "correct": True}},
                        {{"answer": "0", "correct": False}},
                        {{"answer": "150", "correct": False}},
                        {{"answer": "320", "correct": False}},
                    ],
                    "explaination": "5 × 4 × 3 × 2 × 1은 **5! (팩토리얼)**이며, 계산하면 120입니다."
                }},
            ]
            ```
        """

        return prompt