# Documentação do Jogo de Bingo

## Visão Geral
Este documento explica em detalhes o funcionamento do jogo de Bingo implementado em Python usando a biblioteca Tkinter para interface gráfica.

## Estrutura do Código

### 1. Importações
```python
import tkinter as tk
from tkinter import messagebox
import random
import os
```
- `tkinter`: Biblioteca principal para criar a interface gráfica
- `messagebox`: Módulo para exibir mensagens em janelas pop-up
- `random`: Usado para gerar números aleatórios
- `os`: Utilizado para operações do sistema operacional

### 2. Classe Principal: CartelaBingo

#### 2.1 Inicialização (`__init__`)
- Cria a janela principal do jogo
- Configura o título "Bingo Game - SENAC"
- Organiza a interface em frames (áreas) distintas:
  - Frame do logo/título
  - Frame principal
  - Frame da cartela
  - Frame dos controles

#### 2.2 Variáveis Principais
- `numeros_sorteados`: Lista que armazena todos os números já sorteados
- `labels_numeros`: Dicionário que mantém referência aos labels dos números na cartela
- `numeros_cartela`: Dicionário que controla quais números foram marcados

### 3. Componentes Principais

#### 3.1 Título (`criar_titulo`)
- Cria um título estilizado "BINGO SENAC"
- Usa fonte Helvetica, tamanho 24, em negrito
- Cor azul para destaque

#### 3.2 Cartela (`criar_cartela`)
- Gera uma cartela 5x5 com números aleatórios
- Distribuição dos números por coluna:
  - B: 1-15
  - I: 16-30
  - N: 31-45
  - G: 46-60
  - O: 61-75
- Espaço central marcado como "LIVRE"
- Cada número é exibido em um label com borda e fundo branco

#### 3.3 Controles (`criar_controles`)
- Botão "Sortear Número"
- Display do último número sorteado
- Lista de todos os números já sorteados
- Interface organizada verticalmente

### 4. Funcionalidades do Jogo

#### 4.1 Sorteio de Números (`sortear_numero`)
- Verifica se ainda existem números disponíveis
- Sorteia um número aleatório dentre os disponíveis
- Atualiza a interface:
  - Mostra o último número sorteado
  - Adiciona à lista de números sorteados
  - Marca o número na cartela (se presente)
- Verifica condição de vitória após cada sorteio

#### 4.2 Verificação de Vitória (`verificar_vitoria`)
- Verifica se todos os números da cartela foram marcados
- Exibe mensagem de parabéns quando o jogador vence
- Desabilita o botão de sorteio após a vitória

### 5. Interface Gráfica
- Design limpo e organizado
- Feedback visual através de cores:
  - Números marcados ficam verdes
  - Botão de sorteio em azul claro
- Tamanhos de fonte adequados para boa legibilidade
- Espaçamento apropriado entre elementos

### 6. Como Jogar
1. Execute o programa
2. Uma cartela será gerada automaticamente
3. Clique no botão "Sortear Número" para sortear números
4. Os números sorteados serão marcados automaticamente na sua cartela
5. Continue até completar toda a cartela
6. O jogo termina quando você completa a cartela ou quando todos os números foram sorteados

### 7. Requisitos do Sistema
- Python 3.x
- Biblioteca Tkinter (geralmente já vem com Python)
- Sistema operacional com interface gráfica

### 8. Possíveis Melhorias Futuras
1. Adicionar diferentes padrões de vitória (linha, coluna, diagonal)
2. Implementar múltiplas cartelas
3. Adicionar efeitos sonoros
4. Incluir um sistema de pontuação
5. Adicionar um temporizador entre sorteios
6. Implementar salvamento do estado do jogo
7. Adicionar modo multiplayer
