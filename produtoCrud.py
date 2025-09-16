from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

<<<<<<< HEAD
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre

produtos_col = db.produtos

def create_produto():
    produto = {
        "prod_id": int(input("ID do produto: ")),
        "prod_nome": input("Nome: "),
        "prod_descricao": input("Descrição: "),
        "prod_valor": float(input("Valor: ")),
        "prod_quantidade": int(input("Quantidade em estoque: ")),
        "vendedor": {
            "ven_cnpj": int(input("CNPJ do vendedor: ")),
            "ven_nome": input("Nome do vendedor: "),
            "ven_numero": input("Telefone do vendedor: ")
        }
    }
    x = produtos_col.insert_one(produto)
    print("Produto criado com ID:", x.inserted_id)

def read_produto(nome):
    produto = produtos_col.find_one({"prod_nome": nome})
    print(produto if produto else "Produto não encontrado.")

def update_produto(nome):
    novo_valor = float(input("Novo valor do produto: "))
    produtos_col.update_one({"prod_nome": nome}, {"$set": {"prod_valor": novo_valor}})
    print("Produto atualizado.")

def delete_produto(nome):
    produtos_col.delete_one({"prod_nome": nome})
    print("Produto deletado.")
=======
# Conexão com o banco
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.mercado_livre


# ---------------------- CRUD VENDEDOR ----------------------
def create_vendedor():
    col_vendedor = db.vendedor
    print("\nInserindo um novo vendedor")

    ven_id = int(input("ID do vendedor: "))
    ven_nome = input("Nome do vendedor: ")
    ven_numero = input("Número (ex: CNPJ/telefone): ")

    produtos = []
    key = 'S'

    while key != 'N':
        prod_id = int(input("ID do produto: "))
        prod_nome = input("Nome do produto: ")
        prod_valor = float(input("Valor do produto: "))

        produtoObj = {
            "prod_id": prod_id,
            "prod_nome": prod_nome,
            "prod_valor": prod_valor
        }
        produtos.append(produtoObj)

        key = input("Deseja cadastrar um novo produto (S/N)? ").upper()

    vendedor = {
        "ven_id": ven_id,
        "ven_nome": ven_nome,
        "ven_numero": ven_numero,
        "produtos": produtos
    }

    x = col_vendedor.insert_one(vendedor)
    print("Vendedor inserido com ID ", x.inserted_id)


def read_vendedor(nome=None):
    col_vendedor = db.vendedor
    print("\nVendedores existentes: ")
    if not nome:
        docs = col_vendedor.find().sort("ven_nome")
        for x in docs:
            print(x)
    else:
        myquery = {"ven_nome": nome}
        docs = col_vendedor.find(myquery)
        for x in docs:
            print(x)


def update_vendedor(ven_id):
    col_vendedor = db.vendedor
    myquery = {"ven_id": ven_id}
    vendedor = col_vendedor.find_one(myquery)

    if not vendedor:
        print("Vendedor não encontrado.")
        return

    print("Dados atuais do vendedor: ", vendedor)

    novo_nome = input("Novo Nome (Enter para manter): ")
    if len(novo_nome):
        vendedor["ven_nome"] = novo_nome

    novo_numero = input("Novo Número (Enter para manter): ")
    if len(novo_numero):
        vendedor["ven_numero"] = novo_numero

    opcao = input("Deseja atualizar os produtos? (S/N): ").upper()
    if opcao == "S":
        novos_produtos = []
        key = 'S'
        while key != 'N':
            prod_id = int(input("ID do produto: "))
            prod_nome = input("Nome do produto: ")
            prod_valor = float(input("Valor do produto: "))

            produtoObj = {
                "prod_id": prod_id,
                "prod_nome": prod_nome,
                "prod_valor": prod_valor
            }
            novos_produtos.append(produtoObj)
            key = input("Deseja cadastrar outro produto (S/N)? ").upper()

        vendedor["produtos"] = novos_produtos

    col_vendedor.update_one(myquery, {"$set": vendedor})
    print("Vendedor atualizado com sucesso!")


def delete_vendedor(ven_id):
    col_vendedor = db.vendedor
    result = col_vendedor.delete_one({"ven_id": ven_id})
    if result.deleted_count > 0:
        print("Vendedor deletado com sucesso!")
    else:
        print("Nenhum vendedor encontrado.")
>>>>>>> 162eef521c6fa74d200e22eb45ee983197897cf4
