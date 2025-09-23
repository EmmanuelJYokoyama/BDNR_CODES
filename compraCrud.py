from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre

key = 0
sub = 0

def delete_compra(nome, sobrenome):
    #Delete
    global db
    mycol = db.compras
    myquery = {"usuario.usu_nome": nome, "usuario.usu_sobrenome": sobrenome}
    mydoc = mycol.delete_one(myquery)
    print("Deletado o usuário ",mydoc)

def create_compra():
    global db
    compras_col = db.compras    
    usuarios_col = db.usuario
    produtos_col = db.produto
    print("\nInserindo uma nova compra")
    cpf = input("Digite seu CPF: ")
    # Busca o usuário na coleção usuario
    usuario = usuarios_col.find_one({"usu_cpf": cpf})
    if not usuario:
        print("CPF não cadastrado como usuário.")
        return

    dataCompra = input("Data da compra (DD-MM-YYYY): ")
    try:
        data_compra_dt = datetime.strptime(dataCompra, "%d-%m-%Y")
    except ValueError:
        print("Data de compra inválida. Use o formato DD-MM-YYYY.")
        return

    dataEntrega = input("Data da entrega (DD-MM-YYYY, deixe vazio se não entregue): ")
    if dataEntrega.strip():
        data_entrega_dt = datetime.strptime(dataEntrega, "%d-%m-%Y")
        while data_entrega_dt < data_compra_dt:
            dataEntrega = input("Data de entrega não pode ser antes da data de compra. Insira a data novamente: ")
    else:
        dataEntrega = None

    valor = 0
    prod = []
    key = 'S'
    while key == 'S':
        produtoCod = input("Código do produto: ")
        if not produtoCod:
            print("Código do produto não pode ser vazio.")
            continue

        produto = produtos_col.find_one({"prod_id": int(produtoCod)})
        if not produto:
            print("Produto não encontrado! Informe um código válido.")
            continue

        print(f"Produto encontrado: {produto['prod_nome']} - Valor: {produto['prod_valor']} - Quantidade disponível: {produto['prod_quantidade']}")
        produtoQuantidade = int(input("Quantidade do produto: "))
        if produtoQuantidade > produto['prod_quantidade']:
            print("Quantidade solicitada maior que a disponível!")
            continue

        valor += produto['prod_valor'] * produtoQuantidade
        produtosObj = {
            "prod_id": produto['prod_id'],
            "prod_nome": produto['prod_nome'],
            "prod_valor": produto['prod_valor'],
            "prod_quantidade": produtoQuantidade
        }

        nova_quantidade = produto['prod_quantidade'] - produtoQuantidade
        produtos_col.update_one(
            {"prod_id": produto['prod_id']},
            {"$set": {"prod_quantidade": nova_quantidade}}
        )
        prod.append(produtosObj)
        key = input("Deseja cadastrar um novo produto (S/N)? ").upper()

    compra_doc = {
        "comp_valor": valor,
        "comp_data": dataCompra,
        "comp_dataentrega": dataEntrega,
        "usuario": {
            "usu_cpf": usuario.get("usu_cpf"),
            "usu_nome": usuario.get("usu_nome"),
            "usu_email": usuario.get("usu_email")
        },
        "produtos": prod
    }
    x = compras_col.insert_one(compra_doc)
    print("Documento inserido com ID ",x.inserted_id)

def read_compra(cpf):
    compras_col = db.compras
    compras = compras_col.find({"usuario.usu_cpf": cpf})
    encontrou = False
    for compra in compras:
        print(compra)
        encontrou = True
    if not encontrou:
        print("Nenhuma compra encontrada para esse CPF.")

def update_compra(nome):
    #Read
    global db
    mycol = db.compras
    myquery = {"usuario.usu_nome": nome}
    mydoc = mycol.find_one(myquery)
    print("Dados do usuário: ",mydoc)
    nome = input("Mudar Nome:")
    if len(nome):
        mydoc["usuario"]["usu_nome"] = nome

    email = input("Mudar Email:")
    if len(email):
        mydoc["usuario"]["usu_email"] = email

    newvalues = { "$set": mydoc }
    mycol.update_one(myquery, newvalues)