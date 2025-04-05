from django.shortcuts import render,HttpResponse
# from guess_indian_gender import IndianGenderPredictor
from .tblmodels import Tblcv, Tblsearch, Tblindustry, Tblphase, Tblsector ,Tblsearchmeta, Tblcvkeywords, Tblkeywords, Tbllanguage_gen, Tbledumode, Tbledulevel,Tblcvfiles,Tbladdress,Tblcountries, Tblcities, Tblstates,Tbleducation,Tblexperience,Tblfundedproject,Tblsubjects,Tbldesignation,Tbldegree, Tblinstitutes, Tbluniversities,Tblcompany_master,Tblfundagencies,Tblpavement,Tblterrain,Tblcontractmode,Tblprodetails,cvm_run_history
import dateutil.parser as dparser
from .File_to_text_converter import Textgenerator
from .basic_detail import resumeparser
from .education import Education1
import shutil
from pytz import timezone 
from datetime import datetime  
# from .namesplit import split
from datetime import date
from .experience import ADD_PROFESSIONAL_EXPERIENCE, designation
# from .genprojects import ADD_FUNDED_PROJECT
from pathlib import Path
# from nltk import ngrams
# import locationtagger
# from .company_formats import com_format_checker
from .project import getprojectdetails
import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
import re
# import docx2txt
# import glob
import os
from datetime  import datetime
from datetime import date
from . import address
# from .company_formats import com_format_checker
from .company import table_no_finder
import traceback
import PyPDF2
from core.views import final
from .utils import date_checker
import logging
from datetime import datetime
import pytz
from multiprocessing import Process
from . get_data_model import model_data
from . insert_data import basi_data_insert,education_insert,project_insert,company_information_insert,keywords_insert,address_insert
from . utils import logger_creater
from . world_bank import extract_basic_detail_wb
from format_finder import format_finder_fun
from adb import extract_cv_data_adb
from world_bank import extract_cv_data_world_bank
BASE_DIR = Path(__file__).resolve().parent.parent
flurl = str(BASE_DIR) + "/media/"



# ......................................for server.............................
# old_path='/mnt/old_files'
# new_file_path='/mnt/cv_files'
# doc_path='/mnt/doc_files'
# email_path='/mnt/email_not_found'

#......................................for local...............................
old_path='/home/nitinyadav/Documents/files_for_server/old_file'
new_file_path='/home/nitinyadav/Documents/files_for_server/read_file'
# doc_path='/mnt/doc_files'
email_path='/home/nitinyadav/Documents/files_for_server/email_not_found_file'

ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
institute_names = set(Tblinstitutes.objects.using('table_db').filter(is_active=1).values_list('institutename',flat=True))
# print('the length of instiute names is ',len(institute_names))
university_names= set(Tbluniversities.objects.using('table_db').filter(is_active=1).values_list('univname',flat=True))
# print('the length of universtiy name is',len(university_names))
key_data = Tblkeywords.objects.using('table_db').values_list('keyword', flat=True)
indus_data=Tblindustry.objects.using('table_db').values_list('industryname', flat=True)
phs_data  = Tblphase.objects.using('table_db').values_list('phasename', flat=True)
sec_data= Tblsector.objects.using('table_db').values_list('sectorname', flat=True)
PHD = ['PHD','P.HD.','P.H.D.', 'PHD.']
dict_phd={'PHD':PHD}
POST_GRADUATION = ['M.A','M.COM', 'M.COM.','MASTERS','M TECH','M. TECH','ME','MASTER','M.E','M.E.','ME.','M.S','M.S.','M.TECH','M.TECH.','M TECH','MBA','MASTER OF ENGINEERING','MTECH','MASTERS']

dict_pg = {'M.A':['M.A','M.A.','M A'],'M.COM':['M.COM', 'M.COM.','M.COMM','M.COMM.','MCOM','M COM'],'M.E.':['ME','M.E','M.E.','ME.','MASTER OF ENGINEERING'],'MS':['M.S','M.S.','MS'],'M.TECH':['MASTER OF TECHNOLOGY','M.TECH','M.TECH.','M TECH','MTECH'],'MBA':['MBA','M.B.A.','M.B.A']}


