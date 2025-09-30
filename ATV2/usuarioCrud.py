from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre

key = 0
sub = 0

def delete_usuario(nome, sobrenome):
    mycol = db.usuario
    myquery = {"usu_nome": nome, "sobrenome":sobrenome}
    mydoc = mycol.delete_one(myquery)
    print("Deletado o usuário ",mydoc)

def create_usuario():
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

def read_usuario(cpf=None):
    col = db.usuario

    filtro = {"usu_cpf": cpf} if cpf else {}

    encontrou = False
    for u in col.find(filtro).sort("usu_nome"):
        encontrou = True
        print(f"\nNome: {u.get('usu_nome', '')}")
        print(f"Email: {u.get('usu_email', '')}")
        print(f"CPF: {u.get('usu_cpf', '')}")
        print(f"Telefone: {u.get('usu_telefone', '')}") 
        enderecos = u.get("usu_endereco", [])
        if enderecos:
            print("Endereços:")
            for e in enderecos:
                print(f"  - Rua: {e.get('rua','')}, Num: {e.get('num','')}, Bairro: {e.get('bairro','')}, Cidade: {e.get('cidade','')}, Estado: {e.get('estado','')}, CEP: {e.get('cep','')}")
        else:
            print("Endereços: (nenhum)")
        print("-" * 30)

    if not encontrou:
        print("Nenhum usuário encontrado.")

def update_usuario(nome):
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
