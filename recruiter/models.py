from django.db import models
from applicant.models import Work, Work_Category,Applicants
# Create your models here.
from django.contrib.auth.models import User


class User_Recruiter(models.Model):
    user  = models.OneToOneField(User , on_delete=models.CASCADE)
    number = models.CharField(max_length = 20)

    def __str__(self) -> str:
        return self.user.username

class Recruiter(models.Model):
    recruiter = models.ForeignKey(User_Recruiter, on_delete = models.CASCADE  )
    recruiterId = models.AutoField(primary_key=True,unique=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15,default = False)
    phone_number2 = models.CharField(max_length=15, null= True, blank = True) 
    address = models.CharField(max_length = 100, null= True, blank = True )
    location = models.CharField(max_length = 60)
    pin_code = models.CharField(max_length=15,null=True, blank=True)
    requirement = models.CharField(max_length = 60,default = False)
    full_name = models.CharField(max_length = 60)
    job = models.ManyToManyField(Work)
    provided_salary = models.CharField(max_length=12, null= True, blank = True)
    description =  models.TextField(max_length = 200,null= True, blank = True)
    urgency = models.CharField(max_length = 50,default = False)
    status = models.BooleanField(default = False)
    experience= models.IntegerField(default = 0)
    timing = models.CharField(max_length = 30 ,default = False)
    preffered_location = models.CharField(max_length = 50,default = False)  
    source = models.CharField(max_length = 50 ,default= False)
    posted_on = models.DateField(auto_now_add=True,null= True, blank = True)
    selected_applicants = models.ManyToManyField(Applicants, null=True,blank=True)

    def __str__(self) -> str:
        return self.full_name   
    



class Price(models.Model):
    price_id = models.AutoField(primary_key=True,unique=True)
    user_for = models.CharField(max_length=30)
    price = models.CharField(max_length=30)
    pack = models.CharField(max_length=30)
    maid_type = models.CharField(max_length=50)
    working_hours = models.CharField(max_length=50)
    support = models.CharField(max_length=20)


