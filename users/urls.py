from django.urls import path,include
from . import views




urlpatterns = [
    path('', views.index ,name='index'),
    path('login_user', views.login_user, name="login_user"),
    path('register', views.register, name="register"),
    path('recruiter-page/', include('recruiter.urls')),
    path('about-us', views.about_us ,name='about_us'),
    path('steps', views.steps ,name='steps'),
    path('police_verification', views.police_verification ,name='police_verification'),
    path('Privacy-Policy', views.privacy_policy ,name='privacy_policy'),
    path('Terms-of-Use', views.termsofuse ,name='termsofuse'),
    path('Pricing', views.pricing_page ,name='pricing_page'),
    path('TWL-Blogs', views.blogs_page, name='blogs_page'),
    path('Blog/<int:id>', views.blog, name='blog_post'),
    path('TWL-Blacklist', views.blacklisted, name='blacklisted'),

]

 