GRADUATION = ['B.A (HONS.)','BE','GRADUATION','BACHELORS','B E','B.E(MECH)','B.E(CIVIL)','B.E.', 'B.E','B.E ','GRADUATE','BACHELOR OF ENGINEERING','BACHELOR OF TECHNOLOGY','B.SC', 'B.SC.','C.A.','C.A','B.COM','B.COM.','B.TECH.','B.TECH', 'B TECH']
dict_g = {'B.Sc.':['B.SC', 'B.SC.','BSC'],'AMIE':['AMIE'],'BE':['BE','GRADUATION','BACHELORS','B E','B.E(MECH)','B.E(CIVIL)','B.E.', 'B.E','B.E ','GRADUATE','BACHELOR OF ENGINEERING'],'B.TECH':['BACHELOR OF TECHNOLOGY','B.TECH.','B.TECH', 'B TECH','BTECH','BACHELOR','BACHELOR OF CIVIL'],'B.COM':['B.COM','B.COM.','BCOM'],'Bachelor of Architecture':['Bachelor of Architecture'],'BA':['B.A (HONS.)','B.A.','B.A','B A'],}
	

XII = ['HSC','12TH','XII','XIITH','INTERMEDIATE','GRADE–12','HSCC','HIGHER SECONDARY EDUCATION','CLASS 12','CLASS12','12 TH','12TH','HIGHER SECONDARY','SSC','HIGHERSECONDARY']
dict_12={'12th':XII}
X = ['SSC','SSLC','S.S.C','10TH','MATRIC','XTH','X', 'MATRICULATION','GRADE-10','HIGH SCHOOL','10TH','10 TH','CLASS 10','CLASS10']
dict_10={'10th':X}
# DIPLOMA = ['DIPLOMA','POLYTECHNIC']
dict_diploma={'Diploma':['DIPLOMA'],'POLYTECHNIC':['POLYTECHNIC']}
# CERTIFICATE_COURSE = ['CERTIFICATE']
dict_certifaction={'Certificate':['CERTIFICATE'],'CERTIFICATION':['CERTIFICATION']}
# CERTIFICATION_COURSE = ['CERTIFICATION']
# dict_certifaction_courses={'CERTIFICATION':CERTIFICATION_COURSE}
# SPECIALIZATION LIST
specialization_list = ['', 'Management', 'CAD / Draftsmanship', 'Certificate Course in Safety', 'Environmental Science',
 'Technology Science', 'Strategy and Leadership Management', 'Transportation', 'Survey & Testing',
 'Construction Management', 'Civil', 'Highway', 'Mining', 'Environmental', 'Environmental Health', 'Traffic',
 'Geology', 'Geotech', 'Structural', 'Safety', 'Philosophy', 'Soil Mechanics', 'Project Management',
 'Management Development Programme', 'Water Resource', 'Structures', 'Highways and Transportation', 'Geotechnical',
 'SafetyCertificate Course in Safety']

                
institute_names = set(Tblinstitutes.objects.using('table_db').filter(is_active=1).values_list('institutename',flat=True))
# print('the length of instiute names is ',len(institute_names))
university_names= set(Tbluniversities.objects.using('table_db').filter(is_active=1).values_list('univname',flat=True))

def websock(request):
        if request.method == 'GET':
            return render(request,'general/index.html')
            
        logger_insert=logger_creater('insert_logger')
        logger_model=logger_creater('model_logger') 
        if request.method == 'POST' and request.FILES.get('file'):
            upload_dir = os.path.join(BASE_DIR, 'uploaded_files')
            try:
                os.makedirs(upload_dir, exist_ok=True)
            except:
                logger_insert.exception('error in creating the directory')


            uploaded_file = request.FILES['file']
            file_path = os.path.join(upload_dir, uploaded_file.name)

            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            try:
                genview(file_path,upload_dir,old_path,new_file_path,email_path,logger_insert,logger_model) 
            except:
                traceback.print_exc()

            return HttpResponse('done')
        # except:
        #     traceback.print_exc()
    
    # return render(request,'general/index.html')

