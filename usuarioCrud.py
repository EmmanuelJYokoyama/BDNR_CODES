from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre

key = 0
sub = 0

def delete_usuario(nome, sobrenome):
    #Delete
    global db
    mycol = db.usuario
    myquery = {"usu_nome": nome, "sobrenome":sobrenome}
    mydoc = mycol.delete_one(myquery)
    print("Deletado o usuário ",mydoc)

def create_usuario():
    #Insert
    global db
    mycol = db.usuario
    print("\nInserindo um novo usuário")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    nomeFormat = f"{nome} {sobrenome}"
    email = input("Email: ")
    cpf = input("cpf: ")
    telefone = input("Telefone: ")
    key = 1
    end = []
    while (key != 'N'):
        rua = input("Rua: ")
        num = input("Num: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        cep = input("CEP: ")
        endereco = {        #isso nao eh json, isso é chave-valor, eh um obj
            "rua":rua,
            "num": num,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }
        end.append(endereco) #estou inserindo na lista
        key = input("Deseja cadastrar um novo endereço (S/N)? ").upper()
    mydoc = { "usu_nome": nomeFormat, "usu_email": email, "usu_cpf": cpf, "usu_telefone": telefone, "usu_endereco": end }
    x = mycol.insert_one(mydoc)
    print("Documento inserido com ID ",x.inserted_id)

def read_usuario(nome):
    #Read
    global db
    mycol = db.usuario
    print("Usuários existentes: ")
    if not len(nome):
        mydoc = mycol.find().sort("usu_nome")
        for x in mydoc:
            print(x["usu_nome"],x["usu_email"])
    else:
        myquery = {"usu_nome": nome}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x)

def update_usuario(nome):
    #Read
    global db
    mycol = db.usuario
    myquery = {"usu_nome": nome}
    mydoc = mycol.find_one(myquery)
    print("Dados do usuário: ",mydoc)
    nome = input("Mudar Nome:")
    if len(nome): 
        mydoc["usu_nome"] = nome

    email = input("Mudar Email:")
    if len(email):
        mydoc["usu_email"] = email

    newvalues = { "$set": mydoc }
    mycol.update_one(myquery, newvalues)
