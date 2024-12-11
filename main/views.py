import json

import redis
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import TemplateView


r = redis.Redis(host='localhost', port=6379, db=0)


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):
        # Вариант 1
        # if request.GET.get('id'):
        #     username = request.GET.get('u')
        #     u_pass = request.GET.get('id')
        #     name = request.GET.get('name')
        #     user = authenticate(username=username, password=u_pass)
        #     if user:
        #         login(request, user)
        #     else:
        #         user = User.objects.create_user(username=username, email=None, password=u_pass, first_name=name)
        #         login(request, user)

        # Вариант 2
        if r.get('data_user'):
            data = json.loads(r.get('data_user'))
            user = authenticate(username=data['u'], password=data['id'])
            if user:
                login(request, user)
            else:
                user = User.objects.create_user(
                    username=data['u'], email=None, password=str(data['id']), first_name=data['name']
                )
                login(request, user)
        return super().get(request, *args, **kwargs)
