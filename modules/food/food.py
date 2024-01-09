from Tkinter_template.Assets.image import tk_image
from enum import StrEnum, Enum
import os


class _Food(StrEnum):
    french_fries = "french fries"
    nugget = "nugget"
    onion = "onion"

    black_tea = "black tea"
    cola = "cola"
    sprite = "sprite"

    bacon_burger = "bacon burger"
    bacon_toast = "bacon toast"
    beef_burger = "beef burger"
    beef_toast = "beef toast"
    chicken_burger = "chicken burger"
    chicken_toast = "chicken toast"
    chocolate_toast = "chocolate toast"
    peanut_toast = "peanut toast"

    bacon = "bacon"
    chicken = "chicken"
    egg = "egg"
    steak = "steak"

    cheese = "cheese"
    chocolate_jum = "chocolate jum"
    hamburger_bun = "hamburger bun"
    lettuce = "lettuce"
    peanut_jum = "peanut jum"
    toast = "toast"
    tomato = "tomato"

class _Path(StrEnum):
    deep_fry = "deep-fry"
    drink = "drink"
    food = "food"
    iron = "iron"
    single = "single"

class _Ingredient:
    def __init__(self, name, path) -> None:
        self.name = name
        self.path = path
        self.__position = ()
        self.__size = 0
        self.id_ = None
        self.is_done = False
        self.is_over = False
        self.build_time = None

    def __str__(self):
        return f"Ingerdient {self.name}, {self.id_}"
    
    def __eq__(self, value):
        return self.name == value.name
            
    __repr__ = __str__
    
    @property
    def position(self):
        return self.__position
    
    @position.setter
    def position(self, value):
        self.__position = value

    @property
    def size(self):
        return self.__size
    
    @size.setter
    def size(self, value):
        self.__size = value
    
    def done(self):
        self.name = f"{self.name[:-1]}1"
    
    def over(self):
        self.name = f"{self.name[:-1]}2"
    
    def create_image(self, canvas, **option):
        self.id_ = canvas.create_image(*self.__position, image=tk_image(
            f"{self.name}.png", self.__size, self.__size, dirpath=os.path.join("images", "food", self.path)),
        **option)
    
    def can_something(self, genre):
        return (self.name[0:-1] if self.name[-1] in "01234" else self.name) in eval(f"_can_{genre}")
        
_can_iron = (_Food.egg, _Food.bacon, _Food.chicken, _Food.steak)
_can_fry = (_Food.french_fries, _Food.onion, _Food.nugget)
_can_assemble = (_Food.lettuce, _Food.tomato, _Food.toast, _Food.hamburger_bun, _Food.cheese, _Food.chocolate_jum, 
                 _Food.peanut_jum)
_can_drink = (_Food.cola, _Food.sprite, _Food.black_tea)
_can_food = (_Food.beef_burger, _Food.beef_toast, _Food.chicken_burger, 
             _Food.chicken_toast, _Food.bacon_burger, _Food.bacon_toast, 
             _Food.chocolate_toast, _Food.peanut_toast)
_can_trash_bin = _can_assemble + _can_fry + _can_iron + _can_drink + _can_food

class Meal(Enum):
    bacon_burger =    ["bacon1", "cheese", "tomato", "lettuce", "egg1", "hamburger bun"]
    bacon_toast =     ["bacon1", "cheese", "tomato", "lettuce", "egg1", "toast"]
    beef_burger =     ["steak1", "cheese", "tomato", "lettuce", "egg1", "hamburger bun"]
    beef_toast =      ["steak1", "cheese", "tomato", "lettuce", "egg1", "toast"]
    chicken_burger =  ["chicken1", "cheese", "tomato", "lettuce", "egg1", "hamburger bun"]
    chicken_toast =   ["chicken1", "cheese", "tomato", "lettuce", "egg1", "toast"]
    chocolate_toast = ["chocolate jum", "toast"]
    peanut_toast =    ["peanut jum", "toast"]
    
def create_food(genre: str, path: str, suffix :int=None) -> _Ingredient:
    if suffix:
        if suffix not in range(4):
            raise ValueError(f"suffix should be in 0~3, but got {suffix}")
   
    return _Ingredient(
        eval(f"_Food.{genre}") + (str(suffix) if suffix is not None else ""), eval(f"_Path.{path}")
    )
    
def reverse_name_value(genre: str, value):
    if genre not in ("food", "path"):
        raise ValueError(f"genre should be in food or path, but got {genre}")
   
    for name, obj in eval(f"_{genre.capitalize()}.__members__.items()"):
        if obj.value == value:
            return name
    

if __name__ == "__main__":
    
    print(Meal.bacon_burger.value)