# Калькулятор комплексных чисел
# (5-3i) - ( (5+3i) + (10-15i) * (10+3i) )

import operator

print('Введите выражение, значение которого необходимо посчитать\n'
      'Соблюдайте некоторые правила:\n'
      ' - Записывайте число строго в форме (x+yi)\n'
      ' - Ставьте пробелы после записи комплексных чисел и перед/после каждым/каждого знака\n'
      ' - Пример выражения: (5-3i) - ( (5+3i) + (10-15i) * (10+3i) )\n'
      ' - Не делите на ноль (Даже если очень хочется)\n'
      ' - Чтобы выйти из программы введите "exit"')


class Complex:
    def __init__(self, x, y):
        self.a = x
        self.b = y

    def __str__(self):    # Магический метод представления объекта в виде строки
        if self.b > 0:
            if self.a != 0:
                return str(self.a)+'+'+str(self.b)+'i'
            else:
                return str(self.b)+'i'
        elif self.b < 0:
            if self.a != 0:
                return str(self.a) + str(self.b) + 'i'
            else:
                return str(self.b) + 'i'
        elif self.b == 0:
            return str(self.a)

    def __add__(self, other):   # Магический метод сложения
        return Complex(self.a+other.a, self.b+other.b)

    def __sub__(self, other):   # Магический метод вычитания
        return Complex(self.a-other.a, self.b-other.b)

    def __mul__(self, other):   # Магический метод умножения
        return Complex(self.a*other.a-other.b*self.b, self.a*other.b+other.a*self.b)

    def __truediv__(self, other):    # магический метод деления
        if other.b == 0 and other.a == 0:
            print("ERROR: Деление на ноль!\nВыход из программы...")
            input()
            exit(0)
        return Complex((self.a*other.a+self.b*other.b)/(other.a**2+other.b**2), (other.a*self.b-other.b*self.a)/(other.a**2+other.b**2))


def shunting_yard(math_expression):  # Алгоритм сортировочной станции (приведение выражения к обратной польской нотации)
    stack = []
    result = ""  # значение функции (строка, которую возвращает функция)
    vir = math_expression.split(' ')  # разбиение строки на выражения
    operators = {'+', '-', '/', '*', '('}
    for i in range(len(vir)):
        if vir[i] in operators:
            if vir[i] == '+' or vir[i] == '-':
                prior = 2
            if vir[i] == '*' or vir[i] == '/':
                prior = 3
            if vir[i] == '(':
                prior = 1
                stack.append(vir[i])
                continue
            if len(stack) != 0:
                last = stack[- 1]
                if last == "*" or last == "/":
                    lastprior = 3
                if last == "+" or last == "-":
                    lastprior = 2
                if last == "(":
                    lastprior = 1
                while lastprior >= prior:
                    result = result+stack.pop()+" "
                    if len(stack) != 0:
                        last = stack[len(stack)-1]
                        if last == '*' or last == '/':
                            lastprior = 3
                        if last == '+' or last == '-':
                            lastprior = 2
                        if last == '(':
                            lastprior = 1
                    else:
                        break
                if lastprior < prior or len(stack) == 0:
                    stack.append(vir[i])
            else:
                stack.append(vir[i])
        elif vir[i] == ")":
            last = stack[-1]
            while last != '(':
                result = result+stack.pop() + " "
                if len(stack) != 0:
                    last = stack[- 1]
                else:
                    break
            if len(stack) != 0:
                stack.pop()
        else:
            result = result+vir[i]+" "
    while len(stack) != 0:
        result = result+stack.pop()+" "
    return result


def calc(math_expression):
    operators = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
    stack = [complex()]
    math_expression = math_expression.replace('(', ' ')
    math_expression = math_expression.replace(')', ' ')
    for elem in math_expression.split(' '):        # алгоритм считывания и счета данных строки
        if elem in operators:
            o2, o1 = stack.pop(), stack.pop()
            stack.append(operators[elem](o1, o2))
        elif elem:
            plus = 0
            for i in range(len(elem)):
                if elem[i] == '+':
                    plus = 1
                    break
            if plus == 1:
                number = elem.split('+')  # разбиение числа на вещественную и мнимую часть
                if len(number) > 1:
                    if len(number[1].split('i')[0]) == 0:
                        stack.append(Complex(int(number[0]), 1))
                    else:
                        stack.append(Complex(int(number[0]), int(number[1].split('i')[0])))
            elif plus == 0:
                minus = 0
                for i in range(len(elem)):
                    if elem[i] == '-':
                        minus = 1
                        break
                if minus == 1:
                    number = elem.split('-')
                    if len(number) > 1:
                        if len(number[1].split('i')[0]) == 0:
                            stack.append(Complex(int(number[0]), -1))
                        else:
                            stack.append(Complex(int(number[0]), -int(number[1].split('i')[0])))
                else:
                    stack.append(Complex(int(elem), 0))
    return stack.pop()

math_expression = input('Выражение: ')
while math_expression != "exit":
    print("Результат: " + str(calc(shunting_yard(math_expression))))
    math_expression = input("Выражение: ")
