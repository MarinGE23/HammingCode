import copy

def is_power_of_two(n):
    return (n != 0) and (n & (n - 1) == 0)

# Agrega las casillas de los bits de paridad
def add_places(data):
    extended_data = []
    i = 1
    digit = 0
    while digit < len(data):
        if is_power_of_two(i):
            extended_data.append(-1)
        else:
            extended_data.append(data[digit])
            digit += 1
        i += 1
    return extended_data

# Limpia las casillas de los bits de paridad
def clear_places(extended_data):
    clear_data = copy.deepcopy(extended_data)
    i = 1
    while i < len(clear_data):
        if is_power_of_two(i):
            clear_data[i - 1] = -1
        i += 1
    return clear_data

# Retorna 0 si la cantidad de 1 en la lista es par, 1 si es impar
def is_even(data, parity):
    total = 0
    for i in data:
        if i == 1:
            total += 1
    if parity == "Impar":
        return total % 2
    if total % 2 == 0:
        return 1
    return 0

# Revisa la paridad de los datos para un valor Pn y retorna dicha lista con el
# bit de paridad modificado y con -1 en las casillas vacias
def check_parity(n, data, parity):
    data_to_check = []
    m = pow(2, n - 1)
    i = m - 1
    for x in range(i):
        data_to_check.append(-1)
    while i < len(data):
        j = 0
        while i < len(data) and j < m:
            data_to_check.append(data[i])
            i += 1
            j += 1
        j = 0
        while i < len(data) and j < m:
            data_to_check.append(-1)
            i += 1
            j += 1
    data_to_check[m - 1] = is_even(data_to_check, parity)
    return data_to_check

# Construye la matriz de paridad segun el codigo hamming
def get_parity_table(extended_data, parity):
    matrix = []
    n = 1
    while pow(2, n - 1) < len(extended_data):
        matrix.append(check_parity(n, extended_data, parity))
        n += 1
    return matrix

# Retorna el dato final con los bits de paridad respectivos
def final_message(matrix):
    message = []
    for n in range(len(matrix)):
        for i in range(pow(2, n) - 1, len(matrix[n])):
            if matrix[n][i] != -1:
                message.append(matrix[n][i])
            else:
                break
    return message

# Aplica el algoritmo de hamming nuevamente al mensaje con error para comparar
# los bits de paridad donde hay errores
def compare(error_data, parity):
    clear_data = clear_places(error_data)
    new_data = final_message(get_parity_table(clear_data, parity))
    results = []
    bits = []
    n = 1
    while pow(2, n - 1) < len(new_data):
        if error_data[pow(2, n - 1) - 1] != new_data[pow(2, n - 1) - 1]:
            results.append("Error")
            bits.append(1)
        else:
            results.append("Bien")
            bits.append(0)
        n += 1
    return (results, bits)

# Convierte una lista de bits a decimal para encontrar la posicion del error
def position_of_error(binary):
    b = copy.deepcopy(binary)
    decimal = 0
    b.reverse()
    for i in range(len(b)):
        decimal = decimal + pow(2, i) * int(b[i])
    return decimal