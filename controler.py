import random
import mysql.connector
from flask import render_template, make_response
import pdfkit
from datetime import date, datetime, timedelta
#online
'''
config = {
  'user': 'sql10315021',
  'password': 'amqay846Cl',
  'host': 'sql10.freesqldatabase.com',
  'database': 'sql10315021',
  'port': '3306'}
'''

#local
config = {
  'user': 'root',
  'password': 'password',
  'host': '127.0.0.1',
  'database': 'waat',
  'port': '3306'}
con = mysql.connector.connect(**config)
cursor = con.cursor()

def select(fields, tables, where = None):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        query = "SELECT " + fields + " FROM " +tables
        if (where):
            query += " WHERE " + where
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        con.close()


def select_last(id_profissional, id_cliente):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        id_profissional = str(id_profissional)
        id_cliente = str(id_cliente)
        selectionados = id_cliente+', data_consulta, '+id_profissional
        query = "id_cliente = "+id_cliente+ " and id_profissional = " + id_profissional + " FROM atendimentos"
        loc = select("MAX(data_consulta)","atendimentos", "id_cliente = "+id_cliente +" and id_profissional = "+id_profissional)
        query+= "data_consulta = " + str(loc[0][0])
        query+=  "ORDER BY id_cliente, data_consulta;"
        select(selectionados, "atendimentos", )
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        con.close()
        
def exist(cpf, table):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        query = "SELECT COUNT(nome) FROM " + table +" WHERE cpf="+cpf;
        cursor.execute(query)
        return bool(cursor.fetchall()[0][0])
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()

def insert(values, table, fields =None):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        query = "INSERT INTO " +table
        if (fields):
            query += " ("+ fields + ") "
        query += " VALUES " + ",".join(["("+v+")" for v in values])
        cursor.execute(query)
        con.commit()
        
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()


def update(sets, table, where):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        query = "UPDATE " +table
        query += " SET " + ",".join([field+ " = '" + value + "'" for field, value in sets.items()])
        if (where):
            query += " WHERE " + where
        cursor.execute(query)
        con.commit()
    except Exception as e:
        print(e)

    finally:
        cursor.close()
        con.close()

def delete(table, where):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        query = "DELETE FROM "+ table +" WHERE "+where
        cursor.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()


def verifica_id_cliente(id):
    """retorna True se o id_cliente já está cadastrado e False c.c."""
    id = "id_cliente="+str(id)
    id_no_bd = bool(len(select("id_cliente", 'clientes', id)))
    return id_no_bd

def verifica_id_profissional(id):
    """retorna True se o id_profissional já está cadastrado e False c.c."""
    id = "id_profissional="+str(id)
    id_no_bd = bool(len(select("id_profissional", 'profissionais', id)))
    return id_no_bd

def verifica_id_atendimento(id):
    """retorna True se o atendimento já está cadastrado e False c.c."""
    id = "id_atendimento="+str(id)
    id_no_bd = bool(len(select("id_atendimento", 'atendimentos', id)))
    return id_no_bd

def verifica_cpf(cpf, tabela):
    """retorna True se o cpf já está cadastrado e False c.c."""
    cpf = "cpf="+str(cpf)
    cpf_no_db = bool(len(select("cpf", tabela, cpf)))
    return cpf_no_db

def separa_email(email):
    user_mail = email.split('@')[0]
    domain_mail = email.split('@')[1]
    return user_mail, domain_mail
    
def cpf_senha(cpf, tabela):
    """Retorna a senha correspondente ao cpf"""
    cpf = "cpf="+str(cpf)
    senha = select("senha", tabela, cpf)
    return senha[0][0]

def verifica_idade(data_de_nascimento):
    hoje = date.today()
    try:
        nascimento = date(int(data_de_nascimento[6:]),int(data_de_nascimento[3:5]),int(data_de_nascimento[:2]))
    except:
        return "erro"
    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (hoje.month, hoje.day))

    if idade<18:
        return True
    else:
        return False
        
