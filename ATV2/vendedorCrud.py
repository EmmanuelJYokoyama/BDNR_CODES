from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre

key = 0
sub = 0

def delete_vendedor(nome, cnpj):
    global db
    mycol = db.vendedor
    myquery = {"ven_nome": nome, "ven_cnpj": cnpj}
    mydoc = mycol.delete_one(myquery)
    print("\nDeletado o vendedor ",mydoc)

def create_vendedor():
    global db
    col_vendedor = db.vendedor
    col_produto = db.produtos
    print("\n\n\tInserindo um novo vendedor")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    email = input("Email: ")
    nomeFormat = f"{nome} {sobrenome}"
    cnpj = input("CNPJ: ")
    valor = 0  
    mydoc = {
        "ven_nome": nomeFormat,
        "ven_cnpj": cnpj,
        "ven_email": email,
        "produtos": [],
        "ven_valor_total": valor
    }
    x = col_vendedor.insert_one(mydoc)
    print("Documento inserido!")

def read_vendedor(cnpj=None):
    global db
    col = db.vendedor
    filtro = {"ven_cnpj": cnpj} if cnpj else {}

    encontrou = False
    for v in col.find(filtro):
        encontrou = True
        print(f"\nNome: {v.get('ven_nome', '')}")
        print(f"CNPJ: {v.get('ven_cnpj', '')}")
        print(f"Email: {v.get('ven_email', '')}")
        print(f"Valor total: {v.get('ven_valor_total', 0)}")
        produtos = v.get("produtos", [])
        if produtos:
            print("Produtos:")
            for p in produtos:
                print(f"  - ID: {p.get('prod_id', '')} | Nome: {p.get('prod_nome', '')} | Valor: {p.get('prod_valor', '')} | Quantidade: {p.get('prod_quantidade', '')}")
        else:
            print("Produtos: (nenhum)")
        print("-" * 30)

    if not encontrou:
        print("Nenhum vendedor encontrado.")

def update_vendedor(cnpj):
    global db
    mycol = db.usuario
    myquery = {"ven_cnpj": cnpj}
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
