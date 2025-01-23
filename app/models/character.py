class Player():
    
    def __init__(
        self, life = True, 
        btn_Matar = False, rounds = 0
                ):
        
        self.life = life
        self.btn_Matar = btn_Matar
        self.rounds = rounds
        
    def vampiro(self, vampiro_kill):
        self.life
        self.vampiro_kill = 0
        
        if "matou":
            self.vampiro_kill += 1
        
    def condessa(self, button_transform, condessa_kill):
        self.life
        self.btn_Matar = True
        self.condessa_kill = 0
        
        if self.rounds in [0,2,4,6,8,10,12]:
            self.button_transform = True
            
        if "matou":
            self.condessa_kill += 1
        
    def campones(self):
        self.life
        self.btn_Matar
        
    def cacador(self):
        self.life
        self.btn_Matar = True
        self.cacador_kill = 0
        
        if self.rounds in [0,2,4,6,8,10]:
            self.btn_Matar = True
                
    def acougueiro(self, cheiroSangue):
        self.life
        self.btn_Matar
        self.cheiroSangue = True
        if cheiroSangue and self.vampiro_kill > 0 or self.condessa_kill > 0 or self.cacador_kill > 0:
            return "Esse jogador cheira a sangue"
        
# class Player:
#     def __init__(self, name, role, life=True):
#         self.name = name
#         self.role = role  # Ex: Vampiro, Condessa, Caçador, etc.
#         self.life = life
#         self.kills = 0

#     def kill(self, target):
#         if self.life:
#             target.life = False
#             self.kills += 1
#             print(f"{self.name} matou {target.name}")

#     def __str__(self):
#         return f"{self.name} ({self.role}) - {'Vivo' if self.life else 'Morto'}"

# class Vampiro(Player):
#     def __init__(self, name):
#         super().__init__(name, "Vampiro")

#     def action(self, target):
#         if self.life:
#             self.kill(target)

# class Condessa(Player):
#     def __init__(self, name):
#         super().__init__(name, "Condessa")
#         self.transform_button = False

#     def action(self):
#         if self.life:
#             self.transform_button = True
#             print(f"{self.name} se transformou em vampira")

# class Cacador(Player):
#     def __init__(self, name):
#         super().__init__(name, "Caçador")

#     def action(self, target):
#         if self.life:
#             self.kill(target)
#             print(f"{self.name} caçou {target.name}")

# class Acougueiro(Player):
#     def __init__(self, name):
#         super().__init__(name, "Acougueiro")
#         self.cheiro_sangue = False

#     def action(self):
#         if self.life:
#             self.cheiro_sangue = True
#             print(f"{self.name} sente o cheiro de sangue")
#             if self.kills > 0:
#                 print(f"{self.name} cheira a sangue!")

# # Exemplo de uso:
# player1 = Vampiro("Vampiro1")
# player2 = Condessa("Condessa1")
# player3 = Cacador("Cacador1")
# player4 = Acougueiro("Acougueiro1")

# # Jogadores realizam ações:
# player1.action(player2)  # Vampiro mata Condessa
# player3.action(player4)  # Caçador mata Acougueiro

# # Verificando estado dos jogadores:
# print(player1)
# print(player2)
# print(player3)
# print(player4)

# # O Acougueiro sente 
            