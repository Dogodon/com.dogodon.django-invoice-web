# # from django.shortcuts import render

# # # Create your views here.


# # ###
# # def home(request, *args, **kwargs):
# #     return render(request, 'base.html')


# from django.shortcuts import render, redirect
# from django.views import View
# from .models import * 
# from django.contrib import messages

# from django.http import HttpResponse
# from django.db import transaction


# import datetime

# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin


# from django.template.loader import get_template

# from django.db import transaction


# from django.utils.translation import gettext as _


# # Create your views here.

# class HomeView(View):
#     """ Main view """

#     templates_name = 'index.html'

#     invoices = Invoice.objects.select_related('customer', 'save_by').all().order_by('-invoice_date_time')

#     context = {
#         'invoices': invoices
#     }

#     def get(self, request, *args, **kwargs):

#         return render(request, self.templates_name, self.context)


#     def post(self, request, *args, **kwargs):

#         return render(request, self.templates_name, self.context)





# class AddCustomerView(View):
#     """ add new customer """

#     template_name = 'add_customer.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):
#         # print(request.POST)
#         data = {
#             'name': request.POST.get('name'),
#             'email': request.POST.get('email'),
#             'phone': request.POST.get('phone'),
#             'address': request.POST.get('address'),
#             'sex': request.POST.get('sex'),
#             'age': request.POST.get ('age'),
#             'city': request.POST.get('city'),
#             'zip_code': request.POST.get('zip'),
#             'save_by': request.user
#         }
#         try:

#             created = Customer.objects.create( ** data)

#             if created:

#                 messages.success(request, "Customer registered successfully.")

#             else:

#                 messages.error(request, "Sorry, please try again the sent data is corrupt.")

#         except Exception as e:
#             messages.error(request, f"Sorry our system is detecting the following issues {e}")
#         return render(request, self.template_name)








# # from django.contrib.auth.mixins import LoginRequiredMixin

# # class AddCustomerView(LoginRequiredMixin, View):
# #     """ Add a new customer """

# #     template_name = 'add_customer.html'

# #     def get(self, request, *args, **kwargs):
# #         return render(request, self.template_name)

# #     def post(self, request, *args, **kwargs):
# #         try:
# #             customer = Customer.objects.create(
# #                 name=request.POST.get('name'),
# #                 email=request.POST.get('email'),
# #                 phone=request.POST.get('phone'),
# #                 address=request.POST.get('address'),
# #                 sex=request.POST.get('sex'),
# #                 age=request.POST.get('age'),
# #                 city=request.POST.get('city'),
# #                 zip=request.POST.get('zip'),
# #                 save_by=request.user  # ✅ S'assure que c'est un User valide
# #             )

# #             messages.success(request, "Customer registered successfully.")
# #             return redirect("customer_list")  # ✅ Redirige vers une page après l'ajout
# #         except Exception as e:
# #             messages.error(request, f"Sorry our system is detecting the following issues: {e}")
# #             return render(request, self.template_name)







# # class AddInvoiceView(View):
# #     """ add new invoice view """

# #     template_name = 'add_invoice.html'

# #     customers = Customer.objects.select_related('save_by').all()

# #     context= {
# #         'customers' : customers
# #     }
    
# #     def get(self, request, *args, ** kwargs):
# #         return render(request, self.template_name, self.context)
    
# #     @transaction.atomic()
# #     def post(self, request, *args, **kwargs):

# #         items = []

# #         try:

# #             customer = request.POST.get('customer')

# #             type = request.POST.get('invoice_type')

# #         #     articles = request.POST.get('article')

# #         #     qties = request.POST.get('qty')

# #         #     units = request.POST.get('unit')

# #         #     total_a = request.POST.get('total-a')

# #         #     total = request.POST.get('total')

# #         #     comment = request.POST.get('comment')

# #         #     invoice_object ={
# #         #         'customer_id' : customer,
# #         #         'save_by' : request.user,
# #         #         'total' : total,
# #         #         'invoice_type' : type,
# #         #         'comments' : comment
# #         #     }
# #         #     invoice = Invoice.objects.create(**invoice_object)

# #         #     for index, article in enumerate(articles):
# #         #         data = Article(
# #         #             invoice_id = invoice.id,
# #         #             name = article,
# #         #             quantity = qties[index],
# #         #             unit_price = units[index],
# #         #             total = total_a[index],
# #         #         )
# #         #         items.append(data)

# #         #     created = Article.objects.bulk_create(items)
# #         #     if created:
# #         #         messages.succes(request,"Data saved successfully.")
# #         #     else:
# #         #         messages.error(request,"Sorry, please try again the sent data is corrupt.")
                
# #         # except Exception as e:
# #         #     messages.error(request, f"Sorry, the following error has occured {e}.")

# #         # return render(request, self.template_name, self.context)



