import uuid
import streamlit as st
from langraph_backend import bot, checkpointer

def generate_thread_id():
    '''This will generate a thread ID'''
    return uuid.uuid4()


def reset_chat_window():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['message_history']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = bot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])

def retrieve_threads():
    all_threads = set()
    for pointer in checkpointer.list(None):
        all_threads.add(pointer.config['configurable']['thread_id'])
    
    return list(all_threads)