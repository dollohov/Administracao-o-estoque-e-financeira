"""
Middleware para rastreamento de acessos e alteracoes no sistema.

Este middleware registra:
- Acessos a dados sensíveis (LGPD)
- Alteracoes em modelos importantes
- Erros de seguranca
"""

import logging
from django.utils.deprecation import MiddlewareMixin
from .models import LogAcessoDadosSensiveis

logger = logging.getLogger('auditoria')


class AuditoriaMiddleware(MiddlewareMixin):
    """
    Middleware para registrar acessos a dados sensíveis.
    """
    
    # Endpoints que acessam dados sensíveis
    ENDPOINTS_SENSIVEIS = {
        '/clientes/': 'DADOS_COMPLETOS',
        '/clientes/detalhe': 'DADOS_COMPLETOS',
        '/api/buscar-cliente': 'DADOS_COMPLETOS',
    }
    
    def process_request(self, request):
        """Registra acessos a dados sensíveis."""
        
        # Ignorar requisicoes de usuarios nao autenticados
        if not request.user.is_authenticated:
            return None
        
        # Verificar se o endpoint acessa dados sensíveis
        for endpoint, tipo_dado in self.ENDPOINTS_SENSIVEIS.items():
            if endpoint in request.path:
                # Extrair ID do cliente da requisicao
                cliente_id = self._extrair_cliente_id(request)
                
                if cliente_id:
                    try:
                        from clientes.models import Cliente
                        cliente = Cliente.objects.get(id=cliente_id)
                        
                        # Registrar acesso
                        LogAcessoDadosSensiveis.objects.create(
                            usuario=request.user,
                            tipo_dado=tipo_dado,
                            cliente_id=cliente.id,
                            cliente_nome=cliente.nome,
                            motivo=self._extrair_motivo(request),
                            endereco_ip=self._extrair_ip(request),
                            user_agent=request.META.get('HTTP_USER_AGENT', '')
                        )
                        
                        logger.info(
                            f'Acesso a dados sensiveis: usuario={request.user.username}, '
                            f'cliente={cliente.nome}, tipo={tipo_dado}, ip={self._extrair_ip(request)}'
                        )
                    except Exception as e:
                        logger.error(f'Erro ao registrar acesso a dados sensiveis: {str(e)}')
        
        return None
    
    def _extrair_cliente_id(self, request):
        """Extrai o ID do cliente da requisicao."""
        # Tentar extrair de parametros GET
        if 'cliente_id' in request.GET:
            return request.GET.get('cliente_id')
        
        # Tentar extrair de parametros POST
        if 'cliente_id' in request.POST:
            return request.POST.get('cliente_id')
        
        # Tentar extrair da URL (ex: /clientes/123/)
        parts = request.path.split('/')
        if len(parts) > 2 and parts[-2].isdigit():
            return parts[-2]
        
        return None
    
    def _extrair_motivo(self, request):
        """Extrai o motivo do acesso da requisicao."""
        # Tentar extrair de parametros
        if 'motivo' in request.GET:
            return request.GET.get('motivo')
        
        if 'motivo' in request.POST:
            return request.POST.get('motivo')
        
        # Usar a view como motivo
        return request.resolver_match.view_name if request.resolver_match else 'Desconhecido'
    
    def _extrair_ip(self, request):
        """Extrai o endereco IP da requisicao."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LogSegurancaMiddleware(MiddlewareMixin):
    """
    Middleware para registrar eventos de seguranca.
    """
    
    def process_response(self, request, response):
        """Registra erros de seguranca e acessos nao autorizados."""
        
        # Registrar acessos nao autorizados (403)
        if response.status_code == 403:
            logger.warning(
                f'Acesso nao autorizado: usuario={request.user.username}, '
                f'path={request.path}, ip={self._extrair_ip(request)}'
            )
        
        # Registrar tentativas de acesso nao autenticado (401)
        if response.status_code == 401:
            logger.warning(
                f'Acesso nao autenticado: path={request.path}, ip={self._extrair_ip(request)}'
            )
        
        return response
    
    def _extrair_ip(self, request):
        """Extrai o endereco IP da requisicao."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
