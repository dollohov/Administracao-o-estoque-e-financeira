from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings

from .models import Pedido, ItemPedido
from estoque.models import Produto
from clientes.models import Cliente
from decimal import Decimal
import os
import urllib.parse

# Para geração de PDF
# A importação do WeasyPrint é feita dentro da função para evitar erros de inicialização
WEASYPRINT_DISPONIVEL = None  # Será definido na primeira tentativa


@login_required
@permission_required("vendas.view_pedido", raise_exception=True)
def lista_pedidos(request):
    pedidos = Pedido.objects.select_related("cliente", "vendedor").order_by("-data_pedido")
    context = {"pedidos": pedidos}
    return render(request, "vendas/lista_pedidos.html", context)


@login_required
@permission_required("vendas.add_pedido", raise_exception=True)
def criar_pedido(request):
    clientes = Cliente.objects.filter(ativo=True).order_by("nome_completo")
    produtos = Produto.objects.filter(ativo=True).order_by("nome")

    if request.method == "POST":
        cliente_id = request.POST.get("cliente")
        observacoes = request.POST.get("observacoes")
        
        try:
            cliente = get_object_or_404(Cliente, pk=cliente_id)
            
            with transaction.atomic():
                pedido = Pedido.objects.create(
                    cliente=cliente,
                    vendedor=request.user,
                    observacoes=observacoes,
                    status="RASCUNHO" # Começa como rascunho
                )

                # Adicionar itens ao pedido
                for key, value in request.POST.items():
                    if key.startswith("produto_") and value.isdigit():
                        produto_id = value
                        quantidade = Decimal(request.POST.get(f"quantidade_{produto_id}", "0").replace(",", "."))
                        preco_unitario = Decimal(request.POST.get(f"preco_{produto_id}", "0").replace(",", "."))
                        desconto = Decimal(request.POST.get(f"desconto_{produto_id}", "0").replace(",", "."))

                        if quantidade > 0 and preco_unitario >= 0:
                            produto = get_object_or_404(Produto, pk=produto_id)
                            ItemPedido.objects.create(
                                pedido=pedido,
                                produto=produto,
                                quantidade=quantidade,
                                preco_unitario=preco_unitario,
                                desconto=desconto
                            )
                
                pedido.save() # Recalcula o valor total
                messages.success(request, f"Pedido #{pedido.pk} criado com sucesso!")
                return redirect("vendas:detalhe_pedido", pk=pedido.pk)

        except Exception as e:
            messages.error(request, f"Erro ao criar pedido: {e}")

    context = {
        "clientes": clientes,
        "produtos": produtos,
        "page_title": "Novo Pedido"
    }
    return render(request, "vendas/criar_pedido.html", context)


@login_required
@permission_required("vendas.view_pedido", raise_exception=True)
def detalhe_pedido(request, pk):
    pedido = get_object_or_404(Pedido.objects.select_related("cliente", "vendedor"), pk=pk)
    itens = pedido.itens.select_related("produto").all()
    context = {"pedido": pedido, "itens": itens}
    return render(request, "vendas/detalhe_pedido.html", context)


