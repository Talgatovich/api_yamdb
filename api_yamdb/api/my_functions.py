import random


# Произвольно сгенерировать код проверки функции
def random_code(length=16):
    chars = 'quFDGDbtwehykjahuhufHFCUHNCWEHAFDONCJUHU'
    code = ''
    for x in range(length):
        code += random.choice(chars)
    return code
