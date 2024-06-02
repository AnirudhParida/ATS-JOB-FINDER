import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from main import session

job_des = pd.read_csv('job_description.csv')

def job_matching_model():
    s=''
    for i in session['skill_list']:
        s+= " "+i
    num_row = len(job_des)
    cv = CountVectorizer()
    matches = []
    for i in range(num_row):
        job_title1 = str(job_des['JobTitle'].iloc[i])
        job_title2 = str(job_des['Summary'].iloc[i])
        job_title = ""+job_title1 + " " + job_title2
        content = [job_title, s]
        count_matrix = cv.fit_transform(content)
        cosine_sim = cosine_similarity(count_matrix)
        #print(cosine_sim[0][1])

        if cosine_sim[0][1] > 0.05:
            #print("Role:", job_title, "\nCompany:", job_des['Company'].iloc[i], "\nURL:", job_des['JobUrl'].iloc[i], "\n")
            matches.append({
                "Role": job_title,
                "Company": job_des['Company'].iloc[i],
                "URL": job_des['JobUrl'].iloc[i]
            })
    return matches
