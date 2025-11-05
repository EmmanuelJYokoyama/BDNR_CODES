from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import redis
from sync_utils import sync_redis_to_mongo  # novo import

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

    # Lista todos quando vazio/None
    if cod is None or (isinstance(cod, str) and cod.strip() == ""):
        encontrou = False
        for doc in col_produto.find().sort("prod_nome", 1):
            encontrou = True
            _cache_produto(doc)  # mantém cache atualizado
            vend = (doc.get("vendedor") or {})
            valor = doc.get("prod_valor", 0)
            try:
                valor_fmt = f"R$ {float(valor):.2f}"
            except Exception:
                valor_fmt = str(valor)

            print(f"\nCódigo: {doc.get('prod_cod', '')}")
            print(f"Nome: {doc.get('prod_nome', '')}")
            print(f"Descrição: {doc.get('prod_descricao', '')}")
            print(f"Valor: {valor_fmt}")
            print(f"Quantidade: {doc.get('prod_quantidade', 0)}")
            if vend.get("ven_nome") or vend.get("ven_numero"):
                print(f"Vendedor: {vend.get('ven_nome', '')} | CNPJ: {vend.get('ven_numero', '')}")
            print("-" * 40)

        if not encontrou:
            print("Nenhum produto encontrado.")
        return

    try:
        cod_int = int(str(cod).strip())
    except ValueError:
        print("Código inválido.")
        return

    hk = f"produto:{cod_int}"
    hv = r.hgetall(hk)
    if hv:
        try:
            valor_fmt = f"R$ {float(hv.get('prod_valor', 0)):.2f}"
        except Exception:
            valor_fmt = str(hv.get("prod_valor", ""))
        print(f"\nCódigo: {hv.get('prod_cod', '')}")
        print(f"Nome: {hv.get('prod_nome', '')}")
        print(f"Descrição: {hv.get('prod_descricao', '')}")
        print(f"Valor: {valor_fmt}")
        print(f"Quantidade: {hv.get('prod_quantidade', 0)}")
        if hv.get("ven_nome") or hv.get("ven_numero"):
            print(f"Vendedor: {hv.get('ven_nome', '')} | CNPJ: {hv.get('ven_numero', '')}")
        print("-" * 40)
        return

    doc = col_produto.find_one({"prod_cod": cod_int})
    if doc:
        _cache_produto(doc)
        vend = (doc.get("vendedor") or {})
        valor = doc.get("prod_valor", 0)
        try:
            valor_fmt = f"R$ {float(valor):.2f}"
        except Exception:
            valor_fmt = str(valor)

        print(f"\nCódigo: {doc.get('prod_cod', '')}")
        print(f"Nome: {doc.get('prod_nome', '')}")
        print(f"Descrição: {doc.get('prod_descricao', '')}")
        print(f"Valor: {valor_fmt}")
        print(f"Quantidade: {doc.get('prod_quantidade', 0)}")
        if vend.get("ven_nome") or vend.get("ven_numero"):
            print(f"Vendedor: {vend.get('ven_nome', '')} | CNPJ: {vend.get('ven_numero', '')}")
        print("-" * 40)
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

def manipular_produtos(db, cache):
    produto_col = db.produto
    # 3 itens como pede o PDF
    produtos = list(produto_col.find().limit(3))
    if not produtos:
        print("Nenhum produto encontrado.")
        return

    print("Produtos encontrados:")
    for produto in produtos:
        print(produto)

    for produto in produtos:
        chave = f"produto:{produto['prod_cod']}"
        dados = {
            "prod_cod": str(produto.get("prod_cod")),
            "nome": produto.get("prod_nome", ""),
            "valor": str(produto.get("prod_valor", 0)),
            "quantidade": str(produto.get("prod_quantidade", 0)),
        }
        cache.hset(chave, mapping=dados)

    print("\nAumentando valor dos produtos em 10% no Redis...")
    for produto in produtos:
        chave = f"produto:{produto['prod_cod']}"
        valor_str = cache.hget(chave, "valor") or "0"
        try:
            valor = float(valor_str)
        except ValueError:
            valor = 0.0
        novo_valor = round(valor * 1.10, 2)
        cache.hset(chave, "valor", str(novo_valor))
        print(f"Valor do produto {produto.get('prod_nome')} alterado para R${novo_valor}")

    print("\nGravando de volta os produtos no MongoDB...")
    for produto in produtos:
        chave = f"produto:{produto['prod_cod']}"
        dados = cache.hgetall(chave)  # strings
        set_doc = {
            "prod_nome": dados.get("nome", ""),
            "prod_valor": float(dados.get("valor", "0") or "0"),
            "prod_quantidade": int(float(dados.get("quantidade", "0") or "0")),
        }
        produto_col.update_one({"prod_cod": produto["prod_cod"]}, {"$set": set_doc})

    print("Produtos manipulados com sucesso!\n")

