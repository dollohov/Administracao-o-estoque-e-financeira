from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from .models import Cliente, ContatoCliente

@login_required
def lista_clientes(request):
    """
    View para listar todos os clientes cadastrados.
    
    Permite filtrar clientes por nome, email e status (ativo/inativo).
    """
    # Obter parâmetros de filtro da URL
    busca = request.GET.get('busca', '')
    mostrar_inativos = request.GET.get('inativos', 'false') == 'true'
    
    # Iniciar query com todos os clientes
    clientes = Cliente.objects.all()
    
    # Aplicar filtro de busca por nome ou email
    if busca:
        clientes = clientes.filter(
            Q(nome__icontains=busca) | Q(email__icontains=busca) | Q(cpf_cnpj__icontains=busca)
        )
    
    # Aplicar filtro de status
    if not mostrar_inativos:
        clientes = clientes.filter(ativo=True)
    
    # Ordenar por nome
    clientes = clientes.order_by('nome').select_related(
        'usuario_criacao', 'usuario_modificacao'
    )
    
    # Preparar contexto
    context = {
        'clientes': clientes,
        'busca': busca,
        'mostrar_inativos': mostrar_inativos,
    }
    
    return render(request, 'clientes/lista_clientes.html', context)

@login_required
def novo_cliente(request):
    """
    View para criar um novo cliente.
    """
    if request.method == 'POST':
        try:
            cliente = Cliente(
                nome=request.POST.get('nome'),
                email=request.POST.get('email'),
                telefone=request.POST.get('telefone'),
                cpf_cnpj=request.POST.get('cpf_cnpj'),
                endereco=request.POST.get('endereco'),
                cidade=request.POST.get('cidade'),
                estado=request.POST.get('estado'),
                cep=request.POST.get('cep'),
                usuario_criacao=request.user,
                usuario_modificacao=request.user,
            )
            cliente.save()
            messages.success(request, f'Cliente "{cliente.nome}" criado com sucesso!')
            return redirect('clientes:detalhe_cliente', pk=cliente.id)
        except Exception as e:
            messages.error(request, f'Erro ao criar cliente: {str(e)}')
    
    return render(request, 'clientes/novo_cliente.html')

@login_required
def detalhe_cliente(request, pk):
    """
    View para exibir detalhes de um cliente específico.
    """
    cliente = get_object_or_404(
        Cliente.objects.select_related('usuario_criacao', 'usuario_modificacao'),
        pk=pk
    )
    
    # Obter contatos do cliente
    contatos = cliente.contatos.all()
    
    # Preparar contexto
    context = {
        'cliente': cliente,
        'contatos': contatos,
    }
    
    return render(request, 'clientes/detalhe_cliente.html', context)

@login_required
def editar_cliente(request, pk):
    """
    View para editar um cliente existente.
    """
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        try:
            cliente.nome = request.POST.get('nome')
            cliente.email = request.POST.get('email')
            cliente.telefone = request.POST.get('telefone')
            cliente.cpf_cnpj = request.POST.get('cpf_cnpj')
            cliente.endereco = request.POST.get('endereco')
            cliente.cidade = request.POST.get('cidade')
            cliente.estado = request.POST.get('estado')
            cliente.cep = request.POST.get('cep')
            cliente.usuario_modificacao = request.user
            cliente.save()
            messages.success(request, f'Cliente "{cliente.nome}" atualizado com sucesso!')
            return redirect('clientes:detalhe_cliente', pk=cliente.id)
        except Exception as e:
            messages.error(request, f'Erro ao atualizar cliente: {str(e)}')
    
    context = {
        'cliente': cliente,
    }
    
    return render(request, 'clientes/editar_cliente.html', context)

@login_required
def excluir_cliente(request, pk):
    """
    View para excluir um cliente.
    """
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        try:
            nome = cliente.nome
            cliente.delete()
            messages.success(request, f'Cliente "{nome}" excluído com sucesso!')
            return redirect('clientes:lista_clientes')
        except Exception as e:
            messages.error(request, f'Erro ao excluir cliente: {str(e)}')
    
    context = {
        'cliente': cliente,
    }
    
    return render(request, 'clientes/excluir_cliente.html', context)
