from django.contrib import auth
from django.contrib.auth.models import User, Permission, Group
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from career.models import Job, Profile
from django.contrib.contenttypes.models import ContentType

# Create your views here.

#Login functions
def login(request):
  args = {}
  args.update(csrf(request))
  return render_to_response('login.html', args)
def auth_view(request):
  username = request.POST['username']
  password = request.POST['password']
  user = auth.authenticate(username=username, password=password)
  if user is not None and user.is_active:
    auth.login(request, user)
    request.session['user_id'] = user.id
    try:
        profile = Profile.objects.get(user=user.id)
        return render(request, 'profile.html', {'display_profile': profile})
    except:
        return HttpResponseRedirect('/profiles/new/')
    #return HttpResponseRedirect("/accounts/loggedin/")
  else:
    return HttpResponseRedirect("/accounts/invalid/")
def loggedin(request):
  return render(request, 'registration/loggedin.html', {'full_name': request.user.username})
#Logout functions
def logout(request):
  auth.logout(request)
  del request.session['user_id']
  return render(request, 'logged_out.html')
#registration functions
def register(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect("/profiles/new/")
    else:
      return HttpResponseRedirect("/error/")
  args = {}
  args.update(csrf(request))
  args['form'] = UserCreationForm()
  return render_to_response('register.html', args)
def register_success(request):
  return render(request, 'register_success.html')


#
#def check_user():
#    user_id = request.sessions.user_id
#    if user_id != "":
#        user= user.objects.get(id=user_id)
#        user_status = user.is_superuser
#        if user_status == True:
#            status = "super"
#        else:
#            status = "ordinary"
#    else:
#        status  = "anonymous"
#    return render_to_response('base.html', {'check_user': status})
#def check_username(check_user):
#    username = request.check_user.username
#    return render_to_response('base.html', {'check_username': username})
