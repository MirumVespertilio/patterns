"""
Менеджер заказов с реализацией паттерна Singleton.
Гарантирует, что существует только один экземпляр менеджера на всё приложение.
"""

from typing import List, Optional
from models import Order


class OrderManager:
    """
    Менеджер заказов — реализация паттерна Singleton.

    """
    
    # Приватная переменная класса для хранения единственного экземпляра
    _instance: Optional['OrderManager'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'OrderManager':
        """
        Переопределение __new__ для контроля создания экземпляров.
        Если экземпляр ещё не создан — создаём.
        Если уже существует — возвращаем существующий.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        Инициализация экземпляра.
        Флаг _initialized гарантирует, что инициализация выполняется только один раз.
        """
        if self._initialized:
            return
        
        self._orders: List[Order] = []
        self._next_order_id: int = 1
        OrderManager._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'OrderManager':
        """
        Статический метод для получения единственного экземпляра.
        Это "глобальная точка доступа" из определения Singleton.
        
        Returns:
            OrderManager: единственный экземпляр менеджера заказов
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def reset_instance(cls) -> None:
        """
        Сброс экземпляра (для тестирования).
        В реальном приложении этот метод не используется.
        """
        cls._instance = None
        cls._initialized = False
    
    def get_object_id(self) -> int:
        """
        Возвращает уникальный идентификатор объекта (id в Python).
        Используется для демонстрации Singleton в интерфейсе.
        """
        return id(self)
    
    # ========================================================================
    # МЕТОДЫ РАБОТЫ С ЗАКАЗАМИ
    # ========================================================================
    
    def create_order(self) -> Order:
        """
        Создаёт новый заказ с уникальным ID.
        
        Returns:
            Order: созданный заказ
        """
        order = Order(self._next_order_id)
        self._orders.append(order)
        self._next_order_id += 1
        return order
    
    def get_order(self, order_id: int) -> Optional[Order]:
        """
        Получает заказ по ID.
        
        Args:
            order_id: идентификатор заказа
            
        Returns:
            Order или None, если заказ не найден
        """
        for order in self._orders:
            if order.order_id == order_id:
                return order
        return None
    
    def get_all_orders(self) -> List[Order]:
        """
        Возвращает список всех заказов.
        
        Returns:
            List[Order]: копия списка заказов
        """
        return self._orders.copy()
    
    def get_orders_count(self) -> int:
        """
        Возвращает количество заказов.
        
        Returns:
            int: количество заказов в памяти
        """
        return len(self._orders)
    
    def set_orders(self, orders: List[Order]) -> None:
        """
        Заменяет список заказов (используется при загрузке из файла).
        
        Args:
            orders: новый список заказов
        """
        self._orders = orders.copy()
        # Обновляем следующий ID
        if orders:
            max_id = max(order.order_id for order in orders)
            self._next_order_id = max_id + 1
        else:
            self._next_order_id = 1
    
    def delete_order(self, order_id: int) -> bool:
        """
        Удаляет заказ по ID.
        
        Args:
            order_id: идентификатор заказа для удаления
            
        Returns:
            bool: True если заказ удалён, False если не найден
        """
        for i, order in enumerate(self._orders):
            if order.order_id == order_id:
                self._orders.pop(i)
                return True
        return False
    
    def clear_orders(self) -> None:
        """Очищает все заказы"""
        self._orders.clear()
        self._next_order_id = 1
