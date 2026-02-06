"""
Processador de XML de NF-e (Nota Fiscal Eletrônica).

Este módulo contém funções para processar arquivos XML de NF-e,
extrair dados e criar registros no banco de dados.

Autor: Manus AI
Data: 2026-02-05
"""

import xml.etree.ElementTree as ET
from decimal import Decimal
from datetime import datetime
from django.core.files.base import ContentFile
from .models import NotaFiscalEletronica, ItemNotaFiscal, Fornecedor
from estoque.models import Produto, MovimentacaoEstoque
from financeiro.models import Despesa, CapitalGiro


class NFEProcessor:
    """
    Classe para processar arquivos XML de NF-e.
    """
    
    # Namespace padrão do XML de NF-e
    NS = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    
    def __init__(self, xml_file, usuario):
        """
        Inicializa o processador.
        
        Args:
            xml_file: Arquivo XML da NF-e
            usuario: Usuário que está importando a NF-e
        """
        self.xml_file = xml_file
        self.usuario = usuario
        self.tree = None
        self.root = None
        self.fornecedor = None
        self.nfe = None
        self.erros = []
    
    def processar(self):
        """
        Processa o arquivo XML e cria os registros no banco.
        
        Returns:
            tuple: (sucesso: bool, mensagem: str, nfe: NotaFiscalEletronica ou None)
        """
        try:
            # Parse do XML
            self.tree = ET.parse(self.xml_file)
            self.root = self.tree.getroot()
            
            # Extrair dados do fornecedor
            fornecedor_data = self._extrair_dados_fornecedor()
            self.fornecedor = self._obter_ou_criar_fornecedor(fornecedor_data)
            
            # Extrair dados da NF-e
            nfe_data = self._extrair_dados_nfe()
            
            # Verificar se a NF-e já foi importada
            chave_acesso = nfe_data['chave_acesso']
            if NotaFiscalEletronica.objects.filter(chave_acesso=chave_acesso).exists():
                return (False, f"NF-e com chave {chave_acesso} já foi importada anteriormente.", None)
            
            # Criar registro da NF-e
            self.nfe = self._criar_nfe(nfe_data)
            
            # Processar itens da NF-e
            itens_data = self._extrair_itens_nfe()
            self._processar_itens(itens_data)
            
            # Atualizar status para processada
            self.nfe.status = 'PROCESSADA'
            self.nfe.save()
            
            # Criar despesa e atualizar capital de giro
            self._registrar_despesa_compra()
            
            return (True, f"NF-e {self.nfe.numero}/{self.nfe.serie} importada com sucesso!", self.nfe)
            
        except ET.ParseError as e:
            return (False, f"Erro ao processar XML: {str(e)}", None)
        except Exception as e:
            if self.nfe:
                self.nfe.status = 'ERRO'
                self.nfe.observacoes = f"Erro: {str(e)}"
                self.nfe.save()
            return (False, f"Erro ao processar NF-e: {str(e)}", None)
    
    def _extrair_dados_fornecedor(self):
        """Extrai dados do fornecedor do XML."""
        # Tentar namespace padrão
        emit = self.root.find('.//nfe:emit', self.NS)
        
        # Se não encontrar, tentar sem namespace
        if emit is None:
            emit = self.root.find('.//emit')
        
        if emit is None:
            raise ValueError("Não foi possível encontrar dados do emitente no XML")
        
        def get_text(element, tag, default=''):
            """Helper para extrair texto de elemento XML."""
            if element is None:
                return default
            elem = element.find(f'nfe:{tag}', self.NS)
            if elem is None:
                elem = element.find(tag)
            return elem.text if elem is not None and elem.text else default
        
        # Extrair endereço
        ender_emit = emit.find('nfe:enderEmit', self.NS)
        if ender_emit is None:
            ender_emit = emit.find('enderEmit')
        
        return {
            'cnpj': get_text(emit, 'CNPJ'),
            'razao_social': get_text(emit, 'xNome'),
            'nome_fantasia': get_text(emit, 'xFant'),
            'inscricao_estadual': get_text(emit, 'IE'),
            'endereco': get_text(ender_emit, 'xLgr') if ender_emit is not None else '',
            'cidade': get_text(ender_emit, 'xMun') if ender_emit is not None else '',
            'estado': get_text(ender_emit, 'UF') if ender_emit is not None else '',
            'cep': get_text(ender_emit, 'CEP') if ender_emit is not None else '',
        }
    
    def _obter_ou_criar_fornecedor(self, data):
        """Obtém ou cria um fornecedor."""
        cnpj = data['cnpj']
        
        # Tentar encontrar fornecedor existente
        fornecedor = Fornecedor.objects.filter(cnpj=cnpj).first()
        
        if fornecedor:
            # Atualizar dados se necessário
            fornecedor.razao_social = data['razao_social'] or fornecedor.razao_social
            fornecedor.nome_fantasia = data['nome_fantasia'] or fornecedor.nome_fantasia
            fornecedor.save()
        else:
            # Criar novo fornecedor
            fornecedor = Fornecedor.objects.create(
                cnpj=cnpj,
                razao_social=data['razao_social'],
                nome_fantasia=data['nome_fantasia'],
                inscricao_estadual=data['inscricao_estadual'],
                endereco=data['endereco'],
                cidade=data['cidade'],
                estado=data['estado'],
                cep=data['cep'],
                usuario_criacao=self.usuario
            )
        
        return fornecedor
    
    def _extrair_dados_nfe(self):
        """Extrai dados principais da NF-e."""
        # Buscar elementos com e sem namespace
        inf_nfe = self.root.find('.//nfe:infNFe', self.NS)
        if inf_nfe is None:
            inf_nfe = self.root.find('.//infNFe')
        
        ide = self.root.find('.//nfe:ide', self.NS)
        if ide is None:
            ide = self.root.find('.//ide')
        
        total = self.root.find('.//nfe:total/nfe:ICMSTot', self.NS)
        if total is None:
            total = self.root.find('.//total/ICMSTot')
        
        if inf_nfe is None or ide is None or total is None:
            raise ValueError("Estrutura do XML inválida")
        
        def get_text(element, tag, default='0.00'):
            """Helper para extrair texto de elemento XML."""
            if element is None:
                return default
            elem = element.find(f'nfe:{tag}', self.NS)
            if elem is None:
                elem = element.find(tag)
            return elem.text if elem is not None and elem.text else default
        
        # Extrair chave de acesso
        chave_acesso = inf_nfe.get('Id', '').replace('NFe', '')
        
        # Extrair data de emissão
        data_emissao_str = get_text(ide, 'dhEmi')
        if not data_emissao_str:
            data_emissao_str = get_text(ide, 'dEmi')
        
        # Converter data
        try:
            if 'T' in data_emissao_str:
                data_emissao = datetime.fromisoformat(data_emissao_str.replace('Z', '+00:00')).date()
            else:
                data_emissao = datetime.strptime(data_emissao_str, '%Y-%m-%d').date()
        except:
            data_emissao = datetime.now().date()
        
        return {
            'chave_acesso': chave_acesso,
            'numero': get_text(ide, 'nNF'),
            'serie': get_text(ide, 'serie', '1'),
            'data_emissao': data_emissao,
            'natureza_operacao': get_text(ide, 'natOp', 'Compra de Mercadorias'),
            'cfop': get_text(ide, 'CFOP', '5102'),
            'valor_produtos': Decimal(get_text(total, 'vProd', '0.00')),
            'valor_total': Decimal(get_text(total, 'vNF', '0.00')),
            'valor_icms': Decimal(get_text(total, 'vICMS', '0.00')),
            'valor_ipi': Decimal(get_text(total, 'vIPI', '0.00')),
            'valor_pis': Decimal(get_text(total, 'vPIS', '0.00')),
            'valor_cofins': Decimal(get_text(total, 'vCOFINS', '0.00')),
            'valor_frete': Decimal(get_text(total, 'vFrete', '0.00')),
            'valor_desconto': Decimal(get_text(total, 'vDesc', '0.00')),
        }
    
    def _criar_nfe(self, data):
        """Cria o registro da NF-e no banco."""
        # Salvar arquivo XML
        self.xml_file.seek(0)
        xml_content = self.xml_file.read()
        
        nfe = NotaFiscalEletronica.objects.create(
            chave_acesso=data['chave_acesso'],
            numero=data['numero'],
            serie=data['serie'],
            fornecedor=self.fornecedor,
            data_emissao=data['data_emissao'],
            valor_total=data['valor_total'],
            valor_produtos=data['valor_produtos'],
            valor_icms=data['valor_icms'],
            valor_ipi=data['valor_ipi'],
            valor_pis=data['valor_pis'],
            valor_cofins=data['valor_cofins'],
            valor_frete=data['valor_frete'],
            valor_desconto=data['valor_desconto'],
            natureza_operacao=data['natureza_operacao'],
            cfop=data['cfop'],
            status='PENDENTE',
            usuario_importacao=self.usuario
        )
        
        # Salvar arquivo XML
        nfe.xml_arquivo.save(
            f'nfe_{data["numero"]}_{data["serie"]}.xml',
            ContentFile(xml_content)
        )
        
        return nfe
    
    def _extrair_itens_nfe(self):
        """Extrai os itens da NF-e."""
        itens = []
        
        # Buscar todos os itens (det)
        det_list = self.root.findall('.//nfe:det', self.NS)
        if not det_list:
            det_list = self.root.findall('.//det')
        
        for det in det_list:
            def get_text(element, tag, default=''):
                """Helper para extrair texto de elemento XML."""
                if element is None:
                    return default
                elem = element.find(f'nfe:{tag}', self.NS)
                if elem is None:
                    elem = element.find(tag)
                return elem.text if elem is not None and elem.text else default
            
            # Produto
            prod = det.find('nfe:prod', self.NS)
            if prod is None:
                prod = det.find('prod')
            
            # Impostos
            imposto = det.find('nfe:imposto', self.NS)
            if imposto is None:
                imposto = det.find('imposto')
            
            icms = None
            ipi = None
            
            if imposto is not None:
                # ICMS pode estar em diferentes tags
                icms_tags = ['ICMS00', 'ICMS10', 'ICMS20', 'ICMS30', 'ICMS40', 'ICMS51', 'ICMS60', 'ICMS70', 'ICMS90']
                for tag in icms_tags:
                    icms = imposto.find(f'.//nfe:{tag}', self.NS)
                    if icms is None:
                        icms = imposto.find(f'.//{tag}')
                    if icms is not None:
                        break
                
                ipi = imposto.find('.//nfe:IPITrib', self.NS)
                if ipi is None:
                    ipi = imposto.find('.//IPITrib')
            
            item_data = {
                'numero_item': int(det.get('nItem', 0)),
                'codigo_produto': get_text(prod, 'cProd'),
                'descricao': get_text(prod, 'xProd'),
                'ncm': get_text(prod, 'NCM'),
                'cfop': get_text(prod, 'CFOP', '5102'),
                'unidade': get_text(prod, 'uCom', 'UN'),
                'quantidade': Decimal(get_text(prod, 'qCom', '1')),
                'valor_unitario': Decimal(get_text(prod, 'vUnCom', '0.00')),
                'valor_total': Decimal(get_text(prod, 'vProd', '0.00')),
                'valor_desconto': Decimal(get_text(prod, 'vDesc', '0.00')),
                'valor_frete': Decimal(get_text(prod, 'vFrete', '0.00')),
                'valor_icms': Decimal(get_text(icms, 'vICMS', '0.00')) if icms is not None else Decimal('0.00'),
                'valor_ipi': Decimal(get_text(ipi, 'vIPI', '0.00')) if ipi is not None else Decimal('0.00'),
                'aliquota_icms': Decimal(get_text(icms, 'pICMS', '0.00')) if icms is not None else Decimal('0.00'),
                'aliquota_ipi': Decimal(get_text(ipi, 'pIPI', '0.00')) if ipi is not None else Decimal('0.00'),
            }
            
            itens.append(item_data)
        
        return itens
    
    def _processar_itens(self, itens_data):
        """Processa os itens da NF-e."""
        for item_data in itens_data:
            # Tentar encontrar produto existente pelo código
            produto = Produto.objects.filter(nome__icontains=item_data['descricao'][:50]).first()
            
            criado_automaticamente = False
            
            if not produto:
                # Criar novo produto automaticamente
                produto = Produto.objects.create(
                    nome=item_data['descricao'][:200],
                    descricao=f"Produto importado da NF-e {self.nfe.numero}/{self.nfe.serie}",
                    preco_custo=item_data['valor_unitario'],
                    preco_venda=item_data['valor_unitario'] * Decimal('1.3'),  # Margem de 30%
                    estoque_atual=0,  # Será atualizado pela movimentação
                    estoque_minimo=10,
                    usuario_criacao=self.usuario
                )
                criado_automaticamente = True
            
            # Criar item da NF-e
            item_nfe = ItemNotaFiscal.objects.create(
                nota_fiscal=self.nfe,
                numero_item=item_data['numero_item'],
                produto=produto,
                codigo_produto=item_data['codigo_produto'],
                descricao=item_data['descricao'],
                ncm=item_data['ncm'],
                cfop=item_data['cfop'],
                unidade=item_data['unidade'],
                quantidade=item_data['quantidade'],
                valor_unitario=item_data['valor_unitario'],
                valor_total=item_data['valor_total'],
                valor_desconto=item_data['valor_desconto'],
                valor_frete=item_data['valor_frete'],
                valor_icms=item_data['valor_icms'],
                valor_ipi=item_data['valor_ipi'],
                aliquota_icms=item_data['aliquota_icms'],
                aliquota_ipi=item_data['aliquota_ipi'],
                criado_automaticamente=criado_automaticamente
            )
            
            # Criar movimentação de estoque (entrada)
            MovimentacaoEstoque.objects.create(
                produto=produto,
                tipo='ENTRADA',
                quantidade=int(item_data['quantidade']),
                valor_unitario=item_data['valor_unitario'],
                observacao=f"Entrada via NF-e {self.nfe.numero}/{self.nfe.serie} - {self.fornecedor}",
                usuario=self.usuario
            )
    
    def _registrar_despesa_compra(self):
        """Registra a despesa da compra e atualiza o capital de giro."""
        # Criar despesa
        Despesa.objects.create(
            descricao=f"Compra NF-e {self.nfe.numero}/{self.nfe.serie} - {self.fornecedor}",
            valor=self.nfe.valor_total,
            data=self.nfe.data_emissao,
            categoria='COMPRA',
            usuario=self.usuario
        )
        
        # Atualizar capital de giro (saída de capital)
        try:
            CapitalGiro.retirar_capital(
                valor=self.nfe.valor_total,
                descricao=f"Compra NF-e {self.nfe.numero}/{self.nfe.serie} - {self.fornecedor}",
                usuario=self.usuario
            )
        except ValueError as e:
            # Se não houver capital suficiente, apenas registrar no log
            self.nfe.observacoes = f"Aviso: {str(e)}"
            self.nfe.save()
