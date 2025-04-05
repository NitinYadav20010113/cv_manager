from tqdm import tqdm
import re
import pdfplumber
from nltk import flatten
import os
# def pdftotxt(pdf):
#     tables=[]
#     with pdfplumber.open(pdf) as pdf:
#         pages = pdf.pages
#         for i,pg in enumerate(pages):
#             tbl = pages[i].extract_tables()
#             tables.append(tbl)
#     return tables
# def remove_none_type(table):
#     for i in range(len(table)):
#         for j in range(len(table[i])):
#             for k in range(len(table[i][j])):
#                 table[i][j][k]=[j for j in table[i][j][k] if j!=None]  
#     return table
# def replace_nline_c(l):
#     l=[j.replace('\n',' ') for j in l]
#     return l

# def cvdata(filename):
#   text = ""
#   tables=[]
#   with pdfplumber.open(filename) as pdf:
#       pages = pdf.pages
#       for i,pg in enumerate(pages):
#           tbl = pages[i].extract_tables()
#           tables.append(tbl)
#   final_data2=[]
#   for i in tables:
#       for j in i:
#           for k in j:
#               k=[x.strip() for x in k if x!=None]
#               final_data2.append(k)
#   for arr in final_data2:
#     if arr!=None and arr[0]!='':
#       t_txt = ' '.join(arr)
#       t_txt = t_txt.replace('\n',' ')
#       text+=t_txt
#       text+=" "
#   return text


