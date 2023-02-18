import streamlit as st
from components.sidebar import sidebar
from openai.error import OpenAIError
from utils import (
    embed_docs,
    get_answer,
    get_sources,
    parse_docx,
    parse_pdf,
    parse_txt,
    search_docs,
    text_to_docs,
    wrap_text_in_html,
)


def clear_submit():
    st.session_state["submit"] = False


st.set_page_config(page_title="UAPDF2GPT", page_icon="📖", layout="wide")
st.header("ПДФАНАЛІТИКА")

sidebar()

uploaded_file = st.file_uploader(
    "Загрузити pdf, docx, or txt file",
    type=["pdf", "docx", "txt"],
    help="Відскановані документи не підтримаються!(поки що)",
    on_change=clear_submit,
)

index = None
doc = None
if uploaded_file is not None:
    if uploaded_file.name.endswith(".pdf"):
        doc = parse_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        doc = parse_docx(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        doc = parse_txt(uploaded_file)
    else:
        raise ValueError("Відскановані документи не підтримаються!(поки що)!")
    text = text_to_docs(doc)
    try:
        with st.spinner("Індексація документа... Трошки почекайте⏳"):
            index = embed_docs(text)
        st.session_state["api_key_configured"] = True
    except OpenAIError as e:
        st.error(e._message)

query = st.text_area("Задайте питання щодо інформації в документі", on_change=clear_submit)
with st.expander("Додаткові Опції"):
    show_all_chunks = st.checkbox("Показати всі фрагменти, знайдені в результаті векторного пошуку")
    show_full_doc = st.checkbox("Показати парсинг вмісту документу")

if show_full_doc and doc:
    with st.expander("Документ"):
        # Hack to get around st.markdown rendering LaTeX
        st.markdown(f"<p>{wrap_text_in_html(doc)}</p>", unsafe_allow_html=True)

button = st.button("Надіслати")
if button or st.session_state.get("submit"):
    if not st.session_state.get("api_key_configured"):
        st.error("Будь ласка введіть ваш OpenAI API key!")
    elif not index:
        st.error("Будь ласка загрузіть документ!")
    elif not query:
        st.error("Введіть ваше запитання!")
    else:
        st.session_state["submit"] = True
        # Output Columns
        answer_col, sources_col = st.columns(2)
        sources = search_docs(index, query)

        try:
            answer = get_answer(sources, query)
            if not show_all_chunks:
                # Get the sources for the answer
                sources = get_sources(answer, sources)

            with answer_col:
                st.markdown("#### Answer")
                st.markdown(answer["output_text"].split("SOURCES: ")[0])

            with sources_col:
                st.markdown("#### Sources")
                for source in sources:
                    st.markdown(source.page_content)
                    st.markdown(source.metadata["source"])
                    st.markdown("---")

        except OpenAIError as e:
            st.error(e._message)
