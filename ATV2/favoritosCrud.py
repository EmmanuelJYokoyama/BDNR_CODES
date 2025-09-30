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

    cpf_usuario = input("Digite o CPF do usuário: ").strip()
    codigo_str = input("Digite o código do produto: ").strip()

    if not cpf_usuario or not codigo_str:
        print("CPF e código do produto são obrigatórios.")
        return
    
    prod_cod = int(codigo_str)

    usuario = usuario_col.find_one({"usu_cpf": cpf_usuario})
    if not usuario:
        print("Usuário não encontrado.")
        return

    produto = produto_col.find_one({"prod_cod": prod_cod})
    if not produto:
        print("Produto não encontrado.")
        return

    # registra favorito (usu_cpf + prod_cod)
    favorito_col.insert_one({"usu_cpf": cpf_usuario, "prod_cod": prod_cod})

    # opcional: mantém referência no usuário
    usuario_col.update_one(
        {"usu_cpf": cpf_usuario},
        {"$addToSet": {"favoritos": {"prod_cod": prod_cod}}}
    )
    print("Favorito registrado com sucesso!")

def read_favoritos(cpf):
    usuario_col = db.usuario
    favorito_col = db.favorito
    produto_col = db.produto

    usuario = usuario_col.find_one({"usu_cpf": cpf})
    if not usuario:
        print("Usuário não encontrado.")
        return

    print("\nFavoritos do usuário")
    print(f"Nome: {usuario.get('usu_nome', '')}")
    print(f"CPF:  {usuario.get('usu_cpf', '')}")

    encontrou = False
    for fav in favorito_col.find({"usu_cpf": cpf}):
        encontrou = True
        prod_cod = fav.get("prod_cod")
        produto = produto_col.find_one({"prod_cod": prod_cod})

        print("-" * 30)
        if produto:
            print(f"Código: {produto.get('prod_cod', '')}")
            print(f"Nome: {produto.get('prod_nome', '')}")
            print(f"Valor: {produto.get('prod_valor', '')}\n")
        else:
            print(f"Produto não encontrado (prod_cod: {prod_cod})")

    if not encontrou:
        print("Nenhum favorito encontrado.")

def delete_favorito(cpf):
    usuario_col = db.usuario
    favorito_col = db.favorito

    usuario = usuario_col.find_one({"usu_cpf": cpf})
    if not usuario:
        print("Usuário não encontrado.")
        return

    codigo_str = input("Digite o CÓDIGO do produto (prod_cod) a remover: ").strip()
    try:
        prod_cod = int(codigo_str)
    except ValueError:
        print("Código do produto deve ser numérico.")
        return

    favorito = favorito_col.find_one({"usu_cpf": cpf, "prod_cod": prod_cod})
    if not favorito:
        print("Esse produto não está nos favoritos do usuário.")
        return

    favorito_col.delete_one({"usu_cpf": cpf, "prod_cod": prod_cod})
    usuario_col.update_one(
        {"usu_cpf": cpf},
        {"$pull": {"favoritos": {"prod_cod": prod_cod}}}
    )
    print(f"Produto removido dos favoritos de {usuario.get('usu_nome','')}.")