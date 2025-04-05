from django.shortcuts import render, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from guess_indian_gender import IndianGenderPredictor
import re, shutil,os, glob, time
import pyqrcode, png
from fitz import fitz, Rect
from datetime import datetime
from dateutil.tz import gettz
from nltk import ngrams
from .reg import parsing
from .namesplit import split
from .tblmodels import Tblcv, Tblsearch, Tblcontractmode,Tblfundagencies,Tblpavement,Tblterrain,Tblprodetails,Tblphase, Tblsector, Tblindustry, Tblsearchmeta, Tblcvkeywords, Tblkeywords, Tbllanguage_gen, Tbledumode, Tbledulevel,Tblcvfiles,Tbladdress,Tblcountries, Tblcities, Tblstates,Tbleducation,Tblexperience,Tblfundedproject,Tblsubjects,Tbldesignation,Tbldegree, Tblinstitutes, Tbluniversities
from pathlib import Path 
BASE_DIR = Path(__file__).resolve().parent.parent
flurl = str(BASE_DIR) + "/media/"

def home(request):
    return render(request,'core/home3.html')

# DEGREE LIST MANUAL===>>>
POST_GRADUATION_= ['M.Sc', 'M.E.', 'MBA', 'M.TECH', 'MPhil', 'M.COM', 'M.A', 'MS','M.A','M.COM', 'M.COM.','MASTERS','M TECH','M. TECH','ME','MASTER','M.E','M.E.','ME.','M.S','M.S.','M.TECH','M.TECH.','M TECH','MBA']
DOCTORATE_ = ['PHD','P.HD.','P.H.D.', 'PHD.']
GRADUATION_ = ['OTHER DEGREES','B.A (HONS.)','BE','BACHELORS','B E','B.E(MECH)','B.E(CIVIL)','B.E.', 'B.E','B.E ','GRADUATION','BSC','B.SC', 'B.SC.','B.COM','Bachelor of Architecture','BA','B.A','B.A.','B.COM.','B.TECH.','B.TECH', 'B TECH','AMIE']
DIPLOMA_ = ['DIPLOMA', 'Computer Applications', 'Auto CAD','POLYTECHNIC']
PG_DIPLOMA_=['PG DIPLOMA']
CERTIFICATION_COURSE_ = ['CERTIFICATION', 'CERTIFICATE']

# # DIPLOMA = ['DIPLOMA']
# # GRADUATION = ['BE', 'GRADUATION','B.TECH', 'Bachelor of Architecture', 'Other Degrees']
# XII = ['12TH','XII','XII','SSC']
# X = ['10','X','MATRIC']  
# # POST_GRADUATION = ['M.COM.','M.S.','M.TECH', 'M.A', 'Other Master Degrees','MBA',"PG"]
# # PG_DIPLOMA=['PG DIPLOMA']
# # DOCTORATE = ['PHD','P.HD.','P.H.D.', 'PHD.']
# # CERTIFICATION_COURSE = ['CERTIFICATION', 'CERTIFICATE']

specialization_list = ['', 'Management', 'CAD / Draftsmanship', 'Certificate Course in Safety', 'Environmental Science',
 'Technology Science', 'Strategy and Leadership Management', 'Transportation', 'Survey & Testing',
 'Construction Management', 'Civil', 'Highway', 'Mining', 'Environmental', 'Environmental Health', 'Traffic',
 'Geology', 'Geotech', 'Structural', 'Safety', 'Philosophy', 'Soil Mechanics', 'Project Management',
 'Management Development Programme', 'Water Resource', 'Structures', 'Highways and Transportation', 'Geotechnical',
 'SafetyCertificate Course in Safety']
state_dict = [("AP","Andhra Pradesh"),("AR","Arunachal Pradesh"),("HP","Himachal Pradesh"),("JK","Jammu and Kashmir"),
("JH","Jharkhand"), ("KA","Karnataka"),("MP","Madhya Pradesh"),("MH","Maharashtra"),("RJ","Rajasthan"),
("TN","Tamil Nadu"),("UP","Uttar Pradesh"), ("WB","West Bengal"),("TN","Tamil Nadu")]

