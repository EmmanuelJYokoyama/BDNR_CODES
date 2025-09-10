from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre

key = 0
sub = 0

def delete_vendedor(nome, cnpj):
    #Delete
    global db
    mycol = db.vendedor
    myquery = {"ven_nome": nome, "ven_cnpj": cnpj}
    mydoc = mycol.delete_one(myquery)
    print("Deletado o vendedor ",mydoc)

def create_vendedor():
    # Insert
    global db
    col_vendedor = db.vendedor
    col_produto = db.produtos
    print("\nInserindo um novo vendedor")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    nomeFormat = f"{nome} {sobrenome}"
    cnpj = input("CNPJ: ")
    prod = []
    valor = 0  # Inicializa o valor
    key = 'S'
    while key != 'N':
        produtoCod = input("Código do produto: ")
        if not produtoCod:
            print("Código do produto não pode ser vazio.")
            continue

        produtoNome = input("Nome do produto: ")
        produtoValor = float(input("Valor do produto: "))
        produtoQuantidade = int(input("Quantidade do produto: "))
        valor += produtoValor * produtoQuantidade
        produtosObj = {
            "prod_cod": produtoCod,
            "prod_nome": produtoNome,
            "prod_valor": produtoValor,
            "prod_quantidade": produtoQuantidade
        }
        prod.append(produtosObj)
        key = input("Deseja cadastrar um novo produto (S/N)? ").upper()

    mydoc = {
        "ven_nome": nomeFormat,
        "ven_cnpj": cnpj,
        "ven_produtos": prod,
        "ven_valor_total": valor
    }
    x = col_vendedor.insert_one(mydoc)
    print("Documento inserido com ID ",x.inserted_id)

def read_vendedor(nome):
    #Read
    global db
    mycol = db.usuario
    print("Usuários existentes: ")
    if not len(nome):
        mydoc = mycol.find().sort("ven_nome")
        for x in mydoc:
            print(x["ven_nome"],x["ven_email"])
    else:
        myquery = {"ven_nome": nome}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x)

def update_vendedor(nome):
    #Read
    global db
    mycol = db.usuario
    myquery = {"ven_nome": nome}
    mydoc = mycol.find_one(myquery)
    print("Dados do usuário: ",mydoc)
    nome = input("Mudar Nome:")
    if len(nome): 
        mydoc["ven_nome"] = nome

    email = input("Mudar Email:")
    if len(email):
        mydoc["ven_email"] = email

    newvalues = { "$set": mydoc }
    mycol.update_one(myquery, newvalues)
