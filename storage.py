"""
Модуль для работы с внешним хранилищем данных (JSON-файл).
Реализует сохранение и загрузку заказов.
"""

import json
import os
from typing import List
from models import Order


class StorageError(Exception):
    """Базовое исключение для ошибок хранилища"""
    pass


class FileNotFoundError(StorageError):
    """Ошибка: файл не найден"""
    pass


class InvalidDataError(StorageError):
    """Ошибка: данные повреждены или имеют неверный формат"""
    pass


def save_orders(orders: List[Order], filepath: str) -> None:
    """
    Сохраняет список заказов в JSON-файл.
    
    Args:
        orders: список заказов для сохранения
        filepath: путь к файлу
        
    Raises:
        StorageError: при ошибке записи
    """
    try:
        # Создаём директорию, если не существует
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Подготовка данных
        data = {
            "coffee_shop": "PATTERN",
            "orders": [order.to_dict() for order in orders],
            "total_orders": len(orders)
        }
        
        # Запись в файл
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    except PermissionError:
        raise StorageError(f"Нет прав для записи в файл: {filepath}")
    except Exception as e:
        raise StorageError(f"Ошибка при сохранении: {str(e)}")


def load_orders(filepath: str) -> List[Order]:
    """
    Загружает список заказов из JSON-файла.
    
    Args:
        filepath: путь к файлу
        
    Returns:
        List[Order]: список загруженных заказов
        
    Raises:
        FileNotFoundError: если файл не найден
        InvalidDataError: если данные повреждены
    """
    # Проверка существования файла
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Проверка структуры данных
        if not isinstance(data, dict):
            raise InvalidDataError("Неверный формат данных")
        
        if "orders" not in data:
            raise InvalidDataError("В файле отсутствует ключ 'orders'")
        
        # Десериализация заказов
        orders = []
        for order_data in data["orders"]:
            try:
                order = Order.from_dict(order_data)
                orders.append(order)
            except KeyError as e:
                raise InvalidDataError(f"Отсутствует обязательное поле: {e}")
            except Exception as e:
                raise InvalidDataError(f"Ошибка при чтении заказа: {e}")
        
        return orders
        
    except json.JSONDecodeError:
        raise InvalidDataError("Файл содержит невалидный JSON")
    except PermissionError:
        raise StorageError(f"Нет прав для чтения файла: {filepath}")
    except InvalidDataError:
        raise
    except Exception as e:
        raise StorageError(f"Ошибка при загрузке: {str(e)}")


def get_default_filepath() -> str:
    """
    Возвращает путь к файлу хранилища по умолчанию.
    
    Returns:
        str: путь к файлу orders.json
    """
    # Путь относительно расположения скрипта
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "data", "orders.json")
