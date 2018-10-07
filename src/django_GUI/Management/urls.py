from django.conf.urls import url, include

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import uploader.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('uploader.urls')),
]

