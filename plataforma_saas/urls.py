from django.contrib import admin
from django.urls import path
from editor.views import landing_page, dashboard, workspace_editor, api_agente_ia, preparar_sitio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing'),
    path('dashboard/', dashboard, name='dashboard'),
    path('preparar-sitio/', preparar_sitio, name='preparar_sitio'),
    path('editor/', workspace_editor, name='editor'),
    path('api/ia/', api_agente_ia, name='api_ia'),
]
