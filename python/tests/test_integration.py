import pytest
from src.fatura.service import FaturaService

def testa_fluxo_completo_ponta_a_ponta(repo, email_stub, gateway_mock):
    service = FaturaService(repo, email_stub, gateway_mock)

    fatura = service.fechar_fatura("cli-1", [(2, 10.0), (1, 30.0)], cupom=20)

    # Verificaçõess
    assert fatura.total == pytest.approx(44.0)  # (20+30)*0.8*1.1
    assert fatura.pago is True
    assert fatura.pagamento_id == "123"
    assert len(email_stub.enviados) == 1
    assert repo.buscar("cli-1") == fatura
    assert len(gateway_mock.chamadas) == 1
