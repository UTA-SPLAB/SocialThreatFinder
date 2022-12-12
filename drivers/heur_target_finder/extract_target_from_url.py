import re
import difflib
import pandas as pd
import os
import sys
import time # For debugging

def get_url_target(url,seperator):

    target_name=[]
    domain_url=[]
    checked_url=[]
    similarity_scores=[]
    regex="^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)"

    x = re.search(regex, url)
    #print(x)

    url=x[0]
    url=url.replace("https://","") # Following three lines to make URL format similar to domain name in meta database
    url=url.replace("http://","")
    url=url.replace("www.","")
    
    # Tokenizing URL

    url_tokens=url.split(seperator)

    # Remove TLD for faster compute
    length_of_url_tokens=len(url_tokens)
    url_tokens.pop(int(length_of_url_tokens)-1)

    for i in url_tokens: 
        if len(i)<4: # Removes shorter tokens
            url_tokens.pop(url_tokens.index(i))

    #print(url_tokens) # Uncomment for debug


    df=pd.read_csv("drivers/heur_target_finder/orgs_meta.csv")

    # Initializing temp file

    #file=open("temp_dist_scores.csv","a")
    #file.write("domain,url,score\n")


    for index,row in df.iterrows():

        tmp_scores=[] # Holds all tmp similariity scores for each token in url_tokens

        target=row['name']
        if len(target)>3: # Filtering out shorter brand names. After filer=1,128 brands
            
            target_name.append(target)

            domain=row['domain']   
            domain_url.append(domain)
            checked_url.append(url)
            try:
                domain=domain.replace(",","")
            except:
                domain="None"
            #print(f"Checking with {target}") # Un-comment for debug

            for i in url_tokens:
                seq=difflib.SequenceMatcher(a=str(domain), b=str(i)) 

                #print(seq)
                similarity_score=seq.ratio()
                tmp_scores.append(similarity_score)
                max_similarity_score=max(tmp_scores)

            #time.sleep(2)
            similarity_scores.append(max_similarity_score)

        #print(similarity_score)
        #file=open("temp_dist_scores.csv","a")
        #file.write(f"{domain},{url},{similarity_score}\n")

    df2=pd.DataFrame(list(zip(target_name,domain_url,checked_url,similarity_scores)),columns=['target','domain', 'url_checked','score'])
    df2.to_csv("temp_dist_scores.csv")




def most_likely_target():
    # Finding domain with minimum distance score
    df2=pd.read_csv("temp_dist_scores.csv")
    result=df2.iloc[df2['score'].argmax()]
    return result


def get_target_from_url(url_id,url):
 
    #print(f"Checking URL:{url}")

    get_url_target(url,".") # Check once with seperator .

    score1=most_likely_target()
    score1_score=score1['score']
    score1_target=score1['target']

    try:
        get_url_target(url,"-") # Check once with seperator /
        score2=most_likely_target()
        score2_score=score2['score']
        score2_target=score2['target']
    except:
        score2_score=0
        score2_target="None"

    if score1_score>score2_score:
        final_target=score1_target
        score=score1_score
        #print(f"Possible target:{score1_target} with score:{score1_score}")

        
    else:
        final_target=score2_target
        #print(f"Possible target:{score2_target} with score:{score2_score}")
        score=score2_score

    if score>=0.5:
        return final_target
    else:
        return "None"


