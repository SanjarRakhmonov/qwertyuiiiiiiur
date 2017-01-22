from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from courses.models import Course


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(required=True, label="",
								widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username',}))
    email = forms.EmailField(required=True, label="",
								widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email',}))
    password = forms.CharField(label="",
								widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password',}),
        max_length=255)
    password2 = forms.CharField(label="",
								widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Repeat password',}),
        max_length=255)					
								
    class Meta:
        model = User
        fields = ('username', 'email')
		

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email.lower()
        raise forms.ValidationError('A user with that email already exists.')
			
			
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password do not match. ')
        return cd['password2']

		
		
	


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
'''

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('about',)
'''
		
class CourseEnrollForm(forms.Form):
	course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)
	
	
	
	
	
	
