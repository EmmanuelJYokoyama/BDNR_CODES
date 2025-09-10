from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from usuarioCrud import *
from compraCrud import *

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.mercado_livre

key = 0
sub = 0
while (key != 'S'):
    print("1-CRUD Usuário")
    print("2-CRUD Vendedor")
    print("3-CRUD Produto")
    print("4-CRUD Compra")
    key = input("Digite a opção desejada? (S para sair) ").upper()

    if (key == '1'):
        print("Menu do Usuário")
        print("1-Create Usuário")
        print("2-Read Usuário")
        print("3-Update Usuário")
        print("4-Delete Usuário")
        sub = input("Digite a opção desejada? (V para voltar) ").upper()
        if (sub == '1'):
            print("Create usuario")
            create_usuario()
            
        elif (sub == '2'):
            nome = input("Read usuário, deseja algum nome especifico? ")
            read_usuario(nome)
        
        elif (sub == '3'):
            nome = input("Update usuário, deseja algum nome especifico? ")
            update_usuario(nome)

        elif (sub == '4'):
            print("delete usuario")
            nome = input("Nome a ser deletado: ")
            sobrenome = input("Sobrenome a ser deletado: ")
            delete_usuario(nome, sobrenome)
            
    elif (key == '2'):
        print("Menu do Vendedor")        
    elif (key == '3'):
        print("Menu do Produto")        
    elif (key == '4'):
        print("Menu de Compra")
        print("1-Create Compra")
        print("2-Read Compra")
        print("3-Update Compra")
        print("4-Delete Compra")
        sub = input("Digite a opção desejada? (V para voltar) ").upper()
        if (sub == '1'):
            print("Create compra")
            create_compra()
            
        elif (sub == '2'):
            nome = input("Read compra, deseja algum CPF especifico? ")
            read_compra(nome)

        elif (sub == '3'):
            nome = input("Update produto, deseja algum nome especifico? ")
            update_compra(nome)

        elif (sub == '4'):
            print("delete produto")
            nome = input("Produto a ser deletado: ")
            sobrenome = input("Sobrenome a ser deletado: ")
            delete_compra(nome, sobrenome)        

print("Tchau Prof...")