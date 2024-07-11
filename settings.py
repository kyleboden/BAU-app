import streamlit as st


def questionCSS(question_text):
    st.markdown(f"<p style='font-size: 17px; font-family: Arial, sans-serif; margin-bottom: -100px;'>{question_text}</p>", unsafe_allow_html=True)


