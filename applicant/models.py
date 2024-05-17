from django.db import models

# Create your models here.


class Work_Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length = 50)
    def __str__(self) -> str:
        return self.category   

class Work(models.Model):
    Work_id = models.AutoField(primary_key=True)
    work = models.CharField(max_length = 50)
    work_category = models.ManyToManyField(Work_Category)
    def __str__(self) -> str: 
        return self.work   

class Applicants(models.Model):
    applicant_id = models.AutoField(primary_key=True, unique=True)
    language = models.CharField(max_length = 10 )
    photo= models.ImageField(upload_to='user_photo', null= True, blank = True)
    full_name = models.CharField(max_length = 60)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    location = models.CharField(max_length = 60)
    job = models.ManyToManyField(Work)
    experience= models.IntegerField(default = 0)
    description =  models.TextField(max_length = 200,null= True, blank = True)
    age = models.CharField(max_length = 5)
    expected_salary = models.CharField(max_length=50, null= True, blank = True)
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20,default = False)
    phone_number2 = models.CharField(max_length=20, null= True, blank = True)  
    qualification = models.CharField(max_length = 50,default = False)
    last_salary = models.CharField(max_length = 20, null= True, blank = True )
    address = models.CharField(max_length = 150, null= True, blank = True )
    document = models.CharField(max_length = 50, null= True, blank = True  )
    job_duration = models.CharField(max_length = 30,default = False)
    religion = models.CharField(max_length = 10,default = False)
    preffered_location = models.CharField(max_length = 50,default = False)
    work_place = models.ForeignKey(Work_Category, on_delete = models.CASCADE,default = False)
    blacklist = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.full_name   
