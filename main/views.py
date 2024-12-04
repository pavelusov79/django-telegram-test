from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import TemplateView


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('id'):
            username = request.GET.get('u')
            u_pass = request.GET.get('id')
            name = request.GET.get('name')
            user = authenticate(username=username, password=u_pass)
            if user:
                login(request, user)
            else:
                user = User.objects.create_user(username=username, email=None, password=u_pass, first_name=name)
                login(request, user)
        return super().get(request, *args, **kwargs)
