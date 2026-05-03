"""
CLI интерфейс для кофейни "PATTERN".
Содержит функции для взаимодействия с пользователем.
"""

import sys
import os
from typing import Optional

from models import (
    Beverage, Coffee, Tea, Latte, Cappuccino,
    MilkDecorator, SyrupDecorator, CreamDecorator
)
from manager import OrderManager
from storage import save_orders, load_orders, get_default_filepath, StorageError, FileNotFoundError, InvalidDataError


# ============================================================================
# КОНСТАНТЫ
# ============================================================================

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║                    ☕ КОФЕЙНЯ "PATTERN"                      ║
╠══════════════════════════════════════════════════════════════╣
║  Паттерны проектирования в действии:                         ║
║  • Singleton — единый менеджер заказов                       ║
║  • Decorator — компонуемые добавки к напиткам                ║
╚══════════════════════════════════════════════════════════════╝
"""

MENU_ITEMS = {
    "1": "Создать заказ",
    "2": "Показать все заказы",
    "3": "Удалить заказ",
    "4": "Сохранить заказы в файл",
    "5": "Загрузить заказы из файла",
    "6": "🔬 Демонстрация Singleton",
    "0": "Выход"
}

# Словарь напитков
BEVERAGES = {
    "1": {"class": Coffee, "name": "Кофе", "price": 150},
    "2": {"class": Tea, "name": "Чай", "price": 100},
    "3": {"class": Latte, "name": "Латте", "price": 200},
    "4": {"class": Cappuccino, "name": "Капучино", "price": 180}
}

# Словарь добавок
ADDONS = {
    "1": {"name": "Молоко", "price": 30, "type": "milk"},
    "2": {"name": "Сироп (ванильный)", "price": 40, "type": "syrup_vanilla"},
    "3": {"name": "Сироп (карамельный)", "price": 40, "type": "syrup_caramel"},
    "4": {"name": "Взбитые сливки", "price": 50, "type": "cream"}
}


# ============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================================

def clear_screen() -> None:
    """Очищает экран консоли"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_separator(char: str = "═", length: int = 60) -> None:
    """Выводит разделительную линию"""
    print(char * length)


def print_box(text: str, width: int = 60) -> None:
    """Выводит текст в рамке"""
    lines = text.split('\n')
    print("╔" + "═" * (width - 2) + "╗")
    for line in lines:
        padding = width - 4 - len(line)
        print(f"║  {line}{' ' * padding}  ║")
    print("╚" + "═" * (width - 2) + "╝")


def input_with_validation(prompt: str, valid_options: Optional[list] = None) -> str:
    """
    Запрашивает ввод пользователя с валидацией.
    
    Args:
        prompt: текст приглашения
        valid_options: список допустимых значений (если None — любая строка)
        
    Returns:
        str: введённое значение
    """
    while True:
        try:
            value = input(prompt).strip()
            if valid_options is None:
                return value
            if value in valid_options:
                return value
            print(f"❌ Неверный ввод. Допустимые значения: {', '.join(valid_options)}")
        except EOFError:
            print("\n👋 До свидания!")
            sys.exit(0)
        except KeyboardInterrupt:
            print("\n\n👋 До свидания!")
            sys.exit(0)


def confirm(prompt: str) -> bool:
    """
    Запрашивает подтверждение (да/нет).
    
    Args:
        prompt: текст вопроса
        
    Returns:
        bool: True если "да", False если "нет"
    """
    answer = input_with_validation(f"{prompt} (д/н): ", ["д", "н", "y", "n", "yes", "no"])
    return answer.lower() in ["д", "y", "yes"]


# ============================================================================
# ФУНКЦИИ ИНТЕРФЕЙСА
# ============================================================================

def show_main_menu(manager: OrderManager) -> None:
    """Выводит главное меню"""
    print(BANNER)
    
    # Информация о Singleton
    obj_id = manager.get_object_id()
    orders_count = manager.get_orders_count()
    
    print(f"┌────────────────────────────────────────────────────────────┐")
    print(f"│  📍 Менеджер заказов: singleton #{obj_id:<20}      │")
    print(f"│  📦 Заказов в памяти: {orders_count:<36} │")
    print(f"└────────────────────────────────────────────────────────────┘")
    print()
    
    # Меню
    for key, item in MENU_ITEMS.items():
        print(f"  {key}. {item}")
    print()


