from django.shortcuts import render
from django.http import HttpResponse

def ver_produto(request):
    nome = 'Caio'
    return render(request, 'ver_produto.html', {'nome': nome})

def inserir_produto(request):
    return render(request, 'inserir_produto.html')