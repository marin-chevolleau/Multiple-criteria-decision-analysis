class Criterion:
    direction: str = None
    indifference: float = None
    veto: float = None
    satisfaction: float = None
    weight: float = None

    def __init__(
        self,
        direction: str = None,
        indifference: float = None,
        veto: float = None,
        satisfaction: float = None,
        weight: float = None,
    ):
        self.direction = direction
        self.indifference = indifference
        self.veto = veto
        self.satisfaction = satisfaction
        self.weight = weight
