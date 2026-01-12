import math

def numerical_derivative(func, h=1e-8):
    def dfunc(x):
        return (func(x + h) - func(x - h)) / (2 * h)
    return dfunc


def find_gx_newton(func, dfunc=None, h=1e-8):
    if dfunc is None:
        dfunc = numerical_derivative(func, h)
    
    def gx(x):
        df = dfunc(x)
        if abs(df) < 1e-12:
            raise ValueError("Производная слишком близка к нулю")
        return x - func(x) / df
    return gx


def find_gx_simple(func, alpha=1.0):
    def gx(x):
        return x - alpha * func(x)
    return gx


# def find_gx_steffensen(func):
#     """
#     Возвращает g(x) для метода Стеффенсена (ускоренный метод фиксированной точки):
#     g(x) = x - f(x)^2 / (f(x + f(x)) - f(x))
    
#     Args:
#         func: исходная функция f(x)
    
#     Returns:
#         функция g(x)
#     """
#     def gx(x):
#         fx = func(x)
#         fx_plus = func(x + fx)
#         denominator = fx_plus - fx
#         if abs(denominator) < 1e-12:
#             raise ValueError("Знаменатель слишком близок к нулю")
#         return x - (fx * fx) / denominator
#     return gx


# Пример использования
if __name__ == "__main__":
    # Тестовая функция: f(x) = e^x - x^2
    func = lambda x: math.log(x) - 1
    
    # Автоматическое вычисление производной
    dfunc = numerical_derivative(func)
    print(f"f'(1) = {dfunc(1):.6f} (ожидается 1.0)")

    # print(find_gx_simple(func))
    # Проверка производной в точке x = 0
    # f'(x) = e^x - 2x, f'(0) = 1
    # print(f"f'(0) = {dfunc(0):.6f} (ожидается 1.0)")
    # print(f"f'(1) = {dfunc(1):.6f} (ожидается {math.exp(1) - 2:.6f})")
    
    # # Создание g(x) для метода Ньютона
    # gx_newton = find_gx_newton(func)
    # print(f"\ng(x) Newton при x=0: {gx_newton(0):.6f}")
    
    # # Создание простой g(x)
    # # alpha = auto_find_alpha(func, -1)
    # # print(f"\nОптимальный alpha при x0=-1: {alpha:.6f}")
    # # gx_simple = find_gx_simple(func, alpha)
    # # print(f"g(x) Simple при x=-1: {gx_simple(-1):.6f}")
