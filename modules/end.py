from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get
from Tkinter_template.Assets.soundeffect import play_sound
import time
class EffectEnd:
    def __init__(self, main) -> None:
        self.main = main
        self.c = self.main.canvas
        self.cs = self.main.canvas_side

    def enter(self):
        def press(e):
            self.c.delete("result")
            self.c.update()
            self.c.tag_unbind("cover", "<Button-1>")
            if self.main.Player.money >= self.main.Player.get_arguments_in_level()["target"]:
                # pass
                if self.main.Player.level == 3:
                    play_sound("all-clear")
                    self.c.create_image(self.cs[0]/2, self.cs[1]/2, image=tk_image(
                        "success.png", 400, dirpath="images\\items"
                    ))
                    self.c.update()
                    time.sleep(4)
                    self.main.Player.level = 1
                    self.main.Main.enter()
                else:
                    play_sound("success")
                    self.main.Player.level += 1
                    self.main.Game.start_round(self.main.Player.level)
            else:
                play_sound("fail")
                self.c.create_image(self.cs[0]/2, self.cs[1]/2, image=tk_image(
                    "fail.png", 400, dirpath="images\\items"
                ))
                self.c.update()
                time.sleep(4)
                self.main.Player.level = 1
                self.main.Main.enter()
                
            
            
        canvas_reduction(self.c, self.cs, self.main.Music, "result.png")
        play_sound("finish")

        #create
        self.c.create_image(self.cs[0]/2, self.cs[1]/2, image=tk_image(
            "result.png", 700, 400, dirpath="images\\items"
        ), tags=("result"))
        self.c.create_text(self.cs[0]//2, 75, text=f"Level {self.main.Player.level}", 
                           font=font_get(100), fill="#ff6b87", anchor="n", tags=("result"))
        self.c.create_text(self.cs[0]//2, self.cs[1]/2-100, text=self.main.Player.money, 
                           font=font_get(75), fill="white", tags=("result"))
        self.c.create_text(self.cs[0]//2, self.cs[1]/2+100, text=self.main.Player.get_arguments_in_level()["target"], 
                           font=font_get(75), fill="gold", tags=("result"))
        
        self.c.tag_bind("cover", "<Button-1>", press)
        
