from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from django.http import HttpResponseRedirect

# Nyelvi redirect nézet
def redirect_to_default_language(request):
    return HttpResponseRedirect(f'/{settings.LANGUAGE_CODE}/')

# Többnyelvű URL-minták
urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('main_kiado.urls')),
)

# Alapértelmezett nyelvre redirect
#urlpatterns += [
   # path('', redirect_to_default_language),
#]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
