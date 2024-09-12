# Resume Parser
This project processes resumes and job descriptions to extract and match skills, qualifications, and other relevant details. It uses PDF resume uploads, extracts relevant information using natural language processing (NLP), and compares the skills in resumes to job descriptions using cosine similarity. The result is a similarity score for each applicant relative to each job description.

## Technologies used
- Programming language - Python 
- Libraries - Nltk, Spacy, Pandas, Scikit-learn
- User Interface - Streamlit

## Installation
1. Create a python virtual environment and activate it. 
2. Install the dependencies by running:
    ```powershell
    pip install -r requirements.txt
    ```
3. Run the streamlit app.py
    ```python
    streamlit run app.py
    ```
Upload resumes, job descriptions from the streamlit interface.

## Application Flow 
This project has 2 dashboards (divided the page into 2 parts):
1. Applicant Dashboard 
    - Enter applicant name
    - Upload resume pdf file
    - submit resume
2. HR Dashboard
    - Add multiple job descriptions in the text input field
    - Click on submit to retrieve similarity scores of candidates with respect to the job description.
    
![Applicant dashboard](/Readme_media/Applicant.png)
> **_NOTE:_** Multiple job descriptions can be added. The resumes will be categorized into the one with maximum similarity score.

![HR Dashboard](/Readme_media/HR_dashboard.jpg)
# Working
![Flowchart](/Readme_media/Flowchart.png)
<!-- Explain ner, cosine similarity in short -->
## Future scope
- NER Accuracy: Train the model on domain-specific datasets and continuously improve skill pattern sets to extract the right entities from resumes.
- Skill Similarity: Use word embeddings (like Word2Vec or BERT) to capture variations and the semantic relationships between skills.
- Semantic Similarity: Implement sentence-level embeddings to capture context and meaning rather than just comparing individual words.
- Extract More Resume Attributes: Expand the set of attributes the model extracts, such as extracurriculars, certifications, and publications. Also, calculate years of experience based on work history.