# #         articles = request.POST.getlist('article')  # ✅ getlist() récupère tous les articles envoyés sous forme de liste
# # qties = request.POST.getlist('qty')
# # units = request.POST.getlist('unit')
# # total_a = request.POST.getlist('total-a')

# # if not articles:
# #     messages.error(request, "No articles provided.")
# #     return render(request, self.template_name, self.context)

# # items = []
# # for index, article in enumerate(articles):
# #     try:
# #         data = Article(
# #             invoice_id=invoice.id,
# #             name=article,
# #             quantity=int(qties[index]),
# #             unit_price=float(units[index]),
# #             total=float(total_a[index]),
# #         )
# #         items.append(data)
# #     except (IndexError, ValueError) as e:
# #         messages.error(request, f"Error processing articles: {e}")
# #         return render(request, self.template_name, self.context)

# # created = Article.objects.bulk_create(items)
# #         #     if created:
# #         #         messages.succes(request,"Data saved successfully.")
# #         #     else:
# #         #         messages.error(request,"Sorry, please try again the sent data is corrupt.")
                
# #         # except Exception as e:
# #         #     messages.error(request, f"Sorry, the following error has occured {e}.")

# #         # return render(request, self.template_name, self.context)


# class AddInvoiceView(View):
#     """ Add new invoice view """

#     template_name = 'add_invoice.html'

#     def get(self, request, *args, **kwargs):
#         customers = Customer.objects.select_related('save_by').all()
#         context = {'customers': customers}
#         return render(request, self.template_name, context)

#     @transaction.atomic()
#     def post(self, request, *args, **kwargs):
#         try:
#             customer_id = request.POST.get('customer')
#             invoice_type = request.POST.get('invoice_type')
#             comment = request.POST.get('comment')
#             total = request.POST.get('total')

#             # Vérifier que le client existe
#             customer = Customer.objects.get(id=customer_id)

#             # Créer l'objet facture
#             invoice = Invoice.objects.create(
#                 customer=customer,
#                 save_by=request.user,
#                 total=total,
#                 invoice_type=invoice_type,
#                 comments=comment
#             )

#             # Récupérer les articles
#             articles = request.POST.getlist('article')
#             qties = request.POST.getlist('qty')
#             units = request.POST.getlist('unit')
#             total_a = request.POST.getlist('total-a')

#             if not articles or not qties or not units or not total_a:
#                 messages.error(request, "Veuillez remplir tous les champs des articles.")
#                 return redirect('add-invoice')  # Rediriger pour éviter le rechargement avec des erreurs

#             items = []
#             for index, article in enumerate(articles):
#                 try:
#                     data = Article(
#                         invoice=invoice,
#                         name=article,
#                         quantity=int(qties[index]),
#                         unit_price=float(units[index]),
#                         total=float(total_a[index]),
#                     )
#                     items.append(data)
#                 except (IndexError, ValueError) as e:
#                     messages.error(request, f"Erreur dans les articles : {e}")
#                     return redirect('add-invoice')

#             Article.objects.bulk_create(items)
#             messages.success(request, "Facture et articles enregistrés avec succès.")
#             return redirect('invoice_list')  # Rediriger après l'ajout

#         except Customer.DoesNotExist:
#             messages.error(request, "Le client sélectionné n'existe pas.")
#         except Exception as e:
#             messages.error(request, f"Erreur lors de l'enregistrement : {e}")

#         return redirect('add-invoice')  # Rediriger en cas d'erreur



























from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Customer, Invoice, Article
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View):
    """ Main view """

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        invoices = Invoice.objects.select_related('customer', 'save_by').all().order_by('-invoice_date_time')
        context = {'invoices': invoices}
        return render(request, self.template_name, context)


class AddCustomerView(LoginRequiredMixin, View):
    """ Add a new customer """

    template_name = 'add_customer.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'sex': request.POST.get('sex'),
            'age': request.POST.get('age'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip'),
            'save_by': request.user
        }

        try:
            customer = Customer.objects.create(**data)
            messages.success(request, "Client enregistré avec succès.")
            return redirect('home')  # Redirection après ajout
        except Exception as e:
            messages.error(request, f"Erreur lors de l'enregistrement : {e}")
            return render(request, self.template_name)


# class AddInvoiceView(LoginRequiredMixin, View):
#     """ Add new invoice view """

#     template_name = 'add_invoice.html'

#     def get(self, request, *args, **kwargs):
#         customers = Customer.objects.select_related('save_by').all()
#         context = {'customers': customers}
#         return render(request, self.template_name, context)

#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         print(request.POST)  # Voir les données envoyées par le formulaire

