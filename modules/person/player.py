class Player:
    
    def __init__(self, main: object) -> None:
        self.main = main
        self.c = self.main.canvas
        self.cs = self.main.canvas_side
        self.level = 1

        # during the game
        self.hand = None
        self.__money = None
        self.is_assemble = None
        self.only_for_customer = None
        self.items_state = {}

    @property
    def money(self):
        return self.__money
    
    @money.setter
    def money(self, value):
        if value <= 0:
            self.__money = 0
        else:
            self.__money = value

    def refresh(self):
        self.hand = None
        self.__money = 5000
        self.items_state = {
            "iron-1": None,
            "iron-2": None,
            "iron-3": None,
            "iron-4": None,
            "fry-1": None,
            "fry-2": None,
            "assemble": [],
        }
        self.is_assemble = False
        self.only_for_customer = False
        
    def get_arguments_in_level(self):
        s = self.level - 1
        arguments = {
            "countdown": self.main.__dict__[f"timeCountdown_{s}"].get(),
            "target": self.main.__dict__[f"moneyTarget_{s}"].get(),
            "patience": self.main.__dict__[f"customerPatience_{s}"].get(),
        }
        return arguments
