from langchain_community.llms import Ollama
import streamlit as st
import os


try:
    cllm = Ollama(model="llama3:8b")
    st.write("Model initialized successfully.")
except Exception as e:
    st.error(f"Model initialization failed: {str(e)}")


st.title("Chatbot using Llama3 8B")

prompt = st.text_area("Enter your prompt:")

uploaded_file = st.file_uploader("Choose a document", type=["txt", "pdf", "docx"])


def read_file(file):
    if file.type == "text/plain":
        return file.read().decode("utf-8")
    elif file.type == "application/pdf":
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
        return text
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        import docx
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    return ""


if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


if st.session_state.chat_history:
    st.write("Chat History:")
    for chat in st.session_state.chat_history:
        st.write(f"**You:** {chat['prompt']}")
        st.write(f"**Bot:** {chat['response']}")


if st.button("Generate"):
    if prompt or uploaded_file:
        with st.spinner("Generating response..."):
            try:
               
                file_content = ""
                if uploaded_file:
                    file_content = read_file(uploaded_file)
                
             
                combined_prompt = prompt + "\n" + file_content if file_content else prompt
                
                st.write("Debug: Combined Prompt ->", combined_prompt)
                
                
                try:
                    response = cllm.invoke(combined_prompt)
                    st.write("Debug: Model response ->", response)
                    if response:
                        st.write(response)
                   
                        st.session_state.chat_history.append({'prompt': combined_prompt, 'response': response})
                    else:
                        st.error("No response from the model.")
                except Exception as e:
                    st.error(f"Model invocation failed: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")


if st.button("Clear History"):
    st.session_state.chat_history = []

if st.button("Export History"):
    chat_history_str = "\n".join([f"You: {chat['prompt']}\nBot: {chat['response']}" for chat in st.session_state.chat_history])
    st.download_button(label="Download Chat History", data=chat_history_str, file_name='chat_history.txt', mime='text/plain')
