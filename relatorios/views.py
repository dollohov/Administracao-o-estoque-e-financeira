from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.utils import timezone
from datetime import timedelta

from estoque.models import Produto, MovimentacaoEstoque
from vendas.models import Pedido, ItemPedido
from financeiro.models import Receita, Despesa


@login_required
@permission_required("relatorios.view_dashboard", raise_exception=True)
def dashboard_relatorios(request):
    # Exemplo de dados para o dashboard
    total_produtos = Produto.objects.count()
    total_pedidos = Pedido.objects.count()
    total_vendas_mes = Pedido.objects.filter(
        data_pedido__month=timezone.now().month,
        data_pedido__year=timezone.now().year,
        status="FINALIZADO"
    ).aggregate(Sum("valor_total"))["valor_total__sum"] or Decimal("0.00")

    context = {
        "total_produtos": total_produtos,
        "total_pedidos": total_pedidos,
        "total_vendas_mes": total_vendas_mes,
        "page_title": "Dashboard de Relatórios"
    }
    return render(request, "relatorios/dashboard.html", context)


@login_required
@permission_required("relatorios.view_curva_abc", raise_exception=True)
def curva_abc(request):
    # Lógica para calcular a Curva ABC
    # Produtos mais vendidos/lucrativos
    produtos_vendidos = ItemPedido.objects.filter(pedido__status="FINALIZADO") \
        .values("produto__nome", "produto__preco_venda") \
        .annotate(
            total_vendido=Sum(F("quantidade") * F("preco_unitario") * (1 - F("desconto") / 100)),
            quantidade_vendida=Sum("quantidade")
        ) \
        .order_by("-total_vendido")

    total_geral_vendas = sum(p["total_vendido"] for p in produtos_vendidos)
    
    curva_a = []
    curva_b = []
    curva_c = []
    acumulado = Decimal("0.00")

    for produto in produtos_vendidos:
        percentual = (produto["total_vendido"] / total_geral_vendas) * 100 if total_geral_vendas else Decimal("0.00")
        acumulado += percentual
        produto["percentual_vendas"] = percentual
        produto["acumulado_vendas"] = acumulado

        if acumulado <= 80:
            curva_a.append(produto)
        elif acumulado <= 95:
            curva_b.append(produto)
        else:
            curva_c.append(produto)

    context = {
        "curva_a": curva_a,
        "curva_b": curva_b,
        "curva_c": curva_c,
        "page_title": "Curva ABC de Produtos"
    }
    return render(request, "relatorios/curva_abc.html", context)


@login_required
@permission_required("relatorios.view_previsao_estoque", raise_exception=True)
def previsao_estoque(request):
    # Lógica para previsão de estoque (exemplo simplificado)
    produtos_criticos = []
    for produto in Produto.objects.filter(ativo=True, estoque_minimo__gt=0):
        # Calcular vendas nos últimos 30 dias
        data_limite = timezone.now() - timedelta(days=30)
        vendas_30_dias = ItemPedido.objects.filter(
            produto=produto,
            pedido__data_pedido__gte=data_limite,
            pedido__status="FINALIZADO"
        ).aggregate(Sum("quantidade"))["quantidade__sum"] or Decimal("0.00")

        if vendas_30_dias > 0:
            consumo_diario = vendas_30_dias / 30
            dias_restantes = (produto.estoque_atual / consumo_diario) if consumo_diario > 0 else float("inf")

            if produto.estoque_atual <= produto.estoque_minimo or dias_restantes <= 7: # Alerta se menos de 7 dias de estoque
                produtos_criticos.append({
                    "produto": produto,
                    "estoque_atual": produto.estoque_atual,
                    "estoque_minimo": produto.estoque_minimo,
                    "vendas_30_dias": vendas_30_dias,
                    "consumo_diario": consumo_diario,
                    "dias_restantes": round(dias_restantes, 2),
                    "sugestao_compra": produto.estoque_minimo * 2 - produto.estoque_atual # Exemplo
                })
        elif produto.estoque_atual <= produto.estoque_minimo:
             produtos_criticos.append({
                    "produto": produto,
                    "estoque_atual": produto.estoque_atual,
                    "estoque_minimo": produto.estoque_minimo,
                    "vendas_30_dias": Decimal("0.00"),
                    "consumo_diario": Decimal("0.00"),
                    "dias_restantes": float("inf"),
                    "sugestao_compra": produto.estoque_minimo - produto.estoque_atual # Exemplo
                })

    context = {
        "produtos_criticos": produtos_criticos,
        "page_title": "Previsão e Sugestão de Estoque"
    }
    return render(request, "relatorios/previsao_estoque.html", context)


@login_required
@permission_required("relatorios.view_vendas_performance", raise_exception=True)
def vendas_performance(request):
    # Lógica para performance de vendas por vendedor/produto
    vendas_por_vendedor = Pedido.objects.filter(status="FINALIZADO") \
        .values("vendedor__username") \
        .annotate(total_vendas=Sum("valor_total")) \
        .order_by("-total_vendas")

    context = {
        "vendas_por_vendedor": vendas_por_vendedor,
        "page_title": "Performance de Vendas"
    }
    return render(request, "relatorios/vendas_performance.html", context)


@login_required
@permission_required("relatorios.view_financeiro_saude", raise_exception=True)
def financeiro_saude(request):
    # Lógica para saúde financeira (receitas vs despesas)
    hoje = timezone.now().date()
    primeiro_dia_mes_atual = hoje.replace(day=1)
    ultimo_dia_mes_atual = (primeiro_dia_mes_atual + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    receitas_mes = Receita.objects.filter(
        data_recebimento__gte=primeiro_dia_mes_atual,
        data_recebimento__lte=ultimo_dia_mes_atual
    ).aggregate(Sum("valor"))["valor__sum"] or Decimal("0.00")

    despesas_mes = Despesa.objects.filter(
        data_pagamento__gte=primeiro_dia_mes_atual,
        data_pagamento__lte=ultimo_dia_mes_atual
    ).aggregate(Sum("valor"))["valor__sum"] or Decimal("0.00")

    lucro_liquido_mes = receitas_mes - despesas_mes

    context = {
        "receitas_mes": receitas_mes,
        "despesas_mes": despesas_mes,
        "lucro_liquido_mes": lucro_liquido_mes,
        "page_title": "Saúde Financeira"
    }
    return render(request, "relatorios/financeiro_saude.html", context)
