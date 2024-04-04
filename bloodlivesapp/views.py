from django.shortcuts import render, redirect
from . models import user
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def listToString(s):
    str1 = " " 
    return (str1.join(s)) 

def index(request):
    return render(request,'login.html')

def signuppage(request):
    return render(request,'signup.html')

def logout(request):
    request.session['uid'] = None
    return redirect('index')

def home(request):
    uid = request.session['uid']
    print(uid)
    if uid != None:
        return render(request,'home.html')
    else:
        messages.info(request,'Restricted')
    return redirect('index')

def userlogin(request):
    if request.method=='POST':
        mail = request.POST['email']
        pwd = request.POST['password']

        try:
            users = user.objects.get(email=mail, password=pwd)
            request.session['uid'] = users.id
            return redirect('home')

        except ObjectDoesNotExist:
            uid = None
            messages.info(request,'Invalid credentials')
            return redirect('index')
         
    return redirect('index')

def usersignup(request):
    if request.method=='POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        bg = request.POST['bloodgroup']
        mail = request.POST['email']
        ph = request.POST['phone']
        dob = request.POST['dob']
        gender = request.POST['gender']
        address = request.POST['address']    
        dist = request.POST['district']
        state = request.POST['state']
        country = request.POST['country']
        pwd = request.POST['password']
        cpwd = request.POST['confirmpassword']

        if cpwd == pwd:
            if dob < "2003-1-1":
                usignup = user(firstname=fname,lastname=lname,email=mail,phone=ph,dob=dob,gender=gender,bloodgroup=bg,country=country,state=state,district=dist,password=pwd)
                usignup.save()
                messages.info(request,'Successfully Registered')
            else:
                messages.info(request,'Age is Not eligible')
        else:
            messages.info(request,'Confirm Password does not Match')

    return render(request,'login.html')
    

def search(request):
    if request.method=="POST":
        bg = request.POST['bloodgroup']
        dist = request.POST['district']

        request.session['bg'] = bg
        request.session['dist'] = dist
        try:
            res = user.objects.filter(bloodgroup=bg,district=dist)
            if not res:
                messages.info(request,'Doner Not found')
                return redirect('home')
            else:
                messages.info(request,'Doner found')
                return render(request,'home.html', { 'res':res })

        except ObjectDoesNotExist:
            messages.info(request,'Doner Not found')
            return redirect('home')

    return redirect("home")
             
def sendmail(request,id):
    bg = request.session['bg']
    uid = request.session['uid']
    sender = user.objects.get(id = uid)
    reciver = user.objects.get(id=id)

    text = []
    text.append(bg)
    text.append(" Blood is Needed please contect: ")
    text.append(sender.phone)
    text.append("Email: ")
    text.append(sender.email)

    Subject = "Emergency Blood Needed"
    Main_Text = listToString(text)
    From_mail = settings.EMAIL_HOST_USER
    To_mail = [reciver.email]

    send_mail(Subject, Main_Text, From_mail, To_mail, fail_silently=False)
    messages.info(request,'Email Sent Successfully')
    return redirect("home")


def sendmassmail(request):
    bg = request.session['bg']
    dist = request.session['dist']
    uid = request.session['uid']
    
    try:
        res = user.objects.filter(bloodgroup=bg,district=dist)
        sender = user.objects.get(id = uid)
        text = []
        text.append(bg)
        text.append(" Blood is Needed please contect: ")
        text.append(sender.phone)
        text.append("or Email: ")
        text.append(sender.email)

        reciver = []
        for r in res:
            reciver.append(r.email)
        
        print(reciver)
        Subject = "Emergency Blood Needed"
        Main_Text = listToString(text)
        From_mail = settings.EMAIL_HOST_USER
        To_mail = reciver

        send_mail(Subject, Main_Text, From_mail, To_mail, fail_silently=False)
        messages.info(request,'Email Sent Successfully')
        return redirect("home")
    except ObjectDoesNotExist:
        messages.info(request,'No Results Found')
        return redirect('home')

    return redirect("home")
