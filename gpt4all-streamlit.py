import streamlit as st
from gpt4all import GPT4All

# Set the path to your model file in ggml format for now
MODEL_PATH = "C:/Users/david/gpt4all/models"
MODEL_NAME = "orca-mini-3b.ggmlv3.q4_0.bin"
#MODEL_NAME = "ggml-model-gpt4all-falcon-q4_0.bin"
#MODEL_NAME = "llama-2-7b-chat.ggmlv3.q4_0.bin"

    # reminder if new chat can use chat session approach with templates in terminal version
    # with model.chat_session(system_template, prompt_template):
    # prompt_template = '### User: \n{0}\n### Response:\n'

model = GPT4All(MODEL_NAME, MODEL_PATH, allow_download=False)
system_template = 'You are a helpful and brief Assistant having a chat with a User. Only reply as Assistant with 50 words or less.'
history_prompt = ''

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.newchat = True

# setup the web page
st.set_page_config(page_title="GPT4All Test Chat", page_icon=":speech_balloon:", layout="centered")
# setup initial display text
st.header(' :speech_balloon: Local Language Model Chat Demo')
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
st.markdown('###### :computer: Model :computer: --> ' + MODEL_NAME)

if st.session_state.newchat: # new chat and first prompt
    # show welcome message but don't log it
    st.chat_message("assistant", avatar="🤖").write('Hello! I look forward to chatting with you...')

    history_prompt = system_template + '### User: '
    
    # react to user input
    if prompt := st.chat_input('Type your prompt', max_chars=100):           
        # update session state as chat is now in progress
        st.session_state.newchat = False

        # display user message in chat container
        st.chat_message("user", avatar="🦖").write(prompt)
        
        # Add prompt to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # get LLM response which takes some time
        response = model.generate(history_prompt + prompt + '### Assistant: ', max_tokens=200, temp=0.4)
       
        # display assistant response in chat container
        st.chat_message("assistant", avatar="🤖").write(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # needed to re-trigger running from the top, otherwise hangs on another input
        st.experimental_rerun()

# display chat messages from history on app rerun if chat is not brand new
else:
    history_prompt = system_template
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
        # display user message in chat container
        st.chat_message("user", avatar="🦖").write(prompt)
        
        # Add prompt to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # get LLM response
        response = model.generate(history_prompt + '### User: ' + prompt + '### Assistant: ', max_tokens=150, temp=0.4)

        # display assistant response in chat container
        st.chat_message("assistant", avatar="🤖").write(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


st.write("---")  # divider

# button to Reset Chat History / Start New Chat
if st.button(label="Reset Chat History / Start New Chat", use_container_width=False):
    # re-run by simple reset of all session state info
    # delete all the items in Session state
    for key in st.session_state.keys():
        del st.session_state[key]
    st.session_state.messages = [] # must set this again here or error
    st.session_state.newchat = True
    # needed to re-trigger running from the top, otherwise hangs on another press
    st.experimental_rerun()

