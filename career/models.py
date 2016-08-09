from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from localflavor.fr.forms import FRPhoneNumberField
from django.forms import ModelForm
from django.contrib.auth.models import User, Permission

# Create your models here.

#Academic degree choices
COMPUTERSCIENCEBACHELOR = 'CB'
LAWLICENCE = 'LL'
ACCOUNTINGBACHELOR = 'AB'

STUDY_CHOICES = (
  ('CB', 'Computer Science Bachelor Degree'),
  ('LL', 'Law Licence Degree'),
  ('AB', 'Accounting Bachelor Degree'),
)
#Gender Choices
GENDER_CHOICES = (
  ('M', 'Male'),
  ('F', 'Female'),
)
class Job(models.Model):
  #Job title [Required Field]
  title = models.CharField(max_length=200, blank=False, null=False)
  #Department in which the job is available
  department = models.CharField(max_length=200, blank=True)
  #Job description [Required Field]
  job_Description = models.TextField(blank=False)
  #Minimum academic degree required for the job, get choices from pre-defined STUDY_CHOICES  [Required Field]
  min_Qualifications = models.CharField(max_length=2, choices=STUDY_CHOICES, default='CB')
  #Gender required for the job, get choices from pre-defined GENDER_CHOICES [Optional Field]
  gender_Required = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
  #Starting salary for the job [Required Field]
  starting_Salary = models.PositiveIntegerField()
  #Number of daily working hours (3 - 12 hours) [Required Field]
  daily_Working_Hours = models.PositiveIntegerField(validators=[MinValueValidator(3),MaxValueValidator(12),])
  #Number of weekly working days (1 - 6 days) [Required Field]
  weekly_Working_days = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(6),])
  #Application
  #applicants = models.ManyToManyField(Profile)
  def __str__(self):
    if self.department == "":
      return self.title
    else:
      return '%s in %s department' % (self.title, self.department)

  class Meta:
    #Order the jobs by the title
    ordering = ['title']
    verbose_name_plural= "jobs"
    permissions = (
        ("apply_job", "Can apply to job"),
        ("save_job", "Can save a job"),
        ("create_job", "Can create a job"),
        ("check_applicants", "Can check applicants to a job"),
    )


  #def get_absolute_url(self):
  #  return "/jobs/%s/" % self.id
  #def get_fields(self):
  #  return [(field.name, field.value_to_string(self)) for field in jobs._meta.fields]

class Profile(models.Model):
  #This link a profile to a single user
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  #User's first name [Required Field], REQUIRED
  first_Name = models.CharField(max_length=25, blank=False, null=False, verbose_name=('First Name'), help_text=('Put your first name, Mandatory'))
  #User's middle name [optional Field]
  middle_Name = models.CharField(max_length=25, blank=True, verbose_name=('Middle Name'), help_text=('Put your middle name, Optional'))
  #User's last name [Required Field]
  last_Name = models.CharField(max_length=25, blank=False, null=False, verbose_name=('Last Name'), help_text=('Put your last name, Mandatory'))
  #User's gender, get choices from pre-defined GENDER_CHOICES [Optional Field]
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
  #User's date of birth
  date_of_Birth = models.DateField()
  #User's email
  email = models.EmailField()
  #User's address
  address = models.TextField()
  #User's mobile number
  mobile = FRPhoneNumberField()
  #User's academic degree
  academic_Degree = models.CharField(max_length=2, choices=STUDY_CHOICES, default='CB')
  #User's date of graduation
  date_of_Graduation = models.DateField()
  #Jobs that the user applied on
  jobs_applied = models.ManyToManyField(Job, blank=True, verbose_name=('Jobs he applied on'), related_name=('applied_job'))
  #Jobs the user is saving for future
  saved_jobs = models.ManyToManyField(Job, blank=True, verbose_name=('Saved jobs'), related_name=('saved_jobs'))
  #Jobs the user is saving for future
  saved_profiles = models.ManyToManyField('self', blank=True, verbose_name=('Saved profiles'), related_name=('saved_profiles'))


  def __str__(self):
    return '%s %s' % (self.first_Name, self.last_Name)
  class Meta:
    #Order the profiles by the First and Last Name
    ordering = ['first_Name', 'last_Name']
    verbose_name_plural= "profiles"
    permissions = (
        ("view_profile", "Can check profiles"),
    )
