# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete

from django.db import models
class Tbledulevel(models.Model):
	edulevel=models.CharField(max_length=100)
	is_active=models.IntegerField()
	created_by=models.IntegerField()
	created_at=models.DateTimeField()
	modified_by=models.IntegerField()
	modified_at=models.DateTimeField()	
	class Meta:
		managed=False
		db_table = 'tbledulevel'
  
  
  
class Tbledumode(models.Model):
	edumode=models.CharField(max_length=30)
	is_active=models.IntegerField()
	created_by=models.IntegerField()
	# created_at=models.DateTimeField()
	modified_by=models.IntegerField()
	modified_at=models.DateTimeField()
	class Meta:
		db_table = 'tbledumode'
  
  
  
class Tblcountries(models.Model):
	sortname = models.CharField(max_length=3)
	name = models.CharField(max_length=150)
	phonecode = models.IntegerField(null=True,blank=True)
	class Meta:
		db_table = 'tblcountries'	
  
  
class Tbladdress(models.Model):
    candidate_id = models.IntegerField()
    address_type = models.CharField(max_length=1)
    address = models.CharField(max_length=255)
    city_id = models.IntegerField()
    state_id = models.IntegerField()
    country_id = models.IntegerField()
    zipcode = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbladdress'
class Tblinstitutes(models.Model):
	
	institutename=models.CharField(max_length=400)
	is_active=models.IntegerField()
	created_by=models.IntegerField()
	created_at=models.DateTimeField()
	modified_by=models.IntegerField()
	modified_at=models.DateTimeField()	
	class Meta:
		managed=False
		db_table = 'tblinstitutes'
class Tblcities(models.Model):
    name = models.CharField(max_length=30)
    state_id = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'tblcities'
class Tblstates(models.Model):
    name = models.CharField(max_length=100)
    country_id = models.IntegerField()
    class Meta:
        db_table = 'tblstates'
class Tblcv(models.Model):
	id = models.IntegerField(primary_key=True)
	fname = models.CharField(max_length=100)
	mname = models.CharField(max_length=100, blank=True, null=True)
	lname = models.CharField(max_length=100, blank=True, null=True)
	dob = models.DateField(blank=True, null=True)
	email = models.CharField(max_length=100)
	email2 = models.CharField(max_length=100, blank=True, null=True)
	phone = models.CharField(max_length=22)
	phone2 = models.CharField(max_length=22, blank=True, null=True)
	gender = models.CharField(max_length=20)
	nationality_id = models.IntegerField()
	fathername = models.CharField(max_length=100, blank=True, null=True)
	mothername = models.CharField(max_length=100, blank=True, null=True)
	languages = models.CharField(max_length=128, blank=True, null=True)
	aadharno = models.CharField(max_length=16, blank=True, null=True)
	panno = models.CharField(max_length=10, blank=True, null=True)
	isvalidpassport = models.IntegerField()
	passportno = models.CharField(max_length=30, blank=True, null=True)
	issuecountry = models.CharField(max_length=30, blank=True, null=True)
	expirydate = models.DateField(blank=True, null=True)
	profileimage = models.CharField(max_length=100, blank=True, null=True)
	is_online = models.IntegerField()
	onlinesource = models.CharField(max_length=16, blank=True, null=True)
	status = models.IntegerField()
	verified_by = models.IntegerField(blank=True, null=True)
	verified_at = models.DateTimeField(blank=True, null=True)
	created_by = models.IntegerField(blank=True, null=True)
	# created_at = models.DateTimeField()
	modified_by = models.IntegerField(blank=True, null=True)
	modified_at = models.DateTimeField(blank=True, null=True)
	contacted_at = models.DateTimeField(blank=True, null=True)
	contacted_by = models.IntegerField(blank=True, null=True)
	lastviewed_by = models.IntegerField(blank=True, null=True)
	lastviewed_at = models.DateTimeField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'tblcv'
class Tblcvfiles(models.Model):
    filename = models.CharField(max_length=64)
    candidate_id = models.IntegerField()
    resume_text = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblcvfiles'
class Tbleducation(models.Model):
    candidate_id = models.IntegerField()
    qualification_id = models.IntegerField()
    course_id = models.IntegerField()
    subject_id = models.IntegerField(blank=True, null=True)
    subject = models.CharField(max_length=64)
    specialization = models.CharField(max_length=50, blank=True, null=True)
    institute = models.CharField(max_length=100, blank=True, null=True)
    university = models.CharField(max_length=100, blank=True, null=True)
    yearpassed = models.CharField(max_length=20, blank=True, null=True)
    percentage = models.CharField(max_length=20, blank=True, null=True)
    edumode_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbleducation'
