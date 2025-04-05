import re
from stop_words import get_stop_words
from nltk.corpus import stopwords
import spacy
import pgeocode
from guess_indian_gender import IndianGenderPredictor
from .name import name_recog


stop_words = list(get_stop_words('en'))         #Have around 900 stopwords
nltk_words = list(stopwords.words('english'))   #Have around 150 stopwords
stop_words.extend(nltk_words)
nlp = spacy.load('en_core_web_sm')
stop_words = [x for x in stop_words if x!='of']
from pathlib import Path
from os import path
BASE_DIR = Path(__file__).resolve().parent.parent
flurl = str(BASE_DIR) + "/media/"
# text_data2=[]
# for file in os.listdir('C:\\Users\\raj\\Desktop\\R315\\'):
#     txt = docx2txt.process('C:\\Users\\raj\\Desktop\\R315\\'+file)
#     txt = txt.replace("\n\n","  ")
#     txt = txt.replace("\n", "  ")
#     txt = txt.replace("\t","  ")
#     text_data2.append(txt)

class resumeparser():    
    def basic_details(txt):
        u_text=txt
        text=u_text.lower()
        text=text.replace('+91','')
        file_dict = {}
        numbers=[]
        for i in re.findall(re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'), text.replace('+91','')):
            if len(re.findall(r'[0-9]',i))==10 or len(re.findall(r'[0-9]',i))==12:
                i=''.join(re.findall(r'[0-9]',i))
                numbers.append(i[-10:])

        nums = list(dict.fromkeys(numbers))[:2]
        # emails = list(dict.fromkeys(re.findall(r'[\w\.-]+@[\w\.-]+', text)))
        emails=list(dict.fromkeys(re.findall(r'[\w\.-]+\s{0,1}@\s{0,1}[\w\.-]+\.\w{2,3}', text)))
        emails = emails[0:2]
        pan = list(dict.fromkeys(re.findall(r"[a-z]{5}[0-9]{4}[A-z]{1}", text)))
        passport = list(dict.fromkeys(re.findall(r"[a-z]{1}[0-9]{7}", text)))
        aadhar = list(dict.fromkeys(re.findall(r'aadhar [a-z]{2,6}[.]{0,1}[ ]{0,}[:-]{1}[ ]{0,}[0-9]{4}[ -]{0,1}[0-9]{4}[ -]{0,1}[0-9]{4}',text)))
        
        nationality = re.findall(r'nationality[ ]{0,}[:-]{1}[ ]{0,}[a-z]{1,}',text)
        # nationality=re.finditer(r'nationality(\s|\t|\n){0,}[-:]{1}')
        
        # dob = re.finditer(r"(date of birth|dob|d-o-b|d.o.b.)([ ]{0,}[-: ]{1}[ ]{0,})", text)  
        dob = re.finditer(r"(date of birth|dob|d-o-b|d.o.b.)(\s|\n|\t){0,}[-:]{0,1}(\s|\n|\t){0,}(.+)", text)
        dob_text=''
        for i in dob:
            dob_text = i.group(4).strip()[0:15]
            # print(text[i.end():i.end()+20])               
            break
        # print('dob==>>',dob)
        
        father_name = re.findall(r"(father[’]{0,1}[s]{0,1} name)([ ]{1,}[-: ]{1}[ ]{1,})([a-z]{1,}[.]{0,1}[ ]{0,}[a-z]{1,}[.]{0,1}[ ]{0,}[a-z]{1,}[.]{0,1}[ ]{0,1}[a-z]{0,})", text)
        mother_name = re.findall(r"(mother[’]{0,1}[s]{0,1} name)([ ]{1,}[-: ]{1}[ ]{1,})([a-z]{1,}[.]{0,1}[ ]{0,}[a-z]{1,}[.]{0,1}[ ]{0,}[a-z]{1,}[.]{0,1}[ ]{0,1}[a-z]{0,})", text)
        # gender = re.findall(r"(gender)([ ]{0,}[-:, ]{1}[ ]{0,})(^m|male|f|female)",text) 
        gender=''
        gen=re.finditer(r'(gender|sex){1}(\s|\n|\t){0,}[-:,]{1}(\s|\n|\t){0,}(male|m|female|f){1}',text)
        for x in gen:
            try:
                gender=x.group(4)
                if len(gender)!=0:
                    break
                else:
                    gender=''
            except:
                gender=''
                
                
        # print('the gender is ',gender)

        name_text = u_text[0:200]    
        t_list=name_recog(name_text)
        n_length=t_list
        if len(t_list)!=0:
            # n_length = t_list[0].split()
            if len(n_length) ==1:
                file_dict['First_Name'] = n_length[0] 
                file_dict['Middle_Name'] = ''
                file_dict['Last_Name'] =''
            if len(n_length) ==2:
                file_dict['First_Name'] = n_length[0] 
                file_dict['Middle_Name'] = ''
                file_dict['Last_Name'] = n_length[1]

            if len(n_length) ==3 or len(n_length)>3:
                file_dict['First_Name'] = n_length[0] 
                file_dict['Middle_Name'] = n_length[1]
                file_dict['Last_Name'] = n_length[2]

        if len(t_list)==0:
            file_dict['First_Name'] = 'Demo' 
            file_dict['Middle_Name'] = ''
            file_dict['Last_Name'] ='Demo' 

        if len(nums) ==1:
            file_dict['Primary Number']=nums[0]
            file_dict['Secondary Number'] = ''
        if len(nums)==2:
            file_dict['Primary Number']=nums[0]
            file_dict['Secondary Number']=nums[1]  
        if len(nums) == 0:
            file_dict['Primary Number']=''
            file_dict['Secondary Number'] = ''
            
        if file_dict['First_Name'] != '' and gender=='':    
            nomi = IndianGenderPredictor()
            na=file_dict['First_Name']
            gender_= nomi.predict(na) 
            # print('the gender is',gender)
            file_dict['GENDER'] = gender_
        else:
            if len(gender)!=0:
                file_dict['GENDER'] = gender
            else:
                file_dict['GENDER'] = ''
        
        if len(emails) ==1:
            file_dict['Primary Email']=emails[0]
            file_dict['Secondary Email'] = ''
        if len(emails)==2:
            file_dict['Primary Email']=emails[0]
            file_dict['Secondary Email']=emails[1]   

        if len(pan)==0:
            file_dict['Pan Number']=''       
        if len(pan)!=0:
            file_dict['Pan Number']=pan[0]   
        if len(passport)==0:
            file_dict['Passport Number']=''
        if len(passport)!=0:
            file_dict['Passport Number']=passport[0]   
        if len(aadhar)==0:
            file_dict['Aadhar Number'] = ''
        if len(aadhar)!=0:
            file_dict['Aadhar Number'] = aadhar[0]        
        if  len(nationality)==0:
            file_dict['Nationality'] = ''
        if len(nationality) !=0:
            file_dict['Nationality'] = re.findall(r'\s*([\S]+)$', nationality[0])[0]        

        file_dict['Date of Birth'] = dob_text        
        if len(father_name)==0:
            file_dict['Father Name'] = ''
        if len(father_name)!=0:
            file_dict['Father Name'] = father_name[0][2]        
        if len(mother_name)==0:
            file_dict['Mother Name'] = ''
        if len(mother_name) != 0:
            file_dict['Mother Name'] = mother_name[0][2]        
       
        return file_dict
    def ADDRESS(text):
        a_dict={} # address dict
        cu_dict={}
        pr_dict={}  # temporary dict
        co_dict={}
        
        if 'address' in text:  
            a=re.findall(r"(permanent address)(.+?(?=((?<!\d)\d{3}(?!\d) (?<!\d)\d{3}(?!\d))|((?<!\d)\d{6}(?!\d))))",text.lower())
            b=re.findall(r"(present address|current address|residance)(.+?(?=((?<!\d)\d{3}(?!\d) (?<!\d)\d{3}(?!\d))|((?<!\d)\d{6}(?!\d))))",text.lower())
            c=re.findall(r"(correspondance address)(.+?(?=((?<!\d)\d{3}(?!\d) (?<!\d)\d{3}(?!\d))|((?<!\d)\d{6}(?!\d))))",text.lower())            
            if len(a)==0 and len(b)==0 and len(c)==0:
                pin = re.findall(r'((?<!\d)\d{3}(?!\d) (?<!\d)\d{3}(?!\d))|((?<!\d)\d{6}(?!\d))', text)                
                if len(pin) != 0:
                    if pin[0][0]=='':
                        pin=pin[0][1]
                    else:
                        pin = pin[0][0]                    
                    index=text.index(pin)
                    words = text[:index].replace('-',' ').split()                    
                    nomi = pgeocode.Nominatim('IN')
                    d=nomi.query_postal_code(pin)                       
                    address = ' '.join([' '.join(words[-10:]),pin]).upper()                   
                    address=address.replace(d['country_code'].upper() ,'')
                    address=address.replace(d['state_name'].upper() ,'')
                    address=address.replace(d['county_name'].upper() ,'')
                    address=address.replace(d['postal_code'].upper() ,'')                    
                    pr_dict['ADDRESS']=''
                    pr_dict['CITY']=''
                    pr_dict['STATE']=''
                    pr_dict['COUNTRY']=''                   
                    pr_dict['ZIP CODE']=''
                    cu_dict['ADDRESS']=address
                    cu_dict['CITY']=d['county_name']
                    cu_dict['STATE']=d['state_name']
                    cu_dict['COUNTRY']='INDIA'                   
                    cu_dict['ZIP CODE']=d['postal_code']                    
                    co_dict['ADDRESS']=''
                    co_dict['CITY']=''
                    co_dict['STATE']=''
                    co_dict['COUNTRY']=''                   
                    co_dict['ZIP CODE']=''
                else:
                    pr_dict['ADDRESS']=''
                    pr_dict['CITY']=''
                    pr_dict['STATE']=''
                    pr_dict['COUNTRY']='INDIA'                    
                    pr_dict['ZIP CODE']=0
                    cu_dict['ADDRESS']=''
                    cu_dict['CITY']=''
                    cu_dict['STATE']=''
                    cu_dict['COUNTRY']='INDIA'                    
                    cu_dict['ZIP CODE']=0                    
                    co_dict['ADDRESS']=''
                    co_dict['CITY']=''
                    co_dict['STATE']=''
                    co_dict['COUNTRY']='INDIA'                    
                    co_dict['ZIP CODE']=0
            else:
                if len(a)!=0:                
                    address=re.sub('\s+',' ',' '.join(a[0][1:]).replace(':','').strip().upper())
                    pin = re.findall(r'((?<!\d)\d{3}(?!\d) (?<!\d)\d{3}(?!\d))|((?<!\d)\d{6}(?!\d))', address)
                    if pin[0][0]=='':
                        pin=pin[0][1]
                    else:
                        pin = pin[0][0]
                    nomi = pgeocode.Nominatim('IN')
                    d=nomi.query_postal_code(pin.replace(' ',''))                  
                    address=address.replace(d['country_code'].upper() ,'')
                    address=address.replace(d['state_name'].upper() ,'')
                    address=address.replace(d['county_name'].upper() ,'')
                    address=address.replace(d['postal_code'].upper() ,'')                   
                    pr_dict['ADDRESS']=address
                    pr_dict['CITY']=d['county_name']
                    pr_dict['STATE']=d['state_name']
                    pr_dict['COUNTRY']='INDIA'                   
                    pr_dict['ZIP CODE']=d['postal_code']  
                    
                    cu_dict['ADDRESS']=''
                    cu_dict['CITY']=''
                    cu_dict['STATE']=''
                    cu_dict['COUNTRY']=''                   
                    cu_dict['ZIP CODE']=0
                    
                    co_dict['ADDRESS']=''
                    co_dict['CITY']=''
                    co_dict['STATE']=''
                    co_dict['COUNTRY']=''                   
                    co_dict['ZIP CODE']=0
                
                if len(b)!=0:                
                    address=re.sub('\s+',' ',' '.join(b[0][1:]).replace(':','').strip().upper())
                    pin = re.findall(r'((?<!\d)\d{3}(?!\d) (?<!\d)\d{3}(?!\d))|((?<!\d)\d{6}(?!\d))', address)
                    if pin[0][0]=='':
                        pin=pin[0][1]
                    else:
                        pin = pin[0][0]
                    nomi = pgeocode.Nominatim('IN')
                    d=nomi.query_postal_code(pin.replace(' ',''))                  
                    address=address.replace(str(d['country_code']).upper() ,'')
                    address=address.replace(str(d['state_name']).upper() ,'')
                    address=address.replace(str(d['county_name']).upper() ,'')
                    address=address.replace(str(d['postal_code']).upper() ,'')
                    cu_dict['ADDRESS']=address
                    cu_dict['CITY']=d['county_name']
                    cu_dict['STATE']=d['state_name']
                    cu_dict['COUNTRY']='INDIA'                   
                    cu_dict['ZIP CODE']=d['postal_code']  
                    
                    pr_dict['ADDRESS']=''
                    pr_dict['CITY']=''
                    pr_dict['STATE']=''
                    pr_dict['COUNTRY']=''                   
                    pr_dict['ZIP CODE']=0
                    
                    co_dict['ADDRESS']=''
                    co_dict['CITY']=''
                    co_dict['STATE']=''
                    co_dict['COUNTRY']=''                   
                    co_dict['ZIP CODE']=0
                    
                
                if len(c)!=0:                
                    address=re.sub('\s+',' ',' '.join(c[0][1:]).replace(':','').strip().upper())
                    pin = re.findall(r'((?<!\d)\d{3}(?!\d) (?<!\d)\d{3}(?!\d))|((?<!\d)\d{6}(?!\d))', address)
                    if pin[0][0]=='':
                        pin=pin[0][1]
                    else:
                        pin = pin[0][0]
                    nomi = pgeocode.Nominatim('IN')
                    d=nomi.query_postal_code(pin.replace(' ',''))                  
                    address=address.replace(d['country_code'].upper() ,'')
                    address=address.replace(d['state_name'].upper() ,'')
                    address=address.replace(d['county_name'].upper() ,'')
                    address=address.replace(d['postal_code'].upper() ,'')
                    co_dict['ADDRESS']=address
                    co_dict['CITY']=d['county_name']
                    co_dict['STATE']=d['state_name']
                    co_dict['COUNTRY']='INDIA'                   
                    co_dict['ZIP CODE']=d['postal_code']
                    
                    pr_dict['ADDRESS']=''
                    pr_dict['CITY']=''
                    pr_dict['STATE']=''
                    pr_dict['COUNTRY']=''                   
                    pr_dict['ZIP CODE']=0 
                    
                    cu_dict['ADDRESS']=''
                    cu_dict['CITY']=''
                    cu_dict['STATE']=''
                    cu_dict['COUNTRY']=''                   
                    cu_dict['ZIP CODE']=0
                    
                    
        else:            
            pin = re.findall(r'((?<!\d)\d{3}(?!\d) (?<!\d)\d{3}(?!\d))|((?<!\d)\d{6}(?!\d))', text)
            if len(pin) != 0:
                if pin[0][0]=='':
                    pin=pin[0][1]
                else:
                    pin = pin[0][0]
                index = text.index(pin)
                words = text[:index].replace('-',' ').split()                 
                address = ' '.join([' '.join(words[-10:]),pin]).upper()  
                nomi = pgeocode.Nominatim('IN')
                d=nomi.query_postal_code(pin.replace(' ','')) 
                address=address.replace(str(d['country_code']).upper() ,'')
                address=address.replace(str(d['state_name']).upper() ,'')
                address=address.replace(str(d['county_name']).upper() ,'')
                address=address.replace(str(d['postal_code']).upper() ,'')        
                pr_dict['ADDRESS']=''
                pr_dict['CITY']=''
                pr_dict['STATE']=''
                pr_dict['COUNTRY']='INDIA'                    
                pr_dict['ZIP CODE']=0
                
                cu_dict['ADDRESS']=address
                cu_dict['CITY']=d['county_name']
                cu_dict['STATE']=d['state_name']
                cu_dict['COUNTRY']='INDIA'                   
                cu_dict['ZIP CODE']=d['postal_code']
                
                co_dict['ADDRESS']=''
                co_dict['CITY']=''
                co_dict['STATE']=''
                co_dict['COUNTRY']='INDIA'                    
                co_dict['ZIP CODE']=0
            else:
                pr_dict['ADDRESS']=''
                pr_dict['CITY']=''
                pr_dict['STATE']=''
                pr_dict['COUNTRY']=''                    
                pr_dict['ZIP CODE']=0
                
                cu_dict['ADDRESS']=''
                cu_dict['CITY']=''
                cu_dict['STATE']=''
                cu_dict['COUNTRY']=''                   
                cu_dict['ZIP CODE']=0
                
                co_dict['ADDRESS']=''
                co_dict['CITY']=''
                co_dict['STATE']=''
                co_dict['COUNTRY']=''                    
                co_dict['ZIP CODE']=0
        a_dict['PARMANENT_ADDRESS']= cu_dict
        a_dict['CURRENT_ADDRESS']=pr_dict
        a_dict['CORRESPONDANCE_ADDRESS']=co_dict
        return a_dict
    def LANGUAGES(text):
        ttxt = text.upper()
        l_known=[]
        LANGUAGES=['assamese','english','bengali','gujarati','hindi','kannada','kashmiri','konkani','malayalam','manipuri','marathi','nepali','oriya','punjabi','sanskrit','sindhi','tamil','telugu','urdu','bodo','santhali','maithili','dogri']
        languages=re.findall('(LANGUAGES KNOWN | LANGUAGE KNOWN )',ttxt)
        if len(languages)==0:
            languages.append(re.findall('LANGUAGES', ttxt))
        else:
            i = ttxt.index(languages[0].strip())
            ttxt = ttxt[i:i+60]
            ttxt = re.sub(r"[,.(:);@#?!&$/]+ *", "  ", ttxt)
            words = ttxt.split()
            for word in words:
                word=word.strip()
                if any(n in word.lower() for n in LANGUAGES)==True:
                    l_known.append(word)
        if len(l_known)==0:
            l_known.append('ENGLISH')
        return l_known
    
    # def binary_search(arr, x,instiute_name):
    #     low = 0
    #     high = len(arr)-1
    #     mid = 0
    #     x_before=x
    #     x=len(x)
    
    #     while low <= high:
    
    #         mid = (high + low) // 2
    
    #         # If x is greater, ignore left half
    #         if arr[mid] < x:
    #             low = mid + 1
    
    #         # If x is smaller, ignore right half
    #         elif arr[mid] > x:
    #             high = mid - 1
    
    #         # means x is present at mid
    #         else:
    #             while arr[mid]<=x:
    #                 mid_before=instiute_name[mid]
    #                 mid_text=re.sub(r"[,;@#?!&$/%^\s.]+ *"," ", mid_before)
    #                 mid_text=mid_text.replace(' ','')
    #                 if mid_text.lower()==x_before.lower():
    #                     return mid_text
    #                 else:
    #                     mid+=1
    #             return -1
                   
                        
                    
    
        # If we reach here, then the element was not present
        return -1
    