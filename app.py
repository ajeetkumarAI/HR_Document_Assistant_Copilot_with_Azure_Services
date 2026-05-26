import streamlit as st

from src.rag_pipeline import get_answer
from src.blob_storage import list_blobs

from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="HR Policy Assistant", page_icon=":robot_face:", layout="centered")
st.title("HR Policy Assistant Chatbot")

# ── Sidebar: documents stored in Azure Blob Storage ──────────
with st.sidebar:
    st.header("Indexed Documents")
    if st.button("Refresh"):
        st.session_state.pop("blob_list", None)

    if "blob_list" not in st.session_state:
        try:
            st.session_state["blob_list"] = list_blobs()
        except Exception as e:
            st.error(f"Could not list blobs: {e}")
            st.session_state["blob_list"] = []

    if st.session_state["blob_list"]:
        for name in st.session_state["blob_list"]:
            st.write(f"- {name}")
    else:
        st.info("No documents in blob storage yet.")

# ── Question Answering ───────────────────────────────────────
st.subheader("Ask a question about the HR policies")

question = st.text_input("Enter your question here", key="question_input")

if st.button("Get Answer"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Querying Azure AI Search & Azure OpenAI …"):
            try:
                answer = get_answer(question)
                st.markdown(f"**Answer:** {answer}")
            except Exception as e:
                st.error(f"Error getting answer: {e}")