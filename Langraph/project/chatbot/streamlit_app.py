import streamlit as st
from langraph_backend import bot
from langchain_core.messages import HumanMessage
from utilities import generate_thread_id, reset_chat_window, add_thread, load_conversation


#************************************Session Setup************************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=[]

add_thread(st.session_state['thread_id'])


#************************************ Sidebar UI************************************
if st.sidebar.button('Start New Conversation'):
    reset_chat_window()

st.sidebar.header('Chat History')

for thread_id in st.session_state['chat_threads'][::-1]:
    # Load the first message to show as preview
    messages = load_conversation(thread_id)
    preview_text = "New Conversation"
    
    if messages:
        # Get the first message content
        first_msg = messages[0].content if hasattr(messages[0], 'content') else str(messages[0])
        # Show first 40 characters of the message
        preview_text = first_msg[:30] + "..." if len(first_msg) > 30 else first_msg
    
    if st.sidebar.button(preview_text, key=thread_id):
        st.session_state['thread_id']=thread_id
        messages = load_conversation(thread_id)

        temp_message = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'ai'
            temp_message.append({'role':'role','content':msg.content})
        st.session_state['message_history'] = temp_message

#************************************Main UI Code************************************

## Loading the conversation
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

## User Input Box
user_input = st.chat_input('Type Here')

CONFIG = {'configurable':{'thread_id':st.session_state['thread_id']}}


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

