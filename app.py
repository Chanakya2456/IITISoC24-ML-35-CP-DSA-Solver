import streamlit as st
import pandas as pd
import time
from rag import *
from llm import *
from scapper import *
from recommender import *
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import GridUpdateMode, DataReturnMode
st.set_page_config(
   page_title="CP/DSA QUESTION SOLVER",
   layout="wide",
   initial_sidebar_state="expanded",
)

st.sidebar.title('CP/DSA QUESTION SOLVER')
def get_answer(language):
    answer = f"This is a simulated answer for the given question in '{language}'"
    return answer
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 500px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)
#st.title("CP/DSA Solver")
st.sidebar.subheader('Select type of question')
question_type = st.sidebar.selectbox(
    "Select type:",
    ("Codeforces","Leetcode","Others")
)
#question_type = st.selectbox("Choose the type of question you would like to enter:", ("Select","CodeForces", "Leetcode", "Others"))

if question_type in ("CodeForces", "Leetcode"):
    question_number = st.sidebar.text_input("Enter question number:")
    # Language dropdown
    language_options = ("C++", "Java", "Python")
    language = st.sidebar.selectbox("Choose language:", language_options)
    data = load_data(language)
    embed = mod()
    database = retriever(embed,data)
else:
    question = st.sidebar.text_input("Enter your question:")
    language = None  

submit = st.sidebar.button("Submit")


if submit:
    if(question_type == "Leetcode"):
        if(question_number in data["index"]):
            question = scrape_leetcode(question_number)
            answer = leetcode(question,database)
        else:
            question = scrapeL(question_number)
            answer = leetcode(question,database)
    elif(question_type == "Codeforces"):
        question, tag_lst, Rating = scrapecf(question_number)
        answer = codeforces_problem(question)
    else:
        answer = new_problem(question)
    # Clear layout for better presentation (optional)
    st.empty()
    container = st.container(border=True)
    container.write("### Solution")

    container.markdown(
    """
    <style>.
[data-testid="container"]:nth-child(2){
            background-color: lightgrey;
        }
    </style>
    """,
    unsafe_allow_html=True
)
    # Create two columns for clear output display
    with container:
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.write("*Your question:*")
            if question_type in ("Leetcode", "CodeForces"):
                st.write(f"Question number " + question_number)
            else:
                st.write(question)
        with col2:
            st.write("*Answer:*")
            st.write(answer)
    st.write("##")
    container1 = st.container(border=True)
    container1.write("### Recommender System")
    with container1:
        st.divider()
        st.write("The following are the similar questions we recommend you attempt next:")

        if(question_type == "Leetcode" or "Others"):
            docs = RecommenderL(question,database)
            for i in range(5):
                st.write("Question "+i)
                st.write(docs[i].page_content)
                st.write(" ")
        else:
            problems = recommend_cf(Rating,tag_lst)
            for i in problems:
                st.write(i)
                st.write(" ")

            
