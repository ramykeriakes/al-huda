from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from django import forms
from django.forms import ModelForm

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea)

class JobForm(ModelForm):
    class Meta:
        model = models.Job
        fields= '__all__'

class ProfileForm(ModelForm):
    class Meta:
        model = models.Profile
        exclude = ['user', 'jobs_applied', 'saved_jobs', 'saved_profiles']
#  if JobForm.is_valid():
#  return render_to_response("form.html")
#  else:
#    return HttpResponseRedirect("/error/")
