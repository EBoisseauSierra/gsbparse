from abc import ABCMeta
from dataclasses import dataclass


@dataclass
class Fruit(metaclass=ABCMeta):
    color: str
    yummy: bool


class Apricot(Fruit):
    color: str = "orange"
    yummy: bool = True


class Banana(Fruit):
    color: str = "yellow"
    yummy: bool = True


def make_new_fruit(fruit_class: type[Fruit]) -> Fruit:
    return fruit_class()


my_apricot: Apricot = make_new_fruit(Apricot)
my_banana: Banana = make_new_fruit(Banana)
