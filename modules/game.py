from Tkinter_template.Assets.project_management import canvas_reduction, making_widget, new_window
from Tkinter_template.Assets.extend_widget import EffectButton
from Tkinter_template.Assets.soundeffect import play_sound
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get, measure
import time
import os

class Game:
    def __init__(self, main):
        self.main = main
        self.c = self.main.canvas
        self.cs = self.main.canvas_side
        
        self.real_clock = None
        self.arguments = None
        self.timer_for_recipe = time.time()
        self.timer_for_customer = time.time()

    def __create_items_image(self):
        img_path = "images\\items"
        # iron plate
        self.c.create_image(30, self.cs[1]-200, anchor="sw", image=tk_image(
            "iron-plate-l.png", 200, 200, dirpath=img_path), tags=("iron-1"))
        self.c.create_image(230, self.cs[1]-200, anchor="sw", image=tk_image(
            "iron-plate-r.png", 200, 200, dirpath=img_path), tags=("iron-2"))
        self.c.create_image(30, self.cs[1], anchor="sw", image=tk_image(
            "iron-plate-l.png", 200, 200, dirpath=img_path), tags=("iron-3"))
        self.c.create_image(230, self.cs[1], anchor="sw", image=tk_image(
            "iron-plate-r.png", 200, 200, dirpath=img_path), tags=("iron-4"))
        # assemble area
        self.c.create_image(500, self.cs[1], anchor="sw", image=tk_image(
            "assemble.png", 400, 400, dirpath=img_path), tags=("assemble"))
        # assemble button
        self.c.create_window(900-4, self.cs[1]-11, anchor="se", 
                             window=EffectButton(("gold", "black"), root=self.c, text="Done", bg="lightyellow",
                                                 font=font_get(20)))
        self.c.create_window(500+4, self.cs[1]-11, anchor="sw", 
                             window=EffectButton(("gold", "black"), root=self.c, text="Clear", bg="lightyellow",
                                                 font=font_get(16)))                     
        # deep-fry
        self.c.create_image(1000, self.cs[1], anchor="sw", image=tk_image(
            "deep-fry.png", 200, 200, dirpath=img_path), tags=("fry-1"))
        self.c.create_image(1000, self.cs[1]-200, anchor="sw", image=tk_image(
            "deep-fry.png", 200, 200, dirpath=img_path), tags=("fry-1"))
        # refrigerator
        self.c.create_image(self.cs[0], self.cs[1]-200, anchor="se", image=tk_image(
            "refrigerator.png", 180, dirpath=img_path), tags=("refrigerator"))
        self.c.tag_bind("refrigerator", "<Button-1>", lambda e: self.__open_refrigerator())
        # trash bin
        self.c.create_image(self.cs[0], self.cs[1], anchor="se", image=tk_image(
            "trash-bin.png", 150, dirpath=img_path), tags=("trash-bin"))
        # recipe
        self.c.create_image(self.cs[0]-30, self.cs[1]-200-250, anchor="se", image=tk_image(
            "recipe.png", 80, dirpath=img_path), tags=("recipe"))
        # recipe outframe
        img = tk_image("recipe.png", 80, dirpath=img_path, get_object_only=True)
        width, height = img.width, img.height
        self.c.create_rectangle(self.cs[0]-30-width, self.cs[1]-200-250-height,
            self.cs[0]-30, self.cs[1]-200-250, outline="red", width=6, tag=("recipe-outframe"))
        # pick up
        self.c.create_image(0, 0, anchor="nw", image=tk_image(
            "pick-up.png", 120, 120, dirpath=img_path))
        self.c.create_rectangle(2, 0, 120-2, 28, fill="black")
        self.c.create_text(120/2, 0, anchor="n", text="PICK", font=font_get(21), fill="gold")
        # table
        for i in range(1, 4):
            self.c.create_image(120+(self.cs[0]-450)/3*(i-1)+int((self.cs[0]-450)/6), 220, anchor="n", image=tk_image(
                "table.png", int((self.cs[0]-450)/3), self.cs[1]-670, dirpath=img_path), tags=(f"table-{i}"))

    def __create_label(self):
        frame = making_widget("Frame")(self.c)
        self.c.create_window(self.cs[0]-30, 10, anchor="ne", window=frame)

        self.time_label = making_widget("StringVar")(value="")
        making_widget("Label")(frame, font=font_get(30), textvariable=self.time_label).pack()
        self.money_label = making_widget("StringVar")(value="")
        making_widget("Label")(frame, font=font_get(30), textvariable=self.money_label).pack()
        self.target_label = making_widget("StringVar")(value="")
        making_widget("Label")(frame, font=font_get(30), textvariable=self.target_label, bg="gold").pack()


    def __open_refrigerator(self):
        def press(name):
            frame_id = c.find_withtag("frame")
            for id in frame_id:
                c.itemconfig(id, state="hidden")
            c.itemconfig(f"{name}-frame", state="normal")
        
        def double_press(name, path):
            self.c.delete("pick")
            self.c.create_image(2, 30, anchor="nw", image=tk_image(
                name, 90, 90, dirpath=path), tag=("pick"))
            win.destroy()
        
        win = new_window("Refrigerator", "refrigerator.ico", (800, 600))
        c = making_widget("Canvas")(win, width=800, height=600, bg="lightblue")
        c.pack()
        c.bind('<MouseWheel>', lambda event: c.yview_scroll(-(event.delta//120), 'units'))
        
        # create ingredient
        row = -1
        font_size_name = 18  # 24
        font_size_header = 30 # 40
        count = 0
        for dir in os.listdir("images\\food"):
            if dir == "food":
                continue
            column = 0
            row += 1
            path = os.path.join("images\\food", dir)
            c.create_rectangle(0, 60*count+(200+40)*row, measure(dir, font_size_header), 60*count+(200+40)*row+40, 
                               fill="#ff6b87")
            c.create_text(0, 60*count+(200+40)*row, text=dir, font=font_get(font_size_header), anchor="nw")
            count += 1
            for filename in os.listdir(path):
                name = filename[0:filename.rfind(".")]
                if name[-1] in "123456789":
                    continue
                if filename in ("egg0.png"):
                    continue
                if name[-1] == "0":
                    name = name[:-1]
                if column == 4:
                    column = 0
                    row += 1

                c.create_image(200*column, 60*count+(200+40)*row, 
                               anchor="nw", image=tk_image(filename, 200, 200, dirpath=path), tags=(filename, ))
                c.create_text(200*column+100, 60*count+(200+40)*row+200, text=name, anchor="n", font=font_get(font_size_name), 
                              tags=(filename, ))
                c.create_rectangle(200*column, 60*count+(200+40)*row, 
                                   200*(column+1), 60*count+(200+40)*(row+1), outline="#ff6b87", width=5, state="hidden", 
                                   tags=(f"{filename}-frame", "frame"))
                column += 1
                c.tag_bind(filename, "<Button-1>", lambda e, n=filename: press(n))
                c.tag_bind(filename, "<Double-Button-1>", lambda e, n=filename, p=path: double_press(n, p))
                
        c['scrollregion'] = (
            0, 0, 800, 60*count+(200+40)*row+200+30
        )
        win.grab_set()
            

    def start(self):
        play_sound("start_a_game")
        # initialize
        canvas_reduction(self.c, self.cs, self.main.Music, "game.png", "game.mp3")
        self.c.tag_unbind("cover", "<Button-1>")
        self.arguments = self.main.Player.get_arguments_in_level()
       
          #player ini
        # customer clear
        self.main.Customer.refresh()
        self.main.Customer.random_priority()
        self.__create_items_image()
        self.__create_label()
        self.config_label("money", 0)
        self.config_label("target", self.arguments["target"])
        self.real_clock = time.time()
        

        # testing
        def test(e):
            print([self.c.gettags(x) for x in self.c.find_overlapping(e.x, e.y, e.x+1, e.y+1)])
        self.main.root.bind("<Button-1>", test)
        
        
        
        
       
    
    def config_label(self, genre: str, value):
        if genre not in ("time", "money", "target"):
            raise ValueError(f"Genre should be in time, money, target, but got {genre}")
        match genre:
            case "time":
                minute, second = divmod(value, 60)
                self.time_label.set(f"Time  {minute:02d}:{second:02d}")
            case "money":
                self.money_label.set(f"Money  {value:>4d}")
            case "target":
                self.target_label.set(f"Target {value:>4d}")
                
        
    

    def start_round(self, round_: int):
        img_path = "images\\round"
        canvas_reduction(self.c, self.cs, self.main.Music, "game.png", "game.mp3")

        # round
        width_round = tk_image("round.png", height=200,
                               dirpath=img_path, get_object_only=True).width
        middle_point = width_round
        for number in str(round_):
            middle_point += tk_image(f"{number}.png", height=200,
                                     dirpath=img_path, get_object_only=True).width
            middle_point += 20
        middle_point = (middle_point + 50) / 2

        self.c.create_image(
            self.cs[0]/2 - middle_point + width_round / 2, self.cs[1]/2, image=tk_image("round.png", height=200, dirpath=img_path),
            tags=("round"))
        revise_term = 0
        for number in str(round_):
            self.c.create_image(
                self.cs[0]/2 - middle_point + width_round + 50 + revise_term, self.cs[1]/2, image=tk_image(f"{number}.png", height=200, dirpath=img_path), anchor='w',
                tags=("round"))
            revise_term += tk_image(f"{number}.png", height=200,
                                    dirpath=img_path, get_object_only=True).width + 20
            
        self.c.tag_bind("cover", "<Button-1>", lambda e: self.start())

    def loop(self):
        if not self.c.find_withtag("recipe-outframe"):
            return

        if (t := time.time()) - self.timer_for_recipe >= self.main.recipeOutframeFrequency.get():
            state = self.c.itemcget("recipe-outframe", "state")
            self.c.itemconfig("recipe-outframe", state="normal" if state == "hidden" else "hidden")
            self.timer_for_recipe = t
        if t - self.timer_for_customer >= self.main.customerFrequency.get():
            # refresh customer
            self.main.Customer.check(t, self.arguments["patience"]/5)
            self.timer_for_customer = t
        
        
        remain = int(self.arguments["countdown"] - (time.time() - self.real_clock))
        self.config_label("time", remain)




