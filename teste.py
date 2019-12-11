from datetime import date, datetime

# a = 21

# a = "0" + str(a)

# a = a[-2:]

# print(a)

def valida_data(data):
    '''Checa se a data inserida é maior que a data atual, logo é inválida'''
    hoje = date.today()
    hoje = int(str(hoje.year) + ("0" + str(hoje.month))[-2:] + ("0" + str(hoje.day))[-2:])
    data = int(data[6:] + data[3:5] + data[0:2])
    return data > hoje

# valida_data("01/12/1999")

def converte_data(data):
    '''converte uma data do tipo DD/MM/AAAA em date
    str -> date'''
    dia = int(data[:2])
    mes = int(data[3:5])
    ano = int(data[6:])
    dataFormatada = date(ano, mes, dia)
    return dataFormatada

print(converte_data("27/02/2019"))