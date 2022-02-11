import pickle
from typing import TypeVar, Generic, List
from pydantic import BaseModel
from dataclasses import dataclass


T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: List[T] = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()

    @property
    def isEmpty(self):
        return not self.items

class Test(Generic[T], BaseModel):
    pass

test = Test[int]()
