from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre

key = 0
sub = 0

def create_favorito():
    global db
    produto_col = db.produto
    usuario_col = db.usuario
    favorito_col = db.favorito

    cpf_usuario = input("Digite o CPF do usuário: ")
    id_produto = input("Digite o ID do produto: ")

    usuario = usuario_col.find_one({"cpf": cpf_usuario})
    if not usuario:
        print("Usuário não encontrado.")
        return
   
    produto = produto_col.find_one({"id": id_produto})
    if not produto:
        print("Produto não encontrado.")
        return
    
    doc = {"id_produto": id_produto, "cpf_usuario": cpf_usuario }
    favorito_col.insert_one(doc)
    usuario_col.update_one(
        {"cpf": cpf_usuario},
        {"$push": {"favoritos": {
            "id": id_produto
        }}}
    )
    print(f"Favorito registrado com sucesso!")

def read_favoritos_usuario(cpf):
    global db
    usuario_col = db.usuario
    favorito_col = db.favorito
    produto_col = db.produto

    usuario = usuario_col.find_one({"cpf": cpf})
    if not usuario:
        print("Usuário não encontrado.")
        return

    print(f"\nProdutos favoritados pelo usuário {usuario['nome']}")

    favoritos = favorito_col.find({"cpf_usuario": cpf})

    for favorito in favoritos:
        produto = produto_col.find_one({"id": favorito["id_produto"]})
        print("-" * 40)
        print(f"Produto: {produto['nome']}")

def delete_favorito(cpf):
    global db
    usuario_col = db.usuario
    favorito_col = db.favorito

    usuario = usuario_col.find_one({"cpf": cpf})
    if not usuario:
        print("Usuário não encontrado.")
        return
    
    id_produto = input("Digite o ID do produto a remover dos favoritos: ")

    favorito = favorito_col.find_one({"cpf_usuario": cpf, "id_produto": id_produto})
    if not favorito:
        print("Esse produto não está nos favoritos do usuário.")
        return
    
    favorito_col.delete_one({"cpf_usuario": cpf, "id_produto": id_produto})

    usuario_col.update_one(
        {"cpf": cpf},
        {"$pull": {"favoritos": {"id": id_produto}}}
    )
    print(f"Produto removido dos favoritos de {usuario['nome']}.")