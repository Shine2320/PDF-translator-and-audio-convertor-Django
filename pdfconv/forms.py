from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class PDFForm(forms.Form):   
    file= forms.FileField() # for creating file input  

from_languages =(
	('auto','Auto Detect'),
    ('ml', 'Malayalam'),
	('kn', 'Kannada'),
    ('en', 'English'),
    ('hi', 'Hindi'),
    ('ta', 'Tamil')
)
languages =(
    ('ml', 'Malayalam'),
	('kn', 'Kannada'),
    ('en', 'English'),
    ('hi', 'Hindi'),
    ('ta', 'Tamil')
)
class PDFtranslate(forms.Form):
	file = forms.FileField() # for creating file input
	from_language = forms.ChoiceField(choices = from_languages)
	to_language = forms.ChoiceField(choices = languages)