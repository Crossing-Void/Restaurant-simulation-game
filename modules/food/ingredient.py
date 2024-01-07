from Tkinter_template.Assets.image import tk_image


class Ingredient:
    def __init__(self, name, path) -> None:
        self.name = name
        self.path = path

    def to_image(self, size: int):
        return tk_image(self.name, size, size, dirpath=self.path)
