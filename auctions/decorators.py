from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

#decoration that will be used to redirect already logged in users if they try to access registration/login page
def redirect_authenticated_user(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view