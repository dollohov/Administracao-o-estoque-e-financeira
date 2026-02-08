"""
Validadores customizados para integridade de dados do ERP.

Este modulo contem validadores para:
- Validacao de valores monetarios
- Validacao de quantidades de estoque
- Validacao de cálculos financeiros
"""

from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation


def validar_valor_positivo(valor):
    """
    Valida se um valor é positivo.
    
    Args:
        valor: Valor a validar (Decimal ou float)
    
    Raises:
        ValidationError: Se o valor nao for positivo
    """
    try:
        valor_decimal = Decimal(str(valor))
        if valor_decimal <= 0:
            raise ValidationError('O valor deve ser maior que zero.')
    except (InvalidOperation, ValueError):
        raise ValidationError('O valor deve ser um numero valido.')


def validar_quantidade_positiva(quantidade):
    """
    Valida se uma quantidade é um inteiro positivo.
    
    Args:
        quantidade: Quantidade a validar
    
    Raises:
        ValidationError: Se a quantidade nao for um inteiro positivo
    """
    try:
        qtd = int(quantidade)
        if qtd <= 0:
            raise ValidationError('A quantidade deve ser maior que zero.')
    except (ValueError, TypeError):
        raise ValidationError('A quantidade deve ser um numero inteiro.')


def validar_percentual(percentual):
    """
    Valida se um percentual está entre 0 e 100.
    
    Args:
        percentual: Percentual a validar
    
    Raises:
        ValidationError: Se o percentual nao estiver entre 0 e 100
    """
    try:
        perc = Decimal(str(percentual))
        if perc < 0 or perc > 100:
            raise ValidationError('O percentual deve estar entre 0 e 100.')
    except (InvalidOperation, ValueError):
        raise ValidationError('O percentual deve ser um numero valido.')


def validar_ncm(ncm):
    """
    Valida o formato do NCM (Nomenclatura Comum do Mercosul).
    
    Args:
        ncm: NCM a validar (deve ter 8 digitos)
    
    Raises:
        ValidationError: Se o NCM nao for valido
    """
    if not ncm:
        return  # Campo opcional
    
    ncm_limpo = ncm.replace('.', '').replace('-', '')
    
    if not ncm_limpo.isdigit() or len(ncm_limpo) != 8:
        raise ValidationError('O NCM deve conter exatamente 8 digitos.')


def validar_ean(ean):
    """
    Valida o formato do EAN/GTIN (codigo de barras).
    
    Args:
        ean: EAN a validar (deve ter 13 ou 14 digitos)
    
    Raises:
        ValidationError: Se o EAN nao for valido
    """
    if not ean:
        return  # Campo opcional
    
    ean_limpo = ean.replace('-', '').replace(' ', '')
    
    if not ean_limpo.isdigit() or len(ean_limpo) not in [13, 14]:
        raise ValidationError('O EAN deve conter 13 ou 14 digitos.')
    
    # Validar digito verificador (EAN-13)
    if len(ean_limpo) == 13:
        if not _validar_digito_verificador_ean(ean_limpo):
            raise ValidationError('O digito verificador do EAN é invalido.')


def _validar_digito_verificador_ean(ean):
    """
    Valida o digito verificador de um EAN-13.
    
    Args:
        ean: EAN-13 com 13 digitos
    
    Returns:
        bool: True se valido, False caso contrario
    """
    if len(ean) != 13:
        return False
    
    digitos = [int(d) for d in ean[:12]]
    soma = sum(d * (3 if i % 2 else 1) for i, d in enumerate(digitos))
    digito_verificador = (10 - (soma % 10)) % 10
    
    return int(ean[12]) == digito_verificador


def validar_integridade_venda(venda):
    """
    Valida a integridade de uma venda.
    
    Args:
        venda: Instancia de Venda
    
    Raises:
        ValidationError: Se houver inconsistencia
    """
    # Validar se ha itens
    if venda.itens.count() == 0:
        raise ValidationError('Uma venda deve ter pelo menos um item.')
    
    # Validar se o total é consistente
    subtotal_calculado = sum(item.subtotal for item in venda.itens.all())
    total_calculado = subtotal_calculado - venda.desconto
    
    # Permitir pequenas variacoes por arredondamento (0.01)
    if abs(venda.total - total_calculado) > Decimal('0.01'):
        raise ValidationError(
            f'Inconsistencia no total da venda. '
            f'Esperado: {total_calculado}, Atual: {venda.total}'
        )
    
    # Validar se todos os itens tem preco positivo
    for item in venda.itens.all():
        if item.preco_unitario <= 0:
            raise ValidationError(
                f'O item {item.produto.nome} tem preco invalido: {item.preco_unitario}'
            )
        
        if item.quantidade <= 0:
            raise ValidationError(
                f'O item {item.produto.nome} tem quantidade invalida: {item.quantidade}'
            )


def validar_integridade_estoque(movimentacao):
    """
    Valida a integridade de uma movimentacao de estoque.
    
    Args:
        movimentacao: Instancia de MovimentacaoEstoque
    
    Raises:
        ValidationError: Se houver inconsistencia
    """
    # Validar quantidade
    if movimentacao.quantidade <= 0:
        raise ValidationError('A quantidade deve ser maior que zero.')
    
    # Validar se ha estoque suficiente para saidas
    if movimentacao.tipo == 'SAIDA':
        if movimentacao.produto.estoque_atual < movimentacao.quantidade:
            raise ValidationError(
                f'Estoque insuficiente. Disponivel: {movimentacao.produto.estoque_atual}, '
                f'Solicitado: {movimentacao.quantidade}'
            )
    
    # Validar valor unitario
    if movimentacao.valor_unitario <= 0:
        raise ValidationError('O valor unitario deve ser maior que zero.')
