# contas/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Transacao
from django import forms
from django.db.models import Sum


class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ["descricao", "valor", "categoria", "tipo"]


# View da página inicial
def home(request):
    return render(request, "home.html")


# View da pagina de logout
def logout_view(request):
    logout(request)
    messages.info(request, "Você foi desconectado com sucesso.")
    return redirect("pagina_logout")


def pagina_logout(request):
    return render(request, "logout.html")


# View do registro
def registro(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Conta criada com sucesso! Bem-vindo(a), {username}!")
            return redirect("login")  # Redireciona para login após o cadastro
    else:
        form = UserCreationForm()
    return render(request, "registro.html", {"form": form})


# View protegida do painel
@login_required
def painel(request):
    user = request.user

    # Buscar transação do usuário logado
    transacoes = Transacao.objects.filter(usuario=user).order_by("-data")[:5]

    # Calcular totais
    total_receitas = Transacao.objects.filter(usuario=user, tipo="Receita").aggregate(total=Sum("valor"))["total"] or 0
    total_despesas = Transacao.objects.filter(usuario=user, tipo="Despesa").aggregate(total=Sum("valor"))["total"] or 0
    saldo = total_receitas - total_despesas

    context = {
        "user": user,
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": saldo,
        "transacoes": transacoes,
    }
    return render(request, "painel.html", context)


@login_required
def nova_transacao(request):
    if request.method == "POST":
        form = TransacaoForm(request.POST)
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.usuario = request.user
            transacao.save()
            return redirect("painel")
    else:
        form = TransacaoForm()
    return render(request, "nova_transacao.html", {"form": form})


@login_required
def editar_transacao(request, id):
    transacao = get_object_or_404(Transacao, pk=id, usuario=request.user)

    if request.method == "POST":
        form = TransacaoForm(request.POST, instance=transacao)
        if form.is_valid():
            form.save()
            return redirect("painel")

    else:
        form = TransacaoForm(instance=transacao)

    return render(request, "nova_transacao.html", {"form": form, "transacao": transacao})
