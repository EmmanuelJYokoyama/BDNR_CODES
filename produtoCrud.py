from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Conexão com o banco
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

def read_produto(idprod=None):
    col_produto = db.produto
    print("\nProdutos encontrados:")
    if not idprod:
        docs = col_produto.find().sort("prod_nome")
        for x in docs:
            print(x)
    else:
        myquery = {"prod_cod": idprod}
        docs = col_produto.find(myquery)
        for x in docs:
            print(x)

def update_produto(prod_cod):
    col_produto = db.produto
    myquery = {"prod_cod": prod_cod}
    produto = col_produto.find_one(myquery)

    if not produto:
        print("Produto não encontrado.")
        return

    print("Dados atuais do produto:", produto)

    novo_nome = input("Novo Nome (Enter para manter): ")
    if novo_nome:
        produto["prod_nome"] = novo_nome

    nova_descricao = input("Nova Descrição (Enter para manter): ")
    if nova_descricao:
        produto["prod_descricao"] = nova_descricao

    novo_valor = input("Novo Valor (Enter para manter): ")
    if novo_valor:
        produto["prod_valor"] = float(novo_valor)

    nova_quantidade = input("Nova Quantidade (Enter para manter): ")
    if nova_quantidade:
        produto["prod_quantidade"] = int(nova_quantidade)

    opcao = input("Deseja atualizar os dados do vendedor? (S/N): ").upper()
    if opcao == "S":
        novo_ven_id = input("Novo ID do vendedor (Enter para manter): ")
        if novo_ven_id:
            produto["vendedor"]["ven_id"] = int(novo_ven_id)
        novo_ven_nome = input("Novo Nome do vendedor (Enter para manter): ")
        if novo_ven_nome:
            produto["vendedor"]["ven_nome"] = novo_ven_nome
        novo_ven_numero = input("Novo Número do vendedor (Enter para manter): ")
        if novo_ven_numero:
            produto["vendedor"]["ven_numero"] = novo_ven_numero

    col_produto.update_one(myquery, {"$set": produto})
    print("Produto atualizado com sucesso!")

def delete_produto(prod_id):
    col_produto = db.produto
    result = col_produto.delete_one({"prod_id": prod_id})
    if result.deleted_count > 0:
        print("Produto deletado com sucesso!")
    else:
        print("Nenhum produto encontrado com esse ID.")