#         try:
#             customer_id = request.POST.get('customer')
#             invoice_type = request.POST.get('invoice_type')
#             comment = request.POST.get('comment')
#             try:
#                 total = float(request.POST.get('total', 0))
#             except ValueError:
#                 messages.error(request, "Le total doit être un nombre valide.")
#                 return redirect('add-invoice')

#             # Vérifier que le client existe
#             customer = get_object_or_404(Customer, id=customer_id)

#             # Créer l'objet facture
#             invoice = Invoice.objects.create(
#                 customer=customer,
#                 save_by=request.user,
#                 total=total,
#                 invoice_type=invoice_type,
#                 comments=comment
#             )

#             # Récupérer les articles
#             articles = request.POST.getlist('article')
#             qties = request.POST.getlist('qty')
#             units = request.POST.getlist('unit')
#             total_a = request.POST.getlist('total-a')

#             if not (len(articles) == len(qties) == len(units) == len(total_a)):
#                 messages.error(request, "Données des articles invalides.")
#                 return redirect('add-invoice')

#             items = []
#             for index, article in enumerate(articles):
#                 try:
#                     data = Article(
#                         invoice_id=invoice.id,
#                         name=article,
#                         quantity=int(qties[index]),
#                         unit_price=float(units[index]),
#                         total=float(total_a[index]),
#                     )
#                     items.append(data)
#                 except (IndexError, ValueError) as e:
#                     messages.error(request, f"Erreur dans les articles : {e}")
#                     return redirect('add-invoice')

#             Article.objects.bulk_create(items)  # Création en masse après vérification
#             messages.success(request, "Facture et articles enregistrés avec succès.")
#             return redirect('home')

#         except Exception as e:
#             messages.error(request, f"Erreur lors de l'enregistrement : {e}")
#             return redirect('add-invoice')






















































from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Invoice, Customer

def register_invoice(request):
    if request.method == 'POST':
        # Récupérer les données envoyées
        customer_id = request.POST.get('customer')
        invoice_type = request.POST.get('invoice_type')
        comments = request.POST.get('comment')
        total = request.POST.get('total')

        # Récupérer les articles et leurs informations
        articles = request.POST.getlist('article[]')
        quantities = request.POST.getlist('qty[]')
        unit_prices = request.POST.getlist('unit[]')
        total_prices = request.POST.getlist('total-a[]')

        # Assurez-vous que toutes les informations sont présentes et valides
        if not all([customer_id, invoice_type, articles, quantities, unit_prices, total_prices]):
            return HttpResponse("Missing required fields", status=400)

        # Créer l'objet facture
        customer = Customer.objects.get(id=customer_id)
        invoice = Invoice.objects.create(
            customer=customer,
            invoice_type=invoice_type,
            total=total,
            comments=comments
        )

        # Créer les articles associés à la facture
        for i in range(len(articles)):
            article = articles[i]
            qty = float(quantities[i])
            unit_price = float(unit_prices[i])
            total_price = float(total_prices[i])

            # Assurez-vous que chaque article a des données valides
            if article and qty > 0 and unit_price > 0:
                invoice.items.create(
                    name=article,
                    quantity=qty,
                    unit_price=unit_price,
                    total=total_price
                )

        return redirect('invoice_success')  # Rediriger vers une page de succès ou de confirmation

    return render(request, 'register_invoice.html', {'customers': Customer.objects.all()})




class AddInvoiceView(View):
    """ add a new invoice view """

    template_name = 'add_invoice.html'

    customers = Customer.objects.select_related('save_by').all()

    context = {
        'customers': customers
    }

    def get(self, request, *args, ** kwargs):
        return render(request, self.template_name, self.context)


    @transaction.atomic()
    def post(self, request, *args, ** kwargs):

        items = []

        try:
            customer = request.POST.get('customer')
            type = request.POST.get('invoice_type')
            articles = request.POST.getlist('article')

            qties = request.POST.getlist('qty')
            units = request.POST.getlist('unit')
            total_a =request.POST.getlist('total-a')
            total = request.POST.get('total')

            comment = request.POST.get('comment')

            invoice_object = {
                'customer_id': customer,
                'save_by': request.user,
                'total': total,
                'invoice_type': type,
                'comments': comment
            }
            invoice = Invoice.objects.create(**invoice_object)
    
            for index, article in enumerate(articles):

                data = Article(
                    invoice_id = invoice.id,
                    name = article,
                    quantity=qties[index],
                    unit_price = units[index],
                    total = total_a[index],
                )
                items.append(data)

            created = Article.objects.bulk_create(items)

            if created:
                # Si tout se passe bien
                messages.success(request, "Data saved successfully.")
                return redirect('home')  # Redirection vers une autre page après la soumission
            else:
                messages.error(request, "Sorry, please try again the sent data is corrupt.")

        except Exception as e:
            messages.error(request, f"Sorry the following error has occured {e}.")

        return render(request, self.template_name, self.context)