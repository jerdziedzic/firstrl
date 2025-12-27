from components.base_component import BaseComponent


class Fighter(BaseComponent):
    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    @property # Getter; just returns HP value
    def hp(self) -> int:
        return self._hp
    
    @hp.setter # Setter; modifies the value as it's set within the method, never <0 or > max_hp
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))