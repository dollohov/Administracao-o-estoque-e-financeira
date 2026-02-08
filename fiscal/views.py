"""
Views do módulo Fiscal.

Este arquivo contém as views para importação de NF-e e gestão de fornecedores.

Autor: Manus AI
Data: 2026-02-05
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Sum, Count
from .models import NotaFiscalEletronica, ItemNotaFiscal, Fornecedor
from .nfe_processor import NFEProcessor


@login_required
def dashboard_fiscal(request):
    """
    Dashboard do módulo fiscal com estatísticas de NF-es importadas.
    """
    # Estatísticas
    total_nfes = NotaFiscalEletronica.objects.count()
    nfes_processadas = NotaFiscalEletronica.objects.filter(status='PROCESSADA').count()
    nfes_pendentes = NotaFiscalEletronica.objects.filter(status='PENDENTE').count()
    nfes_erro = NotaFiscalEletronica.objects.filter(status='ERRO').count()
    
    # Valor total importado
    valor_total = NotaFiscalEletronica.objects.filter(
        status='PROCESSADA'
    ).aggregate(total=Sum('valor_total'))['total'] or 0
    
    # Últimas NF-es importadas
    ultimas_nfes = NotaFiscalEletronica.objects.select_related('fornecedor').order_by('-data_importacao')[:10]
    
    # Fornecedores mais frequentes
    top_fornecedores = Fornecedor.objects.annotate(
        total_nfes=Count('notas_fiscais')
    ).order_by('-total_nfes')[:5]
    
    context = {
        'total_nfes': total_nfes,
        'nfes_processadas': nfes_processadas,
        'nfes_pendentes': nfes_pendentes,
        'nfes_erro': nfes_erro,
        'valor_total': valor_total,
        'ultimas_nfes': ultimas_nfes,
        'top_fornecedores': top_fornecedores,
    }
    
    return render(request, 'fiscal/dashboard.html', context)


@login_required
def importar_nfe(request):
    """
    View para importar arquivo XML de NF-e.
    """
    if request.method == 'POST':
        xml_file = request.FILES.get('xml_file')
        
        if not xml_file:
            messages.error(request, 'Por favor, selecione um arquivo XML.')
            return redirect('fiscal:importar_nfe')
        
        # Verificar extensão do arquivo
        if not xml_file.name.endswith('.xml'):
            messages.error(request, 'O arquivo deve ser um XML (.xml).')
            return redirect('fiscal:importar_nfe')
        
        # Processar o XML
        processor = NFEProcessor(xml_file, request.user)
        sucesso, mensagem, nfe = processor.processar()
        
        if sucesso:
            messages.success(request, mensagem)
            return redirect('fiscal:detalhe_nfe', pk=nfe.pk)
        else:
            messages.error(request, mensagem)
            return redirect('fiscal:importar_nfe')
    
    return render(request, 'fiscal/importar_nfe.html')


@login_required
def lista_nfes(request):
    """
    Lista todas as NF-es importadas.
    """
    nfes = NotaFiscalEletronica.objects.select_related('fornecedor').order_by('-data_emissao')
    
    # Filtros
    status = request.GET.get('status')
    if status:
        nfes = nfes.filter(status=status)
    
    fornecedor_id = request.GET.get('fornecedor')
    if fornecedor_id:
        nfes = nfes.filter(fornecedor_id=fornecedor_id)
    
    # Fornecedores para filtro
    fornecedores = Fornecedor.objects.filter(ativo=True).order_by('razao_social')
    
    context = {
        'nfes': nfes,
        'fornecedores': fornecedores,
        'status_selecionado': status,
        'fornecedor_selecionado': fornecedor_id,
    }
    
    return render(request, 'fiscal/lista_nfes.html', context)


@login_required
def detalhe_nfe(request, pk):
    """
    Exibe detalhes de uma NF-e específica.
    """
    nfe = get_object_or_404(NotaFiscalEletronica, pk=pk)
    itens = nfe.itens.select_related('produto').all()
    
    context = {
        'nfe': nfe,
        'itens': itens,
    }
    
    return render(request, 'fiscal/detalhe_nfe.html', context)


@login_required
def lista_fornecedores(request):
    """
    Lista todos os fornecedores cadastrados.
    """
    fornecedores = Fornecedor.objects.annotate(
        total_nfes=Count('notas_fiscais')
    ).order_by('razao_social')
    
    # Filtro por status
    status = request.GET.get('status')
    if status == 'ativo':
        fornecedores = fornecedores.filter(ativo=True)
    elif status == 'inativo':
        fornecedores = fornecedores.filter(ativo=False)
    
    context = {
        'fornecedores': fornecedores,
        'status_selecionado': status,
    }
    
    return render(request, 'fiscal/lista_fornecedores.html', context)


@login_required
def detalhe_fornecedor(request, pk):
    """
    Exibe detalhes de um fornecedor específico.
    """
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    nfes = fornecedor.notas_fiscais.order_by('-data_emissao')[:20]
    
    # Estatísticas
    total_compras = fornecedor.notas_fiscais.filter(
        status='PROCESSADA'
    ).aggregate(total=Sum('valor_total'))['total'] or 0
    
    total_nfes = fornecedor.notas_fiscais.count()
    
    context = {
        'fornecedor': fornecedor,
        'nfes': nfes,
        'total_compras': total_compras,
        'total_nfes': total_nfes,
    }
    
    return render(request, 'fiscal/detalhe_fornecedor.html', context)

@login_required
@permission_required('estoque.add_produto', raise_exception=True)
def cadastrar_produto_fiscal(request):
    """
    View para cadastrar um novo produto a partir do módulo fiscal.
    """
    from estoque.models import Produto
    
    if request.method == 'POST':
        try:
            # Criar novo produto com dados do formulário
            produto = Produto(
                nome=request.POST.get('nome'),
                descricao=request.POST.get('descricao', ''),
                preco_custo=request.POST.get('preco_custo'),
                preco_venda=request.POST.get('preco_venda'),
                estoque_atual=request.POST.get('estoque_inicial', 0),
                estoque_minimo=request.POST.get('estoque_minimo', 10),
                usuario_criacao=request.user
            )
            produto.save()
            
            # Mensagem de sucesso
            messages.success(
                request,
                f'Produto "{produto.nome}" cadastrado com sucesso via módulo Fiscal!'
            )
            
            return redirect('fiscal:dashboard')
            
        except Exception as e:
            # Mensagem de erro
            messages.error(
                request,
                f'Erro ao cadastrar produto: {str(e)}'
            )
    
    return render(request, 'fiscal/cadastrar_produto.html')
