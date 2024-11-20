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


llm = OpenAI(api_token=os.environ.get("OPENAI_API_KEY"))

st.sidebar.title("PandasAI")

st.sidebar.subheader("Configuration")

OpenAI_API_KEY = st.sidebar.text_input("OpenAI API Key", type="password")
explain = st.sidebar.toggle("Explain", False, key="explain")
questions = st.sidebar.toggle("Questions", False, key="questions")

st.sidebar.subheader("Data")
csv_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# csv_file = st.file_uploader("Upload a CSV file", type=["csv"])

if csv_file:

    df = pd.read_csv(csv_file)
    # st.write(df.head(5))
    columns = df.columns
    column_selection = st.multiselect("Column Selector", columns, list(columns))

    if column_selection:
        df = df[column_selection]
        st.write(df.head(5))

    prompt = st.text_area("Prompt")

    if st.button("Process"):

        if not OpenAI_API_KEY:
            st.error("Please provide an OpenAI API Key")
            st.stop()

        if prompt:
            
            with st.spinner("Processing..."):
                #sdf = SmartDataframe(df, config={"llm": llm, "verbose": True, "response_parser": StreamlitResponse})
                agent = Agent(df, config={"llm": llm, "verbose": True, "response_parser": StreamlitResponse}, memory_size=5)
                #response = sdf.chat(prompt)
                response = agent.chat(prompt)
                if os.path.isfile(response):
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
                
        else:
            st.error("Please provide a prompt")
                       
       