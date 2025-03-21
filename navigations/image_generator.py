# Streamlit 을 사용하기 위해 불러옵니다. 이 때, 이름은 st 로 변경해 줍니다.
# (pass를 지우고 코드를 작성하세요.)
import streamlit as st

# 이미지 생성을 위한 openai 라이브러리를 불러옵니다.
# (pass를 지우고 코드를 작성하세요.)
import openai

# 이미지 URL 을 사용하기 위한 requests 라이브러리를 불러옵니다.
# (pass를 지우고 코드를 작성하세요.)
import requests

# [ 확장 2 - 1 ] 이미지를 저장할 DB 를 사용하기 위해 SQLite 라이브러리를 불러옵니다.
# (pass를 지우고 코드를 작성하세요.)
import sqlite3

# =========================== 관련 함수 정의 ===========================
# 이미지 생성 함수를 정의합니다. ( 생성한 이미지는 URL 형태로 나옵니다. )
def generate_image_url(prompt):
    # DALL-E-3 모델을 이용해 생성한 이미지 응답을 받도록 합니다.
    # (아래에 코드를 작성하세요.)
    response = openai.images.generate(
        prompt=prompt,
        model='dall-e-3',
        size="1024x1024",
        n=1
    )
    
    # 응답(response)을 Python 에서 사용할 수 있는 딕셔너리 형태로 변환해 줍니다.
    # (pass를 지우고 코드를 작성하세요.)
    image_dict = response.to_dict()

    # 생성 이미지 딕셔너리 에서 이미지 URL 만 꺼내옵니다.
    # (pass를 지우고 코드를 작성하세요.)
    image_url = image_dict['data'][0]['url']

    # 이미지 URL 을 반환해 줍니다.
    # (pass를 지우고 코드를 작성하세요.)
    return image_url

# [ 확장 1 ] 이미지 URL 을 전달받아, 이미지를 다운로드하는 버튼을 생성하는 함수를 정의합니다.
# [ 필수 ] st.download_button() 을 반드시 사용합니다.
# (아래에 코드를 작성하세요.)
def create_download_button(image_url):
    # 이미지 다운로드 버튼을 생성합니다.
    st.download_button(
        label="이미지 다운로드",
        data=requests.get(image_url).content,
        file_name="generated_image.png",
        mime="image/png"
    )