@csrf_exempt
def final(request):
	global candid_id
	global file
	if request.method == "POST":
		try:
			f=request.FILES.getlist("file")
			if len(f)==0:
				return HttpResponse("Please Select Some Files")
			for fl in f:
				fs = FileSystemStorage()
				file=str(fl) 
				logdata=[]
				if file.endswith('.pdf'):
					logdata.append('pdf file here')
					try:
						try:
							file=file.replace(' ','_').replace(',','')	
							fullname = fs.save(file,fl)						
							flnameURL = fs.url(fullname)
							flnameURL =  str(BASE_DIR) + flnameURL
							# print(str(BASE_DIR)+'/media/')
							logdata.append('resume processing')
							data=parsing(flnameURL)
							logdata.append('resume processed')
							data2=data['cvtext']
							os.remove(flnameURL)
							time.sleep(1)
							

							name = data['Name']    # BASIC DETAIL VARIABLES ===>>>
							fstname,midname,lstname =split(name) 
							m_name=data['Mother Name']
							f_name= data['Father Name']
							email=data['Email']
							mobile=data['Mobile']
							alt_mobile=data['Alternate Mobile']
							pan=data['PAN Number']
							passport=data['Passport Number']
							if data['DOB']!='':
								dob= datetime.strptime(data['DOB'],"%d/%m/%Y").strftime("%Y-%m-%d")
							if data['DOB']=='':
								dob = "1111-11-11" #"1970-01-01"
							adhaar=data['Adhaar no']
						except:
							pass
						try:
							nomi = IndianGenderPredictor()
							na=name
							gen= nomi.predict(na)
						except:
							pass
						gender_="M"
						try:
							if gen == 'male':
								gender_="M"
						except:
							gender_="f"	
						try:
							logdata.append('email check in tblcv')
							email_check = Tblcv.objects.using('table_db').filter(email=email)
							if email_check:
								candid_id=email_check[0].id
							else :
								logdata.append('not found in tblcv, create new one')
								candid_id = Tblcv.objects.using('table_db').update_or_create(fname = fstname, mname = midname, lname = lstname, email = email, dob = dob, email2 = ' ', phone = mobile, phone2 = alt_mobile, gender = gender_,nationality_id = 101,fathername = f_name, mothername = m_name,languages = "2",aadharno = adhaar,panno = pan, isvalidpassport = 0,passportno = passport,issuecountry =" ", created_by=1,is_online = 0,status = 0)[0].id
						except:
							pass
						try:
							srch_n=Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key="nationality_id", meta_value=str(101))
							if srch_n:
								pass
							if not srch_n:
								Tblsearchmeta.objects.using('table_db').update_or_create(candidate_id=candid_id,meta_key="nationality_id", meta_value=str(101))

							srch_l=Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key="languages", meta_value=str(2))
							if srch_l:
								pass
							if not srch_l:
								Tblsearchmeta.objects.using('table_db').update_or_create(candidate_id=candid_id,meta_key="languages", meta_value=str(2))
								
						except:
							pass
						try:  # COPY FILENAME TO SERVER===>>>
							fullnamee= fs.save((str(candid_id)+"_"+str(file)),fl)						
							flnameURL1 = fs.url(fullnamee)
							flnameURL1 =  str(BASE_DIR) + flnameURL1
							# logdata.append('coping file to server')						
							shutil.move(flnameURL1,'/media/serverceg/apps/applications/public_html/cvm/storage/app/public/')
							# shutil.copy(flnameURL1,str(BASE_DIR)+'/files/')														
							# logdata.append('copied to server')
						except:
							pass
						try:    # remove files
							os.remove(flnameURL1)
						except:
							pass						
						try: # CURRENT ADDRESS ===>>>.
							country_id=101
							adType = 'C'
							curr_state = data['Current State']
							try:
								curr_state = ''.join([curr_state[0].upper(),curr_state[1:].lower()])
							except:
								pass
							curr_city=data['Current District'].replace(' District','')
							curr_add=data['Current Address']
							curr_add=curr_add.replace(curr_state,'')
							curr_add=curr_add.replace(curr_city,'').replace(', ,','')
							curr_pin=data['Current Pin']
							try:
								curr_pin_i = int(curr_pin)
							except:
								curr_pin_i = 0
							if(curr_add != ''):
								try:
									cur_state_ = Tblstates.objects.using('table_db').filter(name=curr_state)
									if cur_state_:
										cur_s_id=cur_state_[0].id
									if not cur_state_:
										cur_s_id=4151
									cur_city_ = Tblcities.objects.using('table_db').filter(name=curr_city)
									if cur_city_:
										cur_c_id=cur_city_[0].id
									if not cur_city_:
										cur_c_id=776
									Tbladdress.objects.using('table_db').update_or_create(candidate_id = int(candid_id),address_type = adType,address = curr_add,city_id=cur_c_id,state_id = cur_s_id,country_id = country_id, zipcode = curr_pin_i)
									logdata.append('current addres entered')
								except:
									pass
						except:
							pass
						try:	 # PERMANENT ADDRESS===>>>>
							country_id=101	
							per_city=data['Permanent District'].replace(' District','')
							per_state=data['Permanent State']
							try:
								per_state = ''.join([per_state[0].upper(),per_state[1:].lower()])
							except:
								pass
							per_add=data['Permanent Address']
							per_add=per_add.replace(per_state,'')
							per_add=per_add.replace(per_city,'').replace(', ,','')
							adType = 'P'
							per_pin=data['Current Pin']
							try:
								per_pin_i = int(per_pin)
							except:
								per_pin_i = 0
							if(per_add != ''):
								try:
									per_state_ = Tblstates.objects.using('table_db').filter(name=per_state)
									if per_state_:
										per_s_id=per_state_[0].id
									if not per_state_:
										per_s_id=4151
									per_city_ = Tblcities.objects.using('table_db').filter(name=per_city)
									if per_city_:
										per_c_id=per_city_[0].id
									if not per_city_:
										per_c_id=776
									Tbladdress.objects.using('table_db').update_or_create(candidate_id = int(candid_id),address_type = adType,address = per_add,city_id=per_c_id,state_id = per_s_id,country_id = country_id, zipcode = per_pin_i)
									logdata.append('permanent address entered')
								except:
									pass
						except:
							pass
						try: # TBLSEARCH HERE===>>>
							check_search = Tblsearch.objects.using('table_db').filter(candidate_id=candid_id)
							if check_search:
								check_search.update(cvdata=data2)
							if not check_search:
								Tblsearch.objects.using('table_db').update_or_create(candidate_id=candid_id, cvdata = data2)
								logdata.append('tblsearch entry completed')
						except:
							pass
						try:  # TBLCVKEYWORDS HERE
							key_data = Tblkeywords.objects.using('table_db').values_list('keyword', flat=True)
							indus_data=Tblindustry.objects.using('table_db').values_list('industryname', flat=True)
							phs_data  = Tblphase.objects.using('table_db').values_list('phasename', flat=True)
							sec_data= Tblsector.objects.using('table_db').values_list('sectorname', flat=True)
							
							key_words=[]
							phase_id_l=[]
							sector_id_l=[]
							indus_id_l=[]

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
						try:  # EDUCATION DETAILS HERE===>>>
							logdata.append('education entry started')
							X = ['10','X','MATRIC','HSC','H.S.C.','H.S.C']
							X = sorted(X,key = lambda x:len(x), reverse=True)					
							XII = ['12TH','XII','XII','SSC','S.S.C','S.S.C.']
							XII = sorted(XII,key = lambda x:len(x), reverse=True)		
							GRADUATION=Tbldegree.objects.using('table_db').filter(edulevel_id=2).values_list('degreename', flat=True)
							GRADUATION=sorted(GRADUATION,key = lambda x:len(x), reverse=True)	
							POST_GRADUATION=Tbldegree.objects.using('table_db').filter(edulevel_id=11).values_list('degreename', flat=True)							
							POST_GRADUATION=sorted(POST_GRADUATION,key = lambda x:len(x), reverse=True)
							PG_DIPLOMA=Tbldegree.objects.using('table_db').filter(edulevel_id=12).values_list('degreename', flat=True)							
							PG_DIPLOMA=sorted(PG_DIPLOMA,key = lambda x:len(x), reverse=True)
							DIPLOMA=Tbldegree.objects.using('table_db').filter(edulevel_id=1).values_list('degreename', flat=True)							
							DIPLOMA=sorted(DIPLOMA,key = lambda x:len(x), reverse=True)
							DOCTORATE=Tbldegree.objects.using('table_db').filter(edulevel_id=10).values_list('degreename', flat=True)
							DOCTORATE=sorted(DOCTORATE,key = lambda x:len(x), reverse=True)
							CERTIFICATION_COURSE=Tbldegree.objects.using('table_db').filter(edulevel_id=20).values_list('degreename', flat=True)
							CERTIFICATION_COURSE=sorted(CERTIFICATION_COURSE,key = lambda x:len(x), reverse=True)

							level=data['level']
							qual_level=data['qual_level']				
							topic=data['topic']
							college=data['college']
							university=data['university']
							yop=data['yop']
							percentage=data['percentage']
							subject_list = Tblsubjects.objects.using('table_db').values_list('subject', flat=True)
							inst_list=list(Tblinstitutes.objects.using('table_db').values_list('institutename', flat=True))
							
							for i in range(len(level)):
								# try:                
								crs_= qual_level[i]						
								# SUBJECTS TEXT
								subject_text=""
								crs=crs_
								for sl in subject_list:  
									if sl!="":                       
										if sl.upper() in crs_.upper():                                
											subject_text+=sl                                
											break
								# SUBJECT ID
								subject_id = Tblsubjects.objects.using('table_db').filter(subject=subject_text.strip())[0].id

								# FINDING DEGREE_id					
								verifi=0
								spec = ""
								if verifi==0:    # post graduation
									if any(i.upper() in crs.upper() for i in POST_GRADUATION_)==True: 
										for st in POST_GRADUATION:	
											d_degree=""	
											st_1=st						
											crs=crs_									
											st_1=re.sub(r'[.]','',st.strip().lower())	
											st_1=st_1.replace('m','m.')																	
											crs=re.sub(r'[.]','',crs.strip().lower())

											crs=re.sub(r'\s{2,}',' ',crs)	
											crs=crs.replace('m','m.')								
											if st_1.lower() in crs.lower():
												d_degree+=st
												degree_id = Tbldegree.objects.using('table_db').filter(degreename=d_degree)
												if degree_id:
													degree_idd=degree_id[0].id
												if not degree_id:
													degree_idd=31
												lvlid=11	
												verifi+=1
												#INSTITUTES 									
												college_check=[',','.','-',' ','*']
												if college[i].strip() in college_check:
													inst= Tblinstitutes.objects.using('table_db').filter(institutename= 'NA')
													if inst:
														inst_id = inst[0].id
													if not inst:
														inst_id = Tblinstitutes.objects.using('table_db').create(institutename= 'NA',is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
												else:
													inst= Tblinstitutes.objects.using('table_db').filter(institutename= college[i])
													if inst:
														inst_id = inst[0].id
													if not inst:
														inst_id = Tblinstitutes.objects.using('table_db').create(institutename= college[i],is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
												
												# UNIVERSITIES
												univ = Tbluniversities.objects.using('table_db').filter(univname= university[i])
												if univ:
													univr_id = univ[0].id
												if not univ:
													univr_id = Tbluniversities.objects.using('table_db').create(univname= university[i],is_active = 1, created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
												
												break													
										# SPECIALIZATION  
										
										for sp in specialization_list:                  
											if sp!="" and sp!=None:
												if sp.upper() in topic[i].upper():
													spec+=sp
													break
												else:
													if sp.upper() in crs.upper():
														spec+=sp
														break   
								if any(i in crs.upper() for i in GRADUATION_)==True:   
									if verifi==0:                             
										for st in GRADUATION:	
											d_degree=""	
											crs=crs_									
											st_1=re.sub(r'[.]','',st.strip())																		
											crs=re.sub(r'[.]','',crs.strip().lower())
											crs=re.sub(r'\s{2,}',' ',crs)								
											if st_1.lower() in crs.lower():
												d_degree+=st
												degree_id = Tbldegree.objects.using('table_db').filter(degreename=d_degree)
												if degree_id:
													degree_idd=degree_id[0].id
												if not degree_id:
													degree_idd=31
												lvlid=2	
												verifi+=1
												#INSTITUTES 									
												college_check=[',','.','-',' ','*']
												if college[i].strip() in college_check:
													inst= Tblinstitutes.objects.using('table_db').filter(institutename= 'NA')
													if inst:
														inst_id = inst[0].id
													if not inst:
														inst_id = Tblinstitutes.objects.using('table_db').create(institutename= 'NA',is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
												else:
													inst= Tblinstitutes.objects.using('table_db').filter(institutename= college[i])
													if inst:
														inst_id = inst[0].id
													if not inst:
														inst_id = Tblinstitutes.objects.using('table_db').create(institutename= college[i],is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
												
							
												# UNIVERSITIES
												univ = Tbluniversities.objects.using('table_db').filter(univname= university[i])
												if univ:
													univr_id = univ[0].id
												if not univ:
													univr_id = Tbluniversities.objects.using('table_db').create(univname= university[i],is_active = 1, created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
											
												break	
								if verifi==0:	# 12th
									crs=crs_											
									if any(i.lower() in crs.lower() for i in XII)==True:							
										degree_idd =42
										lvlid=8
										verifi+=1
										#INSTITUTES 							
										college_check=[',','.','-',' ','*','0']
										if college[i].strip() in college_check:
											inst= Tblinstitutes.objects.using('table_db').filter(institutename= 'NA')
											if inst:
												inst_id = inst[0].id
											if not inst:
												inst_id = Tblinstitutes.objects.using('table_db').create(institutename= 'NA',is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
										else:
											inst= Tblinstitutes.objects.using('table_db').filter(institutename= college[i])
											if inst:
												inst_id = inst[0].id
											if not inst:
												inst_id = Tblinstitutes.objects.using('table_db').create(institutename= college[i],is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
											
										# UNIVERSITIES
										univ = Tbluniversities.objects.using('table_db').filter(univname= university[i])
										if univ:
											univr_id = univ[0].id
										if not univ:
											univr_id = Tbluniversities.objects.using('table_db').create(univname= university[i],is_active = 1, created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id

								if verifi==0:    # 10th
									if any(i.lower() in crs.lower() for i in X)==True:   
										crs=crs_	
										degree_idd=54
										lvlid=10
										verifi+=1							
										#INSTITUTES						
										college_check=[',','.','-',' ','*']
										if college[i].strip() in college_check:
											inst= Tblinstitutes.objects.using('table_db').filter(institutename= 'NA')
											if inst:
												inst_id = inst[0].id
											if not inst:
												inst_id = Tblinstitutes.objects.using('table_db').create(institutename= 'NA',is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
										else:

											inst= Tblinstitutes.objects.using('table_db').filter(institutename= college[i])
											if inst:
												inst_id = inst[0].id
											if not inst:
												inst_id = Tblinstitutes.objects.using('table_db').create(institutename= college[i],is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
											
										# UNIVERSITIES
										univ = Tbluniversities.objects.using('table_db').filter(univname= university[i])
										if univ:
											univr_id = univ[0].id
										if not univ:
											univr_id = Tbluniversities.objects.using('table_db').create(univname= university[i],is_active = 1, created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id

								if verifi==0:    # doctorate
									if any(i.lower() in crs.lower() for i in DOCTORATE_)==True:
										for st in DOCTORATE:	
											d_degree=""		
											crs=crs_							
											st_1=re.sub(r'[.]','',st.strip())																		
											crs=re.sub(r'[.]','',crs.strip().lower())
											crs=re.sub(r'\s{2,}',' ',crs)
											crs=crs.replace('m','m.')								
											if st_1.lower() in crs.lower():
												d_degree+=st
												degree_id = Tbldegree.objects.using('table_db').filter(degreename=d_degree)
												if degree_id:
													degree_idd=degree_id[0].id
												if not degree_id:
													degree_idd=31
												lvlid=16
												verifi+=1	
												#INSTITUTES 									
												college_check=[',','.','-',' ','*']
												if college[i].strip() in college_check:
													inst= Tblinstitutes.objects.using('table_db').filter(institutename= 'NA')
													if inst:
														inst_id = inst[0].id
													if not inst:
														inst_id = Tblinstitutes.objects.using('table_db').create(institutename= 'NA',is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
												else:
													inst= Tblinstitutes.objects.using('table_db').filter(institutename= college[i])
													if inst:
														inst_id = inst[0].id
													if not inst:
														inst_id = Tblinstitutes.objects.using('table_db').create(institutename= college[i],is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
												
												# UNIVERSITIES
												univ = Tbluniversities.objects.using('table_db').filter(univname= university[i])
												if univ:
													univr_id = univ[0].id
												if not univ:
													univr_id = Tbluniversities.objects.using('table_db').create(univname= university[i],is_active = 1, created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
													
												break	
								if verifi==0:    # pg diploma
									for st in PG_DIPLOMA:
										d_degree=""		
										crs=crs_									
										st_1=re.sub(r'[.]','',st.strip())																		
										crs=re.sub(r'[.]','',crs.strip().lower())
										crs=re.sub(r'\s{2,}',' ',crs)							
										if st_1.lower() in crs.lower():
											degree_idd=9
											lvlid    =12								
											verifi+=1	
											#INSTITUTES 								
											college_check=[',','.','-',' ','*']
											if college[i].strip() in college_check:
												inst= Tblinstitutes.objects.using('table_db').filter(institutename= 'NA')
												if inst:
													inst_id = inst[0].id
												if not inst:
													inst_id = Tblinstitutes.objects.using('table_db').create(institutename= 'NA',is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
											else:

												inst= Tblinstitutes.objects.using('table_db').filter(institutename= college[i])
												if inst:
													inst_id = inst[0].id
												if not inst:
													inst_id = Tblinstitutes.objects.using('table_db').create(institutename= college[i],is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
												
											# UNIVERSITIES
											univ = Tbluniversities.objects.using('table_db').filter(univname= university[i])
											if univ:
												univr_id = univ[0].id
											if not univ:
												univr_id = Tbluniversities.objects.using('table_db').create(univname= university[i],is_active = 1, created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
													
											break	
								if verifi==0:    # diploma
									for st in DIPLOMA:
										d_degree=""	
										crs=crs_										
										st_1=re.sub(r'[.]','',st.strip())																		
										crs=re.sub(r'[.]','',crs.strip().lower())
										crs=re.sub(r'\s{2,}',' ',crs)								
										if st_1.lower() in crs.lower():
											d_degree+=st
											degree_id = Tbldegree.objects.using('table_db').filter(degreename=d_degree)
											if degree_id:
												degree_idd=degree_id[0].id
											if not degree_id:
												degree_idd=31
											lvlid=1	
											verifi+=1
											#INSTITUTES 								
											college_check=[',','.','-',' ','*']
											if college[i].strip() in college_check:
												inst= Tblinstitutes.objects.using('table_db').filter(institutename= 'NA')
												if inst:
													inst_id = inst[0].id
												if not inst:
													inst_id = Tblinstitutes.objects.using('table_db').create(institutename= 'NA',is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
											else:
												inst= Tblinstitutes.objects.using('table_db').filter(institutename= college[i])
												if inst:
													inst_id = inst[0].id
												if not inst:
													inst_id = Tblinstitutes.objects.using('table_db').create(institutename= college[i],is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
												
											# UNIVERSITIES
											univ = Tbluniversities.objects.using('table_db').filter(univname= university[i])
											if univ:
												univr_id = univ[0].id
												# print(university[i])
											if not univ:
												# univr_id = 1150
												univr_id = Tbluniversities.objects.using('table_db').create(univname= university[i],is_active = 1, created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
													
											break
								                          
									
								if verifi==0:    # certification
									for st in CERTIFICATION_COURSE:	
										d_degree=""	
										crs=crs_									
										st=re.sub(r'[.]','',st.strip())																		
										crs=re.sub(r'[.]','',crs.strip().lower())
										crs=re.sub(r'\s{2,}',' ',crs)	
										crs=crs.replace('m','m.')										
										if st.lower() in crs.lower():
											d_degree+=st	
											degree_id = Tbldegree.objects.using('table_db').filter(degreename=d_degree)
											if degree_id:
												degree_idd=degree_id[0].id
											if not degree_id:
												degree_idd=31
											lvlid=20
											verifi+=1
											#INSTITUTES 
											college_check=[',','.','-',' ','*']
											if college[i].strip() in college_check:
												inst= Tblinstitutes.objects.using('table_db').filter(institutename= 'NA')
												if inst:
													inst_id = inst[0].id
												if not inst:
													inst_id = Tblinstitutes.objects.using('table_db').create(institutename= 'NA',is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
											else:
												inst= Tblinstitutes.objects.using('table_db').filter(institutename= college[i])
												if inst:
													inst_id = inst[0].id
												if not inst:
													inst_id = Tblinstitutes.objects.using('table_db').create(institutename= college[i],is_active = 1,created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
												
											# UNIVERSITIES
											univ = Tbluniversities.objects.using('table_db').filter(univname= university[i])
											if univ:
												univr_id = univ[0].id
											if not univ:
												univr_id = Tbluniversities.objects.using('table_db').create(univname= university[i],is_active = 1, created_by=1,modified_by=1,modified_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).id
													
											break
								
								# CHECK EDUCATION
								try:
									check_edu = Tbleducation.objects.using('table_db').filter(candidate_id = int(candid_id),qualification_id =lvlid,course_id = degree_idd)
									if check_edu:
										check_edu.update(subject_id=subject_id,subject=subject_text, specialization = spec)
									if not check_edu:
										Tbleducation.objects.using('table_db').update_or_create(candidate_id = int(candid_id),qualification_id =lvlid,course_id = degree_idd,subject_id=subject_id ,subject=subject_text, specialization = spec, institute=inst_id, university=univr_id, yearpassed = int(yop[i]),percentage =percentage[i], edumode_id = 1)
								except:
									pass

								# SEARCHMETAS
								try:
									# QUALIFICATION_ID
									srch_q=Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key="qualification_id", meta_value=str(lvlid))
									if srch_q:
										pass
									if not srch_q:
										Tblsearchmeta.objects.using('table_db').update_or_create(candidate_id=candid_id,meta_key="qualification_id", meta_value=str(lvlid))
									# COURSE_ID
									srch_c=Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key="course_id", meta_value=str(degree_idd))		
									if srch_c:
										pass
									if not srch_c:
										Tblsearchmeta.objects.using('table_db').update_or_create(candidate_id=candid_id,meta_key="course_id", meta_value=str(degree_idd))		
									# INSTITUTE_ID
									srch_i=Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key="institute", meta_value=str(inst_id))
									if srch_i:
										pass
									if not srch_i:
										Tblsearchmeta.objects.using('table_db').update_or_create(candidate_id=candid_id,meta_key="institute", meta_value=str(inst_id))
									# UNIVERSITY_ID
									srch_u=Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key="university", meta_value=str(univr_id))
									if srch_u:
										pass
									if not srch_u:
										Tblsearchmeta.objects.using('table_db').update_or_create(candidate_id=candid_id,meta_key="university", meta_value=str(univr_id))
									# SUBJECT_ID
									srch_u=Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key="subject_id", meta_value=str(subject_id))
									if srch_u:
										pass
									if not srch_u:
										Tblsearchmeta.objects.using('table_db').update_or_create(candidate_id=candid_id,meta_key="subject_id", meta_value=str(subject_id))
									
								
								except:
									pass
							logdata.append('education entry completed')
						except:
							pass
						try:  # TBLCVFILES HERE ===>>>
							restxt = 1
							createdBy = 1
							Tblcvfiles.objects.using('table_db').update_or_create(filename = str(str(candid_id)+"_"+str(file)), candidate_id = int(candid_id), resume_text = restxt, created_by = createdBy)			
							logdata.append('tblcvfiles entry started')
						except:
							pass
						try: # EXPERIENCE DETAILS ===>>>		
							com_name=data['company_name']
							from_=data['from_year']
							to_=data['to_year']					
							if com_name!='':
								for i in range(len(com_name)):
									try:
										if from_[i].count('/')==2 and 8<=len(from_[i])<=10:
											compvar = com_name[i]
											if from_[i] =="":
												strtdate= "1111-11-11"
											if from_[i] !="":
												strtdate = datetime.strptime(from_[i],"%d/%m/%Y").strftime("%Y-%m-%d")
											if to_[i] =="":
												enddate = "1111-11-11"
											if to_[i]!="":
												enddate =  datetime.strptime(to_[i],"%d/%m/%Y").strftime("%Y-%m-%d")
											Tblexperience.objects.using('table_db').update_or_create(candidate_id=candid_id,companyname=compvar,startdate = strtdate,enddate = enddate, country_id = 101,employmentnature="Undefined")
									except:
										pass
								logdata.append('tblexperience entry started')

						except:
							pass
						try:  #  PROJECTS HERE===>>>
							logdata.append('project work starting')				
							sno_work=data['sno_work']
							work_name_=data['work_name']							
							client=data['client']
							designation=data['designation']
							project_cost=data['project_cost']
							start_date=data['start_date']
							completion_date=data['completion_date']
							country=data['country']
							# calculating companies name from date range
							c_names=[]					
							for d in start_date:
								if d.count('/')==2 and 8<=len(d)<=10:
									c_text=""
									try:
										cd=datetime.strptime(d,"%d/%m/%Y").strftime("%Y-%m-%d")
										for i in range(len(from_)):
											if from_[i].count('/')==2 and 8<=len(from_[i])<=10:
												if to_[i].count('/')==2 and 8<=len(to_[i])<=10:
													d1=datetime.strptime(from_[i],"%d/%m/%Y").strftime("%Y-%m-%d")
													d2=datetime.strptime(to_[i],"%d/%m/%Y").strftime("%Y-%m-%d")
													if (d1<=cd<=d2) == True:
														c_text+=com_name[i]
														break				
									except:
										pass
									c_names.append(c_text)
								else:
									c_names.append('')
				
							work_name = []   # STATE WORKS===>>>
							for wn in work_name_:
								# print("orginal text==>>",wn)
								string = wn.strip()
								string=re.sub(r'[)(]',' ',string)
								string=re.sub(r'[.,/\-_]','',string)
								string=re.sub(r'\s{2,}',' ',string)
								work_name.append(string)
								# print("modified text==>>",string)
								
							s_list = ["Andhra Pradesh","A.P.","A.P","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","G.J.","G.J","Haryana","H.R.","H.R",
							"Himachal Pradesh","H.P.","H.P","Jharkhand","J.H.","J.H","Karnataka","K.A.","K.A","Kerala","Madhya Pradesh","M.P.","M.P","Maharashtra","M.H.",
							"M.H","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","R.J.","R.J","Sikkim","Tamil Nadu","T.N.","T.N","Telangana",
							"Tripura","Uttar Pradesh","U.P.","U.P","Uttarakhand","U.T.","U.T","Dehradun","West Bengal","W.B.","W.B","Andaman and Nicobar Islands",
							"Chandigarh","C.H.","C.H","Dadra and Nagar Haveli and Daman and Diu","Delhi","D.L.","D.L","Jammu and Kashmir","Ladakh","Lakshadweep"]
							s_list=[x.lower() for x in s_list]
							s_names=[]			
							for i in work_name:					
								grams=[]
								for df in range(1,3):
									s = ngrams(i.split(), df) 
									for j in s:
										grams.append(' '.join(j))
								state_en = [x for x in grams if x.lower() in s_list]
								if len(state_en)==0:
									s_names.append('')
								if len(state_en) != 0:
									s_names.append(state_en[0])
				
							cities_data=list(Tblcities.objects.using('table_db').values_list('name', flat=True))
							if sno_work!='':
								for i in range(len(sno_work)):
									logdata.append('project entry started-'+str(i))						
									try:												
										if int(sno_work[i]) >0:	
								# CITIES CHECK ===>>>
											city_idd=530			
											for cit in cities_data:
												if cit != '':
													if cit.lower() in work_name[i].lower():			#.split()								
														city_idd = Tblcities.objects.using('table_db').filter(name=cit)[0].id
														break															
											Tblsearchmeta.objects.using('table_db').update_or_create(candidate_id=candid_id,meta_key="city", meta_value=str(city_idd))
											wrk_name = work_name_[i]
											try:
												start_d=datetime.strptime(start_date[i],"%d/%m/%Y").strftime("%Y-%m-%d")
											except:
												start_d='1111-11-11'
											try:
												end_d = (datetime.strptime(completion_date[i],"%d/%m/%Y").strftime("%Y-%m-%d"))
											except:
												end_d= "1111-11-11"										
											protempclient=client[i]
								# CHECK COUNTRY
											check_cntry = Tblcountries.objects.using('table_db').filter(name=country[i])
											if check_cntry:
												cntry_id=check_cntry[0].id
											if not check_cntry:
												cntry_id=250
											if cntry_id == 101:
												exp_  = 'N'
											else:
												exp_ = 'I'
								# CHECK STATE ===>>>
											state_check = Tblstates.objects.using('table_db').filter(name=s_names[i])
											if state_check:
												state_idd = state_check[0].id
											if not state_check:
												state_idd=4151
								# PROJECT COST==>>>
											if project_cost[i].count('.')==1:
												pro_cost=project_cost[i].replace(',','')
												pro_cost=re.findall('\d*\.?\d+',pro_cost)
												if pro_cost:
													p_cost=float(pro_cost[0])
											else:
												p_cost=0.0
								#get the designation id 
											desig = Tbldesignation.objects.using('table_db').filter(designation=designation[i])
											if desig:
												desig_id=desig[0].id							
											else:
												desig_id=340
								# CEHCK PROJECT
											if 'detailed project report' in wrk_name.lower() or 'dpr' in wrk_name.lower():
												check_project_dpr= Tblfundedproject.objects.using('table_db').filter(candidate_id=candid_id, projectname=wrk_name,startdate=start_d  ,enddate= end_d)  #projectname=Work_Name[pr]
												if check_project_dpr:
													pass
												if not check_project_dpr:
													Tblfundedproject.objects.using('table_db').update_or_create(candidate_id=candid_id,startdate = start_d,enddate = end_d,projdesig=str(desig_id),projectname = wrk_name,industry_id=1,sector_id=1,phase_id=1,employername=c_names[i],natureemployer='N',projectexp=exp_,country_id=cntry_id, state_id=state_idd, city_id=city_idd,projectcost = p_cost,clientname=protempclient,fundingagency_id=0)
											else:
												check_project= Tblfundedproject.objects.using('table_db').filter(candidate_id=candid_id, startdate=start_d  ,enddate= end_d)  #projectname=Work_Name[pr]
												if check_project:
													check_dpr = [(x.id,x.projectname) for x in check_project]
													check_dpr = [x[0] for x in check_dpr if any(y in x[1].lower() for y in ['dpr','detailed project report'] )==False]
													for cd in check_dpr:
														Tblfundedproject.objects.using('table_db').filter(id=cd).update(projectname=wrk_name, projectcost=p_cost)
												else: 	
													Tblfundedproject.objects.using('table_db').update_or_create(candidate_id=candid_id,startdate = start_d,enddate = end_d,projdesig=str(desig_id),projectname = wrk_name,industry_id=1,sector_id=1,phase_id=1,employername=c_names[i],natureemployer='N',projectexp=exp_,country_id=cntry_id, state_id=state_idd, city_id=city_idd,projectcost = p_cost,clientname=protempclient,fundingagency_id=0)
								# CHECK SEARCHMETA
											sm_dgn = Tblsearchmeta.objects.using('table_db').filter(candidate_id=candid_id,meta_key="designation_id", meta_value=str(desig_id))
											if sm_dgn:
												pass
											if not sm_dgn:
												Tblsearchmeta.objects.using('table_db').update_or_create(candidate_id=candid_id,meta_key="designation_id", meta_value=str(desig_id))
									except:
										pass
								logdata.append('project entry completed')
						except:
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
									pass
							logdata.append('project details entry completed')
						except:
							pass

						# print(logdata)
						# with open(str(BASE_DIR)+'/media/logdata.txt', 'w') as f:
						# 		f.write(str(logdata))
					except:
						pass
															
				else:
					pass
		except:
			pass						
	return HttpResponse("All Files Successfully Processed")