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

def _cache_vendedor(doc):
    if not doc: 
        return
    key = f"vendedor:{doc['ven_cnpj']}"
    r.hset(key, mapping={
        "ven_nome": doc.get("ven_nome", ""),
        "ven_cnpj": doc.get("ven_cnpj", ""),
        "ven_email": doc.get("ven_email", ""),
    })

def create_vendedor():
    col_vendedor = db.vendedor
    print("\n\n\tInserindo um novo vendedor")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    email = input("Email: ")
    nomeFormat = f"{nome} {sobrenome}"
    cnpj = input("CNPJ: ")

    doc = {
        "ven_nome": nomeFormat,
        "ven_cnpj": cnpj,
        "ven_email": email,
        "produtos": [],
        "ven_valor_total": 0
    }
    col_vendedor.create_index("ven_cnpj", unique=True)
    x = col_vendedor.insert_one(doc)
    _cache_vendedor(doc)
    print("Vendedor inserido com ID", x.inserted_id)

def read_vendedor(cnpj=None):
    col = db.vendedor

    if cnpj:
        # cache-first
        hv = r.hgetall(f"vendedor:{cnpj}")
        if hv:
            print(f"\nNome: {hv.get('ven_nome','')}\nCNPJ: {hv.get('ven_cnpj','')}\nEmail: {hv.get('ven_email','')}\n" + "-"*30)
            return
        v = col.find_one({"ven_cnpj": cnpj})
        if v:
            _cache_vendedor(v)
            print(f"\nNome: {v.get('ven_nome', '')}\nCNPJ: {v.get('ven_cnpj', '')}\nEmail: {v.get('ven_email', '')}\n" + "-"*30)
        else:
            print("Nenhum vendedor encontrado.")
        return

    # lista todos pelo Mongo e aquece o cache
    encontrou = False
    for v in col.find({}).sort("ven_nome"):
        encontrou = True
        _cache_vendedor(v)
        print(f"\nNome: {v.get('ven_nome', '')}")
        print(f"CNPJ: {v.get('ven_cnpj', '')}")
        print(f"Email: {v.get('ven_email', '')}")
        print("-" * 30)
    if not encontrou:
        print("Nenhum vendedor encontrado.")

def update_vendedor(cnpj):
    col = db.vendedor
    doc = col.find_one({"ven_cnpj": cnpj})
    if not doc:
        print("Vendedor não encontrado.")
        return

    print("Atual:", doc)
    v = input("Novo nome (Enter mantém): ").strip()
    if v: doc["ven_nome"] = v
    v = input("Novo email (Enter mantém): ").strip()
    if v: doc["ven_email"] = v

    col.update_one({"ven_cnpj": cnpj}, {"$set": doc})
    _cache_vendedor(doc)
    print("Vendedor atualizado.")

def delete_vendedor(cnpj):
    col = db.vendedor
    res = col.delete_one({"ven_cnpj": cnpj})
    if res.deleted_count:
        r.delete(f"vendedor:{cnpj}")
        print("Vendedor deletado com sucesso!")
    else:
        print("Nenhum vendedor encontrado com esse CNPJ.")

def manipular_vendedores(db, cache):
    vendedor_col = db.vendedor
    vendedores = list(vendedor_col.find().limit(1))
    if not vendedores:
        print("Nenhum vendedor encontrado.")
        return

    print("Vendedores encontrados:")
    for vendedor in vendedores:
        print({"ven_cnpj": vendedor.get("ven_cnpj"), "ven_nome": vendedor.get("ven_nome")})

    # a) -> Redis
    for vendedor in vendedores:
        chave = f"vendedor:{vendedor['ven_cnpj']}"
        cache.hset(chave, mapping={"cnpj": vendedor["ven_cnpj"], "nome": vendedor.get("ven_nome", "")})

    print("\nAlterando nome do vendedor no Redis...")
    for vendedor in vendedores:
        chave = f"vendedor:{vendedor['ven_cnpj']}"
        novo_nome = input("Digite o novo nome: ").strip()
        if novo_nome:
            cache.hset(chave, "nome", novo_nome)
            print(f"Nome do vendedor alterado para {novo_nome}")

    print("\nGravando de volta no MongoDB...")
    for vendedor in vendedores:
        chave = f"vendedor:{vendedor['ven_cnpj']}"
        dados = cache.hgetall(chave)
        vendedor_col.update_one({"ven_cnpj": vendedor["ven_cnpj"]}, {"$set": {"ven_nome": dados.get("nome", "")}})

    print("Vendedores manipulados com sucesso!\n")
