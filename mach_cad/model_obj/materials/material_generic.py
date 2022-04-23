__all__ = ["MaterialGeneric"]


class MaterialGeneric:
    def __init__(self, name: str, color="#FE840E"):
        self._name = name
        self._color = color

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