def create_order_flow(manager: OrderManager) -> None:
    """Процесс создания нового заказа"""
    order = manager.create_order()
    
    print()
    print_separator("═", 60)
    print(f"  📝 СОЗДАНИЕ ЗАКАЗА #{order.order_id}")
    print_separator("═", 60)
    
    add_more_beverages = True
    
    while add_more_beverages:
        # Выбор напитка
        print("\nВыберите напиток:")
        for key, bev in BEVERAGES.items():
            print(f"  {key}. {bev['name']:<12} — {bev['price']}₽")
        
        choice = input_with_validation("\nВаш выбор: ", list(BEVERAGES.keys()))
        beverage_class = BEVERAGES[choice]["class"]
        beverage: Beverage = beverage_class()
        
        print(f"\n✓ Добавлено: {beverage.get_description()} ({beverage.get_cost():.0f}₽)")
        
        # Добавки
        while True:
            print(f"\nДобавить добавку?")
            for key, addon in ADDONS.items():
                print(f"  {key}. {addon['name']:<20} +{addon['price']}₽")
            print("  0. Готово — больше не добавлять")
            
            addon_choice = input_with_validation("Выбор: ", list(ADDONS.keys()) + ["0"])
            
            if addon_choice == "0":
                break
            
            addon = ADDONS[addon_choice]
            
            # Применяем декоратор
            if addon["type"] == "milk":
                beverage = MilkDecorator(beverage)
            elif addon["type"] == "syrup_vanilla":
                beverage = SyrupDecorator(beverage, "ванильный")
            elif addon["type"] == "syrup_caramel":
                beverage = SyrupDecorator(beverage, "карамельный")
            elif addon["type"] == "cream":
                beverage = CreamDecorator(beverage)
            
            print(f"✓ Добавлено: {addon['name']} (+{addon['price']}₽)")
            print(f"  Текущая цена: {beverage.get_cost():.0f}₽")
        
        # Добавляем напиток в заказ
        order.add_beverage(beverage)
        
        print()
        print_separator("─", 50)
        print(f"☕ {beverage.get_description()} — {beverage.get_cost():.0f}₽")
        print_separator("─", 50)
        
        # Спрашиваем про ещё напитки
        add_more_beverages = confirm("\nДобавить ещё напиток в заказ?")
    
    # Итог по заказу
    print()
    print_box(
        f"✅ ЗАКАЗ #{order.order_id} СОЗДАН!\n\n"
        f"Напитков: {order.get_beverages_count()}\n"
        f"Сумма: {order.get_total():.0f}₽",
        width=50
    )


def show_all_orders(manager: OrderManager) -> None:
    """Показывает все заказы"""
    orders = manager.get_all_orders()
    
    print()
    print_separator("═", 60)
    print("  📋 ВСЕ ЗАКАЗЫ")
    print_separator("═", 60)
    
    if not orders:
        print("\n  📭 Заказов пока нет. Создайте первый заказ!\n")
        return
    
    for order in orders:
        print(f"\n{order.get_receipt()}")
        print()
    
    print_separator("─", 60)
    print(f"  Всего заказов: {len(orders)}")
    total_sum = sum(o.get_total() for o in orders)
    print(f"  Общая сумма: {total_sum:.0f}₽")
    print_separator("─", 60)


def save_to_file(manager: OrderManager) -> None:
    """Сохраняет заказы в файл"""
    orders = manager.get_all_orders()
    
    if not orders:
        print("\n❌ Нет заказов для сохранения.\n")
        return
    
    filepath = get_default_filepath()
    
    try:
        save_orders(orders, filepath)
        print()
        print_box(
            f"✅ ЗАКАЗЫ СОХРАНЕНЫ!\n\n"
            f"Файл: {filepath}\n"
            f"Количество: {len(orders)}",
            width=50
        )
    except StorageError as e:
        print(f"\n❌ Ошибка сохранения: {e}\n")


def load_from_file(manager: OrderManager) -> None:
    """Загружает заказы из файла"""
    filepath = get_default_filepath()
    
    try:
        orders = load_orders(filepath)
        manager.set_orders(orders)
        
        print()
        print_box(
            f"✅ ЗАКАЗЫ ЗАГРУЖЕНЫ!\n\n"
            f"Файл: {filepath}\n"
            f"Количество: {len(orders)}",
            width=50
        )
    except FileNotFoundError:
        print()
        print_box(
            "ℹ️ ФАЙЛ НЕ НАЙДЕН\n\n"
            "Сохранение создаст новый файл.",
            width=50
        )
    except InvalidDataError as e:
        print(f"\n❌ Ошибка данных: {e}\n")
    except StorageError as e:
        print(f"\n❌ Ошибка загрузки: {e}\n")


