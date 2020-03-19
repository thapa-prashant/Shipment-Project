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
import urllib.parse as urlparse
from urllib.parse import parse_qs



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
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        login_api = "http://127.0.0.1:8000/api/v1/get-token/"
        data = {
            'username': email,
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


class RegistrationView(FormView):
    template_name = "registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('shipmentapp:dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
<<<<<<< HEAD
        citilist_api = "http://127.0.0.1:8000/api/v1/city-list/"
=======
        citilist_api = "http://127.0.0.1:8000/api/v1/partner/city-list/"
>>>>>>> e97af24cd223d838ffa2e5ad5d2b2036e37a4ad7
        resp = requests.get(citilist_api)
        cities = resp.json()
        kwargs['cities'] = cities
        return kwargs

    def form_valid(self, form):
        registration_api = "http://127.0.0.1:8000/api/v1/user-registration/"
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        partner_full_name = form.cleaned_data["partner_full_name"]
        partner_company = form.cleaned_data["partner_company"]
        contact = form.cleaned_data["contact"]
        address = form.cleaned_data["address"]
<<<<<<< HEAD
        city = form.cleaned_data["city"]
=======
        city = form.cleaned_data['city']
>>>>>>> e97af24cd223d838ffa2e5ad5d2b2036e37a4ad7
        data = {'email':email,
                'password':password,
                'partner_full_name':partner_full_name,
                'contact':contact,
                'city':city,
                'address':address,
                'partner_company':partner_company,
                'city':city
                }

        resp = requests.post(registration_api,data=data)
        # print(resp.json())
        if resp.json().get('fail'):
            return render(self.request,self.template_name,{'form':form,'error':"Email you've entered already exists."})
        return super().form_valid(form)


class PartnerRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            if request.session.get('token'):
                token = "Token " + request.session.get('token')
                self.headers = {'Authorization': token}
                resp = requests.get('http://127.0.0.1:8000/api/v1/user-profile/', headers=self.headers)
                if 'partner' in resp.json():
                    self.partner = resp.json()['partner']
                    self.id = resp.json()['partner']['id']
                    self.email = resp.json()['partner']['email']
                    self.company = resp.json()['partner']['partner_company']
                    self.address = resp.json()['partner']['address']
                    self.contact = resp.json()['partner']['contact']
                    self.partner_full_name = resp.json()['partner']['partner_full_name']
                else:
                    return redirect('/login/?err=err')
            else:
                return redirect('shipmentapp:login')
        except:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.email
        context['id'] = self.id
        context['name'] = self.partner_full_name
        return context


class UserUpdateView(PartnerRequiredMixin,FormView):
    template_name = 'userupdate.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('shipmentapp:dashboard')
    # def get_success_url(self):
    #     return  reverse('shipmentapp:userupdate',kwargs={'pk':self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance= self.request.user
        posts = {
            'partner_company': self.partner['partner_company'],
            'partner_full_name':self.partner['partner_full_name'],
            'contact':self.contact,
            'address':self.address,
            'alt_contact': self.partner['alt_contact'],
            'website': self.partner['website'],
            'description': self.partner['description'],
        }

        context['form'] = ProfileEditForm(initial=posts)
        return context

    def form_valid(self,form):
        partner_full_name = form.cleaned_data["partner_full_name"]
        partner_company = form.cleaned_data["partner_company"]
        contact = form.cleaned_data["contact"]
        address = form.cleaned_data["address"]
        alt_contact = form.cleaned_data["alt_contact"]
        website = form.cleaned_data["website"]
        description = form.cleaned_data["description"]
        data = {
                'partner_full_name': partner_full_name,
                'contact': contact,
                'address': address,
                'partner_company': partner_company,
                'alt_contact': alt_contact,
                'website':website,
                'description': description

             }

        response = requests.put("http://127.0.0.1:8000/api/v1/update/" + str(self.id) + "/",data=data,headers=self.headers)
        return super().form_valid(form)


class LogoutView(PartnerRequiredMixin, View):
    def get(self, request):
        del request.session['token']
        return redirect('shipmentapp:home')


class AllShipmentsView(PartnerRequiredMixin, TemplateView):
    template_name = "allshipments.html"

    def get_context_data(self, **kwargs):
        status = self.request.GET.get('status', "all-shipment")
        try:
            page_num = self.request.GET.get('page', "1")
        except:
            page_num = 1
        # print(page_num)
        context = super().get_context_data(**kwargs)
        context['email'] = self.email
        shipmentlist_api = "http://127.0.0.1:8000/api/v1/partner/shipment-list/?page=" + page_num + "&status=" + status
        shipments = requests.get(shipmentlist_api, headers=self.headers)
        context['shipments'] = shipments.json()['results']
        print(shipments.json()['results'])
        context['shipment_type'] = status.upper()
        context['status'] = status
        context['shipment_count'] = len(shipments.json()['results'])

        ## Pagination
        ## Retrieve current Page
        current = self.request.get_full_path()
        currentpage_parsed = urlparse.urlparse(current)
        try:
            current_page = parse_qs(currentpage_parsed.query)['page'][0]
        except:
            current_page = 1

        try:
            current_status = parse_qs(currentpage_parsed.query)['status'][0]
        except:
            current_status = 'all-shipments'


        context['current_page'] = current_page
        context['s_status'] = current_status

        # print(self.request.get_full_path())

        ## Next Page
        if shipments.json()['next']:
            context['next'] = shipments.json()['next']
            next_page_link = shipments.json()['next']
            # print(next_page_link)
            parsed = urlparse.urlparse(next_page_link)
            next_p = parse_qs(parsed.query)['page'][0]
            # print(next_p)
            context['nextpage'] = next_p
            context['nextpage'] = next_p

        ##Previous Page
        if shipments.json()['previous']:
            context['previous'] = shipments.json()['previous']
            # print(shipments.json()['previous'])

            prev_page_link = shipments.json()['previous']
            # print(prev_page_link)
            parsed = urlparse.urlparse(prev_page_link)

            # print(parse_qs(parsed.query))

            if 'page' not in parse_qs(parsed.query):
                context ['prevpage'] = "1"
            else:
                prev_p = parse_qs(parsed.query)['page'][0]
                context['prevpage'] = prev_p

        return context


class ShipmentDetailView(PartnerRequiredMixin,TemplateView):
    template_name = 'shipmentdetail.html'

    def get_context_data(self, **kwargs):
        self.id = self.kwargs['pk']
        shipmentdetail_api = 'http://127.0.0.1:8000/api/v1/partner/shipment-' + str(self.id) +'/detail/'
        resp = requests.get(shipmentdetail_api,headers= self.headers)
        context = super().get_context_data(**kwargs)
        context['shipment'] = resp.json()
        context['activity_set'] = resp.json()['shipmentactivity_set']
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
        return super().form_valid(form)


class PasswordChangeView(PartnerRequiredMixin,FormView):
    template_name = 'passwordchange.html'
    form_class = PasswordUpdateForm
    success_url = reverse_lazy('shipmentapp:dashboard')

    def form_valid(self, form):
        old_password = form.cleaned_data['old_password']
        new_password = form.cleaned_data['new_password']
        data = {
            'old_password': old_password,
            'new_password': new_password,
        }
        response = requests.put("http://127.0.0.1:8000/api/v1/user/changepassword/", data=data,
                                headers=self.headers)
        if response.json().get('error'):
            return render(self.request,self.template_name,{'form':form,'error':'Old password is incorrect.'})
        return super().form_valid(form)


class ReportView(PartnerRequiredMixin,TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        report_api = "http://127.0.0.1:8000/api/v1/reports/"
        resp = requests.get(report_api, headers= self.headers)
        context = super().get_context_data(**kwargs)
        context['header'] = self.headers
        context['chc'] = resp.json()['total_chc']
        context['rhc'] = resp.json()['total_rhc']
        context['sc'] = resp.json()['total_sc']
        return context


class Demoview(TemplateView):
    template_name = 'barcode.html'