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

BASE_DIR = Path(__file__).resolve().parent.parent
flurl = str(BASE_DIR) + "/media/"
logdata=[]
global candid_id

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
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
institute_names = set(Tblinstitutes.objects.using('table_db').filter(is_active=1).values_list('institutename',flat=True))
# print('the length of instiute names is ',len(institute_names))
university_names= set(Tbluniversities.objects.using('table_db').filter(is_active=1).values_list('univname',flat=True))
# print('the length of universtiy name is',len(university_names))
key_data = Tblkeywords.objects.using('table_db').values_list('keyword', flat=True)
indus_data=Tblindustry.objects.using('table_db').values_list('industryname', flat=True)
phs_data  = Tblphase.objects.using('table_db').values_list('phasename', flat=True)
sec_data= Tblsector.objects.using('table_db').values_list('sectorname', flat=True)


# All paths that need to check
old_path='/mnt/old_files'
new_file_path='/mnt/cv_files'
doc_path='/mnt/doc_files'
email_path='/mnt/email_not_found'
directory_path='/home/nitinyadav/Documents/Lot 1 - 20K+ CVs - 26-06-24'


class LocalTimeFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, timezone=None):
        super().__init__(fmt, datefmt)
        self.timezone = timezone

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, self.timezone)
        if datefmt:
            return dt.strftime(datefmt)
        else:
            return dt.isoformat()

# def # logger_creater():
    
#     # Define your local time zone
#     local_tz = pytz.timezone('Asia/Kolkata')  # Replace with your time zone

#     # Create a custom formatter with the local time zone
#     formatter = LocalTimeFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S',timezone=local_tz)

#     # Create a custom # logger
#     global # logger
#     global time_# logger
#     # logger = logging.get# logger(__name__)
#     # logger.setLevel(logging.DEBUG)

#     # creating the app # logger
#     file_handler = logging.FileHandler('app.log')
#     file_handler.setLevel(logging.DEBUG)
#     file_handler.setFormatter(formatter)
#     # logger.addHandler(file_handler)
    
    
#     # creating the time # logger........................
    
#     time_# logger= logging.get# logger(__name__)
#     time_# logger.setLevel(logging.INFO)
#     time_handler= logging.FileHandler('time.log')
#     time_handler.setFormatter(formatter)
#     time_handler.setLevel(logging.INFO)
#     time_# logger.addHandler(time_handler)
    
    
#     # creating the critical # logger.....................
#     critical_handles =logging.FileHandler('critical.log')
#     critical_handles.setLevel(logging.WARNING)
#     critical_handles.setFormatter(formatter)
#     # logger.addHandler(critical_handles)
    

   


