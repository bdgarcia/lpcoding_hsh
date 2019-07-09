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
    path("detalle_residencia/<int:cod>", application.views.detalle_residencia, name= "detalle_residencia"),
    path("detalle_residencia/", application.views.detalle_residencia_solo, name= "detalle_residencia_solo"),
    path("listado_usuarios/", application.views.listado_usuarios, name= "listado_usuarios"),
    path("listado_usuarios/<str:modo>", application.views.listado_usuarios_modo, name= "listado_usuarios_modo"),
    path("alta_residencia/", application.views.alta_residencia, name="alta_residencia"),
    path("residencia/<int:pk>/edit/", application.views.mod_residencia, name="mod_residencia"),
    path("residencia/alquilar/", application.views.alquilar_residencia, name="alquilar_residencia"),
    path("administracion/", application.views.administracion, name="administracion"),
    path("usuario/<int:pk>", application.views.detalle_usuario, name="detalle_usuario"),
    path("administracion/configuracion/", application.views.configurar_tarifas, name="configurar_tarifas"),
    path("usuario/crear", application.views.alta_usuario, name="alta_usuario"),
    path("test/", application.views.test, name="test"),
    path("admin/", admin.site.urls),
    path("auth/", include('django.contrib.auth.urls')),
#    path("usuarios/", application.views.listado_usuarios, name="usuarios"),
    path("subastas/", application.views.listado_subastas, name="subastas"),
    path("subastas/cerrar_subasta/", application.views.run_cerrar_subastas, name="cerrar_subastas"),
    path("como_ser_premium/", application.views.faq_premium, name="faq_premium"),
    path("editar_usuario/<int:pk>", application.views.editar_usuario, name="editar_usuario"),
    path("cambiar_contraseña/<int:pk>", application.views.cambiar_contraseña, name="cambiar_contraseña"),
    path("residencia/alquilar/confirmar/", application.views.confirmar_alquiler, name="confirmar_alquiler"),
    path("hotsale/alquilar/", application.views.alquilar_hotsale, name="alquilar_hotsale"),
    path("residencia/hotsale/confirmar/", application.views.confirmar_hotsale, name="confirmar_hotsale"),
    path("residencia/alquiler/<int:pk>/cancelar/", application.views.confirmar_cancelacion_alquiler, name="confirmar_cancelacion_alquiler"),
    path("hotsale/catalogo/", application.views.catalogo_hotsales, name="catalogo_hotsales"),
]

