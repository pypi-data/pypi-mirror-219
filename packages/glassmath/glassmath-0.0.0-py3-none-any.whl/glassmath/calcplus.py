# mathplus.py

class arithmetic:
    @staticmethod
    def addition(x, y):
        return x + y

    @staticmethod
    def subtraction(x, y):
        return x - y

    @staticmethod
    def multiplication(x, y):
        return x * y

    @staticmethod
    def division(x, y):
        return x / y

    @staticmethod
    def exponentiation(x, y):
        return x ** y

class trigonometry:
    @staticmethod
    def sin(x):
        return arithmetic.sin(x)

    @staticmethod
    def cos(x):
        return arithmetic.cos(x)

    @staticmethod
    def tan(x):
        return arithmetic.tan(x)

    @staticmethod
    def arcsin(x):
        return arithmetic.arcsin(x)

    @staticmethod
    def arccos(x):
        return arithmetic.arccos(x)

    @staticmethod
    def arctan(x):
        return arithmetic.arctan(x)

    @staticmethod
    def opposite(x):
        return x

    @staticmethod
    def adjacent(x):
        return arithmetic.square_root(arithmetic.subtraction(1, arithmetic.exponentiation(x, 2)))

    @staticmethod
    def hypotenuse(x):
        return arithmetic.square_root(arithmetic.addition(1, arithmetic.exponentiation(x, 2)))

class comparisons:
    @staticmethod
    def equal(x, y):
        return x == y

    @staticmethod
    def not_equal(x, y):
        return x != y

    @staticmethod
    def greater_than(x, y):
        return x > y

    @staticmethod
    def greater_than_equal(x, y):
        return x >= y

    @staticmethod
    def less_than(x, y):
        return x < y

    @staticmethod
    def less_than_equal(x, y):
        return x <= y

class logical:
    @staticmethod
    def and_(x, y):
        return x and y

    @staticmethod
    def or_(x, y):
        return x or y

    @staticmethod
    def not_(x):
        return not x

class other:
    @staticmethod
    def modulo(x, y):
        return x % y

    @staticmethod
    def floor_division(x, y):
        return x // y

    @staticmethod
    def square_root(x):
        return arithmetic.exponentiation(x, 0.5)

    @staticmethod
    def gcd(x, y):
        while y != 0:
            x, y = y, x % y
        return x

    @staticmethod
    def lcm(x, y):
        return abs(x * y) // other.gcd(x, y)

    @staticmethod
    def cube_root(x):
        return x ** (1/3)

    @staticmethod
    def root(x, power):
        return x ** (1/power)

class statistics:
    @staticmethod
    def mean(numbers):
        return arithmetic.division(sum(numbers), len(numbers))

    @staticmethod
    def median(numbers):
        sorted_numbers = sorted(numbers)
        length = len(sorted_numbers)
        if length % 2 == 0:
            middle = length // 2
            return arithmetic.division(arithmetic.addition(sorted_numbers[middle - 1], sorted_numbers[middle]), 2)
        else:
            middle = length // 2
            return sorted_numbers[middle]

    @staticmethod
    def mode(numbers):
        counts = {}
        for num in numbers:
            counts[num] = counts.get(num, 0) + 1
        max_count = max(counts.values())
        mode_nums = [num for num, count in counts.items() if count == max_count]
        return mode_nums

class algebra:
    @staticmethod
    def quadratic_formula(a, b, c):
        discriminant = arithmetic.subtraction(arithmetic.exponentiation(b, 2), arithmetic.multiplication(4, arithmetic.multiplication(a, c)))
        if discriminant > 0:
            root1 = arithmetic.division(arithmetic.subtraction(arithmetic.negative(b), arithmetic.square_root(discriminant)), arithmetic.multiplication(2, a))
            root2 = arithmetic.division(arithmetic.addition(arithmetic.negative(b), arithmetic.square_root(discriminant)), arithmetic.multiplication(2, a))
            return root1, root2
        elif discriminant == 0:
            root = arithmetic.division(arithmetic.negative(b), arithmetic.multiplication(2, a))
            return root
        else:
            return None

class geometry:
    @staticmethod
    def area_of_circle(radius):
        return arithmetic.multiplication(arithmetic.multiplication(trigonometry.pi(), radius), radius)

    @staticmethod
    def perimeter_of_circle(radius):
        return arithmetic.multiplication(arithmetic.multiplication(2, trigonometry.pi()), radius)

    @staticmethod
    def area_of_rectangle(length, width):
        return arithmetic.multiplication(length, width)

    @staticmethod
    def perimeter_of_rectangle(length, width):
        return arithmetic.multiplication(2, arithmetic.addition(length, width))

    @staticmethod
    def area_of_triangle(base, height):
        return arithmetic.division(arithmetic.multiplication(base, height), 2)

    @staticmethod
    def perimeter_of_triangle(side1, side2, side3):
        return arithmetic.addition(arithmetic.addition(side1, side2), side3)

class calculus:
    @staticmethod
    def derivative(func, x, h=1e-6):
        return arithmetic.division(arithmetic.subtraction(func(arithmetic.addition(x, h)), func(x)), h)

    @staticmethod
    def integral(func, a, b, n=1000):
        dx = arithmetic.division(arithmetic.subtraction(b, a), n)
        integral_sum = 0
        for i in range(n):
            x = arithmetic.addition(a, arithmetic.multiplication(i, dx))
            integral_sum = arithmetic.addition(integral_sum, arithmetic.multiplication(func(x), dx))
        return integral_sum

class probability:
    @staticmethod
    def factorial(n):
        if n == 0:
            return 1
        else:
            return arithmetic.multiplication(n, probability.factorial(arithmetic.subtraction(n, 1)))

    @staticmethod
    def permutations(n, r):
        return arithmetic.division(probability.factorial(n), probability.factorial(arithmetic.subtraction(n, r)))

    @staticmethod
    def combinations(n, r):
        return arithmetic.division(probability.permutations(n, r), probability.factorial(r))

class values:
    @staticmethod
    def pi(digits=None):
        if digits is None:
            return 3.141592653589793
        else:
            format_str = f"%.{digits}f"
            return float(format_str % 3.141592653589793)

    @staticmethod
    def e(digits=None):
        if digits is None:
            return 2.718281828459045
        else:
            format_str = f"%.{digits}f"
            return float(format_str % 2.718281828459045)

# Update the mathplus module's namespace with the custom classes and functions
globals().update({
    'arithmetic': arithmetic,
    'trigonometry': trigonometry,
    'comparisons': comparisons,
    'logical': logical,
    'other': other,
    'statistics': statistics,
    'algebra': algebra,
    'geometry': geometry,
    'calculus': calculus,
    'probability': probability,
    'values': values,
}
)