def cpf_id(cpf):
    """Retorna o id correspondente ao cpf"""
    where = "cpf = " + str(cpf)
    id = select("id",'usuarios', where)
    return id[0][0]

def cpf_tipo(cpf, tabela):
    """Retorna o id correspondente ao cpf"""
    cpf = "cpf="+str(cpf)
    tipo = select("tipo", tabela, cpf)
    return tipo[0][0]


def gera_id():
    id_gerado = random.randint(1,100)
    id_no_bd = (verifica_id_cliente(id_gerado) or verifica_id_profissional(id_gerado) or verifica_id_atendimento(id_gerado))
    while id_no_bd:        
        id_gerado = random.randint(1,100)
        id_no_bd = (verifica_id_cliente(id_gerado) or verifica_id_profissional(id_gerado) or verifica_id_atendimento(id_gerado))
    return id_gerado

def email_user(cpf):
    cpf = limpa_cpf(cpf)
    error = None
    if exist(cpf, 'usuarios'):
        error='enviado'
        email = select('email', 'usuarios', 'cpf='+cpf)[0][0]
        return (email,error)
    else:
        error = "Não cadastrado"
        return (None, error)

def ApenasUpdate(cpf, table):
    if exist(limpa_cpf(cpf),'clientes'):
        ApenasUpdate = True  #update
    else:
        ApenasUpdate = False #cadastro normal  

def cadastra_usuario(cpf, nome, email, telefone, data_de_nascimento, senha, tipo):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        user_mail = separa_email(email)[0]
        domain_mail = separa_email(email)[1]
        sql = "INSERT INTO usuarios (id, cpf, nome, email, user_mail, domain_mail, telefone, data_de_nascimento, senha, tipo) VALUES(DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (cpf, nome, email, user_mail, domain_mail, telefone, data_de_nascimento, senha, tipo)
        cursor.execute(sql, data)
        con.commit()
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()

