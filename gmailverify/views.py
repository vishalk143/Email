from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from gmailverify.models import Profile
from django.core.mail import send_mail
from django.conf import settings
import datetime
import random

# Create your views here.
def index(request):
    
    return HttpResponse("homepage created")

def register(request):
    content={}
    if request.method=="POST":
        uname=request.POST['umail']
        mb=request.POST['umobile']
        upass=request.POST['upass']
        cpass=request.POST['cpass']
        
        #Fetch data from form POST request
        # print(uname)
        print(mb)
        # print(upass)
        # print(cpass)
       
        
        if uname=="" or mb=="" or upass=="" or cpass=="":
            content['errmsg']="Field Cannot be Empty"
        elif not (mb.isdigit() and len(mb)==10):
             content['errmsg']="Invalid mobile Number. It must be 10 digit mobile number"
        elif upass != cpass:
            content['errmsg']="Password and Confirm Password didn't match"
        else:
            
            #further validation
           
            try:    
                u=User.objects.create(username=uname,password=upass,email=uname,is_active=1,date_joined=datetime.datetime.now())
                u.set_password(upass)
                u.save()
            except Exception:
                content['errmsg']="Username Already Exists!!!"
                return render(request,'register.html',content)

            try:
                p=Profile.objects.create(uid=u,mobile=mb)
                print(p)
                p.save()
            except Exception:
                content['errmsg']="Mobile Number Already exists!!!"
                return render(request,'register.html',content)
            
            if u and p:
               
                s="EMAIL Verification"
                otp=str(random.randrange(1000,9999))
                #store OTP in session to verify with entered OTP
                msg="OTP for gmail verification"+str(otp)
                r=u.email
                request.session[r]=otp
                print(r)

                send_mail(
                    s,
                    msg,
                    settings.EMAIL_HOST_USER,
                    [r],
                    fail_silently=False,

                )
        
                url='/verifyscreen/'+str(u.id)
                return redirect(url)
                
            
        return render(request,'register.html',content)
    else:
        return render(request,'register.html')
    
def userlogin(request):
    if request.method=="POST":
        pass
    else:
        return render(request,'login.html')

def verifygmail(request,rid):
    content={}
    content['user_id']=rid

    return render(request,'verify.html',content)

def verifyotp(request,rid):
    otp=request.POST['uotp']
    #print("userid:",rid)
    u=User.objects.filter(id=rid)
    uemail=u[0].email
    sess_otp=request.session[uemail]
    #print("session otp:",sess_otp)
    #print("User otp:",otp)
    if int(otp)==int(sess_otp):
        return render(request,'gmailsuccess.html')