def infracon_checker(file_path):
   with open(file_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Check if the PDF has at least one page
        if len(pdf_reader.pages) > 0:
            # Get the first page
            first_page = pdf_reader.pages[0]
            
            # Extract text from the first page
            text = first_page.extract_text()
            if text.count('INFRACON')>0:
                return True
            else:
                return False
        else:
            return False
    
    
def genview(file_path,directory_path,old_path,new_file_path,email_path,logger_insert,logger_model):
    # remark=''
    not_email=False
    logger=logger_insert

    try:
        file=file_path.split('/')[-1]
        # remark+=f'The file name is {file},\n'
        global candid_id
        if file.endswith('.docx') or file.endswith('.pdf') or file.endswith('.doc'):	
            print('The file name is ',file)
            file=file.replace(' ','_').replace('[','_').replace(']','_').replace('+','')	
            # file_path is the path of the file 
            if file.endswith('.pdf'):
                infracon=infracon_checker(file_path)
            else:
                infracon=False
            if infracon:
                # remark+='The file is a infracon file,\n'
                print('This is a infracon document')
                final(file_path,old_path,new_file_path)
                return
            
            else:
                # ............................code for extracting the text from the pdf file.................................................
                preprocessed = Textgenerator.file2txt(file_path ,directory_path)
                format=format_finder_fun(preprocessed)
                if format=='adb':
                    data=extract_cv_data_adb(preprocessed,logger)
                elif format=='world_bank':
                    data=extract_cv_data_world_bank(preprocessed,logger)
                
                

                # data_from_wb=extract_basic_detail_wb(preprocessed)
                #................................getting the data from the model.......................................................
                data_from_model=model_data(file_path,logger_model)
                
                #.................................extracting the basic information using the old method..........................
                b_data = resumeparser.basic_details(preprocessed)
                
                
                #.................................extracting the language using the old method.....................................
                language = resumeparser.LANGUAGES(preprocessed)   # languages
                logger.info(f'------------------------The file path is {file_path}-------------------------------\n\n')
                candid_id=basi_data_insert(b_data,data_from_model,language,file,file_path,old_path,new_file_path,logger)
                logger.info(f'The candid id is {candid_id}')
                if candid_id==None:
                    logger.info('This cv already exist in the database')
                    return
                
                # getting the company data from the model....................................................................
                if data_from_model['experience']=='' or data_from_model['experience']==[]:
                    try:
                        company_data=table_no_finder(file_path,preprocessed)
                    except:
                        company_data=None
                else:
                    company_data=data_from_model['company_data']
                    
                # extracting the education informatin from the cv.........................................................
                if data_from_model['education']==[] or data_from_model['education']=='':
                    qual_data=Education1.education_format_checker(institute_names,university_names,file_path,preprocessed,logger)
                else:
                    qual_data=data_from_model['education']
                    
                # extracting the adress from the cv...............................................................
                add_data=address.ADDRESS(preprocessed)
                    
                try:  
                    restxt = 1
                    createdBy = 1
                    Tblcvfiles.objects.using('table_db').update_or_create(filename = str(str(candid_id)+"_"+str(file)), candidate_id = int(candid_id), resume_text = restxt, created_by = createdBy)			
                except:
                    logger.exception('error in the inserting data in the cvfile table')
                    traceback.print_exc()
                    pass

                
                # if company data is None we are using the old method for extracting the company information..........................
                if company_data!=None:
                    qw=0
                    try:
                        for x in company_data:
                            if len(x['COMPANY'])>0:
                                qw+=1
                    except:
                        pass
                    if qw==0:    
                        company_data = ADD_PROFESSIONAL_EXPERIENCE(preprocessed)
                else:
                    company_data= ADD_PROFESSIONAL_EXPERIENCE(preprocessed)
                    
                
                # extracting the project from the cv    
                try:
                    project_data = getprojectdetails(preprocessed)
                except:
                    pass
                
                # code for moving the file 
                try:             
                    new_file_name=str(candid_id)+"_"+str(file)
                    # new_file_path='/'.join(file_path.split('/')[:-1])
                    new_file_path=os.path.join(new_file_path,new_file_name)
                    logger.info(f'-----------------------The file path after reading is-{new_file_path}--------------------------------------')
                    if new_file_path not in os.listdir('/home/nitinyadav/Documents/files_for_server/read_file'): #/mnt/apps/allapps_app/public_html/cvm/storage/app/public/
                        shutil.move(file_path,new_file_path)
                except:
                    logger.exception('exception in moving the file to the server')
                    traceback.print_exc()
                    
                logger.info(f'The file path is {file_path}')
                keywords_insert(preprocessed,candid_id,indus_data,key_data,sec_data,phs_data,logger)
                address_insert(add_data,candid_id,logger)
                education_insert(qual_data,candid_id,dict_g,dict_pg,dict_12,dict_10,dict_phd,dict_certifaction,dict_diploma,specialization_list,logger)
                company_information_insert(company_data,candid_id,logger)
                project_insert(project_data,candid_id,logger)
    except:
        logger.exception('execption in themain exception block')
  