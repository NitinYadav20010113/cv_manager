from datetime import datetime
from pytz import timezone 
from .tblmodels import Tblcv, Tblsearch, Tblindustry, Tblphase, Tblsector ,Tblsearchmeta, Tblcvkeywords, Tblkeywords, Tbllanguage_gen, Tbledumode, Tbledulevel,Tblcvfiles,Tbladdress,Tblcountries, Tblcities, Tblstates,Tbleducation,Tblexperience,Tblfundedproject,Tblsubjects,Tbldesignation,Tbldegree, Tblinstitutes, Tbluniversities,Tblcompany_master,Tblfundagencies,Tblpavement,Tblterrain,Tblcontractmode,Tblprodetails,cvm_run_history

old_path='/mnt/old_files'
new_file_path='/mnt/cv_files'
doc_path='/mnt/doc_files'
email_path='/mnt/email_not_found'

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

