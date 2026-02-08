from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Q
from datetime import timedelta
from django.utils import timezone
from .models import LogAuditoria, LogAcessoDadosSensiveis, SolicitacaoLGPD


@login_required
@permission_required('auditoria.view_logauditoria', raise_exception=True)
def dashboard_auditoria(request):
    """Dashboard de auditoria com resumo de atividades."""
    
    # Ultimas 7 dias
    data_inicio = timezone.now() - timedelta(days=7)
    
    # Contar acessos por usuario
    acessos_por_usuario = LogAuditoria.objects.filter(
        data_hora__gte=data_inicio
    ).values('usuario__username').annotate(
        total=Count('id')
    ).order_by('-total')[:10]
    
    # Contar acessos a dados sensiveis
    acessos_sensiveis = LogAcessoDadosSensiveis.objects.filter(
        data_hora__gte=data_inicio
    ).count()
    
    # Solicitacoes LGPD pendentes
    solicitacoes_pendentes = SolicitacaoLGPD.objects.filter(
        status='PENDENTE'
    ).count()
    
    # Tipos de acao mais comuns
    acoes_comuns = LogAuditoria.objects.filter(
        data_hora__gte=data_inicio
    ).values('tipo_acao').annotate(
        total=Count('id')
    ).order_by('-total')
    
    context = {
        'acessos_por_usuario': acessos_por_usuario,
        'acessos_sensiveis': acessos_sensiveis,
        'solicitacoes_pendentes': solicitacoes_pendentes,
        'acoes_comuns': acoes_comuns,
    }
    
    return render(request, 'auditoria/dashboard.html', context)


@login_required
@permission_required('auditoria.view_logacessodadossensiveis', raise_exception=True)
def relatorio_acessos_sensiveis(request):
    """Relatorio de acessos a dados sensiveis (LGPD)."""
    
    acessos = LogAcessoDadosSensiveis.objects.all().order_by('-data_hora')
    
    # Filtros
    usuario_id = request.GET.get('usuario')
    cliente_id = request.GET.get('cliente')
    tipo_dado = request.GET.get('tipo_dado')
    
    if usuario_id:
        acessos = acessos.filter(usuario_id=usuario_id)
    
    if cliente_id:
        acessos = acessos.filter(cliente_id=cliente_id)
    
    if tipo_dado:
        acessos = acessos.filter(tipo_dado=tipo_dado)
    
    context = {
        'acessos': acessos[:100],  # Paginar depois
    }
    
    return render(request, 'auditoria/relatorio_acessos_sensiveis.html', context)


@login_required
@permission_required('auditoria.view_solicitacaolgpd', raise_exception=True)
def gerenciar_solicitacoes_lgpd(request):
    """Gerenciar solicitacoes de direitos LGPD."""
    
    solicitacoes = SolicitacaoLGPD.objects.all().order_by('-data_solicitacao')
    
    # Filtrar por status
    status = request.GET.get('status')
    if status:
        solicitacoes = solicitacoes.filter(status=status)
    
    context = {
        'solicitacoes': solicitacoes,
        'status_choices': SolicitacaoLGPD.STATUS_CHOICES,
    }
    
    return render(request, 'auditoria/gerenciar_solicitacoes_lgpd.html', context)
