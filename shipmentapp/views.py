from django.db.models.functions import Trunc, Extract
from django.urls import reverse, reverse_lazy 
from django.shortcuts import render, redirect
from django.db.models import DateTimeField
from django.views.generic import *
from django.utils import timezone
from .models import *
from .forms import *
import requests

class HomeView(TemplateView):
    template_name = "home.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     now = timezone.localtime(timezone.now())
    #     print(now)
    #     articles = Article.objects.annotate(start_time=Trunc('featured_starting', 'second', output_field=DateTimeField()))

    #     for art in articles:
    #         if art.start_time < now:
    #             print(art.title, "already started")
    #         else:
    #             print(art.title, "yet to start")
    #     context['articles'] = articles.filter(start_time__lt=now)
    #     context['now'] = now
        
    #     return context


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy('shipmentapp:dashboard')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_api = "http://127.0.0.1:8000/api/v1/get-token/"
        data = {
            'username': username,
            'password': password
        }
        resp = requests.post(url=login_api, data=data)
        resp_data = resp.json()
        # print(resp_data)
        if resp_data.get('token'):
            self.request.session['token'] = resp_data.get('token')
        else:
            return render(self.request, self.template_name, {'form': form, 'error': 'Invalid credentials'})
        return super().form_valid(form)





class PartnerRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('token'):
            token = "Token " + request.session.get('token')
            self.headers = {'Authorization': token}
            resp = requests.get('http://127.0.0.1:8000/api/v1/user-profile/', headers=self.headers)
            if 'partner' in resp.json():
                self.partner = resp.json()['partner']['email']
                self.company = resp.json()['partner']['partner_company']
                self.address = resp.json()['partner']['address']
                self.contact = resp.json()['partner']['contact']
            else:
                return redirect('/login/?err=err')
        else:
            return redirect('shipmentapp:login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.partner

        return context


class LogoutView(PartnerRequiredMixin, View):
    def get(self, request):
        del request.session['token']
        return redirect('shipmentapp:home')


class DashboardView(PartnerRequiredMixin, TemplateView):
    template_name = "dashboard.html"


class AllShipmentsView(PartnerRequiredMixin, TemplateView):
    template_name = "allshipments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.partner
        shipmentlist_api = "http://127.0.0.1:8000/api/v1/partner/shipment-list/"
        shipments = requests.get(shipmentlist_api, headers=self.headers)
        context['shipments'] = shipments.json()['results']
        return context


class RequestShipmentView(PartnerRequiredMixin, FormView):
    template_name = "requestshipment.html"
    form_class = ShipmentForm
    success_url = reverse_lazy('shipmentapp:allshipments')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        citilist_api = "http://127.0.0.1:8000/api/v1/partner/city-list/"
        resp = requests.get(citilist_api, headers=self.headers)
        cities = resp.json()
        kwargs['cities'] = cities
        return kwargs

    def form_valid(self, form):
        request_shipment_api = "http://127.0.0.1:8000/api/v1/partner/shipment-create/"
        data = form.cleaned_data
        data['shipment_status'] = "Order Received"
        data['sender_name'] = self.company
        data['pickup_street_address'] = self.address
        data['contact'] = self.contact
        resp = requests.post(request_shipment_api, headers=self.headers, data=data)
        print(resp.json())
        return super().form_valid(form)