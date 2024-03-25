from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod


class Observable(ABC):
    _observers: List[Observer] = []
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)


class Observer(ABC):
    @abstractmethod
    def update(self, observable: Observable):
        pass