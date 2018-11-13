from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.utils import timezone
import datetime
import time

# Create your views here.
def homepage(request):
    return render(request, 'home/homepage.html', {})

def introduce(request):
    return render(request, 'home/introduce.html', {})
    
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('registration/acc_active_email.html', {
                'user':user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Sharetaxis 이메일 인증'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('<html><head><title>ShareTaxis</title></head><body><h1>입력하신 이메일 주소로 인증 메일을 보내드렸습니다.</h1>'+
                                '<h1>Let\'s Mail 또는 M Portal 메일에서 구성원 인증을 완료해주세요.</h1>'+
                                '<h1><a href="http://sharetaxis.pythonanywhere.com?utm_source=try_signup">ShareTaxis 홈으로 돌아가기</h1></body></html>')
    
    else:
        form = SignupForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('<html><head><title>ShareTaxis</title></head><body><h1>구성원 인증이 완료되었습니다.</h1>'
                            +'<h1>이제 ShareTaxis를 사용할 수 있습니다.</h1>'
                            +'<h1><a href="http://www.talletalle.com/?utm_source=after_signup">ShareTaxis 바로가기</a></h1></body></html></body></html>')
    else:
        return HttpResponse('<html><head></head><body><h1>구성원 인증이 완료되었습니다.</h1>'
                            +'<h1>이제 ShareTaxis를 사용할 수 있습니다.</h1>'
                            +'<h1><a href="http://www.talletalle.com/?utm_source=after_signup">ShareTaxis 바로가기</a></h1></body></html></body></html>')
