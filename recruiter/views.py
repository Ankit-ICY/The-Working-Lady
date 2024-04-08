from django.shortcuts import render,redirect
from .models import Recruiter, User_Recruiter
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from applicant.models import Work
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponseBadRequest
import razorpay  
from django.contrib.auth import logout
import re

# Create your views here.
from applicant.models import Applicants, Work_Category


def log_off(request):
    logout(request)
    return redirect('index')

@login_required
def recruiter_home(request):
    
    jobs = Recruiter.objects.filter(recruiter__user = request.user)
    applicants = Applicants.objects.all()
    shortlisted_applicants = 0
    for job in jobs:
        shortlisted_applicants += job.selected_applicants.count()

    context ={
        'job_count' : jobs.count(),
        'shortlisted' : shortlisted_applicants,
        'applicants_count' : applicants.count(),
        'applicants' : applicants
    }
    return render(request, 'recruiter_home.html', context) 


  
@login_required
def all_jobs(request):
    try:
        if request.method == "POST":
            status = request.POST.get('status')
            user_obj = User_Recruiter.objects.get(user = request.user)
            if status== 'Active':
                jobs = Recruiter.objects.filter(recruiter = user_obj ,status = True)
            elif status == 'Disabled':
                jobs = Recruiter.objects.filter( recruiter = user_obj ,status = False)

            else:
                jobs = Recruiter.objects.filter(recruiter__user=request.user)

        else:
            jobs = Recruiter.objects.filter(recruiter__user=request.user)

        context = {'jobs' : jobs}
        return render(request, 'recruiter_jobs.html', context)
    
    except Exception as e:
        return HttpResponse("An error occurred. Please try again later.", status=500)


@login_required
def status_change(request,id):
    
    job = Recruiter.objects.get(recruiterId = id)
    job.status = not job.status 
    job.save()
    return redirect('all_jobs')
    

@login_required
def view_applicants(request):
    message = ""
    applicants = None
    try:
        if request.method == "POST":
            cat = request.POST.get('category')
            exp = request.POST.get('experience')
            search_job = request.POST.get('search_job')
            if search_job:

                if "," in search_job and " " in search_job:
                    jobs = []

                    string = ""
                    for job in search_job:
                        if job==",":
                            if string:
                                jobs.append(string)
                                string = ""

                        elif job ==" ":
                            if string:
                                jobs.append(string)
                                string = ""

                        else:
                            string +=job

                    if string:
                        jobs.append(string.strip())
                    print(jobs)

                elif ',' in search_job:
                    jobs = [job.strip() for job in search_job.split(',')]
                    print(jobs)

                elif  ' ' in search_job:
                    jobs = [job.strip() for job in search_job.split(' ')]

          
                else:
                    jobs = [search_job.strip()]
          

                applicants = Applicants.objects.filter(
                    job__work__icontains=jobs[0]  # Using icontains for case-insensitive search for the first job
                )
                for job in jobs[1:]:  # Iterate through remaining jobs in the list
                    applicants = applicants.filter(job__work__icontains=job)

                applicants = applicants.annotate(
                    num_matching_jobs=Count('job', filter=Q(job__work__icontains=jobs[0]))  # Using icontains for case-insensitive search for the first job
                ).order_by('-num_matching_jobs')

                message = f"Search result of jobs: {search_job}"
                
               

            elif cat and (cat=='All'  or cat=='All Categories'):
                if exp and exp.isdigit():
                    applicants = Applicants.objects.filter(experience__gte=int(exp)) 
                else:
                    applicants = Applicants.objects.all()

            else:
                if not search_job and not cat and not exp:
                    applicants = Applicants.objects.all()
                
                elif exp and exp.isdigit():
                    specific_category = Work_Category.objects.get(category=cat)
                    applicants = Applicants.objects.filter(work_place=specific_category)
                    applicants = applicants.filter(experience__gte=int(exp)) 
                    message = f'Applicants with specific Category: {cat} and Experience: {int(exp)}'
                else:
                    specific_category = Work_Category.objects.get(category=cat)
                    applicants = Applicants.objects.filter(work_place=specific_category)
                    message = f'Applicants with specific Category: {cat}'
        else:
            applicants = Applicants.objects.all()


        category = Work_Category.objects.all()
        context = {'applicants':applicants, 'categories': category, 'message': message}

        return render(request, 'view_applicants.html', context)
    except Exception as e:
        return HttpResponse(f"Error occurred: {e}")
    




def delete_job(request, id):
    job = get_object_or_404(Recruiter, recruiterId=id)
    job.delete()
    return redirect('all_jobs')
    
@login_required
def contact_us(request):
    return render(request, 'contact_us.html')




@login_required
def view_requirements(request, id):
    
    try:        
        joby = Recruiter.objects.get(recruiterId=id)
        
        applicants = Applicants.objects.annotate(
            num_matching_jobs=Count('job', filter=Q(job__in=joby.job.all()))  
        ).order_by('-num_matching_jobs')  
        
        search_job = list(joby.job.values_list('work', flat=True))        
        message = f"Search result of jobs: {search_job}"
        category = Work_Category.objects.all()
        
        context = {'applicants': applicants, 'categories': category, 'message': message,'filter' : True}
        return render(request, 'view_applicants.html', context)
    
    except Exception as e:
        message = "Recruiter not found."
        return HttpResponse(f"Error occurred: {e}")
    

@login_required
def select_job(request,id):

    jobs = Recruiter.objects.filter(recruiter__user=request.user, status = True)
    context ={'applicant_id' : id , 'jobs' : jobs}
    return render(request,'select_jobs.html' , context)


