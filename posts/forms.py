from django.contrib.auth.models import User
from django import forms
from .models import Post

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']

        eidgets={
		'password': forms.PasswordInput(),
		}
class UserLogin(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())

class Postform(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'content', 'img', 'draft', 'publish']
		


		widgets={
		'publish' : forms.DateInput(attrs={"type":"date"}),
		}


