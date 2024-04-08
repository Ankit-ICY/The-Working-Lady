from django.urls import path,include
from . import views




urlpatterns = [
    path('', views.index ,name='index'),
    path('login_user', views.login_user, name="login_user"),
    path('register', views.register, name="register"),
    path('recruiter-page/', include('recruiter.urls')),
    path('about-us', views.about_us ,name='about_us'),
        
]

 