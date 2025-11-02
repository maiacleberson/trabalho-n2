import pytest
from src.fatura.exceptions import QuantidadeInvalidaError, CupomInvalidoError
from src.fatura.service import FaturaService
from tests.conftest import MockGatewayPagamento

@pytest.mark.parametrize(
    "qtd, preco, desconto, esperado",
    [
        (2, 10.0, 0, 22.0),   # 20 + 10% = 22
        (3, 5.0, 10, 14.85),  # (15 - 1.5) * 1.1 = 14.85
        (1, 100.0, 50, 55.0), # (100 - 50) * 1.1 = 55
        # Análise do Valor Limite (BVA)
        (1, 10.0, 0, 11.0),
        (1, 10.0, 100, 0.0),
    ]
)
def testa_calculo_total(service, qtd, preco, desconto, esperado):
    assert service.calcular_total(qtd, preco, desconto) == pytest.approx(esperado)

def testa_excecao_para_quantidade_invalida(service):
    with pytest.raises(QuantidadeInvalidaError):
        service.calcular_total(0, 10.0, 0)

def testa_excecao_para_cupom_invalido(service):
    with pytest.raises(CupomInvalidoError):
        service.calcular_total(1, 10.0, -1)
    with pytest.raises(CupomInvalidoError):
        service.calcular_total(1, 10.0, 101)

def testa_envio_de_email_apos_pagamento_aprovado(service, email_stub, gateway_mock):
    service.fechar_fatura("cli-1", [(2, 10.0)])
    assert len(email_stub.enviados) == 1
    assert email_stub.enviados[0].pago is True

def testa_nao_envio_de_email_se_pagamento_recusado(service, email_stub):
    gateway_mock = MockGatewayPagamento(aprovar=False)
    service_test = FaturaService(service.repo, email_stub, gateway_mock)
    with pytest.raises(Exception):  # ErroPagamentoRecusado
        service_test.fechar_fatura("cli-1", [(1, 10.0)])
    assert len(email_stub.enviados) == 0

@pytest.mark.slow
def testa_performance_do_fluxo_completo(service):
    import time
    t0 = time.perf_counter()
    service.fechar_fatura("cli-1", [(3, 5.0)], cupom=10)
    duracao = time.perf_counter() - t0
    assert duracao < 0.2  # 200ms
