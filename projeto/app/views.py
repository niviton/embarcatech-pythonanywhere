from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Reservatorio

# Variável global para armazenar o estado da irrigação
estado_irrigacao = {'ligado': False}

def home(request):
    reservatorio = Reservatorio.objects.latest('id')

    contexto = {
        "data_hora": reservatorio.data_hora,
        "capacidade_total": reservatorio.capacidade_total,
        "litros_restantes": reservatorio.litros_restantes,
        "porcentagem_agua": reservatorio.porcentagem_agua,
        "umidade": reservatorio.umidade,
        "distancia_agua": reservatorio.distancia_agua,
        "vazao_agua": reservatorio.vazao_agua,
        "irrigacoes_restantes": reservatorio.irrigacoes_restantes,
        "estado": reservatorio.estado
    }

    return render(request, "home.html", contexto)

@csrf_exempt
def reservatorio(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        capacidade_total = data.get('capacidade_total')
        litros_restantes = data.get('litros_restantes')
        porcentagem_agua = data.get('porcentagem_agua')
        umidade = data.get('umidade')
        distancia_agua = data.get('distancia_agua')
        vazao_agua = data.get('vazao_agua')
        irrigacoes_restantes = data.get('irrigacoes_restantes')
        estado = data.get('estado')

        # Salva os dados no banco de dados
        reservatorio = Reservatorio(
            capacidade_total=capacidade_total,
            litros_restantes=litros_restantes,
            porcentagem_agua=porcentagem_agua,
            umidade=umidade,
            distancia_agua=distancia_agua,
            vazao_agua=vazao_agua,
            irrigacoes_restantes=irrigacoes_restantes,
            estado=estado
        )
        reservatorio.save()

        return JsonResponse({'message': 'Reservatório criado com sucesso!'}, status=201)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)

# Função para controlar o estado da irrigação (ligar/desligar)
@csrf_exempt
def controle_irrigacao(request):
    global estado_irrigacao

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            acao = data.get('acao')  # "ligar" ou "desligar"

            if acao == "ligar":
                estado_irrigacao['ligado'] = True
            elif acao == "desligar":
                estado_irrigacao['ligado'] = False

            return JsonResponse({'status': 'ok', 'estado': estado_irrigacao['ligado']})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'erro', 'mensagem': 'JSON inválido'}, status=400)
    return JsonResponse({'status': 'erro', 'mensagem': 'Método inválido'}, status=400)

# Função para verificar o estado da irrigação
def status_irrigacao(request):
    return JsonResponse({'estado': estado_irrigacao['ligado']})