@login_required
def assign_applicant(request, id1, id2):
    
    applicant = Applicants.objects.get(pk=id1)
    job = Recruiter.objects.get(pk=id2)
    job.selected_applicants.add(applicant)
    job.save()
    notification = f"{applicant.full_name} assigned to the job id : {job.recruiterId}"

    jobs = Recruiter.objects.filter(recruiter__user = request.user ,status = True)

    context ={'applicant_id' : id1 , 'jobs' : jobs, 'notification':notification}
    return render(request,'select_jobs.html' , context)


@login_required
def applicant_view(request, id):
    try:
        applicant  = Applicants.objects.get(applicant_id = id)
        return render(request,'view_applicant.html' ,{'applicant': applicant})
    
    except Exception as e:
        message = "Recruiter not found."
        return HttpResponse(f"Error occurred: {e}")


@login_required
def selected_applicants(request,id):
    try:
        applicants = None
        jobs = Recruiter.objects.get(recruiterId = id)
        applicants = jobs.selected_applicants.all()
        if applicants:
            message = "Your selected candidates for the job"

        else:
            message = "No Applicants Selected for the job" 
        
        category = None
        context  = {'applicants':applicants , 'categories': category, 'message': message,'filter' : True, 'deselect' : id}
        return render(request, 'view_applicants.html',context)
    
    except Exception as e:
        message = "Recruiter not found."
        return HttpResponse(f"Error occurred: {e}")


@login_required
def deselect_applicant(request,id1, id2):

    applicant = Applicants.objects.get(applicant_id = id1)
    job = Recruiter.objects.get(recruiterId = id2)

    job.selected_applicants.remove(applicant)
    job.save()

    return redirect('selected_applicants',id2)



def create_job(request):
    obj_data = request.session.get('obj')
    try:
        if request.method == "POST":
            full_name = request.POST.get('full_name')
            phone_number = request.POST.get('phone_number')
            phone_number2 = request.POST.get('phone_number2')
            email = request.POST.get('email')
            address = request.POST.get('address')
            location = request.POST.get('location')
            urgency = request.POST.get('urgency')
            requirement = request.POST.get('requirement')
            description = request.POST.get('description')
            provided_salary = request.POST.get('provided_salary')
            experience = request.POST.get('experience')
            source = request.POST.get('source')
            preffered_location = request.POST.get('preffered_location')
            timing = request.POST.get('timing')
            jobs = request.POST.getlist('job[]')

            selected_jobs = Work.objects.filter(work__in=jobs)
            if request.user.is_authenticated:
                user_obj = User_Recruiter.objects.get(user=request.user)
                obj = Recruiter.objects.create(
                    full_name=full_name,
                    phone_number=phone_number,
                    phone_number2=phone_number2,
                    email=email,
                    address=address,
                    location=location,
                    urgency=urgency,
                    requirement=requirement,
                    description=description,
                    preffered_location=preffered_location,
                    provided_salary=provided_salary,
                    experience=experience,
                    source=source,
                    timing=timing,
                    status=True,
                    recruiter=user_obj
                )
                obj.job.add(*selected_jobs)
                obj.save()
                messages.success(request, 'Job Posted Successfully !!')
                return redirect('all_jobs')

            else:
                request.session['obj'] = {
                    'full_name': full_name,
                    'phone_number': phone_number,
                    'phone_number2': phone_number2,
                    'email': email,
                    'address': address,
                    'location': location,
                    'urgency': urgency,
                    'requirement': requirement,
                    'description': description,
                    'preffered_location': preffered_location,
                    'provided_salary': provided_salary,
                    'experience': experience,
                    'source': source,
                    'timing': timing,
                    'status': True,
                    'jobs': jobs,
                }
                request.session.save()
                messages.info(request, 'Job will be posted after signup')
                return redirect('register')

        elif obj_data:
            context = {
                'full_name': obj_data['full_name'],
                'phone_number': obj_data['phone_number'],
                'email': obj_data['email'],
                'message': obj_data['message']
            }
            request.session.pop('obj', None)
            return render(request, 'create_job.html', context)

        user = User_Recruiter.objects.get(user=request.user)
        context = {
            'phone_number': user.number
        }
        return render(request, 'create_job.html', context)


    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('all_jobs')




razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def initiate_payment(amount, currency='INR'):
   data = {
       'amount': amount * 100,  # Razorpay expects amount in paise (e.g., 100 INR = 10000 paise)
       'currency': 'INR',
       'payment_capture': '1'  # Auto capture the payment after successful authorization
   }
   response = razorpay_client.order.create(data=data)
   return response['id']

def payment_view(request):
   amount = 100  # Set the amount dynamically or based on your requirements
   order_id = initiate_payment(amount)
   context = {
       'order_id': order_id,
       'amount': amount
   }
   return render(request, 'payment.html', context)


@csrf_exempt
def payment_success_view(request):
   order_id = request.POST.get('order_id')
   payment_id = request.POST.get('razorpay_payment_id')
   signature = request.POST.get('razorpay_signature')
   params_dict = {
       'razorpay_order_id': order_id,
       'razorpay_payment_id': payment_id,
       'razorpay_signature': signature
   }
   print(params_dict)
   try:
       razorpay_client.utility.verify_payment_signature(params_dict)
       # Payment signature verification successful
       # Perform any required actions (e.g., update the order status)
       return render(request, 'payment_success.html')
   except razorpay.errors.SignatureVerificationError as e:
       # Payment signature verification failed
       # Handle the error accordingly
       return render(request, 'payment_failure.html')

def pricing(request):
    return render(request, 'pricing.html')