def websock(request):
        try:
            print('started.................................................................................................................................................')

            # # logger_creater()
            directory_path='/home/nitinyadav/Music/testing'
            files = os.listdir(directory_path)
            files.sort()
            print('The files no are,',len(files))

            
            for file in range(len(files)):
                print('.................................................................................................')
                file_path=os.path.join(directory_path,files[file])
                print('The file path is',file_path)
                try:

                    genview(file_path,directory_path,old_path,new_file_path,email_path,doc_path)  
                except:
                    traceback.print_exc()

            print('............................................Completely readed all the files............................................................')
            return HttpResponse('done')
        except:
            traceback.print_exc()
    
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
    
    
def genview(file_path,directory_path,old_path,new_file_path,email_path,doc_path):
    # remark=''
    not_email=False
    
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
                preprocessed = Textgenerator.file2txt(file_path ,directory_path)
                data_from_model=model_data(file_path)
                # remark+='Extracted the text from the file ,\n'
                # print(type(preprocessed))
                
                b_data = resumeparser.basic_details(preprocessed) # basic details
                # print('basic details====',b_data)
                # remark+='Extracted the basic detail from the file ,\n'
                language = resumeparser.LANGUAGES(preprocessed)   # languages
                # # print('language====',language)
                language = [''.join((x[0].upper(),x[1:].lower())) for x in language]
                if data_from_model['full_name']:
                    dic_to_use=data_from_model
                else:
                    dic_to_use=b_data
                    
                f_name=dic_to_use['First_Name']
                m_name = dic_to_use['Middle_Name']
                l_name = dic_to_use['Last_Name']
                # print('the name is',f_name+m_name+l_name)

                mobile=b_data['Primary Number']
                altmobile=b_data['Secondary Number']
                gender = b_data['GENDER']

                pan = b_data['Pan Number']                
                regex = '^[A-PR-WYa-pr-wy][1-9]\\d\\s?\\d{4}[1-9]$'   
                passport_ = re.findall(regex, b_data['Passport Number'])
                if len(passport_)==0:
                    passport=''
                if len(passport_)!=0:
                    passport =passport_[0]
                adhaar=b_data['Aadhar Number']        
                mother_name=b_data['Mother Name']
                father_name=b_data['Father Name']
                nationality=b_data['Nationality']
                date=b_data['Date of Birth']  
                try:
                    email=b_data['Primary Email']
                except:
                    not_email=True
                    pass
                # # print('emaiol===========',email)
                if email!='':
                    # remark+='The file contains email,\n'
                    try:
                        alt_email = b_data['Secondary Email']
                    except:
                        alt_email=''
                    # # # print('email==>>',email)
                    # # # print('alt_email==>',alt_email)
                    try:
                        dobb = str(dparser.parse(date, fuzzy = True)).split()[0]                    
                    except:
                        dobb = None             
                    national_id=101
                    langs=[]
                    for i in language:
                        l=Tbllanguage_gen.objects.using('table_db').filter(language = i)
                        if l:
                            l_id=l[0].id
                            langs.append(l_id)
                        else :
                            l_id=Tbllanguage_gen.objects.using('table_db').create(language = i)[0].id
                            langs.append(l_id)
                    
                    langs=[str(x) for x in langs]
                    if data_from_model['experience']=='' or data_from_model['experience']==[]:
                        try:
                            company_data=table_no_finder(file_path,preprocessed)
                            # print("company_data:  ", company_data)
                        except:
                            company_data=None
                    else:
                        company_data=data_from_model['company_data']
                    # qual_data=Education1.education_format_checker(file_path,preprocessed)
                    # remark+='Extracted The company information from the file,\n'
                    if data_from_model['education']==[] or data_from_model['education']=='':
                        qual_data=Education1.education_format_checker(institute_names,university_names,file_path,preprocessed)
                    else:
                        qual_data=data_from_model['education']
                    # print('The Education data is ',qual_data)
                    # remark+='Extracted the Education information from the file ,\n'
                # try:
                #     os.remove(file_path)
                # except:
                #     pass
                
                    try: # email check
                        email_check = Tblcv.objects.using('table_db').filter(email=email,status=1)
                        # # print('emailk========',email)
                        if email_check:		 
                            # logger.info(f'The cv already exist {file}')
                            candid_id=email_check[0].id
                            print('........................old cv........................................................')
                            old_path=os.path.join(old_path,file)
                            shutil.move(file_path,old_path)
                            exist=cvm_run_history.objects.using('table_db').filter(file_name=file).exists()
                            if not exist:
                                cvm_run_history.objects.using('table_db').create(candidate_id=candid_id,file_name=file,file_path=old_path,duplicate=1,completed=0)
                            return

                        if not email_check:
                            # # print('comes to read')
                            tblcv = Tblcv.objects.using('table_db').create(fname=f_name,mname=m_name,lname=l_name,dob=dobb,email=email,email2=alt_email,phone=mobile,phone2=altmobile,gender=gender,nationality_id=national_id,fathername=father_name,mothername=mother_name,languages=','.join(langs),aadharno=adhaar,panno=pan,isvalidpassport=0,passportno=passport,is_online=0,status=1)
                            candid_id = Tblcv.objects.using('table_db').filter(email=email,status=1)[0].id
                            print('..............................new cv........................................................')

                    except:
                        # logger.exception('Some error occured while inserting the data in the tblcv')
                        pass 
                    
                    print('The candid id is',candid_id)

                    try: # searchmeta nationality, languages
                        srch_n=Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key="nationality_id", meta_value=str(101))
                        # # print('search meta no found',candid_id)
                        if srch_n:
                            pass
                        if not srch_n:
                            Tblsearchmeta.objects.using('table_db').create(candidate_id=candid_id,meta_key="nationality_id", meta_value=str(101))

                        for l in langs:
                            srch_l=Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key="languages", meta_value=l)
                            if srch_l:
                                pass
                            if not srch_l:
                                Tblsearchmeta.objects.using('table_db').create(candidate_id=candid_id,meta_key="languages", meta_value=l)                        
                    except:
                        pass 
                    try: 
                        
                        new_file_name=str(candid_id)+"_"+str(file)
                        # new_file_path='/'.join(file_path.split('/')[:-1])
                        new_file_path=os.path.join(new_file_path,new_file_name)
                        if new_file_path not in os.listdir('/mnt/cv_files'): #/mnt/apps/allapps_app/public_html/cvm/storage/app/public/
                            shutil.move(file_path,new_file_path)
                    except:
                        traceback.print_exc()
                    # try:
                    #     # os.remove(new_file_path),
                        
                    # except:
                    #     pass

                    try: # TBLSEARCH HERE===>>>
                        data2 = re.sub(' +', ' ', preprocessed)     
                        check_search = Tblsearch.objects.using('table_db').filter(candidate_id=candid_id)
                        if check_search:
                            check_search.update(cvdata=data2)
                        if not check_search:
                            Tblsearch.objects.using('table_db').create(candidate_id=candid_id, cvdata = data2)
                            logdata.append('tblsearch entry completed')
                    except:
                        pass
                    
                    try:  # TBLCVKEYWORDS HERE
                        key_words  =[]
                        phase_id_l =[]
                        sector_id_l=[]
                        indus_id_l =[]

                        for inin in indus_data:
                            if inin.lower() in data2.lower():
                                industry_idd=Tblindustry.objects.using('table_db').filter(industryname=inin)
                                if industry_idd:
                                    industry_id=industry_idd[0].id
                                    indus_id_l.append(industry_id)
                        for kkk in key_data:
                            if kkk.lower() in data2.lower():
                                keyword_idd=Tblkeywords.objects.using('table_db').filter(keyword=kkk)
                                if keyword_idd:
                                    keyword_id=keyword_idd[0].id
                                    key_words.append(keyword_id)
                        for sss in sec_data:
                            if sss.lower() in data2.lower():
                                sector_idd = Tblsector.objects.using('table_db').filter(sectorname=sss)
                                if sector_idd:
                                    s_id= sector_idd[0].id
                                    sector_id_l.append(s_id)
                        for phph in phs_data:
                            if phph.lower() in data2.lower():
                                p_idd= Tblphase.objects.using('table_db').filter(phasename=phph)
                                if p_idd:
                                    p_id=p_idd[0].id					
                                    phase_id_l.append(p_id)						
                        key_words=set(key_words)
                        phase_id_l=set(phase_id_l)
                        sector_id_l=set(sector_id_l)
                        indus_id_l=set(indus_id_l)
                        Tblcvkeywords.objects.using('table_db').update_or_create(candidate_id=candid_id, industries="1", sectors= ','.join([str(i) for i in sector_id_l]), phases=','.join([str(i) for i in phase_id_l]) ,keywords=','.join([str(i) for i in key_words]))
                        if len(key_words)!=0:							
                            for keywrd in key_words:
                                if keywrd!=" " or keywrd!=" ":
                                    Tblsearchmeta.objects.using('table_db').update_or_create(candidate_id=candid_id,meta_key="keywords", meta_value=str(keywrd))								
                        if len(phase_id_l)!=0:
                            for phsd in phase_id_l:
                                if phsd!=" " or phsd!=" ":
                                    Tblsearchmeta.objects.using('table_db').update_or_create(candidate_id=candid_id,meta_key="phases", meta_value=str(phsd))
                        if len(sector_id_l)!=0:
                            for sctrd in sector_id_l:
                                if sctrd!=" " or sctrd!=" ":
                                    Tblsearchmeta.objects.using('table_db').update_or_create(candidate_id=candid_id,meta_key="sector", meta_value=str(sctrd))
                        if len(indus_id_l)!=0:
                            for indid in indus_id_l:
                                if indid!=" " or indid!=" ":
                                    Tblsearchmeta.objects.using('table_db').update_or_create(candidate_id=candid_id,meta_key="industry", meta_value=str(indid))		
                                    logdata.append('tblcvkeyword entry completed')
                    except:
                        pass
                    add_data=address.ADDRESS(preprocessed)
                    # add_data = resumeparser.ADDRESS(preprocessed)
                        
                    # print('address========',add_data)
                    try: # current address
                        curr_add_data = add_data['CURRENT_ADDRESS']
                        if curr_add_data['ADDRESS']=='':
                            curr_add_data = add_data['CORRESPONDANCE_ADDRESS']
                        adType = 'C'
                        curr_add = curr_add_data['ADDRESS']
                        
                        curr_city=curr_add_data['CITY']
                        if curr_city != '':
                            try:
                                curr_city = ''.join([curr_city[0].upper(),curr_city[1:].lower()])
                            except:
                                pass                        
                        curr_state = curr_add_data['STATE']
                        if curr_state != '':
                            try:
                                curr_state = ''.join([curr_state[0].upper(),curr_state[1:].lower()])
                            except:
                                pass
                        country_id= 101                  
                        zip_code = curr_add_data['ZIP CODE']                        
                        if(curr_add != ''):
                            cur_state_ = Tblstates.objects.using('table_db').filter(name=curr_state)
                            if cur_state_:
                                cur_s_id=cur_state_[0].id
                            if not cur_state_:
                                cur_s_id=4122
                            cur_city_ = Tblcities.objects.using('table_db').filter(name=curr_city)
                            if cur_city_:
                                cur_c_id=cur_city_[0].id
                            if not cur_city_:
                                cur_c_id=777
                            Tbladdress.objects.using('table_db').update_or_create(candidate_id = int(candid_id),address_type = adType,address = curr_add,city_id=cur_c_id,state_id = cur_s_id,country_id = country_id, zipcode = zip_code)
                    except:
                        traceback.print_exc()
                        pass
                    try: # permanent address
                        per_add_data = add_data['PARMANENT_ADDRESS']               
                        adType = 'P'
                        per_add=per_add_data['ADDRESS']  
                        per_city=per_add_data['CITY']
                        per_state=per_add_data['STATE']
                        country_id=101
                        zip_code = per_add_data['ZIP CODE']
                        if per_state != '':
                            try:
                                per_state = ''.join([per_state[0].upper(),per_state[1:].lower()])
                            except:
                                pass    
                        if per_state != '':
                            try:
                                per_state = ''.join([per_state[0].upper(),per_state[1:].lower()])
                            except:
                                pass
                        
                        if(per_add != ''):
                            per_state_ = Tblstates.objects.using('table_db').filter(name=per_state)
                            if per_state_:
                                per_s_id=per_state_[0].id
                            if not per_state_:
                                per_s_id=4122
                            per_city_ = Tblcities.objects.using('table_db').filter(name=per_city)
                            if per_city_:
                                per_c_id=per_city_[0].id
                            if not per_city_:
                                per_c_id=777
                            Tbladdress.objects.using('table_db').update_or_create(candidate_id = int(candid_id),address_type = adType,address = per_add,city_id=per_c_id,state_id = per_s_id,country_id = country_id, zipcode = zip_code)
                    except:
                        traceback.print_exc()
                        pass
                    try:                              
                        # qual_data = resumeparser.qual(preprocessed) 
                        # # print('qualification check is here')
                        # function for getting education detail....................

                        # print('qualification data========',qual_data)
                        level=[]
                        qual_level=[]
                        college=[]
                        university=[]
                        yop=[]
                        percentage=[]
                        text = []
                        # # # print(qual_data)
                        if len(qual_data)!=0:
                            for i in qual_data:
                                try:
                                    level.append(i['LEVEL'])
                                    qual_level.append(i['QUALIFICATION_LEVEL'])
                                    college.append(i['INSTITUTE_NAME'].split(",")[0])
                                    university.append(i['BOARD'])
                                    yop.append(i['YEAR OF PASSING'])
                                    percentage.append(i['GRADE'])                        
                                    text.append(i['TEXT'])
                                except:
                                    traceback.print_exc()
                                    pass

                        subject_list = Tblsubjects.objects.using('table_db').values_list('subject', flat=True) 
                        
                        # # # print('***************') 
                        # print('the length of level is',len(level))             
                        for i in range(len(level)):
                            # crs = text[i]                    
                            candidate_id = int(candid_id)
                            # # print('the candidate id is',candidate_id)
                            if level[i]!='':
                                try:
                                    # # print('level_count==>>>',i)
                                    edulevel_id = Tbledulevel.objects.using('table_db').filter(edulevel=level[i])[0].id
                                    # # # print('qual_original',qual_level[i])
                                    breaker=0
                                    if level[i]=='Graduation':
                                        for d_item in dict_g:
                                            if breaker==1:
                                                break
                                            for q in dict_g[d_item]:
                                                if q in qual_level[i].upper():
                                                # # print(qual_level[i])
                                                    degree_id = Tbldegree.objects.using('table_db').filter(degreename=d_item, edulevel_id=edulevel_id)[0].id
                                                    breaker=1
                                                    break
                                            
                                    elif level[i]=='Post Graduate':
                                        for d_item in dict_pg:
                                            if breaker==1:
                                                break
                                            for q in  dict_pg[d_item]:
                                                if q in qual_level[i].upper():
                                                # # print(qual_level[i])
                                                    degree_id = Tbldegree.objects.using('table_db').filter(degreename=d_item, edulevel_id=edulevel_id)[0].id
                                                    breaker=1
                                                    break
                                    
                                    elif level[i]=='12th':
                                        for d_item in dict_12:
                                            if breaker==1:
                                                break
                                            for q  in dict_12[d_item]:
                                                if q in level[i].upper():
                                                # # print(qual_level[i])
                                                    degree_id = Tbldegree.objects.using('table_db').filter(degreename=d_item, edulevel_id=edulevel_id)[0].id
                                                    breaker=1
                                                    break
                                                
                                    elif level[i]=='10th':
                                        for d_item in dict_10:
                                            if breaker==1:
                                                break
                                            for q in dict_10[d_item]:
                                                if q in level[i].upper():
                                                # # print(qual_level[i])
                                                    degree_id = Tbldegree.objects.using('table_db').filter(degreename=d_item, edulevel_id=edulevel_id)[0].id
                                                    breaker=1
                                                    break
                                                
                                    elif level[i]=='Doctorate':
                                        for d_item in dict_phd:
                                            if breaker==1:
                                                break
                                            for q in dict_phd[d_item]:
                                                if q in level[i].upper():
                                                # # print(qual_level[i])
                                                    degree_id = Tbldegree.objects.using('table_db').filter(degreename=d_item, edulevel_id=edulevel_id)[0].id
                                                    breaker=1
                                                    break
                                    elif level[i]=='Certification Courses':
                                        for d_item in dict_certifaction:
                                            if breaker==1:
                                                break
                                            for q  in dict_certifaction[d_item]:
                                                if q in level[i].upper():
                                                # # print(qual_level[i])
                                                    degree_id = Tbldegree.objects.using('table_db').filter(degreename=d_item, edulevel_id=edulevel_id)[0].id
                                                    breaker=1
                                                    break
                                    elif level[i]=='Diploma':
                                        for d_item in dict_diploma:
                                            if breaker==1:
                                                break
                                            for q  in dict_diploma[d_item]:
                                                if q in level[i].upper():
                                                    degree_id = Tbldegree.objects.using('table_db').filter(degreename=d_item, edulevel_id=edulevel_id)[0].id
                                                    breaker=1
                                                    break
                                    
                                    # degree_list = Tbldegree.objects.using('table_db').values_list('id','degreename')                        
                                    # degree_list = [(x[0],x[1].replace('.','').strip().upper()) for x in degree_list]
                                    # for degree_in in degree_list :
                                    #     test_qual = qual_level[i].replace('.','').strip().upper()
                                    #     if test_qual=='XTH' or test_qual=='X':
                                    #         test_qual=='10TH'
                                    #     if test_qual=='XIITH' or test_qual=='XII':
                                    #         test_qual=='12TH'
                                    #     if test_qual=='GRADUATE':
                                    #         test_qual=='GRADUATION'
                                    #     if degree_in[1] in  test_qual:
                                    #         degree_id = degree_in[0]

                                    # # # print(degree_list)
                                    # degree_id = Tbldegree.objects.using('table_db').filter(degreename=qual_level[i])[0].id                        
                                    # SUBJECT ID
                                    subject_text=""                        
                                    for sl in subject_list:  
                                        if sl!="":                       
                                            if sl.upper() in text[i].upper():                                
                                                subject_text+=sl                                
                                                break                        
                                    subject_id = Tblsubjects.objects.using('table_db').filter(subject=subject_text.strip())[0].id
                                    # SPECIALIZATION
                                    specialization = ""
                                    if level[i]=='Post Graduate':
                                        for sp in specialization_list:                  
                                            if sp!="" and sp!=None:
                                                if sp.upper() in text[i].upper():
                                                    specialization+=sp
                                                    break
                                    yearpassed = yop[i]    
                                    # # # print('percentage=========>>>>>>>>>>>.',percentage)                
                                    
                                    edumode_id = 1
                                    institute= Tblinstitutes.objects.using('table_db').filter(institutename=college[i])
                                    if institute:
                                        institute_id=institute[0].id
                                    if not institute:
                                        institute_id=Tblinstitutes.objects.using('table_db').create(institutename=college[i], is_active=1).id
                                        
                                    university_ = Tbluniversities.objects.using('table_db').filter(univname=university[i])
                                    if university_:
                                        university_id = university_[0].id
                                    if not university_:
                                        university_id = Tbluniversities.objects.using('table_db').create(univname=university[i], is_active=1).id
                                    
                                    # CHECK EDUCATION
                                    check_edu = Tbleducation.objects.using('table_db').filter(candidate_id = int(candid_id),qualification_id =edulevel_id,course_id = degree_id)
                                    if check_edu:
                                        pass
                                        # check_edu.update(subject_id=subject_id,subject=subject_text, specialization = specialization)
                                    if not check_edu:
                                        Tbleducation.objects.using('table_db').create(candidate_id = candid_id,qualification_id =edulevel_id,course_id = degree_id,subject_id=subject_id ,subject=subject_text, specialization = specialization, institute=institute_id, university=university_id, yearpassed = yop[i],percentage =percentage[i], edumode_id = 1)
                                    
                                    # SEARCHMETAS
                                    try:
                                        # QUALIFICATION_ID
                                        srch_q=Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key="qualification_id", meta_value=str(edulevel_id))
                                        if srch_q:
                                            pass
                                        if not srch_q:
                                            Tblsearchmeta.objects.using('table_db').create(candidate_id=candid_id,meta_key="qualification_id", meta_value=str(edulevel_id))
                                        # COURSE_ID
                                        srch_c=Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key="course_id", meta_value=str(degree_id))		
                                        if srch_c:
                                            pass
                                        if not srch_c:
                                            Tblsearchmeta.objects.using('table_db').create(candidate_id=candid_id,meta_key="course_id", meta_value=str(degree_id))		
                                        # INSTITUTE_ID
                                        srch_i=Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key="institute", meta_value=str(institute_id))
                                        if srch_i:
                                            pass
                                        if not srch_i:
                                            Tblsearchmeta.objects.using('table_db').create(candidate_id=candid_id,meta_key="institute", meta_value=str(institute_id))
                                        # UNIVERSITY_ID
                                        srch_u=Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key="university", meta_value=str(university_id))
                                        if srch_u:
                                            pass
                                        if not srch_u:
                                            Tblsearchmeta.objects.using('table_db').create(candidate_id=candid_id,meta_key="university", meta_value=str(university_id))
                                        # SUBJECT_ID
                                        srch_u=Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key="subject_id", meta_value=str(subject_id))
                                        if srch_u:
                                            pass
                                        if not srch_u:
                                            Tblsearchmeta.objects.using('table_db').create(candidate_id=candid_id,meta_key="subject_id", meta_value=str(subject_id))
                                    except:
                                        pass
                                    del degree_id
                                except:
                                    traceback.print_exc()
                                    # # # print(qual_level[i])
                    
                    except:
                        traceback.print_exc()
                        pass  
                    
                    # code for inserting file information
                    try:  # TBLCVFILES HERE ===>>>
                        restxt = 1
                        createdBy = 1
                        Tblcvfiles.objects.using('table_db').update_or_create(filename = str(str(candid_id)+"_"+str(file)), candidate_id = int(candid_id), resume_text = restxt, created_by = createdBy)			
                        logdata.append('tblcvfiles entry started')
                    except:
                        traceback.print_exc()
                        pass

                    # try:
                    #     desig_list=Tbldesignation.objects.using('table_db').values_list('designation',flat=True)
                    #     for desi in desig_list:
                    #         if desi.lower() in preprocessed.lower():
                    #             desi_id = Tbldesignation.objects.using('table_db').filter(designation=desi)[0].id
                    #             Tblsearchmeta.objects.using('table_db').update_or_create(candidate_id=candid_id, meta_key='designation_id', meta_value = desi_id)
                    # except:
                    #     pass
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
                    # # print('company=======',company_data)
                    # Experience
                    try:
                        com_name=[]
                        from_= []
                        to_= []
                        des_ = []
                        for com in company_data:
                            com_name.append(com['COMPANY'])
                            from_.append(com['FROM DATE'])
                            to_.append(com['TO DATE']) 
                            des_.append(com['DESIGNATION'])   

                    
                        if com_name[0]!="":                    
                            for i in range(len(com_name)):                        
                                try:
                                    compvar = com_name[i]   
                                    try:
                                        designation=des_[i]
                                        # # print('desig=====',designation)
                                        desig = Tbldesignation.objects.using('table_db').filter(designation=designation)
                                        # # print('tsdfdfdfdf')
                                        if desig:
                                            desig_id=desig[0].id
                                        else:
                                            # # print('not found')
                                            Tbldesignation.objects.using('table_db').create(designation=designation, created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                            desig_id=Tbldesignation.objects.using('table_db').filter(designation=designation)[0].id
                                    except:
                                        desig_id=None

                                    
                                    if from_[i] !="" and from_[i].count('-')==2 and len(from_[i])==10:
                                        strtdate = from_[i]#datetime.strptime(from_[i],"%d/%m/%Y").strftime("%Y-%m-%d")                                         
                                    else:
                                        strtdate= datetime.now().strftime("%Y-%m-%d")

                                    if to_[i]!="" and to_[i].count('-')==2 and len(to_[i])==10:
                                        enddate =  to_[i]#datetime.strptime(to_[i],"%d/%m/%Y").strftime("%Y-%m-%d")   
                                    else:
                                        enddate = datetime.now().strftime("%Y-%m-%d")   
                                        # enddate = '0000-00-00'
                                    # if strtdate == enddate:
                                    #     strtdate = None
                                    #     enddate = None
                                    # if strtdate>=current_date:
                                    #     strtdate=None
                                    # if enddate>=
                                    
                                    # if enddate!='0000-00-00':
                                    check=date_checker(enddate)
                                    if check==False:
                                        enddate=None
                                    check=date_checker(strtdate)
                                    if check==False:
                                        strtdate=None
                                                    
                                    Tblexperience.objects.using('table_db').update_or_create(candidate_id=candid_id,companyname=compvar,startdate = strtdate,enddate = enddate, designation_id=desig_id, country_id = 101,employmentnature="Undefined",tottalexp=1234)
                                except:
                                    traceback.print_exc()
                                    pass
                    except:
                        traceback.print_exc()
                        pass
                        

                    # # print('project testing')
                    
                    # candid_id = Tblcv.objects.using('table_db').filter(email=email)[0].id
                    # # print('candid',candid_id)
                    try:
                        

                        project_data = getprojectdetails(preprocessed)
                        # project_data=complete_data['project_dict']
                        # # print('project======',project_data)
                        work_name=project_data['title']
                        if project_data['title']!='':
                            for i in range(len(work_name)):
                                
                                project=work_name[i]
                                # print(project)
                                try:
                                    client=project_data['client'][i]
                                except:
                                    client=''
                                try:
                                    designation=project_data['position'][i]
                                    # # print('desig=====',designation)
                                    desig = Tbldesignation.objects.using('table_db').filter(designation=designation)
                                    # # print('tsdfdfdfdf')
                                    if desig:
                                        desig_id=desig[0].id
                                    else:
                                        # # print('not found')
                                        Tbldesignation.objects.using('table_db').create(designation=designation, created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                        desig_id=Tbldesignation.objects.using('table_db').filter(designation=designation)[0].id
                                except:
                                    desig_id=None
                                try:
                                    employer=project_data['employer'][i]
                                except:
                                    employer=''
                                # # print('d===',desig_id)
                                # project entry check
                                try:
                                    check_project=Tblfundedproject.objects.using('table_db').filter(candidate_id=candid_id,projdesig=str(desig_id),projectname = project,employername=employer)
                                    if not check_project:
                                        Tblfundedproject.objects.using('table_db').create(candidate_id=candid_id,projdesig=str(desig_id),projectname = project,industry_id=1,sector_id=1,phase_id=1,employername=employer,clientname=client)                               
                                        # Tblprodetails.objects.using('table_db').update_or_create(candidate_id=candid_id, fun_tbl_id = fun_tbl_id, sector=sector,phase=phase, length=float(length_final), funded_by=funded_by, contractmode = contract_text)

                                
                                except:
                                    traceback.print_exc()
                                    pass
                    except:
                        traceback.print_exc()
                        pass
                    try:  # PROJECT DETAILS ===>>>
                        project_work_list = Tblfundedproject.objects.using('table_db').filter(candidate_id=candid_id).values_list('id','projectname')                    
                        for i in project_work_list:
                            try:                        
                                l1=re.findall('([0-9]{1,}[.]{0,1}[0-9]{0,}[ ]{0,2}(m|mtr|km|kms{1}))',i[1].lower())
                                if len(l1)==0:
                                    length = ''
                                else:
                                    length=l1[0][0]
                                if len(l1)==0:
                                    l1 = re.findall('((from)[ ]{0,3}(km|m){0,1}[ ]{0,3}[0-9]{1,}[.]{0,1}[0-9]{0,}[ ]{0,2}(to)[ ]{0,3}(km|m){0,1}[ ]{0,3}[0-9]{1,}[.]{0,1}[0-9]{0,})',i[1].lower())
                                    if len(l1)==0:
                                        length = ''
                                    else:
                                        if 'km' in l1[0][0].lower():
                                            unit='km'
                                        else:
                                            unit='m'
                                        length_raw = sorted(re.findall('[0-9]{1,}[.]{0,1}[0-9]{0,}', l1[0][0]), reverse=True)
                                        length= ' '.join((str(round(float(length_raw[0])-float(length_raw[1]), 2)),unit))
                                funded_list = Tblfundagencies.objects.using('table_db').values_list('agencyname', flat=True)
                                sector_list = Tblsector.objects.using('table_db').values_list('sectorname', flat=True)
                                phase_list  = Tblphase.objects.using('table_db').values_list('phasename', flat=True)
                                contract_list = Tblcontractmode.objects.using('table_db').values_list('contractmode', flat=True)
                                industry_list = Tblindustry.objects.using('table_db').values_list('industryname', flat=True)
                                pavement_list = Tblpavement.objects.using('table_db').values_list('pavementname', flat=True)
                                terrain_list = Tblterrain.objects.using('table_db').values_list('terrainname', flat=True)                
                                lane_list = ['2 lane','4 lane','6 lane','8 lane']

                                industry_text=''
                                sec_text=''
                                phase_text=''
                                agency=''
                                contract_text = ''
                                pavement = ''
                                terrain = ''
                                lane_text=''

                                text = i[1]
                                for indu in industry_list:
                                    if indu.lower() in text.lower():
                                        indu_id = Tblindustry.objects.using('table_db').filter(industryname= indu)[0].id
                                        industry_text+=str(indu_id)
                                        break  
                                for sec in sector_list:
                                    if sec.lower() in text.lower():
                                        sec_id = Tblsector.objects.using('table_db').filter(sectorname = sec)[0].id
                                        sec_text+=str(sec_id)
                                        break
                                for ph in phase_list:
                                    if ph.lower() in text.lower():
                                        ph_id = Tblphase.objects.using('table_db').filter(phasename = ph)[0].id
                                        phase_text+=str(ph_id)
                                        break
                                for fun in funded_list:
                                    if fun.lower() in text.lower():
                                        fun_id = Tblfundagencies.objects.using('table_db').filter(agencyname=fun)[0].id
                                        agency+=str(fun_id)
                                        break
                                for ctc in contract_list:
                                    if ctc.lower() in text.lower():
                                        ctc_id = Tblcontractmode.objects.using('table_db').filter(contractmode = ctc)[0].id
                                        contract_text+=str(ctc_id)
                                        break   
                                for pvmt in pavement_list:
                                    if pvmt.lower() in text.lower():
                                        pvmt_id = Tblpavement.objects.using('table_db').filter(pavementname=pvmt)[0].id
                                        pavement+=str(pvmt_id)
                                        break   
                                for terr in terrain_list:
                                    if terr.lower() in text.lower():
                                        terr_id = Tblterrain.objects.using('table_db').filter(terrainname= terr)[0].id
                                        terrain+=str(terr_id)
                                        break   
                                for lane in lane_list:
                                    if lane.lower() in text.lower():                        
                                        lane_text+=lane
                                        break  
                                # convert to int
                                if industry_text!='':
                                    industry_id = int(industry_text)
                                else:
                                    industry_id = 5
                                if sec_text!='':
                                    sector_id = int(sec_text)
                                else:
                                    sector_id=14
                                if phase_text!='':
                                    phase_id = int(phase_text)
                                else:
                                    phase_id = 61
                                if agency !='':
                                    agency_id = int(agency)
                                else:
                                    agency_id = 20
                                if contract_text != '':
                                    contract_id = int(contract_text)
                                else:
                                    contract_id = 5
                                if  pavement != '':
                                    pavement_id = int(pavement)
                                else:
                                    pavement_id = 6
                                if terrain != '':
                                    terrain_id = int(terrain)
                                else:
                                    terrain_id=6
                                if lane_text!='':
                                    lane_text=re.sub(r'[A-z]','',lane_text)
                                    lane_int=int(float(lane_text))
                                else:
                                    lane_int=0                
                                # search meta
                                candid_id = candid_id

                                check1 = Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key='sector_id')
                                if check1:
                                    pass
                                else:
                                    Tblsearchmeta.objects.using('table_db').create(candidate_id=candid_id, meta_key='sector_id', meta_value=sec_text)
                                check2 = Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key='phase_id')
                                if check2:
                                    pass
                                else:
                                    Tblsearchmeta.objects.using('table_db').create(candidate_id=candid_id, meta_key='phase_id', meta_value=phase_text)
                                check3 = Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key='fundingagency_id')
                                if check3:
                                    pass
                                else:
                                    Tblsearchmeta.objects.using('table_db').create(candidate_id=candid_id, meta_key='fundingagency_id', meta_value=agency)
                                check4 = Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key='contractmode_id')
                                if check4:
                                    pass
                                else:
                                    Tblsearchmeta.objects.using('table_db').create(candidate_id=candid_id, meta_key='contractmode_id', meta_value=contract_text)
                                check5 = Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key='terrain_id')
                                if check5:
                                    pass
                                else:
                                    Tblsearchmeta.objects.using('table_db').create(candidate_id=candid_id, meta_key='terrain_id', meta_value=terrain)
                                check6 = Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key='pavement_id')
                                if check6:
                                    pass
                                else:
                                    Tblsearchmeta.objects.using('table_db').create(candidate_id=candid_id, meta_key='pavement_id', meta_value=pavement)

                                fun_tbl_id = i[0]
                                if 'm' in length.lower():
                                    if 'km' in length.lower():
                                        length_final=re.sub('[A-z]','',length)
                                    else:
                                        length_final = str(round(float(re.sub('[A-z]','',length))/1000, 2))
                                else:
                                    length_final=0.0 

                                test = Tblfundedproject.objects.using('table_db').filter(candidate_id=candid_id,projectname=i[1])
                                test.update(industry_id=industry_id, sector_id=sector_id, phase_id=phase_id, fundingagency_id=agency_id, contractmode_id=contract_id,pavement_id=pavement_id, terrain_id=terrain_id)
                                test.update(projectlength=abs(int(float(length_final))))
                                test.update(lane=lane_int)
                                # print('the candidate id is',candidate_id)
                                sector= sec_text
                                phase = phase_text
                                funded_by=agency
                                sector= sec_text
                                phase = phase_text
                                funded_by=agency                    
                                check_p_details = Tblprodetails.objects.using('table_db').filter(candidate_id=candid_id, fun_tbl_id = fun_tbl_id, sector=sector,phase=phase, length=float(length_final), funded_by=funded_by, contractmode = contract_text)
                                if check_p_details:
                                    pass
                                else:
                                    
                                    Tblprodetails.objects.using('table_db').update_or_create(candidate_id=candid_id, fun_tbl_id = fun_tbl_id, sector=sector,phase=phase, length=float(length_final), funded_by=funded_by, contractmode = contract_text)
                                
                            except:
                                traceback.print_exc()
                                pass
                    
                    except:
                        traceback.print_exc()
                        pass
                    
                    
                
        #                     protmpname = work_name[i]
                    #                     try:
                    #                         prostartdate=datetime.strptime(start_date[i],"%d/%m/%Y").strftime("%Y-%m-%d")
                    #                     except:
                    #                         prostartdate='1970-01-01'
                    #                     try:
                    #                         proenddate = (datetime.strptime(completion_date[i],"%d/%m/%Y").strftime("%Y-%m-%d"))
                    #                     except:
                    #                         proenddate= "1970-01-01"
                    #                     protmpdesig = designation[i]
                    #                     #get the designation id 
                    #                     protempclient=client[i]
                    #                     cntry_id = Tblcountries.objects.using('table_db').get_or_create(name=country[i])[0].id
                    #                     if cntry_id == 101:
                    #                         exp_  = 'N'
                    #                     else:
                    #                         exp_ = 'I'
            
                    #                     if project_cost[i].count('.')==1:
                    #                         pro_cost=project_cost[i].replace(',','')
                    #                         pro_cost=re.findall('\d*\.?\d+',pro_cost)
                    #                         if pro_cost:
                    #                             p_cost=float(pro_cost[0])
                    #                     else:
                    #                         p_cost=0.0
                
                    #                     desig = Tbldesignation.objects.using('table_db').filter(designation=designation[i])
                    #                     if desig:
                    #                         desig_id=desig[0].id
                    #                     else:
                    #                         desig_id=Tbldesignation.objects.using('table_db').create(designation=designation[i], created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id

                    #                     Tblfundedproject.objects.using('table_db').create(candidate_id=candid_id,startdate = prostartdate,enddate = proenddate,projdesig=str(desig_id),projectname = protmpname,industry_id=1,sector_id=1,phase_id=1,employername="Undefined",natureemployer='N',projectexp=exp_,country_id=cntry_id, state_id=5000, city_id=5000,projectcost = p_cost,clientname=protempclient,fundingagency_id=0)
                    #         except:
                    #             traceback.# print_exc()
                    #             pass
                    # except:
                        # pass
        else:
            # logger.warning(f'The file {file} is doc file so not readed')
            print('The file is a doc file')
            doc_path=os.path.join(doc_path,file)
            shutil.move(file_path,doc_path)
            exist=cvm_run_history.objects.using('table_db').filter(file_name=file).exists()
            if not exist:
                cvm_run_history.objects.using('table_db').create(file_name=file,file_path=doc_path,doc_file=1,completed=0)
            return 
        # logger.info(f'Completed the reading process of the file {file}')
        # remark+='Inserted the data in the file'
        exist=cvm_run_history.objects.using('table_db').filter(file_name=file).exists()
        if not exist:
            cvm_run_history.objects.using('table_db').create(candidate_id=candid_id,file_name=new_file_name,file_path=new_file_path,status=1,completed=1)
        print('***********************************************************************************************************')

    except:
        emmil=0
        traceback.print_exc()
        print('In the main exception block**************************')
        if not_email:
            emmil=1
            email_path=os.path.join(email_path,file)
            shutil.move(file_path,email_path)
            
        # logger.exception(f'Some exception occured in the file {file}')
        exist=cvm_run_history.objects.using('table_db').filter(file_name=file).exists()
        if not exist:
            cvm_run_history.objects.using('table_db').create(file_name=file,file_path=email_path,status=0,completed=0,email_not_found=emmil)
        # logger.info(traceback.format_exc()+'\n\n\n\n\n')
  