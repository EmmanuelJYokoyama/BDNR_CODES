from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import redis

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.mercado_livre

r = redis.Redis(
    host='redis-15823.crce216.sa-east-1-2.ec2.redns.redis-cloud.com',
    port=15823,
    decode_responses=True,
    username="admin",
    password="Admin1!admin",
)

def _cache_produto(doc):
    if not doc:
        return
    key = f"produto:{doc['prod_cod']}"
    vend = doc.get("vendedor", {}) or {}
    r.hset(key, mapping={
        "prod_cod": doc.get("prod_cod"),
        "prod_nome": doc.get("prod_nome", ""),
        "prod_descricao": doc.get("prod_descricao", ""),
        "prod_valor": float(doc.get("prod_valor", 0)),
        "prod_quantidade": int(doc.get("prod_quantidade", 0)),
        "ven_id": vend.get("ven_id", ""),
        "ven_nome": vend.get("ven_nome", ""),
        "ven_numero": vend.get("ven_numero", ""),
    })

def create_produto():
    col_produto = db.produto
    col_vendedor = db.vendedor
    print("\nInserindo um novo produto")

    prod_cod = int(input("Código (prod_cod) do produto: "))
    prod_nome = input("Nome do produto: ")
    prod_descricao = input("Descrição do produto: ")
    prod_valor = float(input("Valor do produto: "))
    prod_quantidade = int(input("Quantidade em estoque: "))

    ven_cnpj = input("CNPJ do vendedor responsável: ").strip()
    vendedor = col_vendedor.find_one({"ven_cnpj": ven_cnpj})
    if not vendedor:
        print("Vendedor não encontrado! Cadastre o vendedor antes.")
        return

    produto = {
        "prod_cod": prod_cod,
        "prod_nome": prod_nome,
        "prod_descricao": prod_descricao,
        "prod_valor": prod_valor,
        "prod_quantidade": prod_quantidade,
        "vendedor": {
            "ven_id": str(vendedor.get("_id")),
            "ven_nome": vendedor.get("ven_nome"),
            "ven_numero": vendedor.get("ven_cnpj"),
        }
    }
    col_produto.create_index("prod_cod", unique=True)
    x = col_produto.insert_one(produto)
    _cache_produto(produto)
    print("Produto inserido com ID", x.inserted_id)

def read_produto(cod=None):
    col_produto = db.produto
    if not cod:
        for x in col_produto.find().sort("prod_nome", 1):
            _cache_produto(x)
            print(x)
        return
    try:
        cod_int = int(cod)
    except ValueError:
        print("Código inválido.")
        return

    # cache-first
    hk = f"produto:{cod_int}"
    hv = r.hgetall(hk)
    if hv:
        print(hv)
        return

    doc = col_produto.find_one({"prod_cod": cod_int})
    if doc:
        _cache_produto(doc)
        print(doc)
    else:
        print("Nenhum produto encontrado com esse código.")

def update_produto(prod_cod):
    col_produto = db.produto
    if isinstance(prod_cod, str):
        try:
            prod_cod = int(prod_cod)
        except ValueError:
            print("Código inválido.")
            return

    produto = col_produto.find_one({"prod_cod": prod_cod})
    if not produto:
        print("Produto não encontrado.")
        return

    print("Atual:", produto)

    v = input("Novo nome (Enter mantém): ").strip()
    if v: produto["prod_nome"] = v
    v = input("Nova descrição (Enter mantém): ").strip()
    if v: produto["prod_descricao"] = v
    v = input("Novo valor (Enter mantém): ").strip()
    if v: produto["prod_valor"] = float(v)
    v = input("Nova quantidade (Enter mantém): ").strip()
    if v: produto["prod_quantidade"] = int(v)

    trocar_vendedor = input("Alterar vendedor por CNPJ? (S/N): ").upper()
    if trocar_vendedor == "S":
        ven_cnpj = input("CNPJ do novo vendedor: ").strip()
        vend = db.vendedor.find_one({"ven_cnpj": ven_cnpj})
        if not vend:
            print("Vendedor não encontrado.")
        else:
            produto["vendedor"] = {
                "ven_id": str(vend.get("_id")),
                "ven_nome": vend.get("ven_nome"),
                "ven_numero": vend.get("ven_cnpj"),
            }

    col_produto.update_one({"prod_cod": prod_cod}, {"$set": produto})
    _cache_produto(produto)
    print("Produto atualizado.")

def delete_produto(prod_cod):
    col_produto = db.produto
    try:
        cod = int(prod_cod)
    except (TypeError, ValueError):
        print("Código inválido. Informe um inteiro.")
        return

    res = col_produto.delete_one({"prod_cod": cod})
    if res.deleted_count:
        r.delete(f"produto:{cod}")
        print("Produto deletado com sucesso!")
    else:
        print("Nenhum produto encontrado com esse código.")

