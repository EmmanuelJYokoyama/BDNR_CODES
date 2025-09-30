from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

global db
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.mercado_livre

# ---------------------- CRUD PRODUTO ----------------------

def create_produto():
    col_produto = db.produto
    col_vendedor = db.vendedor
    print("\nInserindo um novo produto")

    prod_cod = int(input("Codigo do produto: "))
    prod_nome = input("Nome do produto: ")
    prod_descricao = input("Descrição do produto: ")
    prod_valor = float(input("Valor do produto: "))
    prod_quantidade = int(input("Quantidade do produto: "))

    print("\nInforme o CNPJ do vendedor responsável pelo produto:")
    ven_cnpj = input("CNPJ do vendedor: ")

    vendedor = col_vendedor.find_one({"ven_cnpj": ven_cnpj})
    if not vendedor:
        print("Vendedor não encontrado! Cadastre o vendedor antes de cadastrar o produto.")
        return

    vendedor_info = {
        "ven_id": str(vendedor.get("_id")),
        "ven_nome": vendedor.get("ven_nome"),
        "ven_cnpj": vendedor.get("ven_cnpj")
    }

    produto = {
        "prod_cod": prod_cod,
        "prod_nome": prod_nome,
        "prod_descricao": prod_descricao,
        "prod_valor": prod_valor,
        "prod_quantidade": prod_quantidade,
        "vendedor": vendedor_info
    }

    x = col_produto.insert_one(produto)
    print("Produto inserido com ID", x.inserted_id)

def read_produto(prod):
    col_produto = db.produto

    if prod:  
        produtos = col_produto.find({"prod_nome": prod})
    else:
        produtos = col_produto.find().sort("prod_nome")

    encontrou = False
    for p in produtos:
        encontrou = True
        print(f"\nCódigo: {p.get('prod_cod', '')}")
        print(f"Nome: {p.get('prod_nome', '')}")
        print(f"Descrição: {p.get('prod_descricao', '')}")
        valor = p.get('prod_valor', 0)
        if isinstance(valor, (int, float)):
            print(f"Valor: R$ {valor:.2f}")
        else:
            print(f"Valor: {valor}")
        print(f"Quantidade: {p.get('prod_quantidade', 0)}")
        vendedor = p.get("vendedor", {}) or {}
        if vendedor:
            print("Vendedor:")
            print(f"- Nome: {vendedor.get('ven_nome', '')}")
            print(f"- CNPJ: {vendedor.get('ven_cnpj', '')}")
        else:
            print("Vendedor: (não informado)")
        print("-" * 30)

    if not encontrou:
        print("Nenhum produto encontrado.")

def update_produto(prod_cod):
    col_produto = db.produto
    col_vendedor = db.vendedor  

    cod = int(str(prod_cod).strip())

    produto = col_produto.find_one({"prod_cod": cod}) or col_produto.find_one({"prod_cod": str(cod)})
    if not produto:
        print("Produto não encontrado.")
        return

    vend = (produto.get("vendedor") or {})
    print(f"\nAtual: Código:{produto.get('prod_cod')} | Nome:{produto.get('prod_nome')} | Valor:{produto.get('prod_valor')} | Qtd:{produto.get('prod_quantidade')}")
    print(f"Vendedor: {vend.get('ven_nome','')} | CNPJ: {vend.get('ven_cnpj','')}")

    novo_nome = input("Novo Nome: ").strip()
    nova_desc = input("Nova Descrição: ").strip()
    novo_valor = input("Novo Valor: ").strip()
    nova_qtd  = input("Nova Quantidade: ").strip()
    novo_cnpj = input("Novo CNPJ do vendedor: ").strip()

    changes = {}
    if novo_nome: changes["prod_nome"] = novo_nome
    if nova_desc: changes["prod_descricao"] = nova_desc
    if novo_valor:
        try: changes["prod_valor"] = float(novo_valor)
        except ValueError: print("Valor inválido. Mantido.")
    if nova_qtd:
        try: changes["prod_quantidade"] = int(nova_qtd)
        except ValueError: print("Quantidade inválida. Mantida.")

    if novo_cnpj:
        vendedor = col_vendedor.find_one({"ven_cnpj": novo_cnpj})
        if vendedor:
            changes["vendedor"] = {
                "ven_id": str(vendedor.get("_id")),
                "ven_nome": vendedor.get("ven_nome"),
                "ven_cnpj": vendedor.get("ven_cnpj"),
            }
        else:
            print("CNPJ não encontrado. Vendedor mantido.")

    if not changes:
        print("Nada para atualizar.")
        return

    col_produto.update_one({"_id": produto["_id"]}, {"$set": changes})
    print("Produto atualizado com sucesso!")

def delete_produto(prod_cod):
    col_produto = db.produto
    try:
        cod = int(prod_cod)
    except (TypeError, ValueError):
        print("Código inválido. Informe um número inteiro.")
        return

    # Tenta deletar pelo inteiro (caso correto)
    result = col_produto.delete_one({"prod_cod": cod})
    if result.deleted_count > 0:
        print("Produto deletado com sucesso!")
        return

    # Fallback: alguns registros podem ter sido salvos como string
    result_str = col_produto.delete_one({"prod_cod": str(cod)})
    if result_str.deleted_count > 0:
        print("Produto deletado (campo salvo como string).")
    else:
        print("Nenhum produto encontrado com esse código.")

