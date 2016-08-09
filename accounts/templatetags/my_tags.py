from django import template

register = template.Library()

@register.simple_tag
def check_user():
    user_id = request.sessions.user_id
    if user_id != "":
        user= user.objects.get(id=user_id)
        user_status = user.is_superuser
        if user_status == True:
            status = "super"
        else:
            status = "ordinary"
    else:
        status  = "super"
    return render_to_response('base.html', {'check_user': status})
