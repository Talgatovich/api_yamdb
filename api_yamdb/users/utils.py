def find_length(value):
    """
    Находит элемент в списке кортежей с максимальной длиной
    """
    sort_value = sorted(value, key=lambda b: len(b[0]))[-1]
    result = len(sort_value[0])
    return result
