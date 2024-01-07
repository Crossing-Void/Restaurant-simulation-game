# from Tkinter_template.Assets.image import tk_image
from enum import StrEnum, auto


class Food(StrEnum):
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
    steat = "steak"

    cheese = "cheese"
    chocolate_jum = "chocolate jum"
    hamburger_bun = "hamburger bun"
    lettuce = "lettuce"
    peanut_jum = "peanut_jum"
    toast = "toast"
    tomato = "tomato"

class Path(StrEnum):
    deep_fry = "deep-fry"
    drink = "drink"
    food = "food"
    iron = "iron"
    single = "single"

def create_food(genre: str, path: str, suffix :int=None):
    if suffix not in range(4):
        raise ValueError(f"suffix should be in 0~3, but got {suffix}")
    return _Ingredient(
        eval(f"Food.{genre}"), eval(f"Path.{path}")
    )


class _Ingredient:
    def __init__(self, name, path) -> None:
        self.name = name
        self.path = path

    def to_image(self, size: int):
        return tk_image(self.name, size, size, dirpath=self.path)
    
if __name__ == "__main__":
    print(
        eval(f"Path.deep_fry")
    )