# [ 확장 2 - 1 ] 이미지 URL 을 전달받아 다운로드한 데이터를 DB 에 저장하는 함수를 정의합니다.
# [ 필수 ] DB 가 생성되어 있지 않다면, 생성하는 코드를 추가해 줍니다.
# [ 필수 ] 단, 이미지의 URL 을 DB 에 저장하는게 아닙니다. 다운로드된 이미지를 저장하는 겁니다.
# (아래에 코드를 작성하세요.)
def save_image_to_db(image_url):
    # 데이터베이스 연결을 생성합니다.
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()

    # 테이블이 존재하지 않으면 생성합니다.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image BLOB NOT NULL
        )
    ''')

    # 이미지를 다운로드합니다.
    image_data = requests.get(image_url).content

    # 이미지를 데이터베이스에 저장합니다.
    cursor.execute('INSERT INTO images (image) VALUES (?)', (image_data,))
    conn.commit()
    conn.close()

# [ 확장 2 - 2 ] SQLite DB 에 저장되어 있는 모든 이미지를 가져와 그리드(Grid) 형식으로 띄워주는 함수를 정의합니다.
# (아래에 코드를 작성하세요.)
def display_images_from_db():
    # SQLite 데이터베이스에 연결합니다.
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()

    # DB에서 모든 이미지를 가져옵니다.
    cursor.execute('SELECT id, image FROM images')  # id도 가져옵니다.
    images = cursor.fetchall()
    conn.close()

    # 이미지를 그리드 형식으로 표시합니다.
    cols = st.columns(3)  # 3개의 열로 나누어 표시합니다.
    for index, (image_id, image_data) in enumerate(images):
        with cols[index % 3]:  # 3개의 열에 이미지를 배치합니다.
            st.image(image_data, width=300)  # 이미지의 너비를 300으로 고정

            # 이미지 다운로드 버튼 생성
            st.download_button(
                label="이미지 다운로드",
                data=image_data,
                file_name=f"image_{index + 1}.png",
                mime="image/png"
            )

            # 쓰레기통 아이콘 생성
            if st.button("🗑️", key=f"delete_{image_id}"):  # 각 이미지에 대해 고유한 키 사용
                delete_image_from_db(image_id)  # DB에서 이미지 삭제
                st.rerun()  # 페이지를 새로 고침하여 변경 사항 반영

# 이미지 삭제 함수 정의
def delete_image_from_db(image_id):
    # SQLite 데이터베이스에 연결합니다.
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()

    # 해당 ID의 이미지를 삭제합니다.
    cursor.execute('DELETE FROM images WHERE id = ?', (image_id,))
    conn.commit()
    conn.close()


# ============================ 웹페이지 UI ============================

# 웹페이지 탭 제목, 아이콘, 화면 레이아웃 크기를 설정합니다.
# (아래에 코드를 작성하세요.)
st.set_page_config(
    page_title="Image Generator",
    page_icon="🎨",
    layout="wide"
)

# 이미지 생성 웹페이지의 제목을 만들어 줍니다.
# (pass를 지우고 코드를 작성하세요.)
st.title("AI Image Generator")

# 어떤 이미지를 생성할지 프롬프트(Prompt)를 입력할 수 있도록 텍스트 입력창을 만들어 줍니다.
# (pass를 지우고 코드를 작성하세요.)
prompt = st.text_input("생성할 이미지 프롬프트를 입력해 주세요.", autocomplete="off")

# 이미지 생성을 시작시키는 버튼을 생성해 줍니다.
# (pass를 지우고 코드를 작성하세요.)
generate_btn = st.button("이미지 생성")

# 생성 버튼을 눌렀을 때, 이미지가 생성되도록 합니다.
# (pass를 지우고 코드를 작성하세요.)
if generate_btn:

    # 이 때, 이미지 프롬프트(prompt)가 입력이 되어있는지 확인합니다.
    # (pass를 지우고 코드를 작성하세요.)
    if prompt:

        # 입력한 프롬프트(Prompt)대로 이미지를 생성하도록 함수를 실행시킵니다.
        # (pass를 지우고 코드를 작성하세요.)
        image_url = generate_image_url(prompt)

        # 이미지 URL 을 이용해 웹페이지에 생성한 이미지를 띄웁니다.
        # (pass를 지우고 코드를 작성하세요.)
        st.image(image_url, use_container_width=True)

        # [ 확장 1 ] 이미지 다운로드 버튼을 생성하는 함수를 실행시 킵니다.
        # (pass를 지우고 코드를 작성하세요.)
        create_download_button(image_url)

        # [ 확장 2 - 1 ] 생성한 이미지를 DB 에 저장하는 함수를 실행시킵니다.
        # (pass를 지우고 코드를 작성하세요.)
        save_image_to_db(image_url)

    # 이미지 프롬프트(prompt)가 입력되어 있지 않다면,
    # (pass를 지우고 코드를 작성하세요.)
    else:

        # 프롬프트를 입력하라는 에러 박스를 띄웁니다.
        # (pass를 지우고 코드를 작성하세요.)
        st.error("이미지 프롬프트를 먼저 입력해 주세요.")

# [ 확장 2 - 2 ] DB 에 저장되어 있는 이미지를 순서대로 가져와 웹페이지에 띄워주는 함수를 실행합니다.
# [ 필수 ] st.toggle() 함수를 사용하여, Toggle 되었을 때만 보이도록 합니다.
# (아래에 코드를 작성하세요.)
if st.toggle("저장된 이미지 보기"):
    display_images_from_db()