from nltk import ngrams
import os
import re
import docx2txt
import re, string
import nltk
from stop_words import get_stop_words
from nltk.corpus import stopwords
import spacy
from textblob import TextBlob
from nltk import ngrams
import pgeocode
from guess_indian_gender import IndianGenderPredictor
from datetime import datetime
import datefinder

stop_words = list(get_stop_words('en'))         #Have around 900 stopwords
nltk_words = list(stopwords.words('english'))   #Have around 150 stopwords
stop_words.extend(nltk_words)
nlp = spacy.load('en_core_web_sm')

stop_words.remove('of')


def subset_rem(list_):
    for i in list_:    
        b=list_.copy()
        b.remove(i)  
        for j in b:
            if j[:-4] in i:
                list_.remove(j)
    return list_



def ADD_PROFESSIONAL_EXPERIENCE(text):
    try:
        exp_data=""
        a=['work experience','professional experience','employment record','working experience','total experience','work history',
        'previous organization','career progression','total work experience']
        b='experience'

        data=text.lower()
        if any(n in data for n in a)==True:  
            check_l=[]
            for i in a:
                if i in data:
                    check_l.append(i)  
                    break
            s_index=data.index(check_l[0])
            exp_data+=text[s_index:]
        else:
            if b in data:
                s_index=data.index(b)
                data_=data[s_index:]
                exp_data+=text[s_index:]
        
        t_data = [] #temporary data

        c=[]
        for i in range(3,7):
            s = ngrams(exp_data.split(), i) 
            for j in s:
                c.append(' '.join(j))
        t_data.append(sorted(c, key = len, reverse = True))

        check = ['pvt ltd','pvt. ltd.','pvt','pvt.','ltd','ltd.','solutions','group','groups','limited','servicees','suppliers']
        companies=[] # companies list 
        if len(t_data)!=0:
            for com in t_data:
                t_list=[]
                for i in com: 
                    if any(n in i.lower().split() for n in stop_words) == False:
                        if any(n in i.lower() for n in ['department','client',',',':','-','(',')','_',';','%','#'])==False:
                            l_word=i.lower().split(' ')[-1]
                            if l_word in check: 
                                doc = nlp(i)
                                for ent in doc.ents:
                                    if ent.label_ == 'ORG':
                                        t_list.append(ent.text) 
                t_list = subset_rem(t_list)
                companies.append(list(set(sorted(t_list, key = len, reverse=True))))  
        
        if len(t_data)==0:
            companies.append([])
        
        exp_data2=[]
        if len(companies[0])!=0:
            for i in range(len(companies[0])):
                l=[]
                if companies[0][i] in exp_data:             
                    s_index= exp_data.index(companies[0][i])
                    l.append(exp_data[s_index-150:s_index+150])
                exp_data2.append(l)  
        else:
            exp_data2.append([])
        
        companies_list=[]
        try:
            if len(exp_data2[0])!=0:        
                if len(companies[0]) !=0:        
                    for i in range(len(companies[0])):
                        f_dict={}
                        f_dict['COMPANY'] = companies[0][i]
                        ft_date = date_parser(exp_data2[i][0])
                        f_dict['FROM DATE']=ft_date[0]
                        f_dict['TO DATE']=ft_date[1]
                        f_dict['DESIGNATION']=''
                        f_dict['H.O. COUNTRY']='INDIA'
                        f_dict['NATURE OF EMPLOYMENT']='PERMANENT'
                        f_dict['RESPONSIBILITIES']=''
                        companies_list.append(f_dict)
                if len(companies[0]) == 0:
                    f_dict={}
                    f_dict['COMPANY'] = ''
                    f_dict['FROM DATE'] = ''
                    f_dict['TO DATE'] = ''
                    f_dict['DESIGNATION'] = ''
                    f_dict['H.O. COUNTRY']='INDIA'
                    f_dict['NATURE OF EMPLOYMENT']='PERMANENT'
                    f_dict['RESPONSIBILITIES']=''
                    companies_list.append(f_dict)
            if len(exp_data2[0])== 0:
                f_dict={}
                f_dict['COMPANY'] = ''
                f_dict['FROM DATE'] = ''
                f_dict['TO DATE'] = ''
                f_dict['DESIGNATION'] = ''
                f_dict['H.O. COUNTRY']='INDIA'
                f_dict['NATURE OF EMPLOYMENT']='PERMANENT'
                f_dict['RESPONSIBILITIES']=''
                companies_list.append(f_dict) 
        except:
            pass
        # print(companies_list)
    except:
        pass
    return companies_list

def designation(text):
        s=0
        if 'designation' in text.lower():
            s=text.lower().index('designation')
            s=s+13
        if s==0:
            if 'role' in text.lower():
                s=text.lower().index('role')
                s=s+6
        if s==0:
            if 'position' in text.lower():
                s=text.lower().index('position')
                s=s+10
        if s==0:
            check  = ['site engineer', 'maintainance engineeer', 'billing engineer','resident engineer','senior manager','senior civil engineer',
                     'project civil engineer','project engineer','site civil engineer','trainee accountant']
            for i in check:
                if i in text.lower():
                    tx=i
                    break
        if s==0:
            tx=''
        if s!=0:
            tx=text[s:s+26]
        return tx
def date_parser(text):
    datet = datetime.now().strftime("%Y-%m-%d")
    for ii in ['till now','till today','at present','till current date']:
        if ii in text.lower():
            text=text.lower().replace(ii,datet)
            break
    string_with_dates = text
    matches = datefinder.find_dates(string_with_dates)
    dates=[]
    for match in matches:
        dates.append(match.strftime("%Y-%m-%d"))
    if len(dates)==0:
        return ['','']
    if len(dates)==1:
        return [dates[0],datet]
    if len(dates)==2:
        return [dates[0],dates[1]]
    if len(dates) >2:
        return [dates[-2],dates[-1]]