def cadastra_cliente(id_cliente, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        sql = "INSERT INTO clientes (id_cliente, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (id_cliente, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel)
        cursor.execute(sql, data)
        con.commit()
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()
def cadastra_profissional(id_profissional, profissao, registro_profissional, telefone_comercial, cep, endereco, numero, complemento, cidade, estado):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        if registro_profissional == "":
            registro_profissional = "-"
        if telefone_comercial == "":
            telefone_comercial == ""
        sql = "INSERT INTO profissionais (id_profissional, profissao, registro_profissional, telefone_comercial, cep, endereco, numero, complemento, cidade, estado) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (id_profissional, profissao, registro_profissional, telefone_comercial, cep, endereco, numero, complemento, cidade, estado)
        cursor.execute(sql, data)
        con.commit()
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()
def cadastra_atendimento(id_profissional, id_cliente, valor, data_consulta, data_gerado, forma_pagamento, numero_parcelas):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        sql = "INSERT INTO atendimentos (id_atendimento, id_profissional, id_cliente, valor, data_consulta, data_gerado,forma_pagamento, numero_parcelas) VALUES(DEFAULT,%s,%s,%s,%s,%s,%s,%s)"
        data = (id_profissional, id_cliente, valor, data_consulta, data_gerado,forma_pagamento, numero_parcelas)
        cursor.execute(sql, data)
        con.commit()
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()

def cadastra_esquecimento(cpf, chave, datahora):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        sql = "INSERT INTO pedido_mudanca_senha (id_pedido, cpf, chave,datahora) VALUES(DEFAULT,%s,%s,%s)"
        data = (cpf, chave, datahora)
        cursor.execute(sql, data)
        con.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        con.close()

def pre_cadastra(nome, cpf, telefone, email):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        user_mail = separa_email(email)[0]
        domain_mail = separa_email(email)[1]
        data_de_nascimento = None
        senha = None
        tipo = 0
        sql = "INSERT INTO usuarios (id, cpf, nome, email, user_mail, domain_mail, telefone, data_de_nascimento, senha, tipo) VALUES(DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (cpf, nome, email, user_mail, domain_mail, telefone, data_de_nascimento, senha, tipo)
        cursor.execute(sql, data)
        con.commit()
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()

def completa_cadastro_cliente(nome, data_de_nascimento, cpf, telefone, email, senha, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        id_cliente = cpf_id(cpf)
        ups_usuario = {'nome':nome, 'data_de_nascimento':data_de_nascimento, 'telefone':telefone, 'email':email, 'user_mail':user_mail, 'domain_mail':domain_mail, 'senha':senha, 'cep':cep, 'endereco':endereco, 'numero':numero, 'complemento':complemento, 'cidade':cidade, 'estado':estado, 'nome_responsavel':nome_responsavel, 'cpf_responsavel':cpf_responsavel}
        update(ups_usuario,'clientes','id_cliente='+str(id_cliente))
    except Exception as e:
        print(e)    
        
    finally:
        cursor.close()
        con.close()

def completa_cadastro_profissional():
    pass


def select_CursorDict(fields, tables, where = None):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        cursor = con.cursor(dictionary = True) 
        query = "SELECT " + fields + " FROM " +tables
        if (where):
            query += " WHERE " + where
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()

def verifica_email(email, table):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        lista_DomainUser = str.split(email, '@')
        user_mail = "'"+ lista_DomainUser[0] +"'"
        domain_mail = "'" +lista_DomainUser[1]+"'"
        query = "select count(user_mail) from {} where domain_mail = {} and user_mail = {} ;".format(table, domain_mail, user_mail)
        cursor.execute(query)
        return bool(cursor.fetchall()[0][0])
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()

def valida_token(token):
    data_registro = select('datahora', 'pedido_mudanca_senha', 'chave= "'+token+'"')[0][0]
    data_agora = datetime.now()
    validacao = (data_agora - data_registro)
    return validacao<timedelta(days=1)

def valida_data(data):
    '''Checa se a data inserida é maior que a data atual, logo é inválida'''
    hoje = date.today()
    hoje = int(str(hoje.year) + ("0" + str(hoje.month))[-2:] + ("0" + str(hoje.day))[-2:])
    data = int(data[6:] + data[3:5] + data[0:2])
    return data > hoje

def converte_data(data):
    '''converte uma data do tipo DD/MM/AAAA em date
    str -> date'''
    dia = int(data[:2])
    mes = int(data[3:5])
    ano = int(data[6:])
    dataFormatada = date(ano, mes, dia)
    return dataFormatada

def inverte_data(data): # 12/34/5678 -> 5678-34-12
    return data[6:]+'-'+data[3:5]+'-'+data[0:2]

def ultima_consulta(id_profissional,id_cliente):
    """
    """
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        id_cliente = str(id_cliente)
        id_profissional = str(id_profissional)
        query = str.format("SELECT MAX(data_consulta) FROM atendimentos WHERE id_cliente = {} and id_profissional = {}", id_cliente, id_profissional)
        cursor.execute(query)
        return cursor.fetchall()[0][0]
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()

def filtro_atendimentos_mes(id_profissional, mes, ano):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        query = "SELECT * FROM atendimentos WHERE month(data_consulta)=" + str(mes) + " AND year(data_consulta)=" +str(ano) +" AND  id_profissional=" + str(id_profissional)
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()

def converte_dinheiro(dinheiro):
    valor = dinheiro[2:]
    split = valor.split(',')
    inteiro = split[0]
    centavos = split[1][0:2]
    grana = round(float(inteiro+'.'+centavos),2)
    return grana


def dinheiro_mes(id_profissional, mes, ano):
    atendimentos = filtro_atendimentos_mes(id_profissional, mes, ano)
    grana = 0
    for atendimento in atendimentos:
        grana+=converte_dinheiro(atendimento[3])
    return grana



def formas_pagamento_mes(id_profissional, mes, ano):
    credito = 0
    debito = 0
    dinheiro = 0
    atendimentos = filtro_atendimentos_mes(id_profissional, mes, ano)
    for atendimento in atendimentos:
        if atendimento[6]==1:
            credito+=1
        elif atendimento[6]==2:
            debito+=1
        elif atendimento[6]==3:
            dinheiro+=1
    formas = [credito, debito, dinheiro]
    total = sum(formas)
    return formas

def lista_meses(mes = datetime.now().month):
    """Retorna uma lista com o nome dos meses até o numero do mes dado 1-12
    valor padrão é o mes atual"""
    lista_meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto","Setembro", "Outubro", "Novembro", "Dezembro"]
    return lista_meses[:mes]

def atendimentos_periodo(id_profissional, data_inicio, data_fim):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        query = "SELECT * FROM atendimentos WHERE id_profissional=" + str(id_profissional)+ " AND data_consulta between '" + data_inicio + "' AND '" + data_fim + "'"
        cursor.execute(query)
        atendimentos_periodo = cursor.fetchall()
        atendimentos = []
        for atendimento in atendimentos_periodo:
            atendimentos.append([atendimento[0],atendimento[2],atendimento[3],atendimento[4],atendimento[6],atendimento[7]])

        for atendimento in atendimentos:
            id = str(atendimento[1])
            nome = select("nome", "usuarios", "id = "+id)[0][0]
            atendimento.append(nome)
            cpf = select("cpf", "usuarios" , "id = " + id)[0][0]
            atendimento.append(cpf)

        return atendimentos

    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()

def cliente_atendido(id_atendimento):
    return select('id_cliente','atendimentos','id_atendimento = '+id_atendimento)[0][0]



def limpa_telefone(telefone):
    if len(telefone)==14:
        ddd = telefone[1:3]
        bloco5 = telefone[4:9]
        bloco4 = telefone[10:]
        return ddd+bloco5+bloco4
    
    if len(telefone)==13:
        ddd = telefone[1:3]
        bloco1 = telefone[4:8]
        bloco2 = telefone[9:]
        return ddd+bloco1+bloco2

def formata_cep(cep):
    return cep[0:2]+cep[2:5]+'-'+cep[5:]

def formata_data(data): # 12/34/5678 <-- 5678-34-12
    return data[8:]+'/'+data[5:7]+'/'+data[0:4]

def formata_telefone(telefone): # 21964011311 - (21) 96401-1311
    """Transforma um telefone vindo do bd no formato (21)1111-1111 ou (21)11111-1111"""
    if len(telefone) == 11:
        telefone = '({}) {}-{}'.format(telefone[0:2],telefone[2:7], telefone[7:])
    else:
        telefone = '({}) {}-{}'.format(telefone[0:2],telefone[2:6], telefone[6:])
    return telefone

def formata_cpf(cpf): # 00000000000 -> 000.000.000-00
    return cpf[0:3]+'.'+cpf[3:6]+'.'+cpf[6:9]+'-'+cpf[9:]

def limpa_cpf(cpf):
    '''Limpa o CPF, tirando ponto e traço'''
    first = cpf[:3]
    second = cpf[4:7]
    third = cpf[8:11]
    final =cpf[12:]
    return first+second+third+final

def valida_cpf(cpf):
    '''Faz a validação do cpf inserido. Retorna True se for válido e False se for inválido'''
    cpf_limpo = limpa_cpf(cpf)

    digitos=[]
    for i in range (0, 11):
        digitos.append(int(cpf_limpo[i]))
    
    primeiro_validador = 0
    for i in range (0, 9):
        buffer = (10-i)*digitos[i]
        primeiro_validador += buffer
    primeiro_resto = primeiro_validador%11    

    if primeiro_resto<2:
        primeiro_digito = 0
    else:
        primeiro_digito = 11-primeiro_resto
    
    if primeiro_digito != digitos[9]:
        return False

    segundo_validador=0

    for i in range (0, 10):
        buffer = (11-i)*digitos[i]
        segundo_validador += buffer
    segundo_resto = segundo_validador%11

    if segundo_resto<2:
        segundo_digito=0
    else:
        segundo_digito = 11-segundo_resto

    if segundo_digito != digitos[10]:
        return False

    return True

def limpa_cep(cep):
    return cep[:5]+cep[6:]
