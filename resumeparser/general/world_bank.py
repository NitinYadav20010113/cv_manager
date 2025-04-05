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



def extract_projects_wb(project_text):
    projects={'title':[],'client':[],'employer':[],'position':[]}
    if project_text:    
        project_texts=project_text.group(0)
        project_texts=re.split('name of assignment or project|name of assignment',project_texts)

        for project_text in project_texts:
            first_split=project_text.split('year')
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


def extract_cv_data_world_bank(cv_text,logger):
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


    name_pattern = r"(?:Name of Expert)[:,]?(?:\s|\n)*(.*?)\n"
    dob_pattern = r"(?:Date of Birth)[:,]?(?:\s|\n)*(.*?)\n"
    citizenship_pattern = r"(?:Country of Citizenship)[:,]?(?:\s|\n)*(.*?)\n"
    emails=re.findall(r'[\w.-]+\s{0,1}@\s{0,1}[\w.-]+.\w{2,3}', cv_text)
    emails = emails[0:2]

    name = re.search(name_pattern, cv_text, re.MULTILINE | re.DOTALL)
    dob = re.search(dob_pattern, cv_text, re.MULTILINE | re.DOTALL)
    citizenship=re.search(citizenship_pattern,cv_text)


# .................................................code for extracting the basic details from the resume.....................................................................................................


    project_text=re.search('name of assignment(.|\n)*',cv_text.lower())   
    try:
        projects=extract_projects_wb(project_text)
    except:
        logger.exception('error occured in the project section')
        projects=None

    return {
        "name": name.group(1).strip() if name else None,
        "date_of_birth": dob.group(1).strip() if dob else None,
        "citizenship":citizenship.group(1).strip() if citizenship else None,
        "emails":emails,
        "projects":projects,
    }







