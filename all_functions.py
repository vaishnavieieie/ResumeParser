import spacy
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
# import jsonlines
import geotext
from phonenumbers import PhoneNumberMatcher

skill_pattern_path = "jz_skill_patterns.jsonl"

from pypdf import PdfReader

job=[]

# extract text from pdf: works
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file) 
    all_text = ""
    for page in reader.pages:
        text = page.extract_text()
        all_text += text
    return all_text

# works
import os.path
def save_to_csv(name,uploaded_file):
    # print("uploading to csv",name)
    text = extract_text_from_pdf(uploaded_file)
    if text == "" or text == None:
        text = "None"
    data = {'File':[uploaded_file.name],'Name': [name], 'Resume': [text]}
    df = pd.DataFrame(data)
    
    if os.path.isfile('extracted_data.csv'):
        existing_df = pd.read_csv('extracted_data.csv')
        df = pd.concat([existing_df, df], ignore_index=True)
        
        df.to_csv('extracted_data.csv', index=False)
        
    else:
        df.to_csv('extracted_data.csv', index=False)

# extract details from reume:
def process_resume(dataset, job_desc):
    # read dataset
    # if dataset exists
    if os.path.isfile(dataset):

        df= pd.read_csv(dataset)
    else:
        return pd.DataFrame()

    # process resume
    df['Resume'] = df['Resume'].apply(lambda x: clean_text(x))
    # extract ner
    df['Skills'] = df['Resume'].apply(lambda x: apply_ner(x))

    # calculate similarity for every job_desc
    # calculate similarity
    # job_desc = clean_text(job_desc)
    # job_desc = apply_ner(job_desc)
    # job=job_desc.copy()
    # print("job",type(job))
    # df['Skills_str'] = df['Skills'].apply(lambda x: list_to_string(x))
    # df['Similarity'] = apply_sim(df['Skills_str'], job_desc)

    for i in range(len(job_desc)):
        # print(i)
        # print(len(job_desc))
        job_proc= clean_text(job_desc[i])
        job_proc = apply_ner(job_proc)
        df['Skills_str'] = df['Skills'].apply(lambda x: list_to_string(x))
        col_name='Job_'+str(i+1)
        df[col_name] = apply_sim(df['Skills_str'], job_proc)

    # extract grades
    df['Grades'] = df['Resume'].apply(lambda x: get_grades(x))


    # extract qualification

    # extract contact info 
    df['Email'] = df['Resume'].apply(lambda x: get_emails(x))
    df['Phone'] = df['Resume'].apply(lambda x: get_phone_numbers(x))
    df['URL'] = df['Resume'].apply(lambda x: get_urls(x))


    # save to csv
    df.drop(columns=['Skills_str', 'Resume'], inplace=True)
    return df

def list_to_string(lst):
  return ' '.join(lst)

def apply_ner(text):
    nlp = spacy.load("en_core_web_sm")
    ruler = nlp.add_pipe("entity_ruler")
    ruler.from_disk(skill_pattern_path)
    doc = nlp(text)
    myset = []
    subset = []
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            if ent.text not in subset:
                subset.append(ent.text)
    # print(subset)
    # typeof subset
    # print(type(subset))
    return subset

def clean_text(text):
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    review = text
    review = review.lower()
    review = review.split()
    lm = WordNetLemmatizer()
    review = [
        lm.lemmatize(word)
        for word in review
        if not word in set(stopwords.words("english"))
    ]
    review = " ".join(review)
    return review

def apply_sim(skills , job_desc):
    job_desc= " ".join(job_desc)
    # print("skills",skills, "job_desc",job_desc)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(skills)
    input_vector = vectorizer.transform([job_desc])
    cosine = cosine_similarity(X, input_vector)
    return cosine

def get_emails(text):
    email_pattern = r'[^\s]+@[^\s]+[.][^\s]+'
    emails = []

    emails = re.findall(email_pattern, text)

    emails = set(emails)
    emails = list(emails)
    emails=list(map(remove_special_characters, emails))
    return emails

def remove_special_characters(text):
    pattern = r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def get_urls(text):
    url_pattern = r'\b(?:https?://|www\.)\S+\b'
    urls = []

    urls = re.findall(url_pattern, text)

    return urls

def get_phone_numbers(text):
    phone_numbers = []
    countries_dict = geotext.GeoText(text).country_mentions

    country_code = "IN"
    for i in countries_dict.items():
        country_code = i[0]
        break

    search_result = PhoneNumberMatcher(text, country_code)

    phone_number_list = []
    for i in search_result:
        i = str(i).split(' ')
        match = i[2:]

        phone_number = ''.join(match)
        phone_number_list.append(phone_number)

    for i in phone_number_list:
        if i not in phone_numbers:
            phone_numbers.append(i)

    return phone_numbers


def get_grades(text):
    # GPA
    gpa = get_gpa(text)
    if len(gpa) != 0:
        return gpa

    # Percentage
    percentage = get_percentage(text)
    if len(percentage) != 0:
        return percentage

    return []

def get_gpa(txt):
        pattern = r'((\d+\.)?\d+/\d+)'
        lst = re.findall(pattern, txt)
        lst = [i[0] for i in lst]
        return lst

def get_percentage(txt):
        pattern = r'((\d+\.)?\d+%)'
        lst = re.findall(pattern, txt)
        lst = [i[0] for i in lst]
        return lst
