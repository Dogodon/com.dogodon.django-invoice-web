# from django.shortcuts import render

# # Create your views here.


# ###
# def home(request, *args, **kwargs):
#     return render(request, 'base.html')


from django.shortcuts import render, redirect
from django.views import View
from .models import * 
from django.contrib import messages

from django.http import HttpResponse


import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from django.template.loader import get_template

from django.db import transaction


from django.utils.translation import gettext as _


# Create your views here.

class HomeView(View):
    """ Main view """

    templates_name = 'index.html'

    invoices = Invoice.objects.select_related('customer', 'save_by').all().order_by('-invoice_date_time')

    context = {
        'invoices': invoices
    }

    def get(self, request, *args, **kwargs):

        return render(request, self.templates_name, self.context)


    def post(self, request, *args, **kwargs):

        return render(request, self.templates_name, self.context)





class AddCustomerView(View):
    """ add new customer """

    template_name = 'add_customer.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'sex': request.POST.get('sex'),
            'age': request.POST.get ('age'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip'),
            'save_by': request.user
        }
        try:

            created = Customer.objects.create( ** data)

            if created:

                messages.success(request, "Customer registered successfully.")

            else:

                messages.error(request, "Sorry, please try again the sent data is corrupt.")

        except Exception as e:
            messages.error(request, f"Sorry our system is detecting the following issues {e}")
        return render(request, self.template_name)








# from django.contrib.auth.mixins import LoginRequiredMixin

# class AddCustomerView(LoginRequiredMixin, View):
#     """ Add a new customer """

#     template_name = 'add_customer.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):
#         try:
#             customer = Customer.objects.create(
#                 name=request.POST.get('name'),
#                 email=request.POST.get('email'),
#                 phone=request.POST.get('phone'),
#                 address=request.POST.get('address'),
#                 sex=request.POST.get('sex'),
#                 age=request.POST.get('age'),
#                 city=request.POST.get('city'),
#                 zip=request.POST.get('zip'),
#                 save_by=request.user  # ✅ S'assure que c'est un User valide
#             )

#             messages.success(request, "Customer registered successfully.")
#             return redirect("customer_list")  # ✅ Redirige vers une page après l'ajout
#         except Exception as e:
#             messages.error(request, f"Sorry our system is detecting the following issues: {e}")
#             return render(request, self.template_name)







class AddInvoiceView(View):
    """ add new invoice view """

    template_name = 'add_invoice.html'

    customers = Customer.objects.select_related('save_by').all()

    context= {
        'customers' : customers
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

