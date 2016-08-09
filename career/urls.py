from django.conf.urls import url
from . import views, models, forms

urlpatterns = [
    url(r'^$', views.welcome, name='careerwelcome'),
    url(r'^jobs/$', views.object_list, {'model': models.Job}),
    url(r'^jobs/(?P<Job_id>\d+)/$', views.display_job, name='job'),
    url(r'^jobs/(?P<Job_id>\d+)/delete/$', views.del_job, name='delete_job'),
    url(r'^jobs/new/$', views.new_job),
    url(r'^jobs/(?P<Job_id>\d+)/save/$', views.save_job, name='save_the_job'),
    url(r'^jobs/(?P<Job_id>\d+)/unsave/$', views.unsave_job, name='unsave_the_job'),
    url(r'^jobs/(?P<Job_id>\d+)/apply/$', views.apply_job, name='apply_to_the_job'),
    url(r'^jobs/(?P<Job_id>\d+)/cancel_application/$', views.cancel_application_job, name='cancel_application_to_the_job'),
    url(r'^jobs/(?P<Job_id>\d+)/applicants/$', views.get_applicants, name='applicants'),
    url(r'^profiles/$', views.object_list, {'model': models.Profile}),
    url(r'^profiles/(?P<Profile_id>\d+)/$', views.display_profile, name='profile'),
    url(r'^profiles/your_profile/$', views.display_your_profile, name='your_profile'),
    url(r'^profiles/(?P<Profile_id>\d+)/delete/$', views.del_profile, name='delete_profile'),
    url(r'^profiles/new/$', views.new_profile),
    url(r'^profiles/(?P<Profile_id>\d+)/save/$', views.save_profile, name='save_a_profile'),
    url(r'^profiles/(?P<Profile_id>\d+)/unsave/$', views.unsave_profile, name='unsave_a_profile'),
    url(r'^profiles/saved_profiles/$', views.get_saved_profiles, name='saved_profiles'),
    url(r'^profiles/saved_jobs/$', views.get_saved_jobs, name='saved_jobs'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^search/results/$', views.search_jobs, name='search_jobs'),
    url(r'^search/advanced/$', views.advanced_search, name='advanced_search_jobs'),
    url(r'^search/advanced_process/$', views.advanced_search_process, name='advanced_search_jobs_process'),
]
