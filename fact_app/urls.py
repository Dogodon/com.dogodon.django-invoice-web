from django.urls import path
from . import views
from .views import export_invoices_csv



urlpatterns = [ 
    path('', views.HomeView.as_view(), name='home'),
    path('add-customer', views.AddCustomerView.as_view(), name='add-customer'),
    path('add-invoice', views.AddInvoiceView.as_view(), name='add-invoice'),
    path('view-invoice/<int:pk>', views.InvoiceVisualizationView.as_view(), name='view-invoice'),
    path('invoice-pdf/<int:pk>', views.get_invoice_pdf, name='invoice-pdf'),








    path('export-csv/', export_invoices_csv, name='export_invoices_csv'),

]
