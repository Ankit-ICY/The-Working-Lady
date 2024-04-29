from django.urls import path,include
from . import views 
from django.conf.urls import handler404



urlpatterns = [
    path('', views.recruiter_home ,name='recruiter_home'),
    path('Jobs/', views.all_jobs ,name='all_jobs'),
    path('status/<int:id>', views.status_change ,name='status_change'),
    path('view-applicants/', views.view_applicants ,name='view-applicants'),
    path('delete_job/<int:id>', views.delete_job ,name='delete_job'),
    path('contact-us', views.contact_us ,name='contact_us'),
    path('view_requirements/<int:id>', views.view_requirements, name='view_requirements'),
    path('select-applicants/<int:id>', views.select_job, name='select_applicants'),
    path('assign/<int:id1>/<int:id2>/', views.assign_applicant, name='assign_applicant'),
    path('applicant-view/<int:id>', views.applicant_view, name='applicant_view'),
    path('selected-applicants/<int:id>', views.selected_applicants, name='selected_applicants'),
    path('deselect-applicants/<int:id1>/<int:id2>/', views.deselect_applicant, name='deselect_applicants'),
    path('create-job', views.create_job , name='create_job'),
    path('pricing/', views.pricing, name='pricing'),
    path('payment/', views.payment_view, name='payment'),
    path('payment/success/', views.payment_success_view, name='payment_success'),
    path('log_off/', views.log_off, name='log_off'),
    path('checkout/<int:id>', views.checkout, name='checkout'),
    path('profile', views.user_profile, name='user_profile'),
    path('remove_photo/<int:id>', views.remove_photo, name='remove_photo'),

    ]

 
