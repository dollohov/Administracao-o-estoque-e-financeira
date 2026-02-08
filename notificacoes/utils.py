from django.contrib.auth.models import User
from .models import Notificacao


def criar_notificacao(usuario, tipo, titulo, mensagem, prioridade='MEDIA', url_acao=None):
    """
    Função auxiliar para criar notificações no sistema.
    
    Args:
        usuario: Usuário que receberá a notificação
        tipo: Tipo da notificação (ESTOQUE, PEDIDO, FINANCEIRO, SISTEMA, VENDA)
        titulo: Título da notificação
        mensagem: Mensagem detalhada
        prioridade: Prioridade (BAIXA, MEDIA, ALTA, URGENTE)
        url_acao: URL opcional para ação rápida
    
    Returns:
        Notificacao: A notificação criada
    """
    notificacao = Notificacao.objects.create(
        usuario=usuario,
        tipo=tipo,
        titulo=titulo,
        mensagem=mensagem,
        prioridade=prioridade,
        url_acao=url_acao
    )
    return notificacao


def criar_notificacao_para_grupo(grupo, tipo, titulo, mensagem, prioridade='MEDIA', url_acao=None):
    """
    Cria uma notificação para todos os usuários de um grupo.
    
    Args:
        grupo: Grupo Django
        tipo: Tipo da notificação
        titulo: Título
        mensagem: Mensagem
        prioridade: Prioridade
        url_acao: URL opcional
    
    Returns:
        list: Lista de notificações criadas
    """
    usuarios = grupo.user_set.all()
    notificacoes = []
    
    for usuario in usuarios:
        notif = criar_notificacao(usuario, tipo, titulo, mensagem, prioridade, url_acao)
        notificacoes.append(notif)
    
    return notificacoes


def criar_notificacao_para_todos_admins(tipo, titulo, mensagem, prioridade='MEDIA', url_acao=None):
    """
    Cria uma notificação para todos os administradores do sistema.
    
    Args:
        tipo: Tipo da notificação
        titulo: Título
        mensagem: Mensagem
        prioridade: Prioridade
        url_acao: URL opcional
    
    Returns:
        list: Lista de notificações criadas
    """
    admins = User.objects.filter(is_superuser=True)
    notificacoes = []
    
    for admin in admins:
        notif = criar_notificacao(admin, tipo, titulo, mensagem, prioridade, url_acao)
        notificacoes.append(notif)
    
    return notificacoes
