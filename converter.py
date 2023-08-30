# Main function, receives a number in hexadecimal and returns error or a list with the conversion to b2, b8 and b10
def hex_to_all(Hex):
    Hex = Hex.upper()
    if len(Hex) == 3:
        if is_hex(Hex):
            b2 = dec_to_base(hex_to_dec(Hex), 2)
            b8 = dec_to_base(hex_to_dec(Hex), 8)
            b10 = dec_to_base(hex_to_dec(Hex), 10)
            return [b2, b8, b10]
    else:
        return []
    
# Valid if a number is hexadecimal and has 3 digits
def is_hex(Hilera):   
    Hilera = Hilera.upper()
    if Hilera == "":
        return True
    if Hilera[0] in "0123456789ABCDEF":
        return is_hex(Hilera[1:])
    else:
        return False
   
# Receive a hexadecimal character and return the decimal equivalent
def get_digit_value(Char):
    Hex = "0123456789ABCDEF"
    return Hex.find(Char)

# Receive a decimal character and return the hexadecimal equivalent
def get_hex_dig(Num):
    Hex = "0123456789ABCDEF"
    return Hex[Num]

# Converts a hexadecimal number to decimal   
def hex_to_dec(Hilera):
    b = 16
    n = len(Hilera)-1
    result = 0
    for x in Hilera:
        result = result+ (get_digit_value(x)*(b**n))
        n = n-1
    return result

# Receives a decimal integer number and converts it to the specified base
def dec_to_base(Numero, Base):
    result = ""
    if (Numero == 0):
        if(Base==2):
            return add_zeros("0")
        else:
            return "0"

    while(Numero!= 0):
        if(Base>11):
            result = str(get_hex_dig(Numero%Base)) + result
        else:
            result = str(Numero%Base) + result
        Numero = Numero//Base

    if(Base==2):
        result = add_zeros(result)
        
    return result 

def add_zeros(Hilera):
    if(len(Hilera)==12):
        return Hilera
    else:
        return add_zeros("0" + Hilera)
        
def str_to_list(Hilera):
    lista = []
    while(Hilera!=""):
        lista.append(int(Hilera[0]))
        Hilera = Hilera[1:]
    return lista