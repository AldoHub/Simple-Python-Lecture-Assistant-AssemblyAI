import os
import assemblyai as aai
import streamlit as st

#import transcriber features
from utils import get_transcript, return_ytdlp_fname, ask_question

#set video temp name
YTDLP_FNAME = return_ytdlp_fname()


#Remove existing temp files in case of improper shutdown
temp_files = [f for f in os.listdir() if f.startswith('tmp')]
for f in temp_files:
    os.remove()


#constants
input_key = None
f = None
entered = None
summary = None
question_submit = None
answer = None

#init state variables
state_strings = ['summary', 'entered', 'transcript']
for s in state_strings:
    if s not in st.session_state:
        st.session_state[s] = None


def set_aai_key():
    aai.settings.api_key = st.session_state.input_aai_key

input_key = st.text_input("API key", key='input_aai_key', on_change=set_aai_key)

"## Lecture"
"""Enter the lecture you would like to summarize below. \
You can use a local file on your computer, a remote file \
that is publicly-available online, or a Youtube video. """

ftype = st.radio("File type", ("Local file", "Remote file", "Youtube link"))

if ftype == 'Local file':
    f = st.file_uploader("File")
    if f:
        uploaded_ftype = f.name.split('.')[-1]
        temp_fname = f"tmp.{uploaded_ftype}"
        with open(temp_fname, 'wb') as fl:
            fl.write(f.read());
        f = temp_fname
elif ftype == 'Remote file':
    f = st.text_input("Link", value='', placeholder='Public link to the file')
elif ftype == 'Youtube link':
    f = st.text_input("Link", value='', placeholder='Youtube link')


context = st.text_input("Context", value="", placeholder="Context about the file or video")

if f:
    entered = st.button("Submit")
    if entered: 
        transcript = get_transcript(f, ftype)
        if ftype == 'Local file':
            os.remove(f)
        elif ftype == 'Youtube link':
            os.remove(YTDLP_FNAME)

        ####---- TODO: 11:46
        st.session_state['transcript'] = transcript

        #define params for the summarization
        params = {
            'answer_format': "**<part of the lesson>**\n <list of important points in that part>",
            'max_output_size': 4000
        }

        with st.spinner("Generating summary..."):
            summary = transcript.lemur.summarize(**params)
            try:
                st.session_state['summary'] = summary.response.strip().split('\n')
                st.session_state['entered'] = True
            except aai.types.LemurError as e:
                st.write(f'Error: {str(e)}')
                st.session_state['entered'] = False    

if st.session_state['entered']:
    "## Results"
    if st.session_state['summary'] :
        for i in st.session_state['summary']:
            st.markdown(i)               


if st.session_state['summary']:
    "## Question"
    "Ask a question about the lesson below"    

    question = st.text_input("Question", placeholder="Type your question about the lesson here")

    question_asked = st.button("Submit", key='question_asked')
    if question_asked:
        with st.spinner('Asking question...'):
            answer = ask_question(st.session_state['transcript'], question)
    answer    