@login_required
@permission_required("vendas.change_pedido", raise_exception=True)
def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido.objects.select_related("cliente", "vendedor"), pk=pk)
    clientes = Cliente.objects.filter(ativo=True).order_by("nome_completo")
    produtos = Produto.objects.filter(ativo=True).order_by("nome")
    
    if request.method == "POST":
        cliente_id = request.POST.get("cliente")
        observacoes = request.POST.get("observacoes")
        status = request.POST.get("status")

        try:
            cliente = get_object_or_404(Cliente, pk=cliente_id)
            
            with transaction.atomic():
                pedido.cliente = cliente
                pedido.observacoes = observacoes
                pedido.status = status
                pedido.save(update_fields=["cliente", "observacoes", "status"])

                # Remover itens existentes e adicionar novos
                pedido.itens.all().delete()
                for key, value in request.POST.items():
                    if key.startswith("produto_") and value.isdigit():
                        produto_id = value
                        quantidade = Decimal(request.POST.get(f"quantidade_{produto_id}", "0").replace(",", "."))
                        preco_unitario = Decimal(request.POST.get(f"preco_{produto_id}", "0").replace(",", "."))
                        desconto = Decimal(request.POST.get(f"desconto_{produto_id}", "0").replace(",", "."))

                        if quantidade > 0 and preco_unitario >= 0:
                            produto = get_object_or_404(Produto, pk=produto_id)
                            ItemPedido.objects.create(
                                pedido=pedido,
                                produto=produto,
                                quantidade=quantidade,
                                preco_unitario=preco_unitario,
                                desconto=desconto
                            )
                
                pedido.save() # Recalcula o valor total
                messages.success(request, f"Pedido #{pedido.pk} atualizado com sucesso!")
                return redirect("vendas:detalhe_pedido", pk=pedido.pk)

        except Exception as e:
            messages.error(request, f"Erro ao atualizar pedido: {e}")

    context = {
        "pedido": pedido,
        "itens_pedido": pedido.itens.all(),
        "clientes": clientes,
        "produtos": produtos,
        "STATUS_PEDIDO": Pedido.STATUS_PEDIDO,
        "page_title": f"Editar Pedido #{pedido.pk}"
    }
    return render(request, "vendas/editar_pedido.html", context)


@login_required
@permission_required("vendas.view_pedido", raise_exception=True)
def gerar_pedido_pdf(request, pk):
    global WEASYPRINT_DISPONIVEL
    
    # Tentar importar WeasyPrint apenas quando necessario
    if WEASYPRINT_DISPONIVEL is None:
        try:
            from weasyprint import HTML
            WEASYPRINT_DISPONIVEL = True
        except (ImportError, OSError) as e:
            WEASYPRINT_DISPONIVEL = False
            messages.error(request, f"WeasyPrint nao esta disponivel. Erro: {str(e)}")
            return redirect("vendas:detalhe_pedido", pk=pk)
    
    if not WEASYPRINT_DISPONIVEL:
        messages.error(request, "WeasyPrint nao esta disponivel. Verifique a instalacao das dependencias de sistema.")
        return redirect("vendas:detalhe_pedido", pk=pk)
    
    # Importar aqui para usar a variavel global
    from weasyprint import HTML
    
    pedido = get_object_or_404(Pedido.objects.select_related("cliente", "vendedor"), pk=pk)
    itens = pedido.itens.select_related("produto").all()

    html_template = get_template("vendas/pedido_pdf.html")
    context = {
        "pedido": pedido,
        "itens": itens,
        "base_url": request.build_absolute_uri("/"),
        "logo_path": os.path.join(settings.STATIC_ROOT, "img/logo.png")
    }
    html_content = html_template.render(context)

    try:
        pdf_file = HTML(string=html_content, base_url=request.build_absolute_uri("/")).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename=\"pedido_{pedido.pk}.pdf\""
        return response
    except Exception as e:
        messages.error(request, f"Erro ao gerar PDF: {str(e)}")
        return redirect("vendas:detalhe_pedido", pk=pk)


@login_required
@permission_required("vendas.view_pedido", raise_exception=True)
def enviar_whatsapp(request, pk):
    pedido = get_object_or_404(Pedido.objects.select_related("cliente"), pk=pk)
    
    if not pedido.cliente.telefone:
        messages.error(request, "Cliente não possui telefone cadastrado para envio de WhatsApp.")
        return redirect("vendas:detalhe_pedido", pk=pedido.pk)

    # Montar mensagem
    mensagem = f"Olá {pedido.cliente.nome_completo}, seu pedido #{pedido.pk} está com o status: {pedido.get_status_display()}.\n"
    mensagem += f"Valor Total: R$ {pedido.valor_total:.2f}\n"
    mensagem += "Itens:\n"
    for item in pedido.itens.all():
        mensagem += f"- {item.quantidade}x {item.produto.nome} (R$ {item.preco_unitario:.2f} cada)\n"
    mensagem += "\nEm breve entraremos em contato!"

    # Codificar mensagem para URL
    encoded_message = urllib.parse.quote(mensagem)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={pedido.cliente.telefone}&text={encoded_message}"

    return redirect(whatsapp_url)
