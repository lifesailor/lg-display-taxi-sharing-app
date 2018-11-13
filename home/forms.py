from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='LG Display 사내 이메일을 입력하세요. ex) abc@lgdipslay.com')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        
    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('@')[1]
        
        #향후 lgdpartner.com
        domain_list = ["lgdisplay.com", "lgdpartner.com"]
        
        if domain not in domain_list:
            raise forms.ValidationError('LG Display 사내 이메일을 입력하세요. ex) abc@lgdipslay.com')
         
        if User.objects.filter(email=email).exists():
                raise forms.ValidationError('이미 존재하는 이메일입니다.')

        return email

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = user.email.lower()
        
        if commit:
            user.save()
        return user