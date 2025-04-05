import requests
import re
import ast
from . education import PHD,GRADUATION,POST_GRADUATION,X,XII,DIPLOMA,CERTIFICATE_COURSE,CERTIFICATION_COURSE
from . tblmodels import education_degree_new
from . utils import logger_creater,format_date
def model_data(pdf_path,logger_model):
    try:
        logger=logger_model
        url = 'http://202.131.122.247:9008/resume' #  server 
        # url="http://192.168.11.172:8000/resume" # local 
        pdf_name=pdf_path.split('/')[-1]
        files = [('file', (f'{pdf_name}', open(pdf_path, 'rb'), 'application/octet-stream'))]
        empy_data={}
        empy_data['full_name']=None
        empy_data['education']=[]
        empy_data['experience']=[]
        empy_data['projects']=[]
        logger.info(f'-----------------------------The file path is {pdf_path}------------------------------------\n\n')
        response = requests.post(url, files=files)
        if response.status_code==200:
            logger.info('The model retuned the status code of 200')
            text=response.json()
            start=text.index('{')
            end=text.rindex('}')
            text=text[start:end+1]
            text=re.sub(r'(\\n+|\\+|//+)', '', text)
            text=re.sub('null','\"\"',text)
            text=text.replace(' No projects are mentioned in the provided resume text','')
            text=text.replace('  No projects mentioned in the provided resume text','')
            text=text.replace('No projects mentioned in the provided text','')
            logger.info(f'The text from the model is {text}')
            try:
                data = ast.literal_eval(text)
                logger.info(f'The data from the model is {data}')
                if isinstance(data, dict):
                    pass
                else:
                    data=None
            except:
                logger.exception(f'unable to get the data from the model text the text is{text}')
                print('returning empty data')
                return empy_data
                
            if data:
                full_name=data['full_name']
                educations=data['education']
                experiences=data['experience']
                projects=data['projects']
                if full_name!='':
                    name=full_name.split(' ')
                    while len(name)<3:
                        name.append('')
                    data.update({'First_Name':name[0]})
                    data.update({'Middle_Name':name[1]})
                    data.update({'Last_Name':name[2]})
                try:
                    if experiences!='':
                        data['company_data']=[]
                        for experience in experiences:
                            try:
                                if type(experience)==list or type(experience)==tuple:
                                    dic={}
                                    dic['COMPANY']=experience[1]
                                    dic['DESIGNATION']=experience[0]
                                    if experience[2]!='':
                                        try:
                                            dates=format_date(experience[2])
                                        except:
                                            dates=[]
                                if type(experience)==dict:
                                    dic={}
                                    try:
                                        dic['COMPANY']=experience['Company']
                                    except:
                                        continue
                                    try:
                                        dic['DESIGNATION']=experience['Role']
                                    except:
                                        pass
                                    try:
                                        dates=experience['Dates'].split('-')
                                    except:
                                        dates=[]
                                
                                # old date code ................................................................................
                                # if len(dates)==0:
                                #     from_date=None
                                #     to_date=None
                                    
                                # if len(dates)==1:
                                #     dates=str(dates[0]).split('–')
                                # if len(dates)==2:
                                #     from_date=dates[0]
                                #     from_date=reformat_date(from_date)
                                #     to_date=dates[1]
                                #     to_date=reformat_date(to_date)
                                # elif len(dates)==1:
                                #     from_date=dates
                                #     from_date=reformat_date(from_date)
                                #     to_date=None
                                    
                                #................................................................................................
                                if len(dates)==2:
                                    dic['FROM DATE']=dates[0]
                                    dic['TO DATE']=dates[1]
                                else:
                                    dic['FROM DATE']=""
                                    dic['TO DATE']=""
                                    
                                data['company_data'].append(dic)
                            except:
                                logger.exception('error in the loop of the model experience')
                except:
                    logger.exception('error in experience')
                    data['experience']=[]
                                
                try:
                    if educations!='':
                        data['education']=[]
                        for education in educations:
                            try:
                                dic={}
                                if type(education)==list or type(education)==tuple:
                                    level=education[0].upper()
                                elif type(education)==dict:
                                    level=education['Degree'].upper()
                                else:
                                    continue

                                if level in PHD:
                                    dic['LEVEL']='Doctorate'
                                elif level in GRADUATION:
                                    dic['LEVEL']='Graduation'
                                elif level in POST_GRADUATION:
                                    dic['LEVEL']='Post Graduate'
                                elif level in X:
                                    dic['LEVEL']='10th'
                                elif level in XII:
                                    dic['LEVEL'] ='12th'
                                elif level in DIPLOMA:
                                    dic['LEVEL']='Diploma'
                                else:
                                    dic['LEVEL']=None
                                    
                                # if not education_degree_new.objects.using('table_db').filter(degree=education[0].upper()).exists():
                                #     education_degree_new.objects.using('table_db').create(degree=education[0].upper())
                                #     print("A new record was inserted.")
                                # else:
                                #     print("Record already exists.")
                                    
                                if dic['LEVEL']!=None:
                                    if type(education)==list or type(education)==tuple:
                                        dic['QUALIFICATION_LEVEL']=education[0]
                                        dic['INSTITUTE_NAME']=education[1]
                                        dic['YEAR OF PASSING']=education[2]
                                        if len(education)>3:
                                            dic['GRADE']=education[3]
                                        else:
                                            dic['GRADE']=''
                                        dic['BOARD']=''
                                        dic['TEXT']=dic['QUALIFICATION_LEVEL']+dic['INSTITUTE_NAME']+dic['YEAR OF PASSING']+dic['GRADE']+dic['BOARD']

                                    elif type(education)==dict:
                                        dic['QUALIFICATION_LEVEL']=education['Degree']
                                        dic['YEAR OF PASSING']=education['Year']
                                        dic['INSTITUTE_NAME']=education['University']
                                        dic['GRADE']=education['Grade']
                                        dic['BOARD']=''
                                        dic['TEXT']=education['Degree']+education['University']+education['Year']+education['Grade']
                                    else:
                                        continue
                                    
                                    data['education'].append(dic)
                            except:
                                logger.exception('error in the loop of education model')
                    else:
                        data['education']=[]     
                       
                except:
                    logger.exception('error in education')
                    data['education']=[]   
                            
            else:
                print('returning empty data')
                logger.info('The model returned empty data \n\n')
                return empy_data
            logger.info(f'The model returned this data after extraction {data}\n\n')
            return data
        else:
            logger.info(f'The model returned empty data {response}\n\n')
            return empy_data
    except:
        logger.exception('error in the complete model and the model returned empty data \n\n')
        return empy_data