def delete_order_flow(manager: OrderManager) -> None:
    """Процесс удаления заказа"""
    orders = manager.get_all_orders()
    
    print()
    print_separator("═", 60)
    print("  🗑️ УДАЛЕНИЕ ЗАКАЗА")
    print_separator("═", 60)
    
    if not orders:
        print("\n  📭 Заказов пока нет. Нечего удалять.\n")
        return
    
    # Показываем список заказов
    print("\n  Список заказов:")
    for order in orders:
        print(f"    #{order.order_id} — {order.get_beverages_count()} напитков, {order.get_total():.0f}₽")
    print()
    
    # Запрос ID заказа
    order_id_str = input_with_validation("  Введите ID заказа для удаления (или 0 для отмены): ")
    
    if order_id_str == "0":
        print("\n  ❌ Удаление отменено.\n")
        return
    
    try:
        order_id = int(order_id_str)
    except ValueError:
        print("\n  ❌ Неверный формат ID. Введите число.\n")
        return
    
    # Проверяем существование заказа
    order = manager.get_order(order_id)
    if order is None:
        print(f"\n  ❌ Заказ #{order_id} не найден.\n")
        return
    
    # Подтверждение удаления
    print(f"\n  Заказ #{order_id}:")
    print(f"    Напитков: {order.get_beverages_count()}")
    print(f"    Сумма: {order.get_total():.0f}₽")
    
    if not confirm("\n  Удалить этот заказ?"):
        print("\n  ❌ Удаление отменено.\n")
        return
    
    # Удаление
    if manager.delete_order(order_id):
        print()
        print_box(f"✅ ЗАКАЗ #{order_id} УДАЛЁН!", width=40)
    else:
        print(f"\n  ❌ Ошибка удаления заказа.\n")


def demo_singleton() -> None:
    """
    Демонстрация паттерна Singleton.
    Показывает, что все вызовы возвращают один и тот же объект.
    """
    print()
    print_separator("═", 60)
    print("        🔬 ДЕМОНСТРАЦИЯ ПАТТЕРНА SINGLETON")
    print_separator("═", 60)
    
    print("\n  Паттерн Singleton гарантирует, что у класса есть только")
    print("  один экземпляр, и предоставляет глобальную точку доступа к нему.\n")
    
    print_separator("─", 60)
    print("  Шаг 1: Получаем экземпляр через OrderManager.get_instance()")
    first = OrderManager.get_instance()
    first_id = id(first)
    print(f"         → ID объекта: {first_id}")
    
    print()
    print("  Шаг 2: Ещё раз вызываем OrderManager.get_instance()")
    second = OrderManager.get_instance()
    second_id = id(second)
    print(f"         → ID объекта: {second_id}")
    
    print()
    print("  Шаг 3: Пробуем создать через OrderManager()")
    third = OrderManager()
    third_id = id(third)
    print(f"         → ID объекта: {third_id}")
    
    print()
    print_separator("─", 60)
    print("  Шаг 4: Сравнение объектов")
    print(f"         first is second → {first is second}")
    print(f"         first is third  → {first is third}")
    print(f"         second is third → {second is third}")
    
    print()
    print_separator("═", 60)
    print("  ✅ РЕЗУЛЬТАТ:")
    print("     Все три способа возвращают ОДИН И ТОТ ЖЕ объект!")
    print()
    print("     Это и есть Singleton — гарантия единственного")
    print("     экземпляра класса на всё приложение.")
    print_separator("═", 60)
    
    input("\n  Нажмите Enter, чтобы вернуться в меню...")


def run_cli() -> None:
    """Запускает главный цикл CLI"""
    # Получаем единственный экземпляр менеджера (Singleton)
    manager = OrderManager.get_instance()
    
    while True:
        clear_screen()
        show_main_menu(manager)
        
        choice = input_with_validation("Выберите действие: ", list(MENU_ITEMS.keys()))
        
        if choice == "0":
            print("\n👋 Спасибо за посещение кофейни 'PATTERN'!\n")
            break
        elif choice == "1":
            create_order_flow(manager)
            input("\nНажмите Enter, чтобы продолжить...")
        elif choice == "2":
            show_all_orders(manager)
            input("\nНажмите Enter, чтобы продолжить...")
        elif choice == "3":
            delete_order_flow(manager)
            input("\nНажмите Enter, чтобы продолжить...")
        elif choice == "4":
            save_to_file(manager)
            input("\nНажмите Enter, чтобы продолжить...")
        elif choice == "5":
            load_from_file(manager)
            input("\nНажмите Enter, чтобы продолжить...")
        elif choice == "6":
            demo_singleton()
