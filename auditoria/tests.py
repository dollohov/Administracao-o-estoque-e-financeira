from django.test import TestCase
from django.contrib.auth.models import User
from .models import LogAuditoria, LogAcessoDadosSensiveis, SolicitacaoLGPD


class LogAuditoriaTestCase(TestCase):
    """Testes para o modelo LogAuditoria."""
    
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_criar_log_auditoria(self):
        """Testa a criacao de um log de auditoria."""
        # Este teste seria implementado com dados reais
        pass


class SolicitacaoLGPDTestCase(TestCase):
    """Testes para o modelo SolicitacaoLGPD."""
    
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_marcar_concluida(self):
        """Testa a marcacao de solicitacao como concluida."""
        solicitacao = SolicitacaoLGPD.objects.create(
            cliente_id=1,
            cliente_nome='Cliente Teste',
            tipo_solicitacao='ACESSO',
            descricao='Solicitacao de acesso aos dados'
        )
        
        solicitacao.marcar_concluida(self.usuario, 'Dados enviados por email')
        
        self.assertEqual(solicitacao.status, 'CONCLUIDA')
        self.assertIsNotNone(solicitacao.data_conclusao)
        self.assertEqual(solicitacao.usuario_responsavel, self.usuario)
