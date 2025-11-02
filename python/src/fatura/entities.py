from dataclasses import dataclass

@dataclass
class Fatura:
    cliente_id: str
    total: float
    pago: bool = False
    pagamento_id: str | None = None