class Tbluniversities(models.Model):
	univname = models.CharField(max_length=100)
	is_active = models.IntegerField()
	created_by = models.IntegerField(blank=True, null=True)
	# created_at = models.DateTimeField(blank=True, null=True)
	modified_by = models.IntegerField(blank=True, null=True)
	modified_at = models.DateTimeField(blank=True, null=True)
	class Meta:
		managed = False
		db_table = 'tbluniversities'
class Tbldegree(models.Model):
    degreename = models.CharField(max_length=50)
    edulevel_id = models.IntegerField()
    is_active = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tbldegree'
class Tbldesignation(models.Model):
    designation = models.CharField(max_length=100)
    created_by = models.IntegerField()
    # created_at = models.DateTimeField()
    modified_by = models.IntegerField()
    modified_at = models.DateTimeField()

    class Meta:
        db_table = 'tbldesignation'
class Tblexperience(models.Model):
    candidate_id = models.IntegerField()
    companyname = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField(blank=True, null=True)
    designation_id = models.IntegerField(blank=True, null=True)
    country_id = models.IntegerField()
    responsibilities = models.TextField(blank=True, null=True)
    tottalexp = models.IntegerField(blank=True, null=True)
    employmentnature = models.CharField(max_length=36)

    class Meta:
        db_table = 'tblexperience'
        
        
class Tblfundedproject(models.Model):
    candidate_id = models.IntegerField()
    startdate = models.DateField()
    enddate = models.DateField()
    projectname = models.TextField()
    projdesig = models.CharField(max_length=50, blank=True, null=True)
    compdesig = models.CharField(max_length=50, blank=True, null=True)
    industry_id = models.IntegerField()
    sector_id = models.IntegerField()
    phase_id = models.IntegerField()
    employername = models.CharField(max_length=100)
    natureemployer = models.CharField(max_length=1)
    projectexp = models.CharField(max_length=30)
    country_id = models.IntegerField()
    state_id = models.IntegerField()
    city_id = models.IntegerField()
    projectlength = models.IntegerField(blank=True, null=True)
    lane = models.IntegerField(blank=True, null=True)
    projectcost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    clientname = models.CharField(max_length=100, blank=True, null=True)
    fundingagency_id = models.IntegerField()
    contractmode_id = models.IntegerField(blank=True, null=True)
    pavement_id = models.IntegerField(blank=True, null=True)
    terrain_id = models.IntegerField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tblfundedproject'
class Tblsubjects(models.Model):
    # id = models.IntegerField(primary_key=True)
    subject = models.CharField(max_length=50)
    is_active = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tblsubjects'
class Tbllanguage_gen(models.Model):
	language = models.CharField(max_length=100)
	created_by = models.IntegerField(blank=True, null=True)
	# created_at = models.DateTimeField(blank=True, null=True)
	modified_by = models.IntegerField(blank=True, null=True)
	modified_at = models.DateTimeField(blank=True, null=True)
	class Meta:
		managed = False
		db_table = 'tbllanguages'
class Tblsearch(models.Model):
    candidate_id = models.IntegerField()
    cvdata = models.TextField()   

    class Meta:
        db_table = 'tblsearch'

class Tblsearchmeta(models.Model):
    candidate_id = models.IntegerField()
    meta_key = models.CharField(max_length=20)
    meta_value = models.CharField(max_length=20)

    class Meta:        
        db_table = 'tblsearchmeta'

class Tblkeywords(models.Model):
    keyword = models.CharField(max_length=100)
    sector_id = models.IntegerField()
    phase_id = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tblkeywords'
        
        
        
class Tblcvkeywords(models.Model):
    candidate_id = models.IntegerField()
    industries = models.CharField(max_length=128)
    sectors = models.CharField(max_length=256)
    phases = models.CharField(max_length=256)
    keywords = models.TextField()

    class Meta:
        db_table = 'tblcvkeywords'
class Tblindustry(models.Model):
    industryname=models.CharField(max_length=100)
    created_by=models.IntegerField(blank=True, null=True)
    # created_at=models.DateTimeField(blank=True, null=True)
    modified_by=models.IntegerField(blank=True, null=True)
    modified_at=models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table= 'tblindustry'

class Tblsector(models.Model):
    sectorname=models.CharField(max_length=100)
    industry_id=models.IntegerField()
    created_by=models.IntegerField(blank=True, null=True)
    # created_at=models.DateTimeField(blank=True, null=True)
    modified_by=models.IntegerField(blank=True, null=True)
    modified_at=models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table= 'tblsector'

