import docx2txt
import cv2, time
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os, subprocess,time
import PyPDF2
from PyPDF2 import PdfReader 
import traceback
import re
import logging
import traceback
from docx import Document
import pandas as pd
import fitz  # PyMuPDF

# ...............................................function for extracting project information from the cv.......................................................................

def extract_projects_adb(project_text):
    projects={'title':[],'client':[],'employer':[],'position':[]}
    if project_text:
        project_texts=project_text.group(0)
        project_texts=re.split('name of assignment or project|name of assignment',project_texts)

        for project_text in project_texts:
            first_split=project_text.split('month and year:')
            projects['title'].append('')
            projects['client'].append('')
            projects['employer'].append('')
            projects['position'].append('')
            if len(first_split)>1:
                project_title=first_split[0]
                text_left=first_split[1]
                project_text=re.sub('(\n|:)*','',project_title)
                projects['title'][-1]=project_text.strip()
                text_left=first_split[1]
                client=text_left.split('client')
                if len(client)>1:
                    client=client[1]
                    client=client.split('main project features')
                    if len(client)>1:
                        client=client[0]
                        client=re.sub('(\n|:)*','',client)
                        projects['client'][-1]=client.strip()
                        position=text_left.split('position held')
                        if len(position)>1:
                            position=position[1]
                            position=position.split('activities performed')[0]
                            position=re.sub('(\n|:)*','',position)
                            projects['position'][-1]=position.strip()
            else:
                if project_text!='':
                    projects['title'][-1]=project_text.replace(':','')
        return projects

#...........................................................................................................................................................................................


# ...............................................function for extracting education information from the cv.......................................................................
def extract_education(education_text):
    education_text=re.sub('(Education|:)','',education_text)
    education_text=re.split('\n+',education_text)
    education_text=education_text[:8]
    output=[]
    for x in range(len(education_text)):
        if education_text[x].strip() == '':
            continue
        dic={}
        dic['degree']=''
        dic['institution']=''
        dic['year']=''
        dic['grade']=''
        splited=education_text[x].split('from')
        dic['degree']=splited[0].strip()
        if len(splited)>1:
            second_split=re.split(r'in (\d{4})',splited[1])
            if len(second_split)>1:
                dic['institution']=second_split[0].strip()
                dic['year']=second_split[1].strip()
            else:
                dic['institution']=splited[1].strip()
            output.append(dic)

    return output
# ...........................................................................................................................................................................................


def extract_cv_data_adb(cv_text,logger):
    """
    Extracts expert information from CV text using regular expressions.

    Args:
        cv_text (str): The text content of the CV.

    Returns:
        dict: A dictionary containing the extracted information, with keys:
              'name', 'address', 'date_of_birth', 'citizenship', 
              'employment_record', 'education_details', 'project_info'.
              Returns None for any field not found.
    """


# .................................................code for extracting the basic details from the resume.....................................................................................................
    name_pattern = r"(?:Name of Expert)[:,]?(?:\s|\n)*(.*?)\n"
    address_pattern = r"(?:Current Residential Address)[:,]?(?:\s|\n)*(.*?)\n"
    dob_pattern = r"(?:Date of Birth)[:,]?(?:\s|\n)*(.*?)\n"
    citizenship_pattern = r"(?:Citizenship)[:,]?(?:\s|\n)*(.*?)\n"
    telephone_pattern=r"\d{10}"
    emails=re.findall(r'[\w.-]+\s{0,1}@\s{0,1}[\w.-]+.\w{2,3}', cv_text)
    emails = emails[0:2]

    name = re.search(name_pattern, cv_text, re.MULTILINE | re.DOTALL)
    address = re.search(address_pattern, cv_text, re.MULTILINE | re.DOTALL)
    dob = re.search(dob_pattern, cv_text, re.MULTILINE | re.DOTALL)
    citizenship=re.search(citizenship_pattern,cv_text)
    telephone_no=re.search(telephone_pattern,cv_text)
    education_text=re.search('Education(.|\n)*?Membership in Professional Associations',cv_text)
    education_text =education_text.group() if education_text else None

    employment_record=re.search('Employment record(.|\n)*?Detailed Tasks Assigned',cv_text)
    employer_text=employment_record.group() if employment_record else None
    if employer_text:
        employer_data=[[],[],[]]
    idx=re.search('Position held(\s|\n)*',employer_text)
    if idx:
        idx=idx.end()
    else: 
        idx=0
    employer_text=employer_text[idx:]

    project_text=re.search('name of assignment(.|\n)*',cv_text.lower())   
    try:
        projects=extract_projects_adb(project_text)
    except:
        logger.exception('error occured in the project section')
        projects=None
    try:
        education=extract_education(education_text)
    except:
        logger.exception('error occured in the education section')
        education=None

#.......................................................................................................................................................................
    return {
        "name": name.group(1).strip() if name else None,
        "address": address.group(1).strip() if address else None,
        "date_of_birth": dob.group(1).strip() if dob else None,
        "citizenship":citizenship.group(1).strip() if citizenship else None,
        "telephone_no":telephone_no.group(0).strip() if telephone_no else None,
        "emails":emails,
        "projects":projects,
        "education": education,
        "employer_text":employer_text,
    }














