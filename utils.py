import assemblyai as aai
import streamlit as st
from yt_dlp import YoutubeDL

YTDLP_FNAME = 'temp.webm'

#returns the temp name of the file for youyube video
def return_ytdlp_fname():
    return YTDLP_FNAME

#returns a transcription from the selecte method - file / remote file / yt video
def get_transcript(f, ftype):
    transcriber = aai.Transcriber()

    if ftype == "Youtube Video":
        with st.spinner("Downloading video..."):
            ydl_opts = {'outtmpl': YTDLP_FNAME}
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([f])
                f = YTDLP_FNAME


    with st.spinner("Transcribing file..."):
        transcript = transcriber.transcribe(f)
    
    #custom exception
    if transcript.error:
        raise TranscriptionException(transcript.error)
    
    return transcript    


def ask_question(transcript, question):

    questions = [
        aai.LemurQuestion(question=question)
    ]

    result = transcript.lemur.question(questions)

    if transcript.error:
        raise QuestionException(result.error)
    
    return result.response[0].answer

class TranscriptionException(Exception):
    pass


class QuestionException(Exception):
    pass