def cache_create_produto(r):
    """
    Cria/atualiza um produto no Redis (cache) e em seguida sincroniza para o Mongo.
    Recebe a conexão redis 'r' (pode ser o r do menu).
    """
    try:
        prod_cod = int(input("Código (prod_cod) do produto (cache): "))
    except ValueError:
        print("Código inválido.")
        return

    prod_nome = input("Nome do produto: ")
    prod_descricao = input("Descrição do produto: ")
    try:
        prod_valor = float(input("Valor do produto: "))
    except ValueError:
        prod_valor = 0.0
    try:
        prod_quantidade = int(input("Quantidade em estoque: "))
    except ValueError:
        prod_quantidade = 0

    # vendedor opcional (apenas referencia)
    ven_cnpj = input("CNPJ do vendedor (opcional): ").strip()

    key = f"produto:{prod_cod}"
    mapping = {
        "prod_cod": prod_cod,
        "prod_nome": prod_nome,
        "prod_descricao": prod_descricao,
        "prod_valor": prod_valor,
        "prod_quantidade": prod_quantidade,
        "ven_numero": ven_cnpj,
    }
    r.hset(key, mapping=mapping)
    print(f"Produto gravado no Redis em {key}.")

    # sincroniza imediatamente para o Mongo
    sync_redis_to_mongo(db, r)
    print("Sincronizado para o Mongo.")

def cache_update_produto(r):
    """
    Atualiza campos do produto no Redis e sincroniza.
    """
    cod = input("Código (prod_cod) do produto a atualizar no cache: ").strip()
    try:
        cod_int = int(cod)
    except ValueError:
        print("Código inválido.")
        return

    key = f"produto:{cod_int}"
    current = r.hgetall(key)
    if not current:
        print("Produto não encontrado no cache (Redis).")
        return

    print("Dados atuais (cache):", current)
    v = input("Novo nome (Enter mantém): ").strip()
    if v: current["prod_nome"] = v
    v = input("Nova descrição (Enter mantém): ").strip()
    if v: current["prod_descricao"] = v
    v = input("Novo valor (Enter mantém): ").strip()
    if v:
        try:
            current["prod_valor"] = float(v)
        except ValueError:
            print("Valor inválido; mantendo antigo.")
    v = input("Nova quantidade (Enter mantém): ").strip()
    if v:
        try:
            current["prod_quantidade"] = int(v)
        except ValueError:
            print("Quantidade inválida; mantendo antiga.")
    v = input("Novo CNPJ vendedor (Enter mantém): ").strip()
    if v: current["ven_numero"] = v

    # grava de volta no redis
    r.hset(key, mapping=current)
    print("Cache atualizado no Redis.")

    # sincroniza
    sync_redis_to_mongo(db, r)
    print("Sincronizado para o Mongo.")

def cache_delete_produto(r):
    """
    Deleta produto do Redis (cache) e sincroniza para remover do Mongo.
    """
    cod = input("Código (prod_cod) do produto a deletar no cache: ").strip()
    try:
        cod_int = int(cod)
    except ValueError:
        print("Código inválido.")
        return
    key = f"produto:{cod_int}"
    if r.exists(key):
        r.delete(key)
        print("Produto removido do Redis (cache).")
        # sincroniza (redis->mongo) para aplicar remoção no Mongo também
        sync_redis_to_mongo(db, r)
        print("Sincronização aplicada no Mongo.")
    else:
        print("Chave não encontrada no Redis.")

