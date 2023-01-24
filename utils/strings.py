def is_positive_number(value):
    try:
        number_string = float(value)

    except ValueError:
        return False

    return number_string > 0


# se number_string for convertido para float, posso
# checar se ele é maior q 0
# se não for maior q 0 ou string/ValueError, retorna False

# se voce quiser ver qual erro ele pode gerar:
# except Exception as i:
# print(e.__class__.__name__)
