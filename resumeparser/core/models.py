# from django.db import models
# from numpy import mod

# class Details(models.Model):
#     date  = models.DateTimeField(auto_now_add=True)
#     name = models.CharField(max_length=254)
#     email= models.EmailField(max_length=150)
#     company = models.TextField()
#     # projects = models.TextField()
#     noproject = models.CharField(max_length=100)
#     mothername = models.CharField(max_length=254)
#     mobileno = models.BigIntegerField()
#     altmobileno = models.BigIntegerField()
#     curraddr = models.TextField()
#     peraddr = models.TextField()
#     pan = models.CharField(max_length=200)
#     passport = models.CharField(max_length=200)
#     dob = models.CharField(max_length=200)
#     level = models.TextField()
#     college = models.TextField()
#     year = models.TextField()
#     university = models.TextField()
#     wnames = models.TextField()
#     client = models.TextField()
#     designation = models.TextField()


# class genDetails(models.Model):
#     date  = models.DateTimeField(auto_now_add=True)
#     firstname = models.CharField(max_length=254)
#     middlename = models.CharField(max_length=254)
#     lastname = models.CharField(max_length=254)
#     q_lvl = models.CharField(max_length=200)
#     course =models.CharField(max_length=50)
#     yearofP = models.CharField(max_length=100)
#     stream = models.CharField(max_length=50)
#     specialization = models.CharField(max_length=100)
#     institute_name = models.CharField(max_length=200)
#     university = models.CharField(max_length=254)
#     percentage = models.CharField(max_length=254)
#     mode = models.CharField(max_length=254)
#     pri_number = models.CharField(max_length=254)
#     sec_number = models.CharField(max_length=254)
#     primary_email = models.CharField(max_length=254)
#     sec_email =models.CharField(max_length=254)
#     p_number = models.CharField(max_length=254)
#     pas_number = models.CharField(max_length=254)
#     ad_number = models.CharField(max_length=254)
#     nationality = models.CharField(max_length=254)
#     dob =models.CharField(max_length=254)
#     fname = models.CharField(max_length=254)
#     mname = models.CharField(max_length=254)
#     gender = models.CharField(max_length=254)
#     curr_addr = models.CharField(max_length=254)
#     per_addr = models.CharField(max_length=254)
#     cor_addr = models.CharField(max_length=254)
#     company = models.CharField(max_length=254)
#     from_date = models.CharField(max_length=254)
#     to_date = models.CharField(max_length=254)
#     design = models.CharField(max_length=254)
#     ho_country = models.CharField(max_length=254)
#     nature = models.CharField(max_length=254)
#     responsibility = models.CharField(max_length=254)
# # Create your models here.
# class Tblcv_gen(models.Model):
#     fname = models.CharField(max_length=100)
#     mname = models.CharField(max_length=100, blank=True, null=True)
#     lname = models.CharField(max_length=100, blank=True, null=True)
#     dob = models.DateField(blank=True, null=True)
#     email = models.CharField(max_length=100)
#     email2 = models.CharField(max_length=100, blank=True, null=True)
#     phone = models.CharField(max_length=22)
#     phone2 = models.CharField(max_length=22, blank=True, null=True)
#     gender = models.CharField(max_length=20)
#     nationality_id = models.IntegerField()
#     fathername = models.CharField(max_length=100, blank=True, null=True)
#     mothername = models.CharField(max_length=100, blank=True, null=True)
#     languages = models.CharField(max_length=128, blank=True, null=True)
#     aadharno = models.CharField(max_length=16, blank=True, null=True)
#     panno = models.CharField(max_length=10, blank=True, null=True)
#     isvalidpassport = models.IntegerField()
#     passportno = models.CharField(max_length=30, blank=True, null=True)
#     issuecountry = models.CharField(max_length=30, blank=True, null=True)
#     expirydate = models.DateField(blank=True, null=True)
#     profileimage = models.CharField(max_length=100, blank=True, null=True)
#     is_online = models.IntegerField()
#     onlinesource = models.CharField(max_length=16, blank=True, null=True)
#     status = models.IntegerField()
#     verified_by = models.IntegerField(blank=True, null=True)
#     verified_at = models.DateTimeField(blank=True, null=True)
#     created_by = models.IntegerField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     modified_by = models.IntegerField(blank=True, null=True)
#     modified_at = models.DateTimeField(blank=True, null=True)
#     contacted_at = models.DateTimeField(blank=True, null=True)
#     contacted_by = models.IntegerField(blank=True, null=True)
#     lastviewed_by = models.IntegerField(blank=True, null=True)
#     lastviewed_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'tblcv'

# # class Tbllanguage_gen(models.Model):
# # 	language = models.CharField(max_length=100)
# # 	# created_by = models.IntegerField(blank=True, null=True)
# # 	# # created_at = models.DateTimeField(blank=True, null=True)
# # 	# modified_by = models.IntegerField(blank=True, null=True)
# # 	# modified_at = models.DateTimeField(blank=True, null=True)
# # 	class Meta:
# #         managed = False
# #         db_table = 'tbllanguages'

# class Tblcountries_gen(models.Model):
# 	sortname = models.CharField(max_length=3)
# 	name = models.CharField(max_length=150)
# 	phonecode = models.IntegerField()
# 	class Meta:
# 		db_table = 'tblcountries'
	
