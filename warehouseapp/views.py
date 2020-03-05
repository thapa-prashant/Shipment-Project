from django.db.models.functions import Trunc, Extract
from django.urls import reverse, reverse_lazy 
from django.shortcuts import render, redirect
from django.db.models import DateTimeField
from django.views.generic import *
from django.utils import timezone
from .models import *
from .forms import *
import requests
from django.http import JsonResponse
from django.conf import settings
import json

class WareHouseMixin(object):
    pass

class LogisticAdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            # print('dispatch try')
            if request.session.get('token'):
                # print(' dispath try if ------------')
                token = "Token " + request.session.get('token')
                self.headers = {'Authorization': token}
                resp = requests.get('http://127.0.0.1:8000/api/ladmin/logisticadmin-profile/', 
                    headers = self.headers)
                # print(resp.json(), ' dispath try if resp ------------')
                if 'logisticadmin' in resp.json():
                    # print(' dispath try if if resp ------------')
                    self.logisticadmin = resp.json()['logisticadmin']
                    self.id = resp.json()['logisticadmin']['id']
                    self.name = resp.json()['logisticadmin']['name']
                    self.user = resp.json()['logisticadmin']['user']
                    self.warehouse = resp.json()['logisticadmin']['warehouse']
                else:
                    # print(' dispath try if else resp ------------')
                    return redirect(
                        '/warehouse/logistic-admin/login/?error=unauthorized-user-login-attempt')
            else:
                # print(' dispath try else resp ------------')
                return redirect('warehouseapp:warehouseadminlogin')
        except:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['user'] = self.user
        # context['id'] = self.id
        # context['name'] = self.name
        # warehouse = self.warehouse
        pk = self.warehouse
        warehouseapi_url = "http://127.0.0.1:8000/api/ladmin/warehouse/" + str(pk) + "/detail/"
        response = requests.get(warehouseapi_url, headers = self.headers)
        warehouse = response.json()
        user = warehouse['logisticadmin_set']
        user_dict = user[0]
        user_name = user_dict['id']
        print(type(user_dict))
        print(type(user))
        # print(warehouse)
        
        context['warehouse'] = warehouse
        context['user'] = user_dict
        return context


class WareHouseHomeView(LogisticAdminRequiredMixin, TemplateView):
    template_name = "warehousetemplates/warehousehome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # warehouseapi_url = "http://127.0.0.1:8000/api/ladmin/warehouse/information/"
        # pk = self.warehouse
        # warehouseapi_url = "http://127.0.0.1:8000/api/ladmin/warehouse/" + str(pk) + "/detail/"
        # response = requests.get(warehouseapi_url, headers = self.headers)
        # warehouse = response.json()
        # print(warehouse)
        # context['warehouse'] = warehouse
        return context



class WareHouseAdminLoginView(FormView):
    template_name = "warehousetemplates/warehouseadminlogin.html"
    form_class = WareHouseAdminLoginForm
    success_url = reverse_lazy("warehouseapp:warehousehome")

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        loginapi_url = "http://127.0.0.1:8000/api/v1/get-token/"
        data = {
            'username': username,
            'password': password,
        }
        try:
            resp = requests.post(url = loginapi_url, data = data)
            resp_data = resp.json()
            print(resp_data, '\n Form valid try case')
            if resp_data.get('token'):
                self.request.session['token'] = resp_data.get('token')
            else:
                return render(self.request, self.template_name, {
                    'form': form, 
                    'error': "--- Invalid Username or Password ---"
                })
        except:
            return redirect('/')
        return super().form_valid(form)



class WareHouseAdminLogoutView(LogisticAdminRequiredMixin, View):
    def get(self, request):
        del request.session['token']
        return redirect('warehouseapp:warehouseadminlogin')


class WareHouseAdminProfileView(LogisticAdminRequiredMixin, TemplateView):
    template_name = "warehousetemplates/warehouseprofile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context