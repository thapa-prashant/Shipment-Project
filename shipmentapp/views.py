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

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
        vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
        user = self.request.user
        return context

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


class SendNotificationView(View):
    def post(self, request, *args, **kwargs):
        try:
            body = request.body
            data = json.loads(body)

            if 'head' not in data or 'body' not in data or 'id' not in data:
                return JsonResponse(status=400, data={"message": "Invalid data format"})

            user_id = data['id']
            user = get_object_or_404(User, pk=user_id)
            payload = {'head': data['head'], 'body': data['body']}
            send_user_notification(user=user, payload=payload, ttl=1000)

            return JsonResponse(status=200, data={"message": "Web push successful"})
        except TypeError:
            return JsonResponse(status=500, data={"message": "An error occurred"})

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
        try:
            resp = requests.post(url=login_api, data=data)
            resp_data = resp.json()
            # print(resp_data)
            if resp_data.get('token'):
                self.request.session['token'] = resp_data.get('token')
            else:
                return render(self.request, self.template_name, {'form': form, 'error': 'Invalid credentials'})
        except:
            return redirect("/")
        return super().form_valid(form)





class PartnerRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
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
        except:
            return redirect("/")
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
        status = self.request.GET.get('status', "all-shipment")
        page_num = self.request.GET.get('page_num', "1")
        context = super().get_context_data(**kwargs)
        context['email'] = self.partner
        shipmentlist_api = "http://127.0.0.1:8000/api/v1/partner/shipment-list/?status=" + status + "&page=" + page_num
        shipments = requests.get(shipmentlist_api, headers=self.headers)
        context['shipments'] = shipments.json()['results']
        context['shipment_type'] = status.upper()
        context['shipment_count'] = len(shipments.json()['results'])
        if shipments.json()['next']:
            context['next'] = shipments.json()['next']
        if shipments.json()['previous']:
            context['previous'] = shipment.json()['previous']
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
        request_shipment_api = "http://127.0.0.1:8000/api/v1/partner/shipment-create/?status"
        data = form.cleaned_data
        data['shipment_status'] = "Order Received"
        data['sender_name'] = self.company
        data['pickup_street_address'] = self.address
        data['contact'] = self.contact
        resp = requests.post(request_shipment_api, headers=self.headers, data=data)
        print(resp.json())
        return super().form_valid(form)