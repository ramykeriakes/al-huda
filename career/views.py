from django.shortcuts import render, render_to_response
from career.models import Job, Profile
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from career.forms import JobForm, ProfileForm, ContactForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.context_processors import csrf


# Create your views here.
def welcome(request):
    return render(request, 'home.html')
def error(request):
  return render(request, 'error.html')
def unautharized(request):
   return render(request, 'unautharized.html')
def contact(request):
    form_class = ContactForm
    return render(request, 'form.html', {'form': form_class})

#permission inside the function
def object_list(request, model):
  obj_type = str(model)
  a=obj_type.split('.')
  b=a[2]
  object_type= b.split("'")[0]
  user =  request.user
  if object_type == 'Profile':
    if request.user.has_perm('view_profile'):
        obj_list = model.objects.all()
        return render(request, 'list.html', {'object_list': obj_list, 'object_type': object_type, 'list_type': 'Available'})
    else:
        return render(request, 'unautharized.html')
  elif object_type == 'Job':
        obj_list = model.objects.all()
        try:
            profile = Profile.objects.get(user= user.id)
            user_applied_jobs = profile.jobs_applied.all()
            key_applied = user_applied_jobs.values_list('applied_job__id', flat=True)
            user_saved_jobs = profile.saved_jobs.all()
            key_saved = user_saved_jobs.values_list('saved_jobs__id', flat=True)
            return render(request, 'list.html', {'object_list': obj_list, 'object_type': object_type, 'list_type': 'Available','key_applied': key_applied, 'key_saved': key_saved})
        except:
            return render(request, 'list.html', {'object_list': obj_list, 'object_type': object_type, 'list_type': 'Available'})
  else:
        return render(request, 'error.html')

@login_required
def display_job(request, Job_id):
    try:
      a_job = Job.objects.get(id=Job_id)
      #data = dict((field.name, field.value_to_string(a_job)) for field in a_job._meta.fields)
      #display = a_job._meta.get_fields()
      return render(request, 'job.html', {'display_job': a_job})
    except:
      return render(request, 'error.html')

