class Player:
    
    def __init__(self, main: object) -> None:
        self.main = main
        self.c = self.main.canvas
        self.cs = self.main.canvas_side
        self.level = 1
    
    def get_arguments_in_level(self):
        s = self.level - 1
        arguments = {
            "countdown": self.main.__dict__[f"timeCountdown_{s}"].get(),
            "target": self.main.__dict__[f"moneyTarget_{s}"].get(),
            "patience": self.main.__dict__[f"customerPatience_{s}"].get(),
        }
        return arguments
