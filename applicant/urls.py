from django.urls import path,include
from . import views 

urlpatterns = [
    path('', views.applicant_form ,name='applicant_form'),
    path('submission' ,views.thankyou_page , name='thankyou_page')
 

 
]

 