from .entities import Fatura
from .exceptions import CupomInvalidoError, PagamentoRecusadoError, QuantidadeInvalidaError
from .repository import FaturaRepository


class FaturaService:
    def __init__(
        self, repo: FaturaRepository, email_service, gateway_pagamento
    ) -> None:
        self.repo = repo
        self.email = email_service
        self.gateway = gateway_pagamento

    def calcular_total(self, qtd: int, preco: float, cupom: int = 0) -> float:
        if qtd <= 0:
            raise QuantidadeInvalidaError("A quantidade deve ser um número positivo.")
        if not (0 <= cupom <= 100):
            raise CupomInvalidoError("O cupom é inválido.")

        subtotal = qtd * preco
        desconto = subtotal * (cupom / 100)
        total_com_desconto = subtotal - desconto
        imposto = total_com_desconto * 0.10  # 10% de imposto
        return total_com_desconto + imposto

    def fechar_fatura(
        self, cliente_id: str, itens: list[tuple[int, float]], cupom: int = 0
    ) -> Fatura:
        subtotal = sum(qtd * preco for qtd, preco in itens)

        # Aplica o cupom no subtotal geral
        desconto = subtotal * (cupom / 100)
        total_com_desconto = subtotal - desconto
        
        # Aplica o imposto
        imposto = total_com_desconto * 0.10
        total = total_com_desconto + imposto

        # Tenta processar o pagamento
        pagamento_id = self.gateway.processar(total)
        if not pagamento_id:
            raise PagamentoRecusadoError("Pagamento recusado pelo gateway.")

        # Cria e salva a fatura
        fatura = Fatura(cliente_id, total, pago=True, pagamento_id=pagamento_id)
        self.repo.salvar(fatura)

        # Envia o e-mail de confirmação
        self.email.enviar(fatura)

        return fatura