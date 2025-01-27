class Player:
    def __init__(self, life=True, rounds=0):
        self.life = life  # Status de vida do jogador
        self.rounds = rounds  # Número de rodadas do jogador

    def vote(self):
        """Função genérica para votar, pode ser sobrescrita."""
        pass


class Campones(Player):
    def __init__(self, life=True, rounds=0):
        super().__init__(life, rounds)
        self.has_voted = False  # Controle se o camponês já votou no dia 2

    def skip_round(self):
        """Camponês apenas pula a rodada."""
        print("Camponês pulou a rodada.")

    def vote(self):
        if self.rounds >= 2 and not self.has_voted:
            self.has_voted = True
            print("Camponês votou.")
        else:
            print("Camponês não pode votar agora.")


class Vampiro(Player):
    def __init__(self, life=True, rounds=0):
        super().__init__(life, rounds)
        self.vampiro_kill_count = 0  # Contador de mortes realizadas pelo vampiro

    def kill(self, target):
        """Vampiro mata um jogador durante a noite."""
        if self.rounds < 3:
            target.life = False
            self.vampiro_kill_count += 1
            print(f"Vampiro matou o jogador {target}.")
        else:
            print("Vampiro não pode matar após a rodada 3.")

    def vote(self):
        if self.rounds >= 3:
            print("Vampiro votou.")
        else:
            print("Vampiro não pode votar antes da rodada 3.")


class Condessa(Player):
    def __init__(self, life=True, rounds=0):
        super().__init__(life, rounds)
        self.condessa_kill_count = 0  # Contador de mortes realizadas pela condessa

    def kill(self, target):
        """Condessa mata um jogador, mas não pode matar vampiros."""
        if not isinstance(target, Vampiro):
            target.life = False
            self.condessa_kill_count += 1
            print(f"Condessa matou o jogador {target}.")
        else:
            print("Condessa não pode matar vampiros.")

    def transform(self, target):
        """Condessa transforma um jogador em vampiro a cada duas rodadas."""
        if self.rounds % 2 == 0:
            if not isinstance(target, Vampiro):
                target.__class__ = Vampiro
                print(f"Condessa transformou o jogador {target} em vampiro.")
            else:
                print("Jogador já é um vampiro, não pode ser transformado.")
        else:
            print("Condessa não pode transformar nesta rodada.")

    def vote(self):
        """Condessa vota normalmente."""
        print("Condessa votou.")


class Cacador(Player):
    def __init__(self, life=True, rounds=0):
        super().__init__(life, rounds)

    def kill(self, target):
        """Caçador pode matar qualquer jogador a cada duas rodadas."""
        if self.rounds % 2 == 0:
            target.life = False
            print(f"Caçador matou o jogador {target}.")
        else:
            print("Caçador não pode matar nesta rodada.")

    def vote(self):
        """Caçador vota normalmente."""
        print("Caçador votou.")


class Acougueiro(Player):
    def __init__(self, life=True, rounds=0):
        super().__init__(life, rounds)

    def inspect(self, target):
        """Açougueiro inspeciona um jogador para ver se ele matou alguém."""
        if hasattr(target, "vampiro_kill_count") and target.vampiro_kill_count > 0:
            print("Ele cheira a sangue.")
        elif hasattr(target, "condessa_kill_count") and target.condessa_kill_count > 0:
            print("Ele cheira a sangue.")
        elif isinstance(target, Cacador) and target.rounds % 2 == 0:
            print("Ele cheira a sangue.")
        else:
            print("Ele não cheira a sangue.")

    def vote(self):
        """Açougueiro vota normalmente."""
        print("Açougueiro votou.")