from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre

key = 0
sub = 0

def create_favorito():
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
    usuario_col = db.usuario
    favorito_col = db.favorito
    produto_col = db.produto

    usuario = usuario_col.find_one({"usu_cpf": cpf}) or usuario_col.find_one({"cpf": cpf})
    if not usuario:
        print("Usuário não encontrado.")
        return

    nome_usuario = usuario.get("usu_nome", usuario.get("nome", ""))
    cpf_usuario = usuario.get("usu_cpf", usuario.get("cpf", cpf))
    print(f"\nFavoritos do usuário")
    print(f"Nome: {nome_usuario}")
    print(f"CPF: {cpf_usuario}")

    favoritos = favorito_col.find({"cpf_usuario": cpf})
    encontrou = False
    for fav in favoritos:
        encontrou = True
        pid = fav.get("id_produto") or fav.get("prod_id") or fav.get("id")

        produto = None
        consultas = []
        if pid is not None:
            try:
                consultas.append({"prod_id": int(pid)})
            except:
                pass
            consultas += [{"prod_id": pid}, {"id": pid}]
            for q in consultas:
                produto = produto_col.find_one(q)
                if produto:
                    break

        print("-" * 30)
        if produto:
            print(f"ID: {produto.get('prod_id', produto.get('id', ''))}")
            print(f"Nome: {produto.get('prod_nome', produto.get('nome', ''))}")
            print(f"Valor: {produto.get('prod_valor', produto.get('valor', ''))}")
            print(f"Quantidade: {produto.get('prod_quantidade', produto.get('quantidade', ''))}")
        else:
            print(f"Produto não encontrado (ID: {pid})")

    if not encontrou:
        print("Nenhum favorito encontrado.")

def delete_favorito(cpf):
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