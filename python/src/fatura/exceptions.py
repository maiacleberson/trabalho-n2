class QuantidadeInvalidaError(ValueError):
    """Exceção para quantidade inválida (≤ 0)"""
    pass

class CupomInvalidoError(ValueError):
    """Exceção para cupom fora do intervalo 0-100"""
    pass

class PagamentoRecusadoError(Exception):
    """Exceção quando o pagamento é recusado pelo gateway"""
    pass