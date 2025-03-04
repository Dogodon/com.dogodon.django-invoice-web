from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin




from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Customer, Invoice, Article
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import pagination, get_invoice
import pdfkit
import datetime
from django.template.loader import get_template #recupérer un fichier html
from .decorators import *
from django.utils.translation import gettext as _


class HomeView(LoginRequiredSuperuserMixin, View):
    """ Main view """

    template_name = 'index.html'
            
    invoices = Invoice.objects.select_related('customer', 'save_by').all().order_by('-invoice_date_time')

    context = {'invoices': invoices}

    def get(self, request, *args, **kwargs):

        items =pagination(request,self.invoices)
        self.context['invoices'] = items

        return render(request, self.template_name, self.context)
    

            
    def post(self, request, *args, **kwargs):
            # Vérifier si une modification est demandée
            invoice_id = request.POST.get("id_modified")

            if invoice_id:
                paid = request.POST.get("modified")

                try:
                    obj = get_object_or_404(Invoice, id=invoice_id)
                    obj.paid = True if paid == "True" else False
                    obj.save()
                    messages.success(request, _("Change made successfully."))

                except Exception as e:
                    messages.error(request, _(f"Sorry, an error occurred: {e}"))

            # Appliquer la pagination après modification
            # items = pagination(request, self.invoices)
            # context = {'invoices': items}

            # return render(request, self.template_name, context)



            if request.POST.get("id_supprimer"):
                try:
                    obj = Invoice.objects.get(pk=request.POST.get("id_supprimer"))
                    obj.delete()
                    messages.success(request, _("The deletion was successful."))
                except Exception as e:
                    messages.error(request, _(f"Sorry, the following error has occurred: {e}"))
            
            
            # Appliquer la pagination après modification

            items = pagination(request, self.invoices)
            self.context['invoices'] = items  # Correction de l'affectation (utilisation de "=" au lieu de "-")

            return render(request, self.template_name, self.context)




class AddCustomerView(LoginRequiredSuperuserMixin, View):
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
            messages.success(request, _("Client enregistré avec succès."))
            return redirect('home')  # Redirection après ajout
        except Exception as e:
            messages.error(request, _(f"Erreur lors de l'enregistrement : {e}"))
            return render(request, self.template_name)








class InvoiceVisualizationView(LoginRequiredSuperuserMixin, View):
    """ This view helps to visualize the invoice """

    template_name = 'invoice.html'

    def get(self, request, *args, **kwargs):

        pk=kwargs.get('pk')
        context = get_invoice(pk)

        return render(request, self.template_name, context)



@superuser_required
def get_invoice_pdf(request, *args, **kwargs):
    """ generate pdf file from html file """

    pk = kwargs.get('pk')

    context = get_invoice(pk)

    context['date'] = datetime.datetime.today()

    #get html file
    template = get_template('invoice-pdf.html')

    #render html with  context variables
    html = template.render(context)

    #options of pdf format
    options ={
        'page-size' :'Letter',
        'encoding' : 'UTF-8',
        # 'enable-local-file-acces' : ''
    }
    # options = {
    #     'page-size': 'A4',  # Corrigé: '--page-size' au lieu de '--page_size'
    #     'encoding': 'UTF-8',
    #     'enable-local-file-access': ''
    # }

    # config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    # pdf = pdfkit.from_string(html, False, options=options, configuration=config)


    #generate pdf
    pdf =pdfkit.from_string(html, False, options)
    response=HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = "attachement"
    return response





from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Invoice, Customer

@superuser_required
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
            return HttpResponse(_("Missing required fields"), status=400)

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




class AddInvoiceView(LoginRequiredSuperuserMixin, View):
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
                messages.success(request, _("Data saved successfully."))
                return redirect('home')  # Redirection vers une autre page après la soumission
            else:
                messages.error(request, _("Sorry, please try again the sent data is corrupt."))

        except Exception as e:
            messages.error(request, _(f"Sorry the following error has occured {e}."))

        return render(request, self.template_name, self.context)
    

from django.utils.translation import get_language_info

def my_view(request):
    languages = [
        get_language_info('en'),
        get_language_info('fr'),
        get_language_info('ar'),
    ]
    return render(request, 'home', {'languages': languages})










# import csv
# from django.http import HttpResponse
# from .models import Invoice  # Assurez-vous d'importer votre modèle Invoice
# import csv
# from django.http import HttpResponse
# from .models import Invoice

# def export_invoices_csv(request):
#     # Récupérer toutes les factures, triées par date d'émission décroissante
#     invoices = Invoice.objects.all().order_by('-invoice_date_time')

#     # Créer une réponse HTTP avec le type CSV
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="invoices.csv"'

#     writer = csv.writer(response)
#     # Écrire la ligne d'en-tête avec les champs disponibles
#     writer.writerow([
#         'ID', 'Customer', 'Saved By', 'Invoice Date Time', 
#         'Total', 'Last Updated Date', 'Paid', 'Invoice Type', 'Comments'
#     ])

#     # Écrire les données pour chaque facture
#     for invoice in invoices:
#         writer.writerow([
#             invoice.id,
#             invoice.customer.name,           # Supposons que Customer possède un attribut 'name'
#             invoice.save_by.username,        # Ou utilisez .get_full_name() selon votre modèle User
#             invoice.invoice_date_time,
#             invoice.total,
#             invoice.last_updated_date,
#             invoice.paid,
#             invoice.get_invoice_type_display(),  # Affiche la valeur lisible de l'option invoice_type
#             invoice.comments,
#         ])

#     return response

import csv
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.utils.translation import activate
from .models import Invoice

def export_invoices_csv(request):
    # Détecter la langue depuis la requête (ex: 'fr', 'ar', 'en')
    language = request.GET.get('lang', 'en')  # 'en' par défaut
    activate(language)  # Activer la langue choisie

    # Récupérer toutes les factures
    invoices = Invoice.objects.all().order_by('-invoice_date_time')

    # Créer une réponse HTTP avec type CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename="invoices_{language}.csv"'

    writer = csv.writer(response)

    # Traduire les en-têtes selon la langue choisie
    writer.writerow([
        _('ID'), _('Customer'), _('Saved By'), _('Invoice Date Time'),
        _('Total'), _('Last Updated Date'), _('Paid'), _('Invoice Type'), _('Comments')
    ])

    # Écrire les données en respectant la langue
    for invoice in invoices:
        writer.writerow([
            invoice.id,
            invoice.customer.name if invoice.customer else _('Unknown'),  # Gestion si `customer` est None
            invoice.save_by.get_full_name() if invoice.save_by else _('Unknown'),  # Gestion si `save_by` est None
            invoice.invoice_date_time.strftime('%Y-%m-%d %H:%M:%S') if invoice.invoice_date_time else _('N/A'),
            invoice.total,
            invoice.last_updated_date.strftime('%Y-%m-%d %H:%M:%S') if invoice.last_updated_date else _('N/A'),
            _('Yes') if invoice.paid else _('No'),  # Traduction de "Paid" en "Oui/Non"
            invoice.get_invoice_type_display(),  # Option traduite automatiquement
            invoice.comments if invoice.comments else _('No comments'),
        ])

    return response
