from .entities import Fatura

class FaturaRepository:
    def __init__(self):
        self._faturas = {}

    def buscar(self, cliente_id: str) -> Fatura | None:
        return self._faturas.get(cliente_id)

    def salvar(self, fatura: Fatura):
        self._faturas[fatura.cliente_id] = fatura
