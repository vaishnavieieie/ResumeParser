import streamlit as st
import os

import all_functions as af

st.write("Applicant Dashboard")
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


st.write("HR Dashboard")

job_desc= st.text_area("Enter Job Description", value=None)


if job_desc:
    button = st.button("Submit")
    if button:
        # display csv as table
        df = af.process_resume("extracted_data.csv", job_desc)
        df=df.drop(columns=['File'])
        df=df.sort_values(by=['Similarity'],ascending=False)
        st.dataframe(df, use_container_width=True)
        
        
        # st.data_editor(
        #     df,
        #     column_config={
                
        #         "File": st.column_config.LinkColumn(
        #             "Resume", display_text="View PDF"
        #         ),
        #     },
        #     hide_index=True,
        # )
