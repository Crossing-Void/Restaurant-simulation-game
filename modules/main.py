from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.extend_widget import EffectButton
from Tkinter_template.Assets.soundeffect import play_sound
from Tkinter_template.Assets.font import font_get


class Effect:
    def __init__(self, main):
        self.main = main
        self.c = self.main.canvas
        self.cs = self.main.canvas_side

    def __start(self):
        play_sound("press")
        self.main.Game.start_round(self.main.Player.level)

    def __rule(self):
        play_sound("press")
        pass

    def enter(self):
        canvas_reduction(self.c, self.cs, self.main.Music,
                         "main.png", "main.mp3")
        # button
        self.c.create_window(self.cs[0]/3, self.cs[1]-100,
                             window=EffectButton(("#ff6b87", "blue"), "enter", self.c, text="Start", font=font_get(30),
                                                 command=self.__start))
        self.c.create_window(self.cs[0]*2/3, self.cs[1]-100,
                             window=EffectButton(("#ff6b87", "blue"), "enter", self.c, text="Rule", font=font_get(30),
                                                 command=self.__rule))
