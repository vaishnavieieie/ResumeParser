import streamlit as st
import os
import pandas as pd
import all_functions as af

st.markdown("<h3 style='text-align: center; color: grey;'>Applicant Dashboard</h3>", unsafe_allow_html=True)
with st.form("my_form" ,clear_on_submit=True):
    name_input = st.text_input(
        "Enter name",
        value=" "
    )
    
 
    uploaded_file = st.file_uploader("Choose a file", type="pdf")

    submitted = st.form_submit_button("Submit")
    if submitted:
       if name_input == " ":
        st.error("Enter a valid name")
       else:
        st.write("Submitted")

if not os.path.exists("uploaded_pdfs"):
        os.makedirs("uploaded_pdfs")

if uploaded_file is not None and submitted:
    with open(os.path.join("uploaded_pdfs", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"PDF file '{uploaded_file.name}' saved successfully.")
    af.save_to_csv(name_input,uploaded_file)
    submitted = False


st.markdown("<h3 style='text-align: center; color: grey;'>HR Dashboard</h3>", unsafe_allow_html=True)

job_desc= st.text_area("Enter Job Description", value=None)

def get_max_sim(row):
    return row.idxmax()

if job_desc:
    job_descriptions = job_desc.split('\n\n') 
    button = st.button("Submit")
    if button:
        # display csv as table
        # df = af.process_resume("extracted_data.csv", job_desc)
        df = af.process_resume("extracted_data.csv", job_descriptions)
        df=df.drop(columns=['File'])
        # df=df.sort_values(by=['Similarity'],ascending=False)

        job_columns=[ 'Job_'+str(i+1) for i in range(len(job_descriptions))]

        df['max_sim_col'] = df[job_columns].apply(get_max_sim, axis=1)
        drop_columns = job_columns.copy()
        drop_columns.append('max_sim_col')
        # display separate tables for each max_sim_col value
        for col in job_columns:
            st.write(f"Applicants with max similarity to {col}")
            cols=drop_columns.copy()
            cols.remove(col)
            data=df[df['max_sim_col'] == col].drop(columns=cols, axis=1)
            data=data.rename(columns={col:'Similarity'}, )
            st.dataframe(data, use_container_width=True)

        # st.dataframe(df, use_container_width=True)

