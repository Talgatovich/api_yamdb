def find_length(value):
    """
    Находит элемент в списке кортежей с максимальной длиной
    """
    result = max(len(role) for role, _ in value)
    return result
