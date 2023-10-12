# gpt4all2-streamlit.py
# run via terminal> streamlit run gpt4all2-streamlit.py

import streamlit as st
from gpt4all import GPT4All

# Set the path to your model file in ggml format for now
MODEL_PATH = "C:/Users/david/gpt4all/models"
SYSTEM_TEMPLATE = 'You are a helpful and brief Assistant having a chat with a User. \
    Only reply as Assistant with 50 words or less.'

def init_page():
    # Initialize page
    st.set_page_config(
        page_title="GPT4All Test Chat",
        page_icon=":speech_balloon:",
        layout="centered"
    )
    # setup initial display text
    st.header(' :speech_balloon: Local Language Model Chat Demo')
    st.markdown('<style>div.block-container{padding-top:2rem;}</style>',
        unsafe_allow_html=True
    )
    st.markdown('###### :computer: Model Path :computer: --> ' + MODEL_PATH)
    st.sidebar.title("Options")
    return

def select_model():
    model_name = st.sidebar.radio(
        "Choose an LLM:", (
            "llama-2-7b-chat.ggmlv3.q4_0.bin",
            "orca-mini-3b.ggmlv3.q4_0.bin",
            "ggml-model-gpt4all-falcon-q4_0.bin"
        )
    )
    # Select the model to run via GPT4All, llama works well
    model = GPT4All(model_name, MODEL_PATH, allow_download=False)
    return model

def init_session():
    # Initialize system state or clear it
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        # delete all the items in Session state
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state.messages = []
        st.session_state.newchat = True   
    return

def first_message(model):
    # show welcome message but don't log it
    with st.chat_message("assistant", avatar="🤖"):
        st.write('Hello! I look forward to chatting with you...')

    history_prompt = SYSTEM_TEMPLATE + '### User: '
    
    # react to user input
    if prompt := st.chat_input('Type your prompt', max_chars=100):           
        # update session state as chat is now in progress
        st.session_state.newchat = False

        with st.chat_message("user", avatar="🦖"):
        # display user message in chat container
            st.write(prompt)
        
        # Add prompt to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # get LLM response which takes some time
        response = model.generate(history_prompt + prompt + '### Assistant: ', max_tokens=200, temp=0.4)
    
        with st.chat_message("assistant", avatar="🤖"):
        # display assistant response in chat container
            st.write(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # needed to re-trigger running from the top, otherwise hangs on another input
        st.experimental_rerun()
    return

def next_message(model):
    history_prompt = SYSTEM_TEMPLATE
    
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message(message["role"], avatar="🤖"):
                st.markdown(message["content"])
            # write into history_prompt as assistant
            history_prompt = history_prompt + '### Assistant: ' + message["content"]
        else:
            with st.chat_message(message["role"], avatar="🦖"):
                st.markdown(message["content"])
            # write into history_prompt as user
            history_prompt = history_prompt + '### User: ' + message["content"]

    # react to user input and feed history into the prompt with new user prompt too
    if prompt := st.chat_input('Type your next prompt', max_chars=100):           
        with st.chat_message("user", avatar="🦖"):
            # display user message in chat container
            st.write(prompt)
        
        # Add prompt to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # get LLM response
        response = model.generate(history_prompt + '### User: ' + prompt + '### Assistant: ', max_tokens=150, temp=0.4)

        with st.chat_message("assistant", avatar="🤖"):
            # display assistant response in chat container
            st.write(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    return

def main():
    # Main program
    init_page()
    model = select_model()
    init_session()
    if st.session_state.newchat: # new chat and first prompt
        first_message(model)
    else: # display messages from history on app rerun if chat is not new
        next_message(model)
    st.write("---")  # divider
    return

if __name__ == "__main__":
    main()