# class Tbladdress_gen(models.Model):
#     candidate_id = models.IntegerField()
#     address_type = models.CharField(max_length=1)
#     address = models.CharField(max_length=255)
#     city_id = models.IntegerField()
#     state_id = models.IntegerField()
#     country_id = models.IntegerField()
#     zipcode = models.IntegerField()

#     class Meta:
#         managed = False
#         db_table = 'tbladdress'

# class Tblinstitutes_gen(models.Model):	
# 	institutename=models.CharField(max_length=400)
# 	is_active=models.IntegerField()
# 	created_by=models.IntegerField()
# 	created_at=models.DateTimeField()
# 	modified_by=models.IntegerField()
# 	modified_at=models.DateTimeField()	
# 	class Meta:
# 		managed=False
# 		db_table = 'tblinstitutes'

# class Tblcvfiles_gen(models.Model):
#     filename = models.CharField(max_length=64)
#     candidate_id = models.IntegerField()
#     resume_text = models.IntegerField()
#     created_by = models.IntegerField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'tblcvfiles'


# class Tbleducation_gen(models.Model):
#     candidate_id = models.IntegerField()
#     qualification_id = models.IntegerField()
#     course_id = models.IntegerField()
#     subject_id = models.IntegerField(blank=True, null=True)
#     subject = models.CharField(max_length=64)
#     specialization = models.CharField(max_length=50, blank=True, null=True)
#     institute = models.CharField(max_length=100, blank=True, null=True)
#     university = models.CharField(max_length=100, blank=True, null=True)
#     yearpassed = models.CharField(max_length=20, blank=True, null=True)
#     percentage = models.CharField(max_length=20, blank=True, null=True)
#     edumode_id = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'tbleducation'


# class Tbluniversities_gen(models.Model):
# 	univname = models.CharField(max_length=100)
# 	is_active = models.IntegerField()
# 	created_by = models.IntegerField(blank=True, null=True)
# 	created_at = models.DateTimeField(blank=True, null=True)
# 	modified_by = models.IntegerField(blank=True, null=True)
# 	modified_at = models.DateTimeField(blank=True, null=True)
# 	class Meta:
# 		managed = False
# 		db_table = 'tbluniversities'


# class Tbldegree_gen(models.Model):
#     degreename = models.CharField(max_length=50)
#     edulevel_id = models.IntegerField()
#     is_active = models.IntegerField()
#     created_by = models.IntegerField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     modified_by = models.IntegerField(blank=True, null=True)
#     modified_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         db_table = 'tbldegree'


# class Tbldesignation_gen(models.Model):
#     designation = models.CharField(max_length=100)
#     created_by = models.IntegerField()
#     created_at = models.DateTimeField()
#     modified_by = models.IntegerField()
#     modified_at = models.DateTimeField()

#     class Meta:
#         db_table = 'tbldesignation'

# class Tblexperience_gen(models.Model):
#     candidate_id = models.IntegerField()
#     companyname = models.CharField(max_length=100)
#     startdate = models.DateField()
#     enddate = models.DateField(blank=True, null=True)
#     designation_id = models.IntegerField(blank=True, null=True)
#     country_id = models.IntegerField()
#     responsibilities = models.TextField(blank=True, null=True)
#     tottalexp = models.IntegerField(blank=True, null=True)
#     employmentnature = models.CharField(max_length=36)

#     class Meta:
#         db_table = 'tblexperience'

# class Tblfundedproject_gen(models.Model):
#     candidate_id = models.IntegerField()
#     startdate = models.DateField()
#     enddate = models.DateField()
#     projectname = models.TextField()
#     projdesig = models.CharField(max_length=50, blank=True, null=True)
#     compdesig = models.CharField(max_length=50, blank=True, null=True)
#     industry_id = models.IntegerField()
#     sector_id = models.IntegerField()
#     phase_id = models.IntegerField()
#     employername = models.CharField(max_length=100)
#     natureemployer = models.CharField(max_length=1)
#     projectexp = models.CharField(max_length=30)
#     country_id = models.IntegerField()
#     state_id = models.IntegerField()
#     city_id = models.IntegerField()
#     projectlength = models.IntegerField(blank=True, null=True)
#     lane = models.IntegerField(blank=True, null=True)
#     projectcost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     clientname = models.CharField(max_length=100, blank=True, null=True)
#     fundingagency_id = models.IntegerField()
#     contractmode_id = models.IntegerField(blank=True, null=True)
#     pavement_id = models.IntegerField(blank=True, null=True)
#     terrain_id = models.IntegerField(blank=True, null=True)
#     remarks = models.TextField(blank=True, null=True)

#     class Meta:
#         db_table = 'tblfundedproject'

# class Tblsubjects_gen(models.Model):
#     id = models.IntegerField(primary_key=True)
#     subject = models.CharField(max_length=50)
#     is_active = models.IntegerField()
#     created_by = models.IntegerField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     modified_by = models.IntegerField(blank=True, null=True)
#     modified_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         db_table = 'tblsubjects'

# # class Tblcities(models.Model):
# #     name = models.CharField(max_length=30)
# #     state_id = models.IntegerField()

# #     class Meta:
# #         # managed = False
# #         db_table = 'tblcities'

