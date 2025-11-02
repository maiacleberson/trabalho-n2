import pytest
from src.fatura.repository import FaturaRepository
from src.fatura.service import FaturaService

class MockEmailService:
    def __init__(self):
        self.enviados = []

    def enviar(self, fatura):
        self.enviados.append(fatura)

class MockGatewayPagamento:
    def __init__(self, aprovar=True):
        self.aprovar = aprovar
        self.chamadas = []

    def processar(self, valor):
        self.chamadas.append(valor)
        if self.aprovar:
            return "123"
        return None

@pytest.fixture
def repo():
    return FaturaRepository()

@pytest.fixture
def email_stub():
    return MockEmailService()

@pytest.fixture
def gateway_mock():
    return MockGatewayPagamento()

@pytest.fixture
def service(repo, email_stub, gateway_mock):
    return FaturaService(repo, email_stub, gateway_mock)
