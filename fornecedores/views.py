from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from .models import Fornecedor, ContatoFornecedor

@login_required
def lista_fornecedores(request):
    """
    View para listar todos os fornecedores cadastrados.
    
    Permite filtrar fornecedores por nome, email e status (ativo/inativo).
    """
    # Obter parâmetros de filtro da URL
    busca = request.GET.get('busca', '')
    mostrar_inativos = request.GET.get('inativos', 'false') == 'true'
    
    # Iniciar query com todos os fornecedores
    fornecedores = Fornecedor.objects.all()
    
    # Aplicar filtro de busca por nome ou email
    if busca:
        fornecedores = fornecedores.filter(
            Q(nome__icontains=busca) | Q(email__icontains=busca) | Q(cnpj__icontains=busca)
        )
    
    # Aplicar filtro de status
    if not mostrar_inativos:
        fornecedores = fornecedores.filter(ativo=True)
    
    # Ordenar por nome
    fornecedores = fornecedores.order_by('nome').select_related(
        'usuario_criacao', 'usuario_modificacao'
    )
    
    # Preparar contexto
    context = {
        'fornecedores': fornecedores,
        'busca': busca,
        'mostrar_inativos': mostrar_inativos,
    }
    
    return render(request, 'fornecedores/lista_fornecedores.html', context)

@login_required
def novo_fornecedor(request):
    """
    View para criar um novo fornecedor.
    """
    if request.method == 'POST':
        try:
            fornecedor = Fornecedor(
                nome=request.POST.get('nome'),
                email=request.POST.get('email'),
                telefone=request.POST.get('telefone'),
                cnpj=request.POST.get('cnpj'),
                endereco=request.POST.get('endereco'),
                cidade=request.POST.get('cidade'),
                estado=request.POST.get('estado'),
                cep=request.POST.get('cep'),
                usuario_criacao=request.user,
                usuario_modificacao=request.user,
            )
            fornecedor.save()
            messages.success(request, f'Fornecedor "{fornecedor.nome}" criado com sucesso!')
            return redirect('fornecedores:detalhe_fornecedor', pk=fornecedor.id)
        except Exception as e:
            messages.error(request, f'Erro ao criar fornecedor: {str(e)}')
    
    return render(request, 'fornecedores/novo_fornecedor.html')

@login_required
def detalhe_fornecedor(request, pk):
    """
    View para exibir detalhes de um fornecedor específico.
    """
    fornecedor = get_object_or_404(
        Fornecedor.objects.select_related('usuario_criacao', 'usuario_modificacao'),
        pk=pk
    )
    
    # Obter contatos do fornecedor
    contatos = fornecedor.contatos.all()
    
    # Preparar contexto
    context = {
        'fornecedor': fornecedor,
        'contatos': contatos,
    }
    
    return render(request, 'fornecedores/detalhe_fornecedor.html', context)

@login_required
def editar_fornecedor(request, pk):
    """
    View para editar um fornecedor existente.
    """
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    
    if request.method == 'POST':
        try:
            fornecedor.nome = request.POST.get('nome')
            fornecedor.email = request.POST.get('email')
            fornecedor.telefone = request.POST.get('telefone')
            fornecedor.cnpj = request.POST.get('cnpj')
            fornecedor.endereco = request.POST.get('endereco')
            fornecedor.cidade = request.POST.get('cidade')
            fornecedor.estado = request.POST.get('estado')
            fornecedor.cep = request.POST.get('cep')
            fornecedor.usuario_modificacao = request.user
            fornecedor.save()
            messages.success(request, f'Fornecedor "{fornecedor.nome}" atualizado com sucesso!')
            return redirect('fornecedores:detalhe_fornecedor', pk=fornecedor.id)
        except Exception as e:
            messages.error(request, f'Erro ao atualizar fornecedor: {str(e)}')
    
    context = {
        'fornecedor': fornecedor,
    }
    
    return render(request, 'fornecedores/editar_fornecedor.html', context)

@login_required
def excluir_fornecedor(request, pk):
    """
    View para excluir um fornecedor.
    """
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    
    if request.method == 'POST':
        try:
            nome = fornecedor.nome
            fornecedor.delete()
            messages.success(request, f'Fornecedor "{nome}" excluído com sucesso!')
            return redirect('fornecedores:lista_fornecedores')
        except Exception as e:
            messages.error(request, f'Erro ao excluir fornecedor: {str(e)}')
    
    context = {
        'fornecedor': fornecedor,
    }
    
    return render(request, 'fornecedores/excluir_fornecedor.html', context)
