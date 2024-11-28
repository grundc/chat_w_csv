## IMPORTS
# standard 
import os

# 3d paryt
import streamlit as st
from pandasai import SmartDataframe
from pandasai import Agent
from pandasai.llm import OpenAI
import pandas as pd
from pandasai.responses.streamlit_response import StreamlitResponse
import pandasai as pai

# **********************************************
# Setup Session prompt history
if "prompt_history" not in st.session_state:
        st.session_state.prompt_history = []
# **********************************************



st.sidebar.title("PandasAI")
st.sidebar.info("*Configuration*")

OpenAI_API_KEY = st.sidebar.text_input("OpenAI API Key", type="password")
explain = st.sidebar.toggle("Explain", False, key="explain")
questions = st.sidebar.toggle("Questions", False, key="questions")

st.sidebar.info("*Data*")
csv_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])



with st.sidebar:
    st.info("*Prompt History*")
    with st.container(height=200, border=True):
        for item in st.session_state.prompt_history:
            if st.button(f"'{item[:20]}...'", help=f"{item}", use_container_width=True):
                st.session_state.prompt = item  
                
if st.sidebar.button("Clear Cache", type="primary", use_container_width=True):
    pai.clear_cache()
    st.session_state.prompt_history = []
    st.session_state.prompt = ''
# *********************************************************************************

st.title("Chat with your CSV")
if csv_file:
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        st.stop()
        
    # st.write(df.head(5))
    columns = df.columns
    column_selection = st.multiselect("Column Selector", columns, list(columns))

    if column_selection:
        df = df[column_selection]
        st.write(df.head(5))
    
    
    st.subheader("Prompt")
    prompt = st.text_area("", value=st.session_state.prompt)

    if st.button("Process"):

        if not OpenAI_API_KEY:
            st.error("Please provide an OpenAI API Key")
            st.stop()
        else:
            llm = OpenAI(api_token=OpenAI_API_KEY)

        if prompt:
            
            with st.spinner("Processing..."):
                #sdf = SmartDataframe(df, config={"llm": llm, "verbose": True, "response_parser": StreamlitResponse})
                agent = Agent(df, config={"llm": llm, "verbose": True, "response_parser": StreamlitResponse}, memory_size=5)
                #response = sdf.chat(prompt)
                response = agent.chat(prompt)
                if os.path.isfile(str(response)):
                    st.image(response)
                else:
                    st.write(response)
                
                if explain:
                    st.info("Explanation")
                    explanation = agent.explain()
                    st.write(explanation)
                if questions:
                    st.info("Clarification Questions")
                    questions = agent.clarification_questions(prompt)
                    st.markdown("\n".join([f"- {question}" for question in questions]))

            if prompt in st.session_state.prompt_history:
                st.session_state.prompt_history.remove(prompt)
            st.session_state.prompt_history.append(prompt)
                
        else:
            st.error("Please provide a prompt")
        
    
                       
       