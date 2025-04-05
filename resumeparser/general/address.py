import re
from stop_words import get_stop_words
from nltk.corpus import stopwords
import spacy
import pgeocode
from guess_indian_gender import IndianGenderPredictor
from nltk.tokenize import sent_tokenize, word_tokenize
from .tblmodels import pincode_master
import traceback



def ADDRESS(text):
        a_dict={} # address dict
        cu_dict={}
        pr_dict={}  # temporary dict
        co_dict={}

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
        try:
            if 'address' or 'add' in text.lower():  
                text = re.sub(r"[,():;@#?!&$/\n\s\t]+ *", " ", text)
                # a=re.findall(r"(permanent address)(.+?(?=((?<!\d)\d{3}(?!\d) (?<!\d)\d{3}(?!\d))|((?<!\d)\d{6}(?!\d))))",text.lower())
                a = re.findall(r"(permanent address)(.+?(?=((?<!\d)\d{3}(?!\d) (?<!\d)\d{3}(?!\d))|((?<!\d)\d{6}(?!\d))))", text.lower())
                b=re.findall(r"(present address|current address|residance|add)(.+?(?=((?<!\d)\d{3}(?!\d) (?<!\d)\d{3}(?!\d))|((?<!\d)\d{6}(?!\d))))",text.lower())
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
                        # address=address.replace(d['country_code'].upper() ,'')
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
                        text = re.sub(r"[\n\t,;@+#?!&$.:/%^\"°-]+ *"," ", text)
                        district_list = list(pincode_master.objects.using('table_db').values_list('pincode', 'district'))
                        cv_beginning = text[0:400]
                        cv_ending = text[len(text)-500:len(text)]
                        cv_beginning_words = word_tokenize(cv_beginning)
                        cv_ending_words = word_tokenize(cv_ending)
                        # refiltered_words = [word for word in words if word.lower() not in district_list]
                        filtered_words1 = [(pincode,district) for pincode, district in district_list if any(word.lower() == district.lower() for word in cv_beginning_words)]
                        if len(filtered_words1) != 0:
                            pin = str(filtered_words1[0][0])
                            if "address" in cv_beginning.lower():
                                add_start = re.search('address', cv_beginning.lower())
                                add_end = re.search(filtered_words1[0][1].lower(), cv_beginning.lower())
                                address = cv_beginning[add_start.end()+1 : add_end.start()]
                                cu_dict['ADDRESS']=address
                            nomi = pgeocode.Nominatim('IN')
                            d=nomi.query_postal_code(pin)

                            cu_dict['CITY']=d['county_name']
                            cu_dict['STATE']=d['state_name']
                            cu_dict['COUNTRY']='INDIA'
                            cu_dict['ZIP CODE']=d['postal_code']
                            pr_dict['ADDRESS']=address
                            pr_dict['CITY']=d['county_name']
                            pr_dict['STATE']=d['state_name']
                            pr_dict['COUNTRY']='INDIA'                 
                            pr_dict['ZIP CODE']=d['postal_code']


                        else: 
                            filtered_words2 = [(pincode,district) for pincode, district in district_list if any(word.lower() == district.lower() for word in cv_ending_words)]
                            if len(filtered_words2) != 0:
                                pin = str(filtered_words2[0][0])   
                                if "address" in cv_ending.lower():  
                                    add_start = re.search('address', cv_ending.lower())
                                    add_end = re.search(filtered_words2[0][1].lower(), cv_ending.lower())
                                    address = cv_ending[add_start.end()+1 : add_end.end()]     
                                    cu_dict['ADDRESS']=address           
                                nomi = pgeocode.Nominatim('IN')
                                d=nomi.query_postal_code(pin)                                      
                                pr_dict['ADDRESS']=address
                                pr_dict['CITY']=d['county_name']
                                pr_dict['STATE']=d['state_name']
                                pr_dict['COUNTRY']='INDIA'                 
                                pr_dict['ZIP CODE']=d['postal_code']
                                

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
                else:
                    if len(a)!=0:                
                        address=re.sub('\s+',' ',' '.join(a[0][1:]).replace(':','').strip().upper())
                        if len(address) > 90:
                            cv_words = word_tokenize(address)
                            district_list = list(pincode_master.objects.using('table_db').values_list('pincode', 'district'))
                            filtered_words = [(pincode,district) for pincode, district in district_list if any(word.lower() == district.lower() for word in cv_words)]
                            add_stop = re.search(filtered_words[0][1].lower(), address.lower())
                            address = address[: add_stop.end()]
                        pin = re.findall(r'((?<!\d)\d{3}(?!\d) (?<!\d)\d{3}(?!\d))|((?<!\d)\d{6}(?!\d))', address)
                        text = re.sub(r"[\n\t,;@+#?!&$.:/%^\"°-]+ *"," ", text)
                        if pin[0][0]=='':
                            pin=pin[0][1]
                        else:
                            pin = pin[0][0]
                        nomi = pgeocode.Nominatim('IN')
                        d=nomi.query_postal_code(pin.replace(' ',''))                  
                        # address=address.replace(d['county_code'].upper(),'')
                        address=address.replace(d['state_name'].upper() ,'')
                        address=address.replace(d['county_name'].upper() ,'')
                        address=address.replace(d['postal_code'].upper() ,'')                   
                        pr_dict['ADDRESS']=address
                        pr_dict['CITY']=d['county_name']
                        pr_dict['STATE']=d['state_name']
                        pr_dict['COUNTRY']='INDIA'                   
                        pr_dict['ZIP CODE']=d['postal_code']  
                        cu_dict['ADDRESS']=address
                        cu_dict['CITY']=d['county_name']
                        cu_dict['STATE']=d['state_name']
                        cu_dict['COUNTRY']='INDIA'                   
                        cu_dict['ZIP CODE']=d['postal_code'] 
                        
                    
                    if len(b)!=0:                
                        address=re.sub('\s+',' ',' '.join(b[0][1:]).replace(':','').strip().upper())
                        pin = re.findall(r'((?<!\d)\d{3}(?!\d) (?<!\d)\d{3}(?!\d))|((?<!\d)\d{6}(?!\d))', address)
                        if len(address) > 90:
                            cv_words = word_tokenize(address[:90])
                            district_list = list(pincode_master.objects.using('table_db').values_list('pincode', 'district'))
                            filtered_words = [(pincode,district) for pincode, district in district_list if any(word.lower() == district.lower() for word in cv_words)]
                            add_stop = re.search(filtered_words[0][1].lower(), address.lower())
                            address = address[: add_stop.end()]
                        text = re.sub(r"[\n\t,;@+#?!&$.:/%^\"°-]+ *"," ", text)
                        if pin[0][0]=='':
                            pin=pin[0][1]
                        else:
                            pin = pin[0][0]
                        nomi = pgeocode.Nominatim('IN')
                        d=nomi.query_postal_code(pin.replace(' ',''))                  
                        # address=address.replace(str(d['county_code']).upper() ,'')
                        address=address.replace(str(d['state_name']).upper() ,'')
                        address=address.replace(str(d['county_name']).upper() ,'')
                        address=address.replace(str(d['postal_code']).upper() ,'')
                        cu_dict['ADDRESS']=address
                        cu_dict['CITY']=d['county_name']
                        cu_dict['STATE']=d['state_name']
                        cu_dict['COUNTRY']='INDIA'                   
                        cu_dict['ZIP CODE']=d['postal_code']
                        if len(a)==0:
                            pr_dict['ADDRESS']=address
                            pr_dict['CITY']=d['county_name']
                            pr_dict['STATE']=d['state_name']
                            pr_dict['COUNTRY']='INDIA'                   
                            pr_dict['ZIP CODE']=d['postal_code'] 
                        
                    
                    if len(c)!=0:                
                        address=re.sub('\s+',' ',' '.join(c[0][1:]).replace(':','').strip().upper())
                        if len(address) > 90:
                            cv_words = word_tokenize(address)
                            district_list = list(pincode_master.objects.using('table_db').values_list('pincode', 'district'))
                            filtered_words = [(pincode,district) for pincode, district in district_list if any(word.lower() == district.lower() for word in cv_words)]
                            add_stop = re.search(filtered_words[0][1].lower(), address.lower())
                            address = address[: add_stop.end()]
                        pin = re.findall(r'((?<!\d)\d{3}(?!\d) (?<!\d)\d{3}(?!\d))|((?<!\d)\d{6}(?!\d))', address)
                        text = re.sub(r"[\n\t,;@+#?!&$.:/%^\"°-]+ *"," ", text)
                        if pin[0][0]=='':
                            pin=pin[0][1]
                        else:
                            pin = pin[0][0]
                        nomi = pgeocode.Nominatim('IN')
                        d=nomi.query_postal_code(pin.replace(' ',''))                  
                        # address=address.replace(d['county_code'].upper() ,'')
                        address=address.replace(d['state_name'].upper() ,'')
                        address=address.replace(d['county_name'].upper() ,'')
                        address=address.replace(d['postal_code'].upper() ,'')
                        co_dict['ADDRESS']=address
                        co_dict['CITY']=d['county_name']
                        co_dict['STATE']=d['state_name']
                        co_dict['COUNTRY']='INDIA'                   
                        co_dict['ZIP CODE']=d['postal_code']
                        
            else:            
                pin = re.findall(r'((?<!\d)\d{3}(?!\d) (?<!\d)\d{3}(?!\d))|((?<!\d)\d{6}(?!\d))', text)
                text = re.sub(r"[\n\t,;@+#?!&$.:/%^\"°-]+ *"," ", text)
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
                    # address=address.replace(str(d['county_code']).upper() ,'')
                    address=address.replace(str(d['state_name']).upper() ,'')
                    address=address.replace(str(d['county_name']).upper() ,'')
                    address=address.replace(str(d['postal_code']).upper() ,'')        

                    cu_dict['ADDRESS']=d['county_name']
                    cu_dict['CITY']=d['county_name']
                    cu_dict['STATE']=d['state_name']
                    cu_dict['COUNTRY']='INDIA'                   
                    cu_dict['ZIP CODE']=d['postal_code']

                    
                else:
                    district_list = list(pincode_master.objects.using('table_db').values_list('pincode', 'district'))
                    starting_text = text[0:300]
                    # ending_text = text[len(text)-400:len(text)]
                    starting_words = word_tokenize(starting_text)
                    # ending_words = word_tokenize(ending_text)
                    # refiltered_words = [word for word in words if word.lower() not in district_list]
                    filtered_words1 = [pincode for pincode, district in district_list if any(word.lower() == district.lower() for word in starting_words)]
                    if len(filtered_words1) != 0:
                        pin = str(filtered_words1[0])                
                        nomi = pgeocode.Nominatim('IN')
                        d=nomi.query_postal_code(pin)                                      
                        cu_dict['ADDRESS']=d['county_name']
                        cu_dict['CITY']=d['county_name']
                        cu_dict['STATE']=d['state_name']
                        cu_dict['COUNTRY']='INDIA'                   
                        cu_dict['ZIP CODE']=d['postal_code']  
    

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
            a_dict['PARMANENT_ADDRESS']= pr_dict
            a_dict['CURRENT_ADDRESS']= cu_dict
            a_dict['CORRESPONDANCE_ADDRESS']=co_dict
            return a_dict
        except:
            traceback.print_exc()
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
            
            a_dict['PARMANENT_ADDRESS']= pr_dict
            a_dict['CURRENT_ADDRESS']= cu_dict
            a_dict['CORRESPONDANCE_ADDRESS']=co_dict
            return a_dict



# text = 'Permanent address : Jai Bhawani Ngr., Ch. Manpada, Ghodbunder Road,\nThane (West), Maharashtra, INDIA, 301002\n\nDate of Birth : 02nd March 1991'
# # print(ADDRESS(text))
# discrict = "kanpur"
# indian_names=list(pincode_master.objects.using('table_db').values_list('pincode', 'district', 'state'))
# queryset = pincode_master.objects.using('table_db').filter(district="alwar")
# print((queryset.first()).pincode)
# print((queryset.first()).district)
# print((queryset.first()).state)
# for item in queryset:
#     print(item.pincode, item.district, item.state)
# print("this is queryset===========",len(queryset))
# print(indian_names)