import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from template import css, bot_template, user_template
import os
from langchain_together import Together
from dotenv import load_dotenv
load_dotenv()

TOGETHER_API = os.getenv("TOGETHER_API")


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="nomic-ai/nomic-embed-text-v1", model_kwargs={"trust_remote_code": True})
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = Together(model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                temperature=0.7, max_tokens=450,
                  together_api_key=TOGETHER_API)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vectorstore.as_retriever(), memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    if st.session_state.conversation is not None:
        response = st.session_state.conversation({"question": user_question})
        st.session_state.chat_history = response["chat_history"]

        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(
                    user_template.replace("{{MSG}}", message.content),
                    unsafe_allow_html=True,
                )
            else:
                st.write(
                    bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True
                )

def main():
    st.set_page_config(page_title="Chatbot")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "show_uploader" not in st.session_state:
        st.session_state.show_uploader = False
    

    st.header("Chatbot for PDFs")

    col1, col2 = st.columns([9, 1])

    with col1:
        user_question = st.text_input("Ask a question about your documents:", key="user_question")
        
        if st.button("Ask"):
            handle_userinput(user_question)
    
    with col2:
        if st.button("📁"):
            st.session_state.show_uploader = True
            st.session_state.conversation = None
            st.session_state.chat_history = None
            #st.session_state.reset_trigger = True
            st.rerun()

    if st.session_state.show_uploader:
        with st.expander("Upload PDFs", expanded=True):
            pdf_docs = st.file_uploader(
                "Upload your PDFs here and click on 'Add Data'", accept_multiple_files=True
            )
            if st.button("Add Data"):
                if pdf_docs:
                    with st.spinner("Adding Data..."):
                        raw_text = get_pdf_text(pdf_docs)

                        text_chunks = get_text_chunks(raw_text)

                        vectorstore = get_vectorstore(text_chunks)

                        st.session_state.conversation = get_conversation_chain(vectorstore)
                        st.session_state.show_uploader = False
                        st.rerun()
    

if __name__ == "__main__":
    main()
