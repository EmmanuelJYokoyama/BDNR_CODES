from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

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