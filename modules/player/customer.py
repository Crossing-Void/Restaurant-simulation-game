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
        
   
        
    def check(self, t, unit):
        print("--------------------")
        for obj in self.__class__.objects.copy():
            print(obj.id, obj.exists, obj.count, obj.time)
        for obj in self.__class__.objects.copy():
            if obj.exists:
                remain = 5 - (t - obj.time) // unit
                for i in range(5, int(remain), -1):
                    self.c.delete(f"heart-{obj.id}-{i}")
                
                if remain <= 0:
                    self.c.delete(f"customer-{obj.id}")
                    self.__class__.objects.remove(obj)
                    self.__class__.objects.insert(obj.id-1, _customer(obj.id))
                continue
            
            obj.count += 1
            if (random.randint(1, 100) <= obj.__class__.probability[obj.count]) or (obj.priority):
                # success 
                
                obj.exists = True
                obj.time = time.time()
                a, b = self.c.coords(f"table-{obj.id}")
                self.c.create_image(a, b, image=obj.get_image(200), anchor="s", tags=(f"customer-{obj.id}"))

                aa = [("images\\food\\food", x) for x in os.listdir("images\\food\\food")] +\
                [("images\\food\\deep-fry", x) for x in os.listdir("images\\food\\deep-fry") 
                 if x[:x.rfind(".")][-1] == "1"] +\
                [("images\\food\\drink", x) for x in os.listdir("images\\food\\drink")]
                result = random.choices(aa, k=2)
                self.c.create_image(a-60, b-150, image=tk_image(
                    result[0][1], 80, 80, dirpath=result[0][0]
                ), anchor="e", tags=(f"customer-{obj.id}"))
                self.c.create_image(a+60, b-150, image=tk_image(
                    result[1][1], 80, 80, dirpath=result[1][0]
                ), anchor="w", tags=(f"customer-{obj.id}"))
                for i in range(1, 6):
                    self.c.create_image(a+(i-3)*25, 0, anchor="n", image=tk_image(
                        "heart.png", 25, 25, dirpath="images\\items"
                    ), tags=(f"heart-{obj.id}-{i}"))
    
    
    
class _customer:
    probability = (6, ) * 8 + (12, ) * 10 + (15, ) * 15 + (100, )

    def __init__(self, id_) -> None:
        self.id = id_
        self.__priority = False
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
        self.time = None

    def create(self):
        pass
    def get_image(self, size):
        return tk_image("customer.png", size, size, dirpath="images\\items")