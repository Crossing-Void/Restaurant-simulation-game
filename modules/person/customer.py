from modules.food.food import create_food, reverse_name_value, Meal
from Tkinter_template.Assets.soundeffect import play_sound
from Tkinter_template.Assets.image import tk_image
import random
import time
import os

    
class Customer:
    objects = []

    def __init__(self, main) -> None:
        self.main = main
        self.c = self.main.canvas
        self.cs = self.main.canvas_side
        # create customer
        for i in range(1, 4):
            self.__class__.objects.append(
                _customer(i)
            )
    
    def refresh(self):
        for obj in self.__class__.objects:
            obj.refresh()
    
    
    def random_priority(self):
        num = random.randint(0, len(self.__class__.objects)-1)
        self.__class__.objects[num].priority = True

    def press(self, id_):
        if not self.main.Player.only_for_customer:
            return 
        for ii in range(2):
            order, state = self.__class__.objects[id_-1].order[ii]
            if (self.main.Player.hand == order) and (not state):
                # create image
                self.c.delete(order.id_)
                self.c.delete(self.main.Player.hand.id_)
                self.main.Player.hand = None
                self.main.Player.only_for_customer = False
                self.__class__.objects[id_-1].order[ii][1] = True
               
                order.size = int((self.cs[1]-670)/1.3)
                a, b = self.c.coords(f"table-{id_}")
                order.position = (a-100, b+(self.cs[1]-670)/2) if not(ii) else (a+100, b+(self.cs[1]-670)/2)
                order.create_image(self.c)
                break
        # all success
        for order, state in self.__class__.objects[id_-1].order:
            if not state:
                break
        else:
            play_sound("correct")
            for order, state in self.__class__.objects[id_-1].order:
                if order.path in ("drink", "deep-fry"):
                    self.main.Player.money += self.main.price.get()
                else:
                    
                    self.main.Player.money += self.main.price.get() * len(eval(f'Meal.{reverse_name_value("food", order.name)}.value'))
            # eat food
            self.__class__.objects[id_-1].satisfy_time = time.time()
            self.__class__.objects[id_-1].eating_second = random.randint(self.main.eatTime_0.get(), self.main.eatTime_1.get())
            self.__class__.objects[id_-1].is_satisfy = True
            for i in range(1, 6):
                self.c.delete(f"heart-{id_}-{i}")
            a, b = self.c.coords(f"customer-{id_}")
            self.c.delete(f"customer-{id_}")
            self.c.create_image(a, b, image=self.__class__.objects[id_-1].get_image2(200), anchor="s", 
                                tags=(f"customer-{id_}"))
            
            
            
        

    def check(self, t, unit):
        for obj in self.__class__.objects.copy():
            if obj.is_satisfy:
                print(t, obj.satisfy_time, obj.eating_second)
                if t - obj.satisfy_time > obj.eating_second:
                    # clear
                    self.c.tag_unbind(f"customer-{obj.id}", "<Button-1>")
                    self.c.delete(f"customer-{obj.id}")
                    self.__class__.objects.remove(obj)
                    self.__class__.objects.insert(obj.id-1, _customer(obj.id))
                    for order in obj.order:
                        self.c.delete(order[0].id_)
                return 
            if obj.exists:
                remain = 5 - (t - obj.time) // unit
                for i in range(5, int(remain), -1):
                    self.c.delete(f"heart-{obj.id}-{i}")
                
                if remain <= 0:
                    self.c.tag_unbind(f"customer-{obj.id}", "<Button-1>")
                    self.c.delete(f"customer-{obj.id}")
                    self.__class__.objects.remove(obj)
                    self.__class__.objects.insert(obj.id-1, _customer(obj.id))
                    for order in obj.order:
                        self.c.delete(order[0].id_)
                    play_sound("left")
                    self.main.Player.money -= self.main.leftMinus.get()
                continue
            
            obj.count += 1
            if (random.randint(1, 100) <= obj.__class__.probability[obj.count]) or (obj.priority):
                # success 
                
                obj.exists = True
                obj.time = time.time()
                a, b = self.c.coords(f"table-{obj.id}")
                self.c.create_image(a, b, image=obj.get_image(200), anchor="s", tags=(f"customer-{obj.id}"))

                aa = os.listdir("images\\food\\food") + os.listdir("images\\food\\deep-fry") +\
                  os.listdir("images\\food\\drink")
                result = random.choices(aa, k=2)
                position2 = [(a-60, b-150), (a+60, b-150)]
                count = 0
            
                
                for order in result:
                    order = order[0:order.rfind(".")]
                    if order[-1] in "01234":
                        order = order[0:-1]
                    
                    try:
                        f = create_food(reverse_name_value("food", order), "drink")
                        f.size = 80
                        f.position = position2[count]
                        f.create_image(self.c, anchor="e" if count == 0 else "w")
                        obj.order.append([f, False])
                    except:
                        try:
                            
                            f = create_food(reverse_name_value("food", order), "food")
                            f.size = 80
                            f.position = position2[count]
                            f.create_image(self.c, anchor="e" if count == 0 else "w")
                            obj.order.append([f, False])
                        except:
                            
                            f = create_food(reverse_name_value("food", order), "deep_fry", 1)
                            f.size = 80
                            f.position = position2[count]
                            f.create_image(self.c, anchor="e" if count == 0 else "w")
                            obj.order.append([f, False])
                   
                    count += 1
              


                for i in range(1, 6):
                    self.c.create_image(a+(i-3)*25, 0, anchor="n", image=tk_image(
                        "heart.png", 25, 25, dirpath="images\\items"
                    ), tags=(f"heart-{obj.id}-{i}"))
                self.c.tag_bind(f"customer-{obj.id}", "<Button-1>", lambda e, i=obj.id: self.press(i))
    
    
    
class _customer:
    probability = (6, ) * 8 + (12, ) * 10 + (15, ) * 15 + (100, )

    def __init__(self, id_) -> None:
        self.id = id_
        self.__priority = False
        self.order = []
        self.is_satisfy = False
        self.refresh()
    
    @property
    def priority(self):
        return self.__priority
    
    @priority.setter
    def priority(self, value):
        if type(value) != bool:
            raise ValueError(f"Property priority must be in bool value, but got {type(value)}")
        self.__priority = value

    def refresh(self):
        self.exists = False
        self.count = -1
        self.order = []
        self.time = None
        self.satisfy_time = None
        self.eating_second = None
        self.is_satisfy = False

    def create(self):
        pass
    def get_image(self, size):
        return tk_image("customer.png", size, size, dirpath="images\\items")
    
    def get_image2(self, size):
        return tk_image("customer_satisfy.png", size, size, dirpath="images\\items")