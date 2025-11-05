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

    cpf_usuario = input("Digite o CPF do usuário: ").strip()
    codigo_str = input("Digite o código do produto: ").strip()

    if not cpf_usuario or not codigo_str:
        print("CPF e código do produto são obrigatórios.")
        return
    try:
        prod_cod = int(codigo_str)
    except ValueError:
        print("Código do produto deve ser numérico.")
        return

    usuario = usuario_col.find_one({"usu_cpf": cpf_usuario})
    if not usuario:
        print("Usuário não encontrado.")
        return

    produto = produto_col.find_one({"prod_cod": prod_cod})
    if not produto:
        print("Produto não encontrado.")
        return

    # adiciona nos favoritos do documento do usuário (evita duplicata)
    fav_entry = {"prod_cod": prod_cod, "prod_nome": produto.get("prod_nome", "")}
    res = usuario_col.update_one(
        {"usu_cpf": cpf_usuario},
        {"$addToSet": {"favoritos": fav_entry}}
    )
    if res.modified_count:
        print("Favorito adicionado ao usuário.")
    else:
        print("Este produto já está nos favoritos do usuário.")

def read_favoritos(cpf):
    usuario_col = db.usuario
    produto_col = db.produto

    usuario = usuario_col.find_one({"usu_cpf": cpf})
    if not usuario:
        print("Usuário não encontrado.")
        return

    favoritos = usuario.get("favoritos", [])
    if not favoritos:
        print("Nenhum favorito encontrado.")
        return

    print("\nFavoritos do usuário")
    print(f"Nome: {usuario.get('usu_nome', '')}")
    print(f"CPF:  {usuario.get('usu_cpf', '')}")

    for fav in favoritos:
        prod_cod = fav.get("prod_cod")
        produto = produto_col.find_one({"prod_cod": prod_cod})
        print("-" * 30)
        if produto:
            print(f"Código: {produto.get('prod_cod', '')}")
            print(f"Nome: {produto.get('prod_nome', fav.get('prod_nome',''))}")
            print(f"Valor: {produto.get('prod_valor', '')}\n")
        else:
            # fallback: show stored name if product removed from coleção
            print(f"Código: {prod_cod}")
            print(f"Nome (cache): {fav.get('prod_nome','')}")
            print("Produto não encontrado na coleção.")

def delete_favorito(cpf, prod_cod=None):
    usuario_col = db.usuario

    usuario = usuario_col.find_one({"usu_cpf": cpf})
    if not usuario:
        print("Usuário não encontrado.")
        return

    if prod_cod is None:
        codigo_str = input("Digite o CÓDIGO do produto (prod_cod) a remover: ").strip()
        try:
            prod_cod = int(codigo_str)
        except ValueError:
            print("Código do produto deve ser numérico.")
            return
    else:
        try:
            prod_cod = int(prod_cod)
        except (TypeError, ValueError):
            print("Código do produto deve ser numérico.")
            return

    favorito = usuario_col.find_one({"usu_cpf": cpf, "favoritos.prod_cod": prod_cod})
    if not favorito:
        print("Esse produto não está nos favoritos do usuário.")
        return

    usuario_col.update_one(
        {"usu_cpf": cpf},
        {"$pull": {"favoritos": {"prod_cod": prod_cod}}}
    )
    print(f"Produto (cod {prod_cod}) removido dos favoritos de {usuario.get('usu_nome','')}.")