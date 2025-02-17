"""
URL configuration for django_invoice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

###
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('fact_app.urls')),  # Ajoute cette ligne
]





###
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)



# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.i18n import i18n_patterns

# # urlpatterns = [
# #     path('admin/', admin.site.urls),
# #     path('set_language/', include('fact_app.urls')),
# # ]

# # Utilisation de i18n_patterns si nécessaire mais pas dans les inclusions
# if settings.USE_I18N:
#     urlpatterns += i18n_patterns(
#         # Tes URL internationales ici, par exemple :
#         path('set_language/', include('fact_app.urls')),
#     )
