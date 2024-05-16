from django.shortcuts import render,redirect
from recruiter.models import User_Recruiter
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from recruiter.models import Recruiter, Work
import re
from .models import Contact
# from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ValidationError
from email_validator import EmailNotValidError, validate_email


def error_404(request, exception):
    
    return render(request, '404.html', status=404)
 
def error_500(request):
    return render(request, '404.html', status=500)

def validate_email_address(email):
    try:
        v = validate_email (email)
        email = v["email"]
        return True
    except EmailNotValidError as e:
        return False


def validate_pass(password):
    while True:
        if (len(password)<=6):
            flag = -1
            break
        elif not re.search("[a-z]", password):
            flag = -1
            break
        elif not re.search("[A-Z]", password):
            flag = -1
            break
        elif not re.search("[0-9]", password):
            flag = -1
            break
        elif not re.search("[_@$]" , password):
            flag = -1
            break
        else:
            flag = 0
            return True
            break
        
    if flag == -1:
        return False

    else:
        return True

def about_us(request):
    return render(request, 'about_us.html')



def validate_mobile_number(mobile_number):
    pattern = re.compile(r'^\d{10}$')
    return bool(pattern.match(mobile_number))







def index(request):
    if request.method == 'POST':
        try:
            if 'form2_submit' in request.POST:
                name = request.POST.get('name')
                email = request.POST.get('email')
                number = request.POST.get('number')
                comment = request.POST.get('comment')

                obj = Contact.objects.create(name=name, email=email, phone_number=number, comment=comment)
                obj.save()
                messages.success(request, f"Hello {name}, Thank you for your message, we will surely get back to you.")
                return redirect('index')
            else:
                username = request.POST.get('full_name')
                block_option = request.POST.get('block_option')
                phone_number = request.POST.get('phone_number')
                email = request.POST.get('email')

                if not validate_mobile_number(phone_number):
                    messages.success(request, f"{phone_number} is not a valid mobile number")
                    return redirect('index')

                request.session['obj'] = {
                    'full_name': username,
                    'phone_number': phone_number,
                    'email': email,
                    'message': 'Post Your job'
                }
                request.session.save()
                return redirect('create_job')

        except ValidationError as e:
            messages.error(request, f"Validation error: {e}")
            return redirect('index')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('index')

    return render(request, 'index.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.info(request, 'Please provide both username and password.')
            return redirect('login_user')

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.warning(request, 'User not found !!')
            return redirect('login_user')

        obj = authenticate(request, username=username, password=password)
        if obj is None:
            messages.warning(request, 'Wrong credentials !!')
            return redirect('login_user')

        login(request, obj)
        return redirect('recruiter_home')

    return render(request, 'login.html')


def register(request):

    if request.method =="POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            number = request.POST.get('number')
            email = request.POST.get('email')

            if  User.objects.filter(username = username):
                messages.info(request, f'Username {username}  Already Exists, Try using another')
                return redirect('register')

            elif not validate_mobile_number(number):
                messages.info(request,f"{number} is not a valid mobile number")
                return redirect('register')
            
            elif not validate_email_address(email):
                messages.info(request,f"{email} is not a valid")
                return redirect('register')

            elif not validate_pass(password):
                messages.error(request, f'Please Create a strong password !!')
                return redirect('register')

            user_obj = User.objects.filter(email = email)

            if user_obj:
                messages.info(request, f'{email}  Already Exists, Try login or use another email')
                return redirect('register')

            else:
                user  = User(username= username , email=email)
                user.set_password(password)
                user.save()
                recruiter_obj = User_Recruiter.objects.create(user = user, number= number)
                
                obj_data = request.session.get('obj')
                if obj_data:
                    rec = Recruiter.objects.create(
                                full_name=obj_data['full_name'],
                                phone_number=obj_data['phone_number'],
                                phone_number2=obj_data['phone_number2'],
                                email=obj_data['email'],
                                address=obj_data['address'],
                                location=obj_data['location'],
                                urgency=obj_data['urgency'],
                                requirement=obj_data['requirement'],
                                description=obj_data['description'],
                                preffered_location=obj_data['preffered_location'],
                                provided_salary=obj_data['provided_salary'],
                                experience=obj_data['experience'],
                                source=obj_data['source'],
                                timing=obj_data['timing'],
                                status=obj_data['status'],
                                recruiter = recruiter_obj,
                                pin_code = obj_data['pin_code']
                                )
                    selected_jobs = Work.objects.filter(work__in=obj_data['jobs'])
                    rec.job.add(*selected_jobs) 
                    rec.save()
                    recruiter_obj.save()
                    request.session.pop('obj', None)
                    messages.success(request, f'Your job is successfully posted, Please Login !!')
                    return redirect('login_user')


                messages.success(request, f'You are successfully registered. Please log in.')
                return redirect('login_user')
            
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('register')
        except Exception as e:
            messages.error(request, 'An error occurred while processing your request.')
            return redirect('register')

    return render(request,'register.html') 



def steps(request):
    return render(request, 'step.html')



def police_verification(request):
    return render(request, 'police_verification.html')


def privacy_policy(request):
    return render(request, 'privacypolicy.html')

def termsofuse(request):
    return render(request, 'termsofuse.html')
    

def pricing_page(request):
    return render(request, 'pricing_page.html')
