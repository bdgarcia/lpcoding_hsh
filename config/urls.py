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
    path("alta_residencia/", application.views.alta_residencia, name="alta_residencia"),
    path("db/", application.views.db, name="db"),
    path("test/", application.views.test, name="test"),
    path("admin/", admin.site.urls),
    path("auth/", include('django.contrib.auth.urls')),
]
