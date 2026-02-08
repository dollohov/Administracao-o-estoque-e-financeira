from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Notificacao


@login_required
def lista_notificacoes(request):
    """Exibe a lista de notificações do usuário."""
    notificacoes = Notificacao.objects.filter(usuario=request.user)
    
    # Filtrar por tipo se fornecido
    tipo = request.GET.get('tipo')
    if tipo:
        notificacoes = notificacoes.filter(tipo=tipo)
    
    # Filtrar por leitura se fornecido
    lidas = request.GET.get('lidas')
    if lidas == 'true':
        notificacoes = notificacoes.filter(lida=True)
    elif lidas == 'false':
        notificacoes = notificacoes.filter(lida=False)
    
    context = {
        'notificacoes': notificacoes,
        'total_nao_lidas': Notificacao.objects.filter(usuario=request.user, lida=False).count(),
        'page_title': 'Notificações'
    }
    return render(request, 'notificacoes/lista.html', context)


@login_required
@require_POST
def marcar_como_lida(request, pk):
    """Marca uma notificação como lida."""
    notificacao = get_object_or_404(Notificacao, pk=pk, usuario=request.user)
    notificacao.marcar_como_lida()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    return redirect(request.META.get('HTTP_REFERER', 'notificacoes:lista'))


@login_required
@require_POST
def marcar_todas_lidas(request):
    """Marca todas as notificações do usuário como lidas."""
    notificacoes = Notificacao.objects.filter(usuario=request.user, lida=False)
    for notificacao in notificacoes:
        notificacao.marcar_como_lida()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'count': notificacoes.count()})
    
    return redirect(request.META.get('HTTP_REFERER', 'notificacoes:lista'))


@login_required
def api_notificacoes_nao_lidas(request):
    """API que retorna as notificações não lidas do usuário em JSON."""
    notificacoes = Notificacao.objects.filter(usuario=request.user, lida=False).values(
        'id', 'titulo', 'mensagem', 'tipo', 'prioridade', 'url_acao', 'data_criacao'
    )
    
    return JsonResponse({
        'count': notificacoes.count(),
        'notificacoes': list(notificacoes)
    })
