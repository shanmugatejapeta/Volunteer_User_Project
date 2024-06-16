from django.forms import ModelForm
from django import forms
from .models import Problems,Volunteers
from django.contrib.auth.forms import UserCreationForm

class ProbForm(ModelForm):
    class Meta:
       model=Problems
       fields=('statement',)
class SignUpForm(UserCreationForm):
    volunteer=forms.ModelChoiceField(queryset=Volunteers.objects.all())