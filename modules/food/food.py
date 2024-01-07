from modules.food.ingredient import Ingredient
import enum

class Food(Ingredient):
    def __init__(self, name, path) -> None:
        super().__init__(name, path)
    
    @classmethod
    def create(cls, genre: str):
        pass


img_path = "images\\food\\food"

# object
