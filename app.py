import streamlit as st

pages = {
    "MENU" : [
        st.Page("./navigations/my_chatgpt.py", title="My ChatGPT"),
        st.Page("./navigations/quiz_gpt.py", title="QuizGPT"),
        st.Page("./navigations/image_generator.py", title="Image Generator"),
    ]
}

pg = st.navigation(pages)
pg.run()
