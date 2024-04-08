
from django.shortcuts import render,redirect
from .forms import ApplicantsForm
from .models import Applicants, Work,Work_Category
# Create your views here.
from django.contrib import messages


def applicant_form(request):
    if request.method == 'POST':
        try:
            jobs = request.POST.getlist('selected_jobs[]')
            work_place = request.POST.get('block_option')
            full_name = request.POST.get('full_name')
            phone_number = request.POST.get('phone_number')
            phone_number2 = request.POST.get('phone_number2')
            qualification = request.POST.get('qualification')
            last_salary = request.POST.get('last_salary')
            duration = request.POST.get('duration')
            job_location = request.POST.get('job_location')
            location = request.POST.get('location')
            gender = request.POST.get('gender')
            description = request.POST.get('description')
            age = request.POST.get('age')
            language = request.POST.get('language')
            experience = request.POST.get('experience')
            photo = request.FILES.get('photo')
            religion = request.POST.get('religion')
            additional_documents = request.POST.get('additional_documents')
            address =  request.POST.get('permanent_address')
            expected_salary =  request.POST.get('expected_salary')
            resume = request.FILES.get('resume')

            print(jobs)
            selected_jobs = Work.objects.filter(work__in=jobs)
            for job in selected_jobs:
                print(job.work)
            place = Work_Category.objects.get(category=work_place)
            print(place)
            if not selected_jobs.exists():
                raise ValueError('No matching jobs found.')

            obj = Applicants.objects.create(full_name=full_name, location=location, experience= experience, description =description, age= age, gender=gender,phone_number= phone_number, language=language,photo= photo,resume = resume
                                ,phone_number2=phone_number2 , qualification=qualification,last_salary = last_salary, 
                                job_duration= duration,preffered_location= job_location, expected_salary= expected_salary ,religion= religion,document = additional_documents , address=address, work_place=place)
            print("yhn tk succeed")
            obj.job.add(*selected_jobs)
            obj.save()

            return redirect('thankyou_page')
        
        except Exception as e:

            messages.info(request, f"Something Went Wrong!! {str(e)}")
            return redirect('index')
    
    return render(request,'applicant_form.html')


def thankyou_page(request):
    return render(request, 'thankyou.html')