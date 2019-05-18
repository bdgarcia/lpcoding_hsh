from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import application.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", application.views.index, name="index"),
    #path(r'^detalle_residencia/(?P<id_residencia>\d+)/$', application.views.detalle_residencia, name = "detalle_residencia"),
    path("detalle_residencia/<int:cod>", application.views.detalle_residencia, name= "detalle_residencia"),
    path("alta_residencia/", application.views.alta_residencia, name="alta_residencia"),
    path("residencia/<int:pk>/edit/", application.views.mod_residencia, name="mod_residencia"),
    path("administracion/", application.views.administracion, name="administracion"),
    path("db/", application.views.db, name="db"),
    path("test/", application.views.test, name="test"),
    path("admin/", admin.site.urls),
    path("auth/", include('django.contrib.auth.urls')),
]
