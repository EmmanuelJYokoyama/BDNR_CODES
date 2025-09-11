from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

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
    myquery = {"usu_nome": nome, "sobrenome":sobrenome}
    mydoc = mycol.delete_one(myquery)
    print("Deletado o usuário ",mydoc)

def create_compra():
    global db
    compras_col = db.compras    
    #compras_col = db.produtos
    usuarios_col = db.usuario
    print("\nInserindo uma nova compra")
    cpf = input("Digite seu CPF: ")
    # Busca o usuário na coleção usuario
    usuario = usuarios_col.find_one({"usu_cpf": cpf})
    if not usuario:
        print("CPF não cadastrado como usuário.")
        return

    dataCompra = input("Data da compra: ")
    dataEntrega = input("Data da entrega: ")
    valor = 0
    prod = []
    key = 1
    while (key != 'N'):
        produtoCod = input("Código do produto: ")
        if not produtoCod:
            print("Código do produto não pode ser vazio.")
            continue

        produtoNome = input("Nome do produto: ")
        produtoValor = float(input("Valor do produto: "))
        produtoQuantidade = int(input("Quantidade do produto: "))
        valor += produtoValor * produtoQuantidade
        produtosObj = {        #isso nao eh json, isso é chave-valor, eh um obj
            "prod_nome":produtoNome,
            "prod_valor":produtoValor,
            "prod_quantidade":produtoQuantidade
        }
        prod.append(produtosObj) #estou inserindo na lista
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
    # Busca compras pelo CPF
    global db
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
    myquery = {"usu_nome": nome}
    mydoc = mycol.find_one(myquery)
    print("Dados do usuário: ",mydoc)
    nome = input("Mudar Nome:")
    if len(nome):
        mydoc["usu_nome"] = nome

    cpf = input("Mudar Email:")
    if len(cpf):
        mydoc["usu_email"] = cpf

    newvalues = { "$set": mydoc }
    mycol.update_one(myquery, newvalues)