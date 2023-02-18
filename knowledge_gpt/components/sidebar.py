import streamlit as st


def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key


def sidebar():
    with st.sidebar:
        st.markdown(
            "## Як використовувати\n"
            "1. Введіть ключ [OpenAI API key](https://platform.openai.com/account/api-keys) нижче🔑\n"
            "2. Завантажте pdf, docx, або txt файл📄\n"
            "3. Задайте питання щодо вмісту документа💬\n"
        )
        api_key_input = st.text_input(
            "Ключ OpenAI API",
            type="password",
            placeholder="Введіть ваш ключ OpenAI API тут (sk-...)",
            help="Ключ API key можете отримати тут https://platform.openai.com/account/api-keys.",
            value=st.session_state.get("OPENAI_API_KEY", ""),
        )

        if api_key_input:
            set_openai_api_key(api_key_input)

        st.markdown("---")
        st.markdown("# Про SmartPDF")
        st.markdown(
            "📖SmartPDF дозволяє задавати питання щодо вмісту ваших "
            "документів і отримуйте точні відповіді з миттєвими посиланнями. "
        )
        st.markdown(
            "Програма в бета-версії. "
        )
        st.markdown("---")
        st.markdown("Made by BEZ")
