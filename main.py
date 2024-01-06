from Tkinter_template.Assets.music import Music
from Tkinter_template.base import Interface 
from modules.initializer import Initializer 
from modules.start import Effect
from modules.game import Game
import time
import sys
Interface.rate = 1.0

class Main(Interface):
    def __init__(self, title: str, icon=None, default_menu=True):
        super().__init__(title, icon, default_menu)
    
        # obejects
        self.Music = Music()
        self.Start = Effect(self)
        self.Game = Game(self)
        # ----- initialize -----
        self.Initializers = Initializer(self)
        if not self.Initializers.check_font_ready():
            sys.exit()

        self.Start.enter()

if __name__ == "__main__":
    main = Main("Serene Flavor on Wheels", "favicon.ico", False)

    while True:
        try:
            main.canvas.update()
            time.sleep(0.01)
            main.Game.loop()
        except BaseException:
            1 / 0


