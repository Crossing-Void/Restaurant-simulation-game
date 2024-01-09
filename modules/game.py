from Tkinter_template.Assets.project_management import canvas_reduction, making_widget, new_window
from Tkinter_template.Assets.extend_widget import EffectButton
from modules.food.food import create_food, reverse_name_value, Meal, _Food
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
        self.item_dict = {}
        self.timer_for_recipe = time.time()
        self.timer_for_customer = time.time()

    def __create_items_image(self):
        img_path = "images\\items"
        # iron plate
        self.item_dict["iron-1"] = self.c.create_image(30, self.cs[1]-200, anchor="sw", image=tk_image(
            "iron-plate-l.png", 200, 200, dirpath=img_path), tags=("iron-1"))
        self.item_dict["iron-2"] = self.c.create_image(230, self.cs[1]-200, anchor="sw", image=tk_image(
            "iron-plate-r.png", 200, 200, dirpath=img_path), tags=("iron-2"))
        self.item_dict["iron-3"] = self.c.create_image(30, self.cs[1], anchor="sw", image=tk_image(
            "iron-plate-l.png", 200, 200, dirpath=img_path), tags=("iron-3"))
        self.item_dict["iron-4"] = self.c.create_image(230, self.cs[1], anchor="sw", image=tk_image(
            "iron-plate-r.png", 200, 200, dirpath=img_path), tags=("iron-4"))
        # assemble area
        self.item_dict["assemble"] = self.c.create_image(500, self.cs[1], anchor="sw", image=tk_image(
            "assemble.png", 400, 400, dirpath=img_path), tags=("assemble"))
        # assemble button
        self.c.create_window(900-4, self.cs[1]-11, anchor="se", 
                             window=EffectButton(("gold", "black"), root=self.c, text="Done", bg="lightyellow",
                                                 font=font_get(20), command=self.__assemble_assemble))
        self.c.create_window(500+4, self.cs[1]-11, anchor="sw", 
                             window=EffectButton(("gold", "black"), root=self.c, text="Clear", bg="lightyellow",
                                                 font=font_get(16), command=self.__clear_assemble))                     
        # deep-fry
        self.item_dict["fry-1"] = self.c.create_image(1000, self.cs[1], anchor="sw", image=tk_image(
            "deep-fry.png", 200, 200, dirpath=img_path), tags=("fry-1"))
        self.item_dict["fry-2"] = self.c.create_image(1000, self.cs[1]-200, anchor="sw", image=tk_image(
            "deep-fry.png", 200, 200, dirpath=img_path), tags=("fry-2"))
        # refrigerator
        self.c.create_image(self.cs[0], self.cs[1]-200, anchor="se", image=tk_image(
            "refrigerator.png", 180, dirpath=img_path), tags=("refrigerator"))
        self.c.tag_bind("refrigerator", "<Button-1>", lambda e: self.__open_refrigerator())
        # trash bin
        self.item_dict["trash_bin"] = self.c.create_image(self.cs[0], self.cs[1], anchor="se", image=tk_image(
            "trash-bin.png", 150, dirpath=img_path), tags=("trash_bin"))
        # recipe
        self.c.create_image(self.cs[0]-30, self.cs[1]-200-250, anchor="se", image=tk_image(
            "recipe.png", 80, dirpath=img_path), tags=("recipe"))
        self.c.tag_bind("recipe", "<Button-1>", lambda e: self.__open_recipe())
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

    def __clear_hand(self):
        # if self.main.Player.hand:
        #     self.c.delete(self.main.Player.hand.id_)
        self.main.Player.hand = None
        self.c.delete("pick")
        

    def __create_label(self):
        frame = making_widget("Frame")(self.c)
        self.c.create_window(self.cs[0]-30, 10, anchor="ne", window=frame)

        self.time_label = making_widget("StringVar")(value="")
        making_widget("Label")(frame, font=font_get(30), textvariable=self.time_label).pack()
        self.money_label = making_widget("StringVar")(value="")
        making_widget("Label")(frame, font=font_get(30), textvariable=self.money_label).pack()
        self.target_label = making_widget("StringVar")(value="")
        making_widget("Label")(frame, font=font_get(30), textvariable=self.target_label, bg="gold").pack()

    def __assemble_assemble(self):
        for name, set_for_mael in Meal.__members__.items():
            t = set([obj.name for obj in self.main.Player.items_state["assemble"]])
            if t == set(set_for_mael.value):
                self.c.delete("in-assemble")
                self.main.Player.items_state["assemble"].clear()
                self.main.Player.is_assemble = True
                f = create_food(name, "food")
                a, b = self.c.coords("assemble")
                f.size = 300
                f.position = (a+200, b-200)
                f.create_image(self.c, tags=("in-assemble"))
                self.main.Player.items_state["assemble"].append(f)
                
                    
    def __clear_assemble(self):
        if self.main.Player.items_state["assemble"]:
            play_sound("trash")
            for order in self.main.Player.items_state["assemble"]:
                if order.path  == "food":
                    self.main.Player.money -= self.main.cost.get() * len(eval(f'Meal.{reverse_name_value("food", order.name)}.value'))
                else:
                    
                    self.main.Player.money -= self.main.cost.get()
            self.main.Player.items_state["assemble"].clear()
            self.c.delete("in-assemble")
            

    def __open_recipe(self):
        win = new_window("Recipe", "recipe.ico", (750, self.cs[1]))
        c = making_widget("Canvas")(win, width=1000, height=self.cs[1], bg="#fffec8")
        c.pack()
        c.bind('<MouseWheel>', lambda event: c.yview_scroll(-(event.delta//120), 'units'))
        count = 0
        for name, obj in Meal.__members__.items():
            c.create_rectangle(0, (300+30)*count, measure(eval(f"_Food.{name}"), 21), (300+30)*count+30,
                               width=2, fill="#ffcbd3")
            c.create_text(0, (300+30)*count, text=eval(f"_Food.{name}"), anchor="nw", font=font_get(21))
            
            f = create_food(name, "food")
            f.size = 300
            f.position = (0, 30+330*count)
            f.create_image(c, anchor="nw")
            count_inner = 0
            c.create_line(0, 330*(count+1), 750, 330*(count+1), width=3, fill="#ffcbd3")
            
            for ingredient in obj.value:
                num = None
                if ingredient[-1] in "01234":
                    num = int(ingredient[-1])
                    ingredient = ingredient[:-1]
                    
                try:
                    f = create_food(
                        reverse_name_value("food", ingredient), "iron", num
                    )
                    f.size = 150
                    f.position = (300+(count_inner%3)*150, (300+30)*count+150*(count_inner//3))
                    f.create_image(c, anchor="nw")
                    
                except:
                    f = create_food(
                        reverse_name_value("food", ingredient), "single", num
                    )
                    f.size = 150
                    f.position = (300+(count_inner%3)*150, (300+30)*count+150*(count_inner//3))
                    f.create_image(c, anchor="nw")
                count_inner += 1
                    
                


            count += 1
        c['scrollregion'] = (
            0, 0, 800,(300+30)*count
        )
        c.create_line(304, 0, 304, (300+30)*count, width=6, fill="#ffcbd3")
        win.grab_set()


    def __open_refrigerator(self):
        def press(name):
            frame_id = c.find_withtag("frame")
            for id in frame_id:
                c.itemconfig(id, state="hidden")
            c.itemconfig(f"{name}-frame", state="normal")
        
        def double_press(f):
            if self.main.Player.only_for_customer:
                win.destroy()
                return 
            self.__clear_hand()
            self.main.Player.hand = f
            f.size = 90
            f.position = (2, 30)
            f.create_image(self.c, anchor="nw", tags=("pick"))
            if f.path == "drink":
                self.main.Player.only_for_customer = True

            win.destroy()
        
        win = new_window("Refrigerator", "refrigerator.ico", (1000, 600))
        c = making_widget("Canvas")(win, width=1000, height=600, bg="lightblue")
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
                lkl = False
                name = filename[0:filename.rfind(".")]
                if name[-1] in "123456789":
                    continue
                if filename in ("egg0.png"):
                    continue
                if name[-1] == "0":
                    lkl = True
                    name = name[:-1]
                if column == 5:
                    column = 0
                    row += 1
                food = create_food(reverse_name_value("food", name), reverse_name_value("path", dir), 0 if lkl else None)
                food.position = 200*column, 60*count+(200+40)*row
                food.size = 200
                food.create_image(c, anchor="nw", tags=(reverse_name_value("food", name)))
                
                c.create_text(200*column+100, 60*count+(200+40)*row+200, text=name, anchor="n", font=font_get(font_size_name), 
                              tags=(filename, ))
                c.create_rectangle(200*column, 60*count+(200+40)*row, 
                                   200*(column+1), 60*count+(200+40)*(row+1), outline="#ff6b87", width=5, state="hidden", 
                                   tags=(f"{filename}-frame", "frame"))
                column += 1
                c.tag_bind(reverse_name_value("food", name), "<Button-1>", lambda e, n=filename: press(n))
                c.tag_bind(reverse_name_value("food", name), "<Double-Button-1>", lambda e, f=food: double_press(f))
                
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
       
        self.main.Player.refresh()
        # customer clear
        self.main.Customer.refresh()
        self.main.Customer.random_priority()
        self.item_dict = {}
        self.__create_items_image()
        self.__create_label()
        self.config_label("money", self.main.Player.money)
        self.config_label("target", self.arguments["target"])
        self.real_clock = time.time()
        

        # bind 
        self.main.root.bind("<Button-1>", self.__identifier)
        self.main.root.bind("<Double-Button-1>", self.__double_identifier)

        
    def __identifier(self, e):
        # hand with ingredient from refrigerator
        h = self.main.Player.hand
        print(h)
        assemble = False 
        change = dict(zip(self.item_dict.values(), self.item_dict.keys()))
        for id_ in self.c.find_overlapping(e.x, e.y, e.x+1, e.y+1):
            if id_ in change:
                touch = change[id_]
                break
        else:
            return  
        if self.main.Player.only_for_customer:
            if touch.startswith("trash"):
                print(self.main.cost.get(), "s")
                play_sound("trash")
                order = self.main.Player.hand 
                if order.path in ("drink", "deep-fry"):
                    self.main.Player.money -= self.main.cost.get()
                else:
                    self.main.Player.money -= self.main.cost.get() * len(eval(f'Meal.{reverse_name_value("food", order.name)}.value'))
                self.__clear_hand()
              
            
                self.main.Player.only_for_customer = False
                return 

        if touch.startswith("assemble"):
            assemble = True
        if (h) and (not self.main.Player.only_for_customer):
          
            
            
            
            if h.can_something(touch[0:-2] if touch[-1] in "123456789" else touch):
                # iron
                
                if touch.startswith("iron"):
                    if self.main.Player.items_state[touch]:
                        play_sound("wrong")
                        return 
                    if h.name == "egg":
                        h.name = "egg0"
                    a, b = self.c.coords(touch)
                    h.size = 150
                    h.position = (a+100, b-100)
                    h.create_image(self.c)
                    self.main.Player.items_state[touch] = h
                    h.build_time = time.time()
                elif touch.startswith("fry"):
                    if self.main.Player.items_state[touch]:
                        play_sound("wrong")
                        return 
                    a, b = self.c.coords(touch)
                    h.size = 150
                    h.position = (a+100, b-100)
                    h.create_image(self.c)
                    self.main.Player.items_state[touch] = h
                    h.build_time = time.time()
                    
                elif touch.startswith("assemble"):
                    if len(self.main.Player.items_state[touch]) >= 6:
                        play_sound("wrong")
                        return 
                    if self.main.Player.is_assemble:
                        return
                    self.main.Player.items_state[touch].append(h)
                    num = len(self.main.Player.items_state["assemble"]) - 1
                    a, b = self.c.coords(touch)
                    h.size = 120
                    h.position = (a+80+120*(num%3), b-400+90+150*(num//3))
                    h.create_image(self.c, tags=("in-assemble"))
                    

                elif touch.startswith("trash"):
                    play_sound("trash")
                    self.main.Player.money -= self.main.cost.get()
                    print(self.main.cost.get())
                self.__clear_hand()
                
                    

            else:
                play_sound("wrong")
        if assemble:
            if self.main.Player.only_for_customer:
                return 
            if self.main.Player.is_assemble:
                if self.main.Player.hand:
                    return 
                f = self.main.Player.items_state["assemble"][0]
                self.c.delete(f.id_)
                f.size = 90
                f.position = (2, 30)
                f.create_image(self.c, anchor="nw", tags=("pick"))
                self.main.Player.items_state["assemble"].clear()
                self.main.Player.hand = f
                self.main.Player.only_for_customer = True
                self.main.Player.is_assemble = False
        else:
            # nothing
            pass

    
    def __double_identifier(self, e):
        change = dict(zip(self.item_dict.values(), self.item_dict.keys()))
        for id_ in self.c.find_overlapping(e.x, e.y, e.x+1, e.y+1):
            if id_ in change:
                touch = change[id_]
                break
        else:
            return 
        if not ((touch.startswith("iron")) or (touch.startswith("fry"))):
            return 

        i = self.main.Player.items_state[touch]
        if touch.startswith("iron"):
            if i:
                if i.is_over:
                    self.c.delete(i.id_)
                    self.main.Player.items_state[touch] = None
                    play_sound("trash")
                    self.main.Player.money -= self.main.cost.get()
                elif i.is_done:
                    if self.main.Player.is_assemble:
                        return 
                    self.c.delete(i.id_)
                    self.main.Player.items_state[touch] = None
                    self.main.Player.items_state["assemble"].append(i)
                    num = len(self.main.Player.items_state["assemble"]) - 1
                    a, b = self.c.coords("assemble")
                    i.size = 120
                    i.position = (a+80+120*(num%3), b-400+90+150*(num//3))
                    i.create_image(self.c, tags=("in-assemble"))
                    
                else:
                    pass
        elif touch.startswith("fry"):
            if i:
                if i.is_over:
                    self.c.delete(i.id_)
                    self.main.Player.items_state[touch] = None
                    play_sound("trash")
                    self.main.Player.money -= self.main.cost.get()
                elif i.is_done:
                    if self.main.Player.only_for_customer:
                        return 
                    if self.main.Player.hand:
                        return 
                    self.main.Player.items_state[touch] = None
                    self.c.delete(i.id_)
                    i.size = 90
                    i.position = (2, 30)
                    i.create_image(self.c, anchor="nw", tags=("pick"))
                    self.main.Player.hand = i
                    self.main.Player.only_for_customer = True
                else:
                    pass
        
        
        
        
       
    
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
            self.config_label("money", self.main.Player.money)
        if t - self.timer_for_customer >= self.main.customerFrequency.get():
            # refresh customer
            self.main.Customer.check(t, self.arguments["patience"]/5)
            self.timer_for_customer = t

            # food
            for key, value in self.main.Player.items_state.items():
                if (key.startswith("iron")) or (key.startswith("fry")):
                    if value:
                        if (t - value.build_time > self.main.doneTime.get()) and (not value.is_done):
                            value.is_done = True
                            self.c.delete(value.id_)
                            value.done()
                            value.create_image(self.c)
                        if (t - value.build_time > self.main.overTime.get()) and (not value.is_over):
                            value.is_over = True
                            self.c.delete(value.id_)
                            value.over()
                            value.create_image(self.c)

        
        
        remain = int(self.arguments["countdown"] - (time.time() - self.real_clock))
        self.config_label("time", remain)
        if remain <= 0:
            self.main.End.enter()




