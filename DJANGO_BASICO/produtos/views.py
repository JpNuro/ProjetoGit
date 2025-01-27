from django.shortcuts import render
from django.http import HttpResponse
from .models import Pessoa

def ver_produto(request):
    if request.method == 'GET':
        nome = 'Caio'
        return render(request, 'ver_produto.html', {'nome': nome})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')
        return HttpResponse(f'Nome: {nome} <br> Idade: {idade}')

def inserir_produto(request):
    return render(request, 'inserir_produto.html')