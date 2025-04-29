import streamlit as st
from dotenv import load_dotenv

load_dotenv()

import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import base64
import io


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content, prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input, pdf_content, prompt])
    return response.text 

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert PDF to images
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_page= images[0]
        
        #convert to bytes
        img_byte_array = io.BytesIO()
        first_page.save(img_byte_array, format='PNG')
        img_byte_array = img_byte_array.getvalue()
        
        pdf_parts ={
                "mime_type": "image/png",
                "data": base64.b64encode(img_byte_array).decode('utf-8'),    
            }
        return pdf_parts
    else:
        raise FileNotFoundError('No file found.')
    
    
#Streamlit

st.set_page_config(page_title="Resume ATS Expert ")
st.header("ATS Tracking System")
input_text = st.text_area("Enter the Job Description here:", key="input")
uploaded_file = st.file_uploader('Upload your resume(PDF)...',type=['pdf'])


if uploaded_file is not None:
    st.write("PDF is Uploaded successfully.")
    
    
    
submit1 = st.button("Tell Me About The Resume")

submit3 = st.button("Percentage Match with Job Description")

submit4 = st.button("What Keywords Are Missing In My Resume?")

submit5 = st.button("How Can I Tailor My Resume?")

input_prompt1 = """
You are a well expereinced Technical Human Resource Manager in the field of Data Science, Software Engineering, Machine Learning and AI, You are given a resume and you have to tell the user about the resume.
Your task is to review and analyze the resume and provide feedback on its strengths and weaknesses for this profiles.
You should also provide suggestions for improvement and highlight any areas that may need further development or clarification.
You should share your professional evaluation on whether the candidate's profile align with the job description and the company culture.
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) expert with a deep understanding of Data Science, Software Engineering, Machine Learning, AI and ATS functionality  . 
Your task is to review and evaluate the resume against the provided job descriptions. First the output should be a percentage match with the job description and then you have to provide feedback on how the resume can be improved to increase its chances of passing through the ATS by providing keywords missing and last final thoughts.
"""   

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) expert with a deep understanding of Data Science, Software Engineering, Machine Learning, AI and ATS functionality  . 
Provide your thoughts and a sample resume for the applicant to use as a guide to beat the ATS system.
"""  

if submit1:
    if uploaded_file is not None:
        pdf_content =input_pdf_setup(uploaded_file)
        resposne = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("Response")
        st.write(resposne)
    else:
        st.error("Please upload a PDF file.")

elif submit3:
    if uploaded_file is not None:
        pdf_content =input_pdf_setup(uploaded_file)
        resposne = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("Response")
        st.write(resposne)
    else:
        st.error("Please upload a PDF file.")
        
elif submit4:
    if uploaded_file is not None:
        pdf_content =input_pdf_setup(uploaded_file)
        resposne = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("Response")
        st.write(resposne)
    else:
        st.error("Please upload a PDF file.")
        
elif submit5:
    if uploaded_file is not None:
        pdf_content =input_pdf_setup(uploaded_file)
        resposne = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("Response")
        st.write(resposne)
    else:
        st.error("Please upload a PDF file.")