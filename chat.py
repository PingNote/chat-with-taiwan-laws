import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory

# Load embeddings and database
embeddings = OpenAIEmbeddings()
db = FAISS.load_local("faiss_index", embeddings)

# Create a retrieval chain with the ChatOpenAI model
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
chain = ConversationalRetrievalChain.from_llm(llm=ChatOpenAI(model_name="gpt-4", temperature=0), retriever=db.as_retriever(), memory=memory)

st.set_page_config(
    page_title="Chat with Taiwan Laws",
    page_icon=":robot:"
)

st.title("台灣法規 Chat AI")
st.markdown("""
[![](https://img.shields.io/badge/tpai/chat_with_taiwan_laws-grey?style=flat-square&logo=github)](https://github.com/tpai/chat-with-taiwan-laws)
""")
st.markdown("""
本工具引用自全國法規資料庫之[民法](https://law.moj.gov.tw/Hot/AddHotLaw.ashx?pcode=B0000001)、[中華民國刑法](https://law.moj.gov.tw/Hot/AddHotLaw.ashx?pcode=C0000001)、[刑事訴訟法](https://law.moj.gov.tw/Hot/AddHotLaw.ashx?pcode=C0010001)、[勞動基準法](https://law.moj.gov.tw/Hot/AddHotLaw.ashx?pcode=N0030001)、[勞工退休金條例](https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0030020)以及[職業安全衛生設施條例](https://law.moj.gov.tw/Hot/AddHotLaw.ashx?pcode=N0060009)之 PDF 檔案，本工具僅供研究和學習使用，如有法律需求請諮詢專業律師。
""")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("請輸入對話：","你好", key="input")
    return input_text 

question = get_text()

if question:
    with st.spinner("🤖 對話生成中，請稍候..."):
        output = chain({"question": f"{question} 請用台灣繁體中文簡單回答"}, return_only_outputs=True)
        st.session_state.past.append(question)
        st.session_state.generated.append(output["answer"])

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')