def parsing(filename):
    try:
        dd={}
        final_data=[]
        tables=[]
        with pdfplumber.open(filename) as pdf:
            pages = pdf.pages
            for i,pg in enumerate(pages):
                tbl = pages[i].extract_tables()
                tables.append(tbl)
        final_data2=[]
        final_data3=[]
        for i in tables:
            for j in i:
                for k in j:
                    k=[x.strip().replace('\xa0',' ').replace('\xad',' ').replace('\n',' ') for x in k if x!=None]                    
                    final_data3.append(k)
                    final_data2.append(k)
                        
        final_data.append(final_data2) 
        
        text = ""
        for arr in final_data3:            
            if arr!=None and arr[0]!='':
                t_txt = ' '.join(arr)
                t_txt = t_txt.replace('\n',' ')
                text+=t_txt
                text+=" "
        dd['cvtext']=text
        
        for file in final_data:   # basic information dict
            for l in file:
                if l[0].startswith('Registration Date:'):
                    t_list=l[0].split('\n')
                    try:
                        dd['Registration date']=t_list[0].split(':')[1].strip()
                    except:
                        dd['Registration date']=''
                    try:
                        dd['Last modified']=t_list[1].split(':')[1].strip()
                    except:
                        dd['Last modified']=''
                    try:
                        dd['Last accepted']=t_list[2].split(':')[1].strip()
                    except:
                        dd['Last accepted']=''
                if l[0].startswith('Aadhar Number'):
                    try:
                        dd['Adhaar no']=re.findall('^[2-9]{1}[0-9]{3}\\s[0-9]{4}\\s[0-9]{4}$',l[1])[0]
                    except:
                        dd['Adhaar no']='0'
                if l[0].startswith('Name'):
                    try:
                        dd['Name']=l[1]
                    except:
                        dd['Name']='X Y Z'
                if l[0].startswith('DOB'):
                    try:
                        dd['DOB']=l[1]
                    except:
                        dd['DOB']=''
                if l[0].startswith('Mother Name'):
                    try:
                        dd['Mother Name']=l[1]
                    except:
                        dd['Mother Name']=''
                if l[0].startswith('Father Name'):                
                    try:
                        dd['Father Name']=l[1]
                    except:
                        dd['Father Name']=''                     
                if l[0].startswith('Email'):
                    try:
                        dd['Email']=l[1]
                    except:
                        dd['Email']=''
                if l[0].startswith('Current State'):
                    try:
                        dd['Current State']=l[1]
                    except:
                        dd['Current State']=''
                if l[0].startswith('Current District'):
                    try:
                        dd['Current District']=l[1]
                    except:
                        dd['Current District']=''
                if l[0].startswith('Current Address'):
                    try:
                        dd['Current Address']=l[1]
                    except:
                        dd['Current Address']=''
                if l[0].startswith('Current Pin'):
                    try:
                        dd['Current Pin']=l[1]
                    except:
                        dd['Current Pin']=''
                if l[0].startswith('Permanent State'):
                    try:
                        dd['Permanent State']=l[1]
                    except:
                        dd['Permanent State']=''
                if l[0].startswith('Permanent District'):
                    try:
                        dd['Permanent District']=l[1]
                    except:
                        dd['Permanent District']=''
                if l[0].startswith('Permanent Address'):
                    try:
                        dd['Permanent Address']=l[1]
                    except:
                        dd['Permanent Address']=''
                if l[0].startswith('Permanent Pin'):
                    try:
                        dd['Permanent Pin']=l[1]
                    except:
                        dd['Permanent Pin']=''
                
                if l[0].startswith('PAN Number'):
                    try:
                        dd['PAN Number']=re.findall(r"[A-z]{5}[0-9]{4}[A-z]{1}",l[1])[0]
                    except:
                        dd['PAN Number']='0'             
                        
                if l[0].startswith('Passport Number'):
                    try:
                        dd['Passport Number']=re.findall("^[A-PR-WYa-pr-wy][1-9]\\d\\s?\\d{4}[1-9]$",l[1])[0]
                    except:
                        dd['Passport Number']='0'

                if l[0].startswith('Mobile'):
                    try:
                        dd['Mobile']=l[1]
                    except:
                        dd['Mobile']=''
                if l[0].startswith('Alternate Mobile'):
                    try:
                        dd['Alternate Mobile']=l[1]
                    except:
                        dd['Alternate Mobile']=''
                if l[0].startswith('Landline Number'):
                    try:
                        dd['Landline Number']=l[1]
                    except:
                        dd['Landline Number']=''
                if l[0].startswith('UAN Number'):
                    try:
                        dd['UAN Number']=l[1]
                    except:
                        dd['UAN Number']=''            
                if l[0].startswith('Knowledge of Modern'):
                    try:
                        dd['Knowledge of Modern']=l[1]
                    except:
                        dd['Knowledge of Modern']=''
        
        try:    #qualification dict
            qual_test_data=[]    
            for file in final_data: 
                qual_s_index=0
                for lis in file:             
                    if 8<=len(lis)<=10:
                        qual_test_data.append(lis)
            for test in qual_test_data[1:]:
                if len(test)>4:
                    if 'Work Name' in ' '.join(test):
                        e_index=qual_test_data.index(test)

            final_qual_data2 = qual_test_data[1:e_index]
            check = ['http://infracon.nic.in','asp?k','&EncHid=','INFRACON, Ministry of Road Transport', 'Transport & consultant_highways,','highways, Government of India']
            final_qual_data = []

            for fqd in final_qual_data2:
                if  any(x in ''.join(fqd) for x in check)==True:
                    pass
                else:
                    final_qual_data.append(fqd)
            level=[]
            Qualification_Level=[]
            Topic_Subject=[]
            College=[]
            University_Board=[]
            Y_of_P=[]
            Percentage=[]
            Certificate_Details=[]
            Certificate_Uploaded=[]
            Supporting_Documents=[]
            for i in final_qual_data:
                i=[x.replace('\n',' ') for x in i ]
                # print(i)
                if 8<=len(i)<=10 and i.count('')<5:
                    level.append(i[0])
                    Qualification_Level.append(i[1])
                    Topic_Subject.append(i[2])
                    College.append(i[3])
                    University_Board.append(i[4])
                    Y_of_P.append(i[5])
                    Percentage.append(i[6])
                            
            dd['level']=level
            dd['qual_level']=Qualification_Level
            dd['topic']=Topic_Subject
            dd['college']=College
            dd['university']=University_Board
            dd['yop']=Y_of_P
            dd['percentage']=Percentage 
        except:
            dd['level']=''
            dd['qual_level']=''
            dd['topic']=''
            dd['college']= ''
            dd['university'] = ''
            dd['yop']= ''
            dd['percentage']= '' 
        try:   # company dict
            com_test_data2=[]    
            for file in final_data:         
                for lis in file:             
                    if len(lis)==5 and lis[0].isdigit()==True:
                        if lis[2].count('/')==2 or lis[3].count('/')==2:
                            lis=[x.replace('\n',' ') for x in lis]
                            com_test_data2.append(lis)
            check = ['http://infracon.nic.in','asp?k','&EncHid=','INFRACON, Ministry of Road Transport', 'Transport & consultant_highways,','highways, Government of India']
            com_test_data = []

            for fqd in com_test_data2:
                if  any(x in ''.join(fqd) for x in check)==True:
                    pass
                else:
                    com_test_data.append(fqd)
            Sno=[]
            Company_Name=[]
            From_Year=[]
            To_Year=[]
            View_File=[]
            for lis in com_test_data:                               
                    Sno.append(lis[0])
                    Company_Name.append(lis[1])
                    From_Year.append(lis[2])
                    To_Year.append(lis[3])
                    View_File.append(lis[4])
            dd['sno_company']=Sno
            dd['company_name']=Company_Name
            dd['from_year']=From_Year
            dd['to_year']=To_Year
            dd['view_file']=View_File
        except:
            dd['sno_company']=''
            dd['company_name']=''
            dd['from_year']=''
            dd['to_year']=''
            dd['view_file']=''
        try:    #project dict
            proj_test_data=[]    
            for file in final_data:         
                for lis in file:             
                    if 8<=len(lis)<=10:
                        lis=[x.replace('\n',' ') for x in lis]
                        proj_test_data.append(lis)
            
            for test in proj_test_data[1:]:
                if len(test)>5:
                    if 'Work Name' in ' '.join(test):
                        s_index=proj_test_data.index(test)
            
            final_proj_data2 = proj_test_data[s_index+1:]
            
            check = ['http://infracon.nic.in','asp?k','&EncHid=','INFRACON, Ministry of Road Transport', 'Transport & consultant_highways,','highways, Government of India']
            final_proj_data = []

            for fqd in final_proj_data2:
                if  any(x in ''.join(fqd) for x in check)==True:
                    pass
                else:
                    final_proj_data.append(fqd)
            print(final_proj_data)
            Sno=[]
            Work_Name=[]
            Client=[]
            Designation=[]
            Project_Cost=[]
            Start_Date=[]
            Completion_Date=[]
            Country=[]
            # Details=[]
            # Supporting_Documents=[]            
            for i in final_proj_data:
                try:
                    if i[0].isdigit()==True and i.count('')<3:
                        if i[5].count('/')==2 or i[5]=='':
                            if i[6].count('/')==2 or i[6]=='':                    
                                Sno.append(i[0])
                                Work_Name.append(i[1])
                                Client.append(i[2])
                                Designation.append(i[3])
                                Project_Cost.append(i[4])
                                Start_Date.append(i[5])
                                Completion_Date.append(i[6])
                                Country.append(i[7])
                                # Details.append(i[8])
                                # Supporting_Documents.append(i[9])
                            if 8<=len(i)<=10 and i.count('')>5:
                                Work_Name[-1]=Work_Name[-1]+' '+i[1]
                except:
                    pass
            dd['sno_work']=Sno
            dd['work_name']=Work_Name
            dd['client']=Client
            dd['designation']=Designation
            dd['project_cost']=Project_Cost
            dd['start_date']=Start_Date
            dd['completion_date']=Completion_Date
            dd['country']=Country
            # dd['details']=Details
            # dd['supporting_documents']=Supporting_Documents
        except:
            dd['sno_work']=''
            dd['work_name']=''
            dd['client']=''
            dd['designation']=''
            dd['project_cost']=''
            dd['start_date']=''
            dd['completion_date']=''
            dd['country']=''
            dd['details']=''
            dd['supporting_documents']=''
        try:    # dict check
            if 'cvtext' not in dd.keys():
                dd['cvtext']=''

            if 'Adhaar no' not in dd.keys():
                dd['Adhaar no']=''
            if 'Name' not in dd.keys():
                dd['Name']=''
            if 'DOB' not in dd.keys():
                dd['DOB']=''
            if 'Mother Name' not in dd.keys():
                dd['Mother Name']=''
            if 'Father Name' not in dd.keys():
                dd['Father Name']=''
            if 'Email' not in dd.keys():
                dd['Email']=''
            if 'Current State' not in dd.keys():
                dd['Current State']=''
            if 'Current District' not in dd.keys():
                dd['Current District']=''
            if 'Current Address' not in dd.keys():
                dd['Current Address']=''
            if 'Current Pin' not in dd.keys():
                dd['Current Pin']=''
            if 'Permanent State' not in dd.keys():
                dd['Permanent State']=''
            if 'Permanent District' not in dd.keys():
                dd['Permanent District']=''
            if 'Permanent Address' not in dd.keys():
                dd['Permanent Address']=''
            if 'Permanent Address' not in dd.keys():
                dd['Permanent Address']=''
            if 'PAN Number' not in dd.keys():
                dd['PAN Number']=''
            if 'Passport Number' not in dd.keys():
                dd['Passport Number']=''
            if 'Mobile' not in dd.keys():
                dd['Mobile']=''
            if 'Alternate Mobile' not in dd.keys():
                dd['Alternate Mobile']=''
            if 'Landline Number' not in dd.keys():
                dd['Landline Number']=''
            if 'UAN Number' not in dd.keys():
                dd['UAN Number']=''
            if 'Knowledge of Modern' not in dd.keys():
                dd['Knowledge of Modern']=''
            if 'level' not in dd.keys():
                dd['level']=''
            if 'qual_level' not in dd.keys():
                dd['qual_level']=''
            if 'topic' not in dd.keys():
                dd['topic']=''
            if 'college' not in dd.keys():
                dd['college']=''
            if 'university' not in dd.keys():
                dd['university']=''
            if 'yop' not in dd.keys():
                dd['yop']=''
            if 'percentage' not in dd.keys():
                dd['percentage']=''
            # if 'certificate_details' not in dd.keys():
            #     dd['certificate_details']=''
            # if 'certificate_uploaded' not in dd.keys():
            #     dd['certificate_uploaded']=''
            # if 'supporting_documents' not in dd.keys():
            #     dd['supporting_documents']=''
            if 'sno_company' not in dd.keys():
                dd['sno_company']=''        
            if 'company_name' not in dd.keys():
                dd['company_name']=''
            if 'from_year' not in dd.keys():
                dd['from_year']=''
            if 'to_year' not in dd.keys():
                dd['to_year']=''
            if 'view_file' not in dd.keys():
                dd['view_file']=''
            if 'sno_work' not in dd.keys():
                dd['sno_work']=''
            if 'work_name' not in dd.keys():
                dd['work_name']=''
            if 'client' not in dd.keys():
                dd['client']=''
            if 'designation' not in dd.keys():
                dd['designation']=''
            if 'project_cost' not in dd.keys():
                dd['project_cost']=''
            if 'start_date' not in dd.keys():
                dd['start_date']=''
            if 'completion_date' not in dd.keys():
                dd['completion_date']=''
            if 'country' not in dd.keys():
                dd['country']=''
            if 'details' not in dd.keys():
                dd['details']=''
        except:
            pass
        # print(dd['sno_work'])
        # print('*********************************')
        return dd
    except:
        pass
        