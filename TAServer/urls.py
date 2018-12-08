# This file is copied straight from Rock's provided code under "Skeleton code for Django" in sprint 2

from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from TAServer import views
from TAServer.views import Home
from django.conf.urls import handler404

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  path('', Home.as_view()),
]

handler404 = views.error_404
handler500 = views.error_500