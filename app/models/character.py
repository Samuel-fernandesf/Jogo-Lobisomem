class Player:
    def __init__(self, nome, papel):
        self.nome = nome
        self.papel = papel
        self.vivo = True

    def realizar_acao(self, alvo=None):
        return f"{self.nome} ({self.papel}) não pode realizar ações."

    def morrer(self):
        self.vivo = False
        return f"{self.nome} foi eliminado!"

    def to_dict(self):
        """Transforma o objeto Player em um dicionário JSON serializável"""
        return {"nome": self.nome, "papel": self.papel, "vivo": self.vivo}

    @staticmethod
    def from_dict(data):
        """Cria um objeto Player a partir de um dicionário"""
        obj = Player(data["nome"], data["papel"])
        obj.vivo = data["vivo"]
        return obj

class Assassino(Player):
    def __init__(self, nome):
        super().__init__(nome, "Vampiro")

    def realizar_acao(self, alvo):
        if not self.vivo:
            return f"{self.nome} está morto e não pode atacar."
        if not alvo.vivo:
            return f"{alvo.nome} já está morto."
        
        alvo.morrer()
        return f"{self.nome} matou {alvo.nome}!"

    def to_dict(self):
        data = super().to_dict()
        data["tipo"] = "Assassino"
        return data

    @staticmethod
    def from_dict(data):
        obj = Assassino(data["nome"])
        obj.vivo = data["vivo"]
        return obj

class Bruxa(Player):
    def __init__(self, nome):
        super().__init__(nome, "Bruxa")

    def realizar_acao(self, alvo):
        if not self.vivo:
            return f"{self.nome} está morta e não pode usar a magia."
        if not alvo.vivo:
            return f"{alvo.nome} já está morto."
        
        # A bruxa pode salvar um jogador (ou outra ação)
        alvo.vivo = True  # Exemplo de ação
        return f"{self.nome} salvou {alvo.nome}!"

    def to_dict(self):
        data = super().to_dict()
        data["tipo"] = "Bruxa"
        return data

    @staticmethod
    def from_dict(data):
        obj = Bruxa(data["nome"])
        obj.vivo = data["vivo"]
        return obj


class GuardaCosta(Player):
    def __init__(self, nome):
        super().__init__(nome, "Guarda-Costa")

    def realizar_acao(self, alvo):
        if not self.vivo:
            return f"{self.nome} está morto e não pode proteger ninguém."
        if not alvo.vivo:
            return f"{alvo.nome} já está morto."
        
        # O Guarda-Costa pode proteger um jogador (ou outra ação)
        alvo.vivo = True  # Exemplo de ação
        return f"{self.nome} protegeu {alvo.nome}!"

    def to_dict(self):
        data = super().to_dict()
        data["tipo"] = "Guarda-Costa"
        return data

    @staticmethod
    def from_dict(data):
        obj = GuardaCosta(data["nome"])
        obj.vivo = data["vivo"]
        return obj


class Acougueiro(Player):
    def __init__(self, nome):
        super().__init__(nome, "Açougueiro")

    def realizar_acao(self, alvo):
        if not self.vivo:
            return f"{self.nome} está morto e não pode atacar."
        if not alvo.vivo:
            return f"{alvo.nome} já está morto."
        
        alvo.morrer()  # Exemplo de matar alguém
        return f"{self.nome} matou {alvo.nome}!"

    def to_dict(self):
        data = super().to_dict()
        data["tipo"] = "Açougueiro"
        return data

    @staticmethod
    def from_dict(data):
        obj = Acougueiro(data["nome"])
        obj.vivo = data["vivo"]
        return obj
    
class Cacador(Player):
    def __init__(self, nome):
        super().__init__(nome, "Caçador")

    def realizar_acao(self, alvo):
        if not self.vivo:
            return f"{self.nome} está morto e não pode caçar."
        if not alvo.vivo:
            return f"{alvo.nome} já está morto."
        
        # O Caçador pode caçar alguém (ou outra ação)
        alvo.morrer()
        return f"{self.nome} caçou e matou {alvo.nome}!"

    def to_dict(self):
        data = super().to_dict()
        data["tipo"] = "Caçador"
        return data

    @staticmethod
    def from_dict(data):
        obj = Cacador(data["nome"])
        obj.vivo = data["vivo"]
        return obj
