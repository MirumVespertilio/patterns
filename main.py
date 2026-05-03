"""
Кофейня "PATTERN" — точка входа в программу.

Демонстрирует паттерны проектирования:
- Singleton — единый менеджер заказов
- Decorator — компонуемые добавки к напиткам
"""

import sys
import os

# Добавляем текущую директорию в путь для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli import run_cli


def main() -> None:
    """Точка входа в программу"""
    run_cli()


if __name__ == "__main__":
    main()