@user_passes_test(lambda u: u.is_superuser, login_url='/unautharized/')
def new_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            post = form.save()
            return display_job(request.POST, post.pk)
    else:
        form = JobForm()
    return render(request, 'form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser, login_url='/unautharized/')
def del_job(request, Job_id):
    job = Job.objects.get(id=Job_id)
    job.delete()
    return render(request, 'done_successfully.html')

@login_required
def save_job(request, Job_id):
    user = request.user
    try:
        profile = Profile.objects.get(user= user.id)
        try:
            save_job = profile.saved_jobs.add(Job_id)
            return render(request, 'done_successfully.html')
        except:
          return render(request, 'error.html')
    except:
        return HttpResponseRedirect('/profiles/new/')

@login_required
def apply_job(request, Job_id):
    user = request.user
    try:
        profile = Profile.objects.get(user= user.id)
        try:
            save_job = profile.jobs_applied.add(Job_id)
            return render_to_response('done_successfully.html')
        except:
          return render_to_response('error.html')
    except:
      return HttpResponseRedirect('/profiles/new/')

@login_required
def unsave_job(request, Job_id):
    user = request.user
    try:
        profile = Profile.objects.get(user= user.id)
        try:
            unsave_job = profile.saved_jobs.remove(Job_id)
            return render(request, 'done_successfully.html')
        except:
          return render(request, 'error.html')
    except:
      return HttpResponseRedirect('/profiles/new/')

@login_required
def cancel_application_job(request, Job_id):
    user = request.user
    try:
        profile = Profile.objects.get(user= user.id)
        try:
            cancel_application_job = profile.jobs_applied.remove(Job_id)
            return render(request, 'done_successfully.html')
        except:
          return render(request, 'error.html')
    except:
      return HttpResponseRedirect('/profiles/new/')

@login_required
def get_saved_jobs(request):
    try:
        user = request.user
        profile = Profile.objects.get(user=user.id)
        saved_jobs = profile.saved_jobs.all()
        return render(request, 'list.html', {'object_list': saved_jobs, 'object_type': 'Job', 'list_type': 'Saved'})
    except:
        return render(request, 'error.html')

@user_passes_test(lambda u: u.is_superuser, login_url='/unautharized/')
def get_applicants(request, Job_id):
    job = Job.objects.get(id=Job_id)
    applicants = job.applied_job.all()
    return render(request, 'list.html', {'object_list': applicants, 'object_type': 'Profile', 'list_type': 'Applicants'})

@user_passes_test(lambda u: u.is_superuser, login_url='/unautharized/')
def display_profile(request, Profile_id):
    try:
      a_profile = Profile.objects.get(id=Profile_id)
      return render(request, 'profile.html', {'display_profile': a_profile})
    except:
        return render(request, 'error.html')

@login_required
def new_profile(request):
    try:
        user = request.user
        a_profile = Profile.objects.get(user=user.id)
        message = "You've already a profile on this site"
        return render(request, 'profile.html', {'display_profile': a_profile, 'message': message})
    except:
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return display_profile(request.POST, post.pk)
            else:
                return render(request, 'error.html')
        else:
            form = ProfileForm()
        return render(request, 'form.html', {'form': form, 'formtype': 'new_profile'})

@user_passes_test(lambda u: u.is_superuser, login_url='/unautharized/')
def del_profile(request, Profile_id):
    instance = Profile.objects.get(id=Profile_id)
    instance.delete()
    return render(request, 'done_successfully.html')

@login_required
def save_profile(request, Profile_id):
    user = request.user
    profile = Profile.objects.get(user= user.id)
    try:
        save_profile = profile.saved_profiles.add(Profile_id)
        return render(request, 'done_successfully.html')
    except:
      return render(request, 'error.html')

@login_required
def unsave_profile(request, Profile_id):
    user = request.user
    profile = Profile.objects.get(user= user.id)
    try:
        unsave_profile = profile.saved_profiles.remove(Profile_id)
        return render(request, 'done_successfully.html')
    except:
      return render(request, 'error.html')

@user_passes_test(lambda u: u.is_superuser, login_url='/unautharized/')
def get_saved_profiles(request):
    user = request.user
    profile = Profile.objects.get(user= user.id)
    saved_profiles = profile.saved_profiles.all()
    return render(request, 'list.html', {'object_list': saved_profiles, 'object_type': 'Profile', 'list_type': 'Saved'})

@login_required
def display_your_profile(request):
    try:
        user = request.user
        a_profile = Profile.objects.get(user=user.id)
        message = "Your profile"
        return render(request, 'profile.html', {'display_profile': a_profile, 'message': message})
    except:
        return render(request, 'error.html')

def  search_jobs(request):
    search = request.POST['search']
    result = Job.objects.filter(title__icontains = search)
    result_list = list(result)
    if not result_list:
        message = "No job contains the word %s" %(search)
        return render(request, 'search_results.html', {'message': message})
    else:
        if search == '':
            message = "Available jobs"
        else:
            message = "Jobs with the word '%s'" %(search)
        try:
            profile = Profile.objects.get(user= user.id)
            user_applied_jobs = profile.jobs_applied.all()
            key_applied = user_applied_jobs.values_list('applied_job__id', flat=True)
            user_saved_jobs = profile.saved_jobs.all()
            key_saved = user_saved_jobs.values_list('saved_jobs__id', flat=True)
            return render(request, 'search_results.html', {'result_list': result_list, 'message': message, 'key_applied': key_applied, 'key_saved': key_saved})
        except:
            return render(request, 'search_results.html', {'result_list': result_list, 'message': message})

def advanced_search(request):
    fields = ['title', 'department', 'job_Description']
    for field in fields:
          field0 = Job.objects.values_list(field)
          field1 = str(field0)
          field2  = field1.split("'")
          n = len(field2)
          if field == 'title':
              titles=[]
              for i in range (0,n):
                  if i % 2 != 0:
                      if field2[i] != '':
                          titles.append(field2[i])
          elif field == 'department':
              departments=[]
              for i in range (0,n):
                  if i % 2 != 0:
                      if field2[i] != '':
                          departments.append(field2[i])
          elif field == 'job_Description':
              job_Descriptions=[]
              for i in range (0,n):
                  if i % 2 != 0:
                      if field2[i] != '':
                          job_Descriptions.append(field2[i])
    return render(request, 'advanced_search.html', {'titles': titles, 'departments': departments, 'job_Descriptions': job_Descriptions})


def advanced_search_process(request):
        title = request.POST['title']
        department = request.POST['department']
        job_Description = request.POST['job_Description']
        min_Qualifications = request.POST['min_Qualifications']
        gender_Required = request.POST['gender_Required']
        starting_Salary = request.POST['starting_Salary']
        daily_Working_Hours = request.POST['daily_Working_Hours']
        weekly_Working_days = request.POST['weekly_Working_days']
        result = Job.objects.filter(title__icontains = title, department__icontains = department, job_Description__icontains = job_Description, min_Qualifications__icontains = min_Qualifications, gender_Required__icontains = gender_Required, starting_Salary__icontains = starting_Salary, daily_Working_Hours__icontains = daily_Working_Hours, weekly_Working_days__icontains = weekly_Working_days)
        result_list = list(result)
        if not result_list:
            message = "No job contains the search criteria you entered"
            return render(request, 'search_results.html', {'message': message})
        else:
            if title == '' and department == '':
                message = "Available jobs"
            else:
                message = "Jobs with the criteria you entered"
            try:
                profile = Profile.objects.get(user= user.id)
                user_applied_jobs = profile.jobs_applied.all()
                key_applied = user_applied_jobs.values_list('applied_job__id', flat=True)
                user_saved_jobs = profile.saved_jobs.all()
                key_saved = user_saved_jobs.values_list('saved_jobs__id', flat=True)
                return render(request, 'search_results.html', {'result_list': result_list, 'message': message, 'key_applied': key_applied, 'key_saved': key_saved})
            except:
                return render(request, 'search_results.html', {'result_list': result_list, 'message': message})
