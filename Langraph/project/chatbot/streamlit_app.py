import streamlit as st
from langraph_backend import bot, CONFIG
from langchain_core.messages import HumanMessage

message_history = st.session_state  # it is a dictionary which retained the conversation history
CONFIG = {'configurable':{'thread_id':"random_id"}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

## Loading the conversation
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

## User Input Box
user_input = st.chat_input('Type Here')

if user_input:
    ## Appending the user input into a Dictionary
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)


    # ## Loading the AI input into a Dictionary
    with st.chat_message('ai'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, _ in bot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                stream_mode="messages",
                config = CONFIG
            )
        )
    st.session_state['message_history'].append({'role':'ai','content':ai_message})

