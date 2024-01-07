from Tkinter_template.Assets.universal import parse_json_to_property
from Tkinter_template.Assets.music import Music
from Tkinter_template.base import Interface
from modules.player.player import Player
from modules.player.customer import Customer
from modules import *
import time
import sys


Interface.rate = 1.0


class Main(Interface):
    def __init__(self, title: str, icon=None, default_menu=True):
        super().__init__(title, icon, default_menu)

        parse_json_to_property(self, "modules\\setting.json")
        # obejects
        self.Music = Music()
        self.Start = start.Effect(self)
        self.Game = game.Game(self)
        self.Player = Player(self)
        self.Customer = Customer(self)
        # ----- initialize -----
        if not initializer.check_font_ready():
            sys.exit()

        self.Start.enter()


if __name__ == "__main__":
    main = Main("Serene Flavor on Wheels", "favicon.ico", False)

    while True:
        try:
            main.canvas.update()
            time.sleep(0.01)
            main.Music.judge()
            main.Game.loop()
        except BaseException:
            1 / 0
