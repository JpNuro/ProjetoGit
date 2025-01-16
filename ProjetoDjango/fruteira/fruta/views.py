from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from .models import Fruta
from .forms import FrutaForm

def home(request):
    frutas = Fruta.objects.all().order_by('nome')
    return render(request, 'home.html', {'frutas': frutas})

def cadastro_fruta(request):
    if request.method == 'POST':
        form = FrutaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fruta cadastrada com sucesso!')
            return redirect('home')
    else:
        form = FrutaForm()
    return render(request, 'cadastro_fruta.html', {'form': form})

def editar_fruta(request, fruta_id):
    fruta = get_object_or_404(Fruta, id=fruta_id)
    if request.method == 'POST':
        form = FrutaForm(request.POST, instance=fruta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fruta atualizada com sucesso!')
            return redirect('home')
    else:
        form = FrutaForm(instance=fruta)
    return render(request, 'cadastro_fruta.html', {'form': form, 'editing': True})

def excluir_fruta(request, fruta_id):
    fruta = get_object_or_404(Fruta, id=fruta_id)
    fruta.delete()
    messages.success(request, 'Fruta excluída com sucesso!')
    return redirect('home')
