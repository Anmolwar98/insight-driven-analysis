## Import Dependencies
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st
import os

# Load env properties
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")

llm_model = ChatOpenAI(api_key=api_key)


## Define schema
class ChatBotSchema(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


## define chat Node
def chat_node(state: ChatBotSchema):
    message = state['messages']
    response = llm_model.invoke(message)
    return {'messages': [response]}

## define graph
graph =StateGraph(ChatBotSchema)

## Add Nodes
graph.add_node('chat_node', chat_node)

## Add Edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)


## define InMemorySaver
checkpointer = InMemorySaver()

## graph compile
bot = graph.compile(checkpointer=checkpointer)

response = bot.invoke(
    {'messages':[HumanMessage(content='Hi my name is anuj')]},
    config={'configurable':{'thread_id':'random'}}
)
print(bot.get_state(config={'configurable':{'thread_id':'random'}}).values['messages'])
