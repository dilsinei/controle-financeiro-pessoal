# financas_pessoais/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Importe as views padrões de autenticação
from contas import views as contas_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("contas.urls")),
    # URLs de autenticação
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("registro/", contas_views.registro, name="registro"),
    # Painel do usuário
    path("painel/", contas_views.painel, name="painel"),
    # Transações
    path("transacao/nova/", contas_views.nova_transacao, name="nova_transacao"),  # ← Adicione esta linha
    path("transacao/<int:id>/editar/", contas_views.editar_transacao, name="editar_transacao"),
]
