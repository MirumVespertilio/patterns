"""
Модели данных для кофейни "PATTERN"
Содержит: Beverage (напитки), BeverageDecorator (декораторы), Order (заказ)
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


# ============================================================================
# БАЗОВЫЙ КЛАСС НАПИТКА
# ============================================================================

class Beverage(ABC):
    """
    Абстрактный базовый класс для всех напитков.
    Реализует паттерн Component для паттерна Decorator.
    """
    
    @abstractmethod
    def get_description(self) -> str:
        """Возвращает описание напитка"""
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        """Возвращает стоимость напитка"""
        pass
    
    def to_dict(self) -> dict:
        """Сериализация напитка в словарь (для JSON)"""
        return {
            "description": self.get_description(),
            "cost": self.get_cost()
        }


# ============================================================================
# КОНКРЕТНЫЕ НАПИТКИ
# ============================================================================

class Coffee(Beverage):
    """Кофе — базовый напиток"""
    
    def __init__(self):
        self._description = "Кофе"
        self._cost = 150.0
    
    def get_description(self) -> str:
        return self._description
    
    def get_cost(self) -> float:
        return self._cost


class Tea(Beverage):
    """Чай — базовый напиток"""
    
    def __init__(self):
        self._description = "Чай"
        self._cost = 100.0
    
    def get_description(self) -> str:
        return self._description
    
    def get_cost(self) -> float:
        return self._cost


class Latte(Beverage):
    """Латте — кофейный напиток с молоком"""
    
    def __init__(self):
        self._description = "Латте"
        self._cost = 200.0
    
    def get_description(self) -> str:
        return self._description
    
    def get_cost(self) -> float:
        return self._cost


class Cappuccino(Beverage):
    """Капучино — кофейный напиток с молочной пенкой"""
    
    def __init__(self):
        self._description = "Капучино"
        self._cost = 180.0
    
    def get_description(self) -> str:
        return self._description
    
    def get_cost(self) -> float:
        return self._cost


# ============================================================================
# АБСТРАКТНЫЙ ДЕКОРАТОР
# ============================================================================

class BeverageDecorator(Beverage):
    """
    Абстрактный декоратор для напитков.
    Реализует паттерн Decorator — динамически добавляет функциональность
    (добавки) к напиткам.
    """
    
    def __init__(self, beverage: Beverage):
        self._beverage = beverage
    
    @abstractmethod
    def get_description(self) -> str:
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        pass


# ============================================================================
# КОНКРЕТНЫЕ ДЕКОРАТОРЫ (ДОБАВКИ)
# ============================================================================

class MilkDecorator(BeverageDecorator):
    """Декоратор: добавляет молоко к напитку"""
    
    def __init__(self, beverage: Beverage):
        super().__init__(beverage)
        self._addition_cost = 30.0
        self._addition_name = "Молоко"
    
    def get_description(self) -> str:
        return f"{self._beverage.get_description()}, {self._addition_name}"
    
    def get_cost(self) -> float:
        return self._beverage.get_cost() + self._addition_cost


class SyrupDecorator(BeverageDecorator):
    """Декоратор: добавляет сироп к напитку (с выбором вкуса)"""
    
    # Доступные вкусы сиропа
    FLAVORS = {
        "1": "ванильный",
        "2": "карамельный"
    }
    
    def __init__(self, beverage: Beverage, flavor: str = "ванильный"):
        super().__init__(beverage)
        self._addition_cost = 40.0
        self._flavor = flavor
        self._addition_name = f"Сироп {flavor}"
    
    def get_description(self) -> str:
        return f"{self._beverage.get_description()}, {self._addition_name}"
    
    def get_cost(self) -> float:
        return self._beverage.get_cost() + self._addition_cost


class CreamDecorator(BeverageDecorator):
    """Декоратор: добавляет взбитые сливки к напитку"""
    
    def __init__(self, beverage: Beverage):
        super().__init__(beverage)
        self._addition_cost = 50.0
        self._addition_name = "Взбитые сливки"
    
    def get_description(self) -> str:
        return f"{self._beverage.get_description()}, {self._addition_name}"
    
    def get_cost(self) -> float:
        return self._beverage.get_cost() + self._addition_cost


# ============================================================================
# КЛАСС ЗАКАЗА
# ============================================================================

class Order:
    """
    Класс заказа.
    Содержит список напитков и методы для работы с ними.
    """
    
    def __init__(self, order_id: int):
        self._order_id = order_id
        self._beverages: List[Beverage] = []
        self._created_at = datetime.now()
    
    @property
    def order_id(self) -> int:
        return self._order_id
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def beverages(self) -> List[Beverage]:
        return self._beverages.copy()
    
    def add_beverage(self, beverage: Beverage) -> None:
        """Добавляет напиток в заказ"""
        self._beverages.append(beverage)
    
    def get_total(self) -> float:
        """Возвращает общую стоимость заказа"""
        return sum(beverage.get_cost() for beverage in self._beverages)
    
    def get_beverages_count(self) -> int:
        """Возвращает количество напитков в заказе"""
        return len(self._beverages)
    
    def get_receipt(self) -> str:
        """Формирует чек заказа"""
        lines = []
        lines.append(f"Заказ #{self._order_id}")
        lines.append(f"Дата: {self._created_at.strftime('%d.%m.%Y %H:%M')}")
        lines.append("-" * 40)
        
        for i, beverage in enumerate(self._beverages, 1):
            lines.append(f"  {i}. {beverage.get_description()} — {beverage.get_cost():.0f}₽")
        
        lines.append("-" * 40)
        lines.append(f"  ИТОГО: {self.get_total():.0f}₽")
        
        return "\n".join(lines)
    
    def to_dict(self) -> dict:
        """Сериализация заказа в словарь (для JSON)"""
        return {
            "order_id": self._order_id,
            "created_at": self._created_at.isoformat(),
            "beverages": [beverage.to_dict() for beverage in self._beverages],
            "total": self.get_total()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Order':
        """
        Десериализация заказа из словаря.
        Примечание: восстанавливает только базовую информацию о напитках.
        """
        order = cls.__new__(cls)
        order._order_id = data["order_id"]
        order._created_at = datetime.fromisoformat(data["created_at"])
        order._beverages = []
        
        # Восстанавливаем напитки как простые объекты с описанием и ценой
        for bev_data in data["beverages"]:
            # Создаём "плоский" напиток для отображения истории
            flat_beverage = FlatBeverage(
                bev_data["description"], 
                bev_data["cost"]
            )
            order._beverages.append(flat_beverage)
        
        return order


class FlatBeverage(Beverage):
    """
    "Плоский" напиток для десериализации.
    Используется при загрузке заказов из файла.
    """
    
    def __init__(self, description: str, cost: float):
        self._description = description
        self._cost = cost
    
    def get_description(self) -> str:
        return self._description
    
    def get_cost(self) -> float:
        return self._cost
