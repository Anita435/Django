from django.shortcuts import render, redirect
from user_api import models as user_model
import http.client, json
from django.contrib import messages
from django.contrib.auth import login
from user_api.models import User
from django.core.paginator import Paginator



def index(request):

    return render(request, 'dashboard/index.html')


def dashboard_base(request):
    if request.user.is_authenticated and request.user.is_superuser:
        user = {
            "first_name":None
        }
        user_admin = user_model.UserProfile.objects.filter(user=request.user).first()
        if user_admin:
            user = user_admin
            return render(request, 'dashboard/base.html', {'user':user})
        else:
            return render(request, 'dashboard/base.html', {'user': user})
    return redirect('/login/')


def fill_data(request):
    return render(request, 'dashboard/reset_password/fill_otp.html')


def all_user(request):
    user = User.objects.all().exclude(id=1)
    paginator = Paginator(user, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request,
                  'dashboard/register.html',
                  {'posts': posts,'total':len(user)})


def password_reset(request):
    return render(request, 'dashboard/reset_password/sent_verification_code.html')


def fill_password(request):
    return render(request, 'dashboard/reset_password/fill_password.html')


def sent_otp(request):
    if request.method == 'POST':
        phone_number = request.POST['mobile_number']
        user = user_model.User.objects.filter(phone_number=phone_number).first()

        if not user or user is None:
            messages.warning(request, "Please enter valid mobile number")

        if user and user.is_superuser:
            conn = http.client.HTTPConnection("2factor.in")
            payload = ""
            headers = {'content-type': "application/x-www-form-urlencoded"}
            conn.request("GET", "/API/V1/ca819fb2-e222-11ea-9fa5-0200cd936042/SMS/" + phone_number + "/AUTOGEN",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()
            user_model.OTPDetails.objects.get_or_create(
                otp_response=data.decode("utf-8"),
                user=user_model.User.objects.get(id=user.id)
            )

            return render(request, 'dashboard/reset_password/fill_otp.html', {'user_number': user.id})
    return render(request, 'dashboard/reset_password/sent_verification_code.html')


def verify_otp(request):
    user = request.POST.get('user_number')
    curr_user = user_model.User.objects.filter(id=user).first()
    otp_session_id = user_model.OTPDetails.objects.filter(user=curr_user).last()

    if request.method == 'POST':
        otp = request.POST['otp']
        if otp_session_id and otp_session_id.otp_response:
            otp_response = json.loads(otp_session_id.otp_response)

            if otp_response['Status']:
                conn = http.client.HTTPConnection("2factor.in")

                payload = ""

                headers = {'content-type': "application/x-www-form-urlencoded"}

                conn.request("GET",
                             "/API/V1/ca819fb2-e222-11ea-9fa5-0200cd936042/SMS/VERIFY/" +
                             otp_response['Details'] + "/" + str(otp),
                             payload, headers)

                res = conn.getresponse()
                data = res.read()
                data = json.loads(data.decode("utf-8"))
                if data.get('Status') == 'Success' and data.get('Details') == "OTP Matched":

                    return render(request, 'dashboard/reset_password/fill_password.html', {'user_number': curr_user.id})
                else:
                    messages.warning(request, "OTP did't verify please try again!")
                    return redirect('dashboard:sent_otp')

    return render(request, 'dashboard/reset_password/sent_verification_code.html')


def change_password(request):
    user = request.POST.get('user_number')
    user = user_model.User.objects.filter(id=user).first()

    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['password']

        if password != confirm_password:
            messages.warning(request, "Password didn't match!")
            return redirect('dashboard:fill_password')

        else:
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('dashboard:dashboard_base')

    return render(request, 'dashboard/login.html')


def change_password_inner(request):
    if request.user:
        if request.method == 'POST':
            user = user_model.User.objects.filter(id=request.user.id).first()
            password = request.POST['password']
            confirm_password = request.POST['password']
            if password != confirm_password:
                messages.warning(request, "Password didn't match!")
                return redirect('dashboard:fill_password')
            else:
                user.set_password(password)
                user.save()
                login(request, user)
                return redirect('dashboard:dashboard_base')
        return render(request,'dashboard/reset_password/fill_password_inner.html')
    return redirect('login')


def edit_profile(request):
    if request.user.is_authenticated and request.user.is_superuser:
        user = user_model.UserProfile.objects.filter(user=request.user).first()
        if request.method == 'POST':
            if user:
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.address = request.POST['address']
                user.gender = request.POST['gender']
                user.save()
                messages.warning(request, "Your details updated!")
                return redirect('dashboard:dashboard_base')
            else:
                user_model.UserProfile.objects.create(
                    first_name=request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    address = request.POST['address'],
                    gender=request.POST['gender'],
                    user=request.user

                    )

    return redirect("dashboard:dashboard_base")
