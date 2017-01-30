from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic import RedirectView


urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admini/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^water/", include("water.urls")),
]



urlpatterns += staticfiles_urlpatterns()


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