class Tblphase(models.Model):
    phasename=models.CharField(max_length=100)
    sector_id=models.IntegerField()
    created_by=models.IntegerField(blank=True, null=True)
    # created_at=models.DateTimeField(blank=True, null=True)
    modified_by=models.IntegerField(blank=True, null=True)
    modified_at=models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table= 'tblphase'

class Tblcompany_master(models.Model):
    fld_id=models.IntegerField(primary_key=True)
    company_name=models.CharField(max_length=255)
    status=models.BooleanField(default=1)
    bd_com_master_id=models.IntegerField(null=True,blank=True)
    class Meta:
        db_table='company_master'
        
        
        
class Tblfundagencies(models.Model):
    agencyname=models.CharField(max_length=100)
    created_by=models.IntegerField()
    created_at=	models.DateTimeField(blank=True, null=True)
    modified_by=models.IntegerField()
    modified_at=models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'tblfundagencies'
        
class Tblcontractmode(models.Model):
    contractmode = models.CharField(max_length=20)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.IntegerField()
    modified_at =models.DateTimeField(blank=True, null=True) 
    class Meta:
        db_table = 'tblcontractmode'
class Tblpavement(models.Model):
    pavementname =models.CharField(max_length=50)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.IntegerField()
    modified_at =models.DateTimeField(blank=True, null=True) 
    class Meta:        
        db_table = 'tblpavement'
        
class Tblterrain(models.Model):
    terrainname =models.CharField(max_length=50)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.IntegerField()
    modified_at =models.DateTimeField(blank=True, null=True) 
    class Meta:        
        db_table = 'tblterrain'
        
        
        
       
class Tblprodetails(models.Model):
    candidate_id = models.DecimalField(decimal_places=2, max_digits=10)
    fun_tbl_id = models.IntegerField()
    sector = models.CharField(max_length=255)
    phase = models.CharField(max_length=255)
    length =models.DecimalField(decimal_places=2, max_digits=10)
    funded_by = models.CharField(max_length=255)
    contractmode = models.CharField(max_length=125)
    class Meta:
        db_table = 'tbl_project_detail'


class names_master(models.Model):
     name= models.CharField(max_length=255)
     gender= models.CharField(max_length=255)
     id=models.IntegerField(primary_key=True)

     class Meta:
          db_table='indian_male_names'

class pincode_master(models.Model):
     pincode= models.IntegerField()
     district= models.CharField(max_length=255)
     state = models.CharField(max_length=255)
     id=models.IntegerField(primary_key=True)
     class Meta:
         db_table='pincode_dataset'
         
         
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.process.user.id, filename)
         
         
class file_model(models.Model):
    name=models.CharField(max_length=255,null=True,blank=True)
    file = models.FileField(upload_to=user_directory_path)
    process = models.ForeignKey('upload_progress', on_delete=models.CASCADE, related_name='process',default=None,null=True,blank=True)

    def delete(self, *args, **kwargs):
    # Delete the file from storage
        self.file.delete(save=False)
        # Call the superclass's delete method to delete the instance
        super().delete(*args, **kwargs)
    
    

    
class process_information(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    percent=models.CharField(max_length=255,null=True,blank=True)
    file_completed=models.CharField(max_length=255,null=True,blank=True)
    total_files=models.CharField(max_length=255,null=True,blank=True)
    completed=models.BooleanField(default=True)    
    
    def save(self, *args, **kwargs):
        if self.file_completed==self.total_files:
            self.completed=True
        else:
            self.completed=False
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return str(self.user.username)
    
    

class upload_progress(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    percent=models.CharField(max_length=255,null=True,blank=True)
    file_completed=models.CharField(max_length=255,null=True,blank=True)
    total_files=models.CharField(max_length=255,null=True,blank=True)
    completed=models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if self.file_completed==self.total_files:
            self.completed=True
        else:
            self.completed=False
            
        super().save(*args, **kwargs)
    
    
    
    @property
    def files(self):
        return self.process.all()
        
        
    def delete_related_files(self):
        related_files=self.process.all()
        for file in related_files:
            file.delete()
        
        
    
    def __str__(self) -> str:
        return self.user.username
    
    
    
class cvm_run_history(models.Model):
    candidate_id=models.IntegerField(null=True)
    file_name=models.TextField(max_length=255)
    file_path=models.TextField(null=True)
    status=models.BooleanField(default=1)
    completed=models.BooleanField(null=True)
    duplicate=models.BooleanField(null=True)
    email_not_found=models.BooleanField(null=True,default=0)
    infracon=models.BooleanField(null=True)
    doc_file=models.BooleanField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    class Meta:
        db_table='cvm_run_history'
        managed=False
        
        
class education_degree_new(models.Model):
    degree=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    class Meta:
        db_table='education_degree_new'
        managed=False