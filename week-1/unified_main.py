"""
UNIFIED MAIN FILE
=================
Объединенный главный файл для запуска всех заданий из week-1.
Заменяет все отдельные main файлы единым интерфейсом.

Доступные задания:
- Assignment 1: Решение нелинейных уравнений (Root Finding Methods)
- Assignment 2: Системы линейных уравнений (Linear Systems)
- Assignment 3: Аппроксимация кривых (Curve Fitting)
- Assignment 4.1: Конечные разности (Finite Differences)
- Assignment 4.2: Интерполяция (Interpolation)
- Assignment 5.1: Численное дифференцирование (Numerical Differentiation)
- Assignment 5.2: Численное интегрирование (Numerical Integration)
"""

import sys
import os
import importlib.util

# Получаем текущую директорию
current_dir = os.path.dirname(os.path.abspath(__file__))


def print_main_menu():
    """Отображение главного меню"""
    print("\n" + "="*80)
    print(" "*25 + "COMPUTE MATH - WEEK 1")
    print(" "*20 + "UNIFIED MAIN PROGRAM")
    print("="*80)
    print("\nВыберите задание:")
    print("-"*80)
    print("  1. Assignment 1 - Решение нелинейных уравнений")
    print("     (Bisection, Fixed Point, Newton-Raphson, Secant, False Position)")
    print()
    print("  2. Assignment 2 - Системы линейных уравнений")
    print("     (Cramer, Gaussian, Gauss-Jordan, Jacobi, Gauss-Seidel, SOR)")
    print()
    print("  3. Assignment 3 - Аппроксимация кривых")
    print("     (Linear, Quadratic, Cubic, Exponential, Logarithmic, Power)")
    print()
    print("  4. Assignment 4.1 - Конечные разности")
    print("     (Forward Differences, Backward Differences)")
    print()
    print("  5. Assignment 4.2 - Интерполяция")
    print("     (Lagrange, Newton Forward, Newton Backward)")
    print()
    print("  6. Assignment 5.1 - Численное дифференцирование")
    print("     (Equally Spaced, Unequally Spaced, Extrema Analysis)")
    print()
    print("  7. Assignment 5.2 - Численное интегрирование")
    print("     (Trapezoidal, Simpson's 1/3, Simpson's 3/8)")
    print()
    print("  0. Выход")
    print("="*80)


def load_and_run_main(module_path, module_name):
    """
    Динамически загружает и запускает main() функцию из указанного модуля
    
    Args:
        module_path: Полный путь к файлу main.py
        module_name: Уникальное имя модуля для загрузки
    """
    try:
        # Сохраняем текущую директорию
        original_dir = os.getcwd()
        
        # Переходим в директорию модуля
        module_dir = os.path.dirname(module_path)
        os.chdir(module_dir)
        
        # Добавляем директорию в sys.path
        if module_dir not in sys.path:
            sys.path.insert(0, module_dir)
        
        # Загружаем модуль
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            print(f"\n❌ Ошибка: Не удалось загрузить модуль {module_name}")
            return
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        # Запускаем main функцию
        if hasattr(module, 'main'):
            module.main()
        else:
            print(f"\n❌ Ошибка: В модуле {module_name} не найдена функция main()")
        
    except Exception as e:
        print(f"\n❌ Ошибка при выполнении {module_name}: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Возвращаемся в исходную директорию
        os.chdir(original_dir)


def run_assignment_1():
    """Запуск Assignment 1 - Root Finding Methods"""
    module_path = os.path.join(current_dir, 'assignment-1', 'main.py')
    load_and_run_main(module_path, 'assignment1_main')


def run_assignment_2():
    """Запуск Assignment 2 - Linear Systems"""
    module_path = os.path.join(current_dir, 'assignment-2', 'main.py')
    load_and_run_main(module_path, 'assignment2_main')


def run_assignment_3():
    """Запуск Assignment 3 - Curve Fitting"""
    module_path = os.path.join(current_dir, 'assignment-3', 'main.py')
    load_and_run_main(module_path, 'assignment3_main')


def run_assignment_4_part1():
    """Запуск Assignment 4.1 - Finite Differences"""
    module_path = os.path.join(current_dir, 'assignment-4', 'part-1', 'main.py')
    load_and_run_main(module_path, 'assignment4p1_main')


def run_assignment_4_part2():
    """Запуск Assignment 4.2 - Interpolation"""
    module_path = os.path.join(current_dir, 'assignment-4', 'part-2', 'main.py')
    load_and_run_main(module_path, 'assignment4p2_main')


def run_assignment_5_part1():
    """Запуск Assignment 5.1 - Numerical Differentiation"""
    module_path = os.path.join(current_dir, 'assignment-5', 'part-1', 'main.py')
    load_and_run_main(module_path, 'assignment5p1_main')


def run_assignment_5_part2():
    """Запуск Assignment 5.2 - Numerical Integration"""
    module_path = os.path.join(current_dir, 'assignment-5', 'part-2', 'main.py')
    load_and_run_main(module_path, 'assignment5p2_main')


def main():
    """Главная функция программы"""
    print("\n" + "*"*80)
    print("*" + " "*78 + "*")
    print("*" + " "*20 + "ДОБРО ПОЖАЛОВАТЬ В COMPUTE MATH" + " "*27 + "*")
    print("*" + " "*25 + "Week 1 - Unified Program" + " "*30 + "*")
    print("*" + " "*78 + "*")
    print("*"*80)
    
    while True:
        print_main_menu()
        
        try:
            choice = input("\nВведите номер задания (0-7): ").strip()
            
            if choice == '0':
                print("\n" + "="*80)
                print(" "*25 + "Программа завершена")
                print(" "*20 + "Спасибо за использование!")
                print("="*80 + "\n")
                break
            
            elif choice == '1':
                print("\n" + ">"*80)
                print(">>> Запуск Assignment 1 - Root Finding Methods")
                print(">"*80 + "\n")
                run_assignment_1()
            
            elif choice == '2':
                print("\n" + ">"*80)
                print(">>> Запуск Assignment 2 - Linear Systems")
                print(">"*80 + "\n")
                run_assignment_2()
            
            elif choice == '3':
                print("\n" + ">"*80)
                print(">>> Запуск Assignment 3 - Curve Fitting")
                print(">"*80 + "\n")
                run_assignment_3()
            
            elif choice == '4':
                print("\n" + ">"*80)
                print(">>> Запуск Assignment 4.1 - Finite Differences")
                print(">"*80 + "\n")
                run_assignment_4_part1()
            
            elif choice == '5':
                print("\n" + ">"*80)
                print(">>> Запуск Assignment 4.2 - Interpolation")
                print(">"*80 + "\n")
                run_assignment_4_part2()
            
            elif choice == '6':
                print("\n" + ">"*80)
                print(">>> Запуск Assignment 5.1 - Numerical Differentiation")
                print(">"*80 + "\n")
                run_assignment_5_part1()
            
            elif choice == '7':
                print("\n" + ">"*80)
                print(">>> Запуск Assignment 5.2 - Numerical Integration")
                print(">"*80 + "\n")
                run_assignment_5_part2()
            
            else:
                print("\n❌ Неверный выбор! Введите число от 0 до 7.")
            
            input("\n\nНажмите Enter для возврата в главное меню...")
        
        except KeyboardInterrupt:
            print("\n\n" + "="*80)
            print(" "*20 + "Программа прервана пользователем")
            print("="*80 + "\n")
            break
        
        except Exception as e:
            print(f"\n❌ Непредвиденная ошибка: {e